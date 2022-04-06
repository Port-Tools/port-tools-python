import requests
import json
from datetime import datetime, timedelta


class ConnectionError(Exception):
    pass

class ResponseError(Exception):
    pass

class FailedRequest(Exception):
    pass



class PortTool:
    URL_ENDPOINT = "https://port.tools/api/remote"

    def __init__(self, id, key = None, cache_time = None, retry = 0, use_last_if_error=True):
        self.id = id
        self.key = key
        self.cache_time = cache_time
        self.retry = retry
        self.use_last_if_error =use_last_if_error

        self.lifetime = None
        self.expiration = None

        self.__clean()

        if self.cache_time:
            self.lifetime = timedelta(seconds=self.cache_time)

    def __clean(self):
        self.ipv4 = None
        self.ipv6 = None
        self.last_update = None
        self.last_request = None

    def __request(self):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = {'id': self.id , 'key': self.key}
        try:
            res = requests.post(self.URL_ENDPOINT, data=json.dumps(data), headers=headers)
        except Exception as ex:
            raise ConnectionError(ex)

        if res.status_code == 200:
            data = res.json()
            if  data.get('ok'):
                self.ipv4 = data.get('ipv4')
                self.ipv6 = data.get('ipv6')
                self.last_update = data.get('last_update')
                if self.last_update:
                    self.last_update = datetime.strptime(self.last_update, "%Y-%m-%d %H:%M:%S %f %z")
                self.last_request = data.get('request_time')
                if self.last_request:
                    self.last_request = datetime.strptime(self.last_request, "%Y-%m-%d %H:%M:%S %f %z")
                return res
            else:
                raise FailedRequest("Res code: {}, Reason: {}, Message: {}".format(res.status_code, res.reason, data.get("msg")), res)
        else:
            raise ResponseError ("Res code: {}, Reason: {}".format(res.status_code, res.reason), res)

    def __request_and_retry(self):
        last_exception = None
        for _ in range(self.retry + 1):
            try:
                self.__request()
                if self.lifetime:
                    self.expiration = datetime.utcnow() + self.lifetime
                return         
            except Exception as ex:
                last_exception = ex
        if last_exception:
            raise last_exception

    def update(self):
        if self.lifetime:
            if not self.expiration or  datetime.utcnow() >= self.expiration:
                if self.use_last_if_error:
                    self.__clean()
                self.__request_and_retry()
        else:
            if self.use_last_if_error:
                self.__clean()
            self.__request_and_retry()

    @property
    def remote_info(self):
        self.update()
        return self.ipv4, self.ipv6, self.last_update, self.last_request

    @property
    def remote_ipv4(self):
        return self.ipv4

    @property
    def remote_ipv6(self):
        return self.ipv6
    
    @property
    def remote_last_update(self):
        return self.last_update

    @property
    def remote_last_request(self):
        return self.last_request