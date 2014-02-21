#! /usr/bin/env python
import socket
import email.utils
import os
from mimetypes import guess_type


def start_server():
    server_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    server_socket.bind(("127.0.0.1", 50000))
    server_socket.listen(1)
    try:
        while True:  # endless loop to permit server to continue echo function
            conn, addr = server_socket.accept()
            message = recv_data(conn)
            response = handle_connection(message)
            conn.sendall(response)
            conn.shutdown(socket.SHUT_WR)
            conn.close()
    finally:
        server_socket.close()


def handle_connection(message):
    msg_split = split_header(message)
    try:
        parse_method(msg_split[0])
        responseraw = map_uri(msg_split[1])
    except:
        return build_response("Error", msg_split, HttpError.value)
    return build_response(responseraw, msg_split)


def recv_data(connection):
    #capping loops for receiving recv_data
    msg = ''
    while True:
        buff = connection.recv(4096)
        msg += buff
        if len(buff) <= 4096:
            connection.shutdown(socket.SHUT_RD)
            return msg


def split_header(data):
    #splits data and maps [method, uri, protocol] to indicies [0,1,2]
    splitdata = data.split('\r\n', 1)
    splitheader = splitdata[0].split(' ', 2)
    return splitheader


def parse_method(header):
    try:
        header == 'GET'
        return
    except:
        raise HttpError(405)


def map_uri(uri):  # switch in os.path.join
    # path = os.environ['PWD'] + '/webroot' + uri
    path = 'webroot' + uri
    try:
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                response = f.read()
            return response
            # return read_response(path)
        elif os.path.isdir(path + '/'):
            return translate_dir(path)
    except:
        raise HttpError(404)


def translate_dir(pth):
    d = os.listdir(pth)
    response = '\n'.join(d)
    return response


def build_response(raw, header, code=200):
    mt = None
    d_code = {200: "OK 200", 404: "Not Found 404",
              405: "Method not allowed 405"}
    resp_list = []
    resp_list.append(header[2] + ("%s" % d_code[code]))
    resp_list.append("Date: %s" % email.utils.formatdate(usegmt=True))
    if code == 200:  # grabs mimetype from header URI
        mt = guess_type('webroot' + header[1])[0]
    if not mt:  # Grabs in the event of a directory or error code
        mt = 'text/plain'
    resp_list.append('Server: Team Python')
    resp_list.append("Content-Type: %s" % mt)
    resp_list.append("Content-Length: %s" % str(len(raw)))
    resp_list.append('\r\n%s' % raw)
    result = '\r\n'.join(resp_list)
    return result


class HttpError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


if __name__ == "__main__":
    start_server()
