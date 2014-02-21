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


class MethodParseTests(unittest.TestCase):

    def setUp(self):
        self.get = 'GET'
        self.post = 'POST'

    def test_get(self):
        self.assertEqual(http_server.parse_method(self.get), None)

    def test_post(self):
        self.assertRaises(http_server.parse_method(self.post))


class SplitHeaderTests(unittest.TestCase):

    def setUp(self):
        self.recv = "GET /path/to/file/index.html HTTP/1.1 \r\n StuffThings"
        self.method = "GET"
        self.URI = "/path/to/file/index.html"
        self.protocol = "HTTP/1.1 "

    def test_split_method(self):
        self.assertEqual(self.method, http_server.split_header(self.recv)[0])

    def test_split_URI(self):
        self.assertEqual(self.URI, http_server.split_header(self.recv)[1])

    def test_split_protocol(self):
        self.assertEqual(self.protocol, http_server.split_header(self.recv)[2])


class MapUriTests(unittest.TestCase):

    def setUp(self):
        self.imguri = "webroot/images/JPEG_example.jpg"
        self.diruri = "webroot/images"

    # def test_file_exist(self):
    #     self.assertEqual(http_server.map_uri("/images/JPEG_example.jpg"),
    #                      self.imguri)

    def test_dir_exist(self):
        self.assertTrue(http_server.map_uri("/images"))

    def test_not_exist(self):
        self.assertRaises(http_server.map_uri("sklfjdh"))

    def tearDown(self):
        pass


class BuildResponseTests(unittest.TestCase):

    def setUp(self):
        self.handle = http_server.handle_connection(
            "GET /a_web_page.html HTTP/1.1 \r\n StuffThings")
        self.handle_dir = http_server.handle_connection(
            "GET / HTTP/1.1 \r\n StuffThings")
        #  self.img = self.img.read()

    def test_response(self):
        # self.assertEqual(http_server.handle_connection(
        #   "GET /images/JPEG_example.jpg HTTP/1.1 \r\n StuffThings"),
        #   'something')
        self.assertEqual(self.handle, 'something')

    def test_dir_response(self):
        self.assertEqual(self.handle_dir, "something")

if __name__ == "__main__":
    unittest.main()
