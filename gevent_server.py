#! /usr/bin/env python
import socket
import email.utils
import os
from mimetypes import guess_type


def start_server(sock, address):

    while True:  # endless loop to permit server to continue echo function
        message = recv_data(sock)
        response = handle_connection(message)
        sock.sendall(response)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()


def recv_data(connection):  # capping loops for receiving recv_data

    msg = ''
    while True:
        buff = connection.recv(4096)
        msg += buff
        if len(buff) <= 4096:
            connection.shutdown(socket.SHUT_RD)
            return msg


def handle_connection(incoming):
    method, uri, protocol = split_header(incoming)
    print method, uri, protocol
    try:
        mapped_uri = map_uri(method, uri)
        return build_response(uri, mapped_uri)
    except Error404:
        return build_response(uri, 'Not Found 404', 404)
    except Error405:
        return build_response(uri, 'Method not allowed 405', 405)
    except:
        return build_response(uri, 'Internal Server Error 500', 500)


def split_header(data):
    #splits data and maps [method, uri, protocol] to indicies [0,1,2]
    splitdata = data.split('\r\n', 1)
    splitheader = splitdata[0].split(' ', 2)
    return splitheader


def map_uri(method, uri):
    if method != 'GET':
        raise Error405
    path = 'webroot' + uri
    if os.path.isfile(path):
        with open(path, 'rb') as f:
            response = f.read()
    elif os.path.isdir(path + '/'):
        d = os.listdir(path)
        response = '\n'.join(d)
    if response:
        return response
    raise Error404


def build_response(uri, data, code=200):
    mt = None
    d_code = {200: "OK 200", 404: "Not Found 404",
              405: "Method not allowed 405", 500: "Internal Server Error"}
    resp_list = []

    if code == 200:  # grabs mimetype from header URI
        mt = guess_type('webroot' + uri)[0]
    if not mt:  # Grabs in the event of a directory or error code
        mt = 'text/plain'

    resp_list.append('HTTP/1.1' + ("%s" % d_code[code]))
    resp_list.append("Date: %s" % email.utils.formatdate(usegmt=True))
    resp_list.append('Server: Team Python')
    resp_list.append("Content-Type: %s" % mt)
    resp_list.append("Content-Length: %s" % str(len(data)))
    resp_list.append('\r\n%s' % data)
    result = '\r\n'.join(resp_list)
    return result


class Error404(Exception):
    pass


class Error405(Exception):
    pass


if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 50000), start_server)
    server.serve_forever()
