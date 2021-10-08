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

BUFFER_SIZE = 1024

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
            part = sock.recv(BUFFER_SIZE)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None): # url = http://127.0.0.1:27685/49872398432
        # code = 500 # default 500 Generic Error 
        # body = ""
        # args_str = ''

        # # consider handling arguments
        # if args:
        #     args_str = urllib.parse.quote_plus(args)
        
        # format request 
        # source: https://www.tutorialspoint.com/http/http_requests.htm
        uri, host = create_uri(url) # Request-Line = Method (GET) Request-URI HTTP-Version (HTTP//1.1) CRLF (\r\n)
        
        # print("host1",host_from_url(url))
        # print("host2",host)

        # request = 'GET {0} HTTP/1.1\r\n'.format(geturl_from_url(url))
        request = 'GET {0} HTTP/1.1\r\n'.format(uri)
        # request += 'Host: {0}\r\n'.format(host_from_url(url))
        request += 'Host: {0}\r\n'.format(host)
        request += 'Accept: */*\r\n\r\n'

        response_str = do_request(url, request)
        statusCode, httpBody = parse(response_str)
        
        return HTTPResponse(statusCode, httpBody)

    def POST(self, url, args=None): 
        '''
        args =  {'a':'aaaaaaaaaaaaa',
                'b':'bbbbbbbbbbbbbbbbbbbbbb',
                'c':'c',
                'd':'012345\r67890\n2321321\n\r'}
        '''
        code = 500
        body = ""

        # arg_string = argstring_from_args(args)
        arg_string = '' 
        if args:
            arg_string = urllib.parse.urlencode(args)
        # print("args1",args)
        # print("arg_string1",arg_string)

        uri, host = create_uri(url)

        # request = 'POST {0} HTTP/1.1\r\n'.format(geturl_from_url(url))
        request = 'POST {0} HTTP/1.1\r\n'.format(uri)
        # request += 'Host: {0}\r\n'.format(host_from_url(url))
        request += 'Host: {0}\r\n'.format(host)
        request += 'Accept: */*\r\n'

        if arg_string != '':
            request += 'Content-Length: {0}'.format(len(arg_string)) + '\r\n'
            request += 'Content-Type : application/x-www-form-urlencoded' + '\r\n'
        else:
            request += 'Content-Length: {0}'.format(0) + '\r\n'

        request += '\r\n'

        # print("request_POST1",request)

        if arg_string != '':
            request += arg_string + '\r\n'
            request += '\r\n'
        # print("request_argStr",request)

        response_str = do_request(url, request)
        print("response_str1",type(response_str),response_str)
        statusCode, httpBody = parse(response_str)
        
        return HTTPResponse(statusCode, httpBody)

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
    uri = "/"
    host = url 
    i = 0 
    while i<len(url):
        if url[i]=="/": # only return the requestURI
            uri = url[i:]
            host = url[:i]
            break
        i += 1 
    
    if "/" in host:
        j = 0 
        while j<len(host):
            j += 1
        host = uri[:j]

    return uri, host 

def parse(response_str):
    print("response_str2",type(response_str),response_str)
    split_response = response_str.split('\r\n\r\n')
    print("split_response",type(split_response),split_response)
    header_statusCode = split_response[0].strip().split("\r\n")[0]
    statusCode = int(header_statusCode.split(" ")[1])

    httpBody = split_response[1].strip()

    return statusCode, httpBody

def do_request(url, request):
    
    _, hosturl = create_uri(url)
    print("hosturl:",hosturl)

    # connect socket
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = hosturl # default 
    port = 80
    if ":" in hosturl:
        hosturl_split = hosturl.split(":")
        host = hosturl_split[0]
        port = int(hosturl_split[1])
    local_socket.connect((host, port))
    local_socket.sendall(str.encode(request, "utf-8"))

    # receive repsonse  
    full_data = b""
    while True: # continueous recieve data until server stops sending 
        try:
            data = local_socket.recv(BUFFER_SIZE)
        except Exception:
            raise
        
        # if no more data, break 
        if data.decode("utf-8")=="":
            break 
        else: # if there is data
            full_data += data
            # ensures complete response
            complete = validate_response_completion(full_data)
            if complete: # returns True if response is valid, False otherwise
                break
    print("fulldata",full_data)

    local_socket.close()

    return full_data.decode("utf-8")

def validate_response_completion(data):

    data = data.decode("utf-8")
    print("buffer1",type(data),data)

    # no "\r\n\r\n" in data, response incomplete
    sections_list = data.split("\r\n\r\n")
    print("sections_list",type(sections_list),sections_list)
    print("sections_list[1]",type(sections_list),sections_list[1])
    if len(sections_list)==1:
        return False 

    headers_list = sections_list[0].split("\r\n")
    print("headers1",type(headers_list),headers_list)

    # check content length 
    content_length = 0 
    for header in headers_list:
        if "Content-Length" in header:
            print("header1",type(header),header)
            content_length = int(header.split(" ")[1])
    if content_length == 0:
        return False 
    print("content_length",type(content_length),content_length)

    # response has finished 
    if "\r\n\r\n" in data:
        print("sections_list_len",len(sections_list[1]))
        return True

    return False


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
