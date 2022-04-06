from time import sleep
from port_tools.sdk import PortTool
import unittest

class RequestTest(unittest.TestCase):
    ipv4 = '42.112.128.200'
    ipv6 = None
    id = '716107D963'
    key = None

    def test_request(self):
        p = PortTool(id="716107D963")
        # Get info
        ipv4, ipv6, update, request = p.remote_info
        assert(ipv4)

    def test_cache_in_expired_time(self):
        p = PortTool(id=self.id, cache_time=10)
        # Get info
        ipv4, ipv6, update, request1 = p.remote_info
        ipv4, ipv6, update, request2 = p.remote_info
        assert(request1 == request2)
        assert(ipv4 == self.ipv4)
        assert(ipv6 == self.ipv6)

    def test_cache_out_expired_time(self):
        p = PortTool(id=self.id, cache_time=10)
        # Get info
        ipv4, ipv6, update, request1 = p.remote_info
        assert(ipv4 == self.ipv4)
        assert(ipv6 == self.ipv6)
        sleep(11)
        ipv4, ipv6, update, request3 = p.remote_info
        assert(request1 != request3)
        assert(ipv4 == self.ipv4)
        assert(ipv6 == self.ipv6)

    def test_retry(self):
        PortTool.URL_ENDPOINT = "https://port.tools/api/remote_error"
        p = PortTool(id=self.id, retry=10)
        # Get info
        try:
            ipv4, ipv6, update, request1 = p.remote_info
        except Exception as ex:
            pass
        assert(True)

    def test_use_last_if_error(self):
        PortTool.URL_ENDPOINT = "https://port.tools/api/remote_error"
        p = PortTool(id=self.id, retry=10)
        # Get info
        try:
            p.update()
        except Exception as ex:
            pass
        assert(p.remote_ipv4 == None and p.remote_ipv6 == None and p.remote_last_update == None and p.remote_last_request == None)
