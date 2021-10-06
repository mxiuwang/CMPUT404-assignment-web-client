#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
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

from helper import * 

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
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

    def GET(self, url, args=None): # url = http://127.0.0.1:27685/49872398432
        code = 500 # default 500 Generic Error 
        body = ""
        args_str = ''

        # consider handling arguments
        if args:
            args_str = urllib.urlencode(args)
        
        # format request 
        # source: https://www.tutorialspoint.com/http/http_requests.htm
        uri = create_uri(url) # Request-Line = Method (GET) Request-URI HTTP-Version (HTTP//1.1) CRLF (\r\n)
        
        print("host1",host_from_url(url))
        # request = 'GET {0} HTTP/1.1\r\n'.format(geturl_from_url(url))
        request = 'GET {0} HTTP/1.1\r\n'.format(uri)
        request += 'Host: {0}\r\n'.format(host_from_url(url))
        request += 'Accept: */*\r\n\r\n'
        response = do_request(url, request)

        print("request1",request)
        print("response1",response)

        # parse 
        response_str = response.decode("utf-8")
        headers = (response_str.split('\r\n\r\n')[0]).strip().split('\r\n')
        body = response_str.split('\r\n\r\n')[1]

        code_header = [header for header in headers if header[:8] == 'HTTP/1.1' or header[:8] == 'HTTP/1.0'][0]
        code = int(code_header.split(' ')[1])
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
def create_uri(url):
    '''
    url = http://127.0.0.1:27685/49872398432 --> uri = 49872398432
    '''
    url = url.replace("http://","") # uri = 49872398432
    i = 0 
    while i<len(url):
        if url[i]=="/": # only return the requestURI
            return url[i:]
        i += 1 

    # no / is found 
    return "/"

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
