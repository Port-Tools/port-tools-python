from port_tools.sdk import request
import unittest

class RequestTest(unittest.TestCase):
    def test_request(self):
        res = request(id="92B0271E4E")
        self.assertTrue(
           res != None
        )
        