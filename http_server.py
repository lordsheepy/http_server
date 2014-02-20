#! /usr/bin/env python

import socket
import email.utils
import os
from mimetypes import guess_type


def start_server():
    #open server socket, bind, listen, infinite running loop
    server_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    server_socket.bind(("127.0.0.1", 50000))
    server_socket.listen(1)

    while True:  # endless loop to permit server to continue echo function
        conn, addr = server_socket.accept()
        response = handle_connection(conn, addr)
        socket.sendall(response)
        conn.close()


def handle_connection(conn, addr):
    message = recv_data(conn)
    msg_split = split_header(message)
    try:
        parse_method(msg_split[0])
        responseraw = map_uri(msg_split[1])
    except HttpError:
        return build_response(str(HttpError), msg_split, HttpError.value)
    return build_response(responseraw, msg_split)


def recv_data(connection):
    #capping loops for receiving recv_data
    msg = ''
    while True:
        buff = connection.recv(4096)
        msg += buff
        if not buff:
            return msg


def split_header(data):
    #splits data and maps [method, uri, protocol, body] to indicies [0,1,2,3]
    splitdata = data.split('\r\n', 1)
    splitheader = splitdata[0].split(' ', 3)
    return splitheader


def parse_method(header):
    if header == 'GET':
        return
    else:
        raise HttpError(405)


def map_uri(uri):
    #use os module to map the URI to the filesystem
    path = os.environ['PWD'] + '/webroot' + uri
    if os.path.isfile(path):
        return read_response(path)
    elif os.path.isdir(path):
        return translate_dir(path)
    else:
        raise HttpError(404)


def read_response(pth):
    #builds response/errors
    f = pth.open()
    response = f.read()
    f.close()
    return response


def translate_dir(pth):
    d = os.listdir(pth)
    response = '\r\n'.join(d)
    return response


def build_response(raw, header, code=200):
    d_code = {200: 'OK', 404: "Not Found", 405: "Method not allowed"}
    head = header[2] + (" %s %s" % ('code', d_code[code]))
    date = "Date: " + email.utils.formatdate()
    if guess_type(os.eviron['PWD'] + '/webroot' + header[1]):
        mt = guess_type(os.eviron['PWD'] + '/webroot' + header[1])[0]
    else:
        mt = 'text/plain'
    mtype = "Content-Type: " + mt
    flen = "Content-Length: " + str(len(raw))
    result = '\r\n'.join(head, date, mtype, flen, raw)
    return result


# def error_builder(err, header):
#     d_err = {200: 'OK', 404: "Not Found", 405: "Method not allowed"}
#     head = ' '.join(header[2], str(err.value), d_err[err.value])
#     date = "Date: " + email.utils.formatdate()
#     result = '\r\n'.join(head, date)
#     return result


class HttpError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
