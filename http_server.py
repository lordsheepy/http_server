#! /usr/bin/env python

import socket
import email.utils
import os


def start_server():
    #open server socket, bind, listen, infinite running loop
    server_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    server_socket.bind(("127.0.0.1", 80))
    server_socket.listen(1)

    while True:  # endless loop to permit server to continue echo function
        conn, addr = server_socket.accept()
        message = recv_data(conn)
        msg_split = split_header(message)
        conn.close()


def recv_data(connection):
    #capping loops for receiving recv_data
    msg = ''
    while True:
        buff = connection.recv(4096)
        msg += buff
        if not buff:
            return msg


def split_header(data):
    #splits data and returns method, URI, protocol
    splitdata = data.split('\r\n', 1)
    splitheader = splitdata[0].split(' ', 3)
    return splitheader


def map_uri(uri):
    #use os module to map the URI to the filesystem
    path = os.environ['PWD'] + '/webroot' + uri
    if os.path.isfile(path):
        return path
    elif os.path.isdir(path):
        return path
    else:
        raise NotFoundError(404)


def build_response():
    #builds response/errors
    pass


class NotFoundError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
