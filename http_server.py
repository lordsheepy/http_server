#! /usr/bin/env python

import socket
import email.utils
import os


def start_server():
    #open server socket, bind, listen, infinite running loop
    server_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    server_socket.bind(("127.0.0.1", 50000))
    server_socket.listen(1)

    while True:  # endless loop to permit server to continue echo function
        conn, addr = server_socket.accept()
        message = recv_data(conn)
        conn.close()


def recv_data(connection):
    #capping loops for receiving recv_data
    msg = ''
    while True:
        buff = connection.recv(32)
        message += buff
        if not buff:
            return msg


def parse_header(method):
    #take message, split, then parsemethod and determine whether okay or
    #raise Exception
    pass


def map_uri(uri):
    #use os module to map the URI to the filesystem
    pass


def build_response():
    #builds response/errors
    pass
