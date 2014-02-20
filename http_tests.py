import http_server
import unittest
from email.utils import formatdate


class StartServerTests(unittest.TestCase):

    def test1(self):
        pass


class RecvDataTests(unittest.TestCase):

    def test1(self):
        pass


class ParseHeaderTests(unittest.TestCase):

    def setUp_URI(self):
        self.recv = "GET /path/to/file/index.html HTTP/1.1 \r\n StuffThings"
        self.header = "GET /path/to/file/index.html HTTP/1.1"
        self.method = "GET"
        self.URI = "/path/to/file/index.html"
        self.protocol = "HTTP/1.1"
        self.join = ''

    def test_split(self):
        self.assertEqual(self.header, self.join.join(http_server.parse_header
                         (self.recv)), "Parse header from correct request")

    def test_split_method(self):
        self.assertEqual(self.method, http_server.parse_header(self.recv)[0])

    def test_split_URI(self):
        self.assertEqual(self.URI, http_server.parse_header(self.recv)[1])

    def test_split_protocol(self):
        self.assertEqual(self.protocol, http_server.parse_header(self.recv)[2])


class MapUriTests(unittest.TestCase):

    def test1(self):
        pass


class BuildResponseTests(unittest.TestCase):

    def test1(self):
        pass


if __name__ == "__main__":
    unittest.main()
