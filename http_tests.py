import http_server
import unittest
import os
from email.utils import formatdate


# class StartServerTests(unittest.TestCase):
#     #assumed working at moment
#     def test1(self):
#         pass


# class RecvDataTests(unittest.TestCase):

#     def test1(self):
#         #no idea how to test this function
#         pass


class SplitHeaderTests(unittest.TestCase):

    def setUp(self):
        self.recv = "GET /path/to/file/index.html HTTP/1.1 \r\n StuffThings"
        self.method = "GET"
        self.URI = "/path/to/file/index.html"
        self.protocol = "HTTP/1.1"

    def test_split_method(self):
        self.assertEqual(self.method, http_server.split_header(self.recv)[0])

    def test_split_URI(self):
        self.assertEqual(self.URI, http_server.split_header(self.recv)[1])

    def test_split_protocol(self):
        self.assertEqual(self.protocol, http_server.split_header(self.recv)[2])


class MapUriTests(unittest.TestCase):

    def setUp(self):
        self.imguri = "/webroot/images/JPEG_example.jpg"
        self.diruri = "/webroot/images"

    def test_file_exist(self):
        self.assertEqual(http_server.map_uri("/images/JPEG_example.jpg"),
                         self.imguri)

    def test_dir_exist(self):
        self.assertEqual(http_server.map_uri("/images"), self.diruri)

    def tearDown(self):
        pass


class BuildResponseTests(unittest.TestCase):

    def test1(self):
        pass


if __name__ == "__main__":
    unittest.main()
