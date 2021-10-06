#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# Copyright 2021 Shiyu XIu
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    #url parser
    def url_parser(self, url):
        after = urllib.parse.urlparse(url)

        
        #get host name and port
        if after.port != None:
            port = after.port
            netloc = after.netloc
            host_name = netloc.split(":")
            host_name = host_name[0]
        else:
            host_name = after.netloc
            port = 80
        #get path
        if after.path == "":
            path = "/"
        else:
            path = after.path

        return  host_name, port, path

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return int(data.split("\r\n")[0].split(" ")[1])

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return data.split("\r\n")[-1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        host_name, port, path = self.url_parser(url)
        req = f"GET {path} HTTP/1.1\r\nHost: {host_name}\r\naccept-charset:utf-8\r\nAccept: */*\r\nConnection: close\r\n\r\n"
        #request if failed return code and body directly
        try:
            self.connect(host_name,port)
            self.sendall(req) #send request
        except:
            #server error
            print(code+"/n"+body)
            return HTTPResponse(code, body)
        recv = self.recvall(self.socket)
        self.close()
        #read the body and code from the sockets
        body = self.get_body(recv)
        code = self.get_code(recv)
        print(body+"/n"+body)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        host_name, port, path = self.url_parser(url)
        if args == None:
            args=""
        else:
            args = urllib.parse.urlencode(args)
        req = f"POST {path} HTTP/1.1\r\nHost: {host_name}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {str(len(args))}\r\nAccept: */*\r\naccept-charset:utf-8\r\nConnection: close\r\n\r\n{args}"
        try:
            self.connect(host_name,port)
            self.sendall(req) #send request
        except:
            #server error

            print(code+"/n"+body)
            return HTTPResponse(code, body)
        recv = self.recvall(self.socket)
        self.close()
        #read the body and code from the sockets
        body = self.get_body(recv)
        code = self.get_code(recv)
        print(body+"/n"+body)

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
