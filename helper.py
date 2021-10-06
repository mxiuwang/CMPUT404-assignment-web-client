import urllib
import socket 

# def geturl_from_url(url): # url = http://127.0.0.1:27685/49872398432
#     """
#     Return the /url for the request
#     Example: 'localhost/hi/ha.html' -> '/hi/ha.html'
#     """
#     url = url.replace('http://', '')
#     if url.find('/') == -1:
#         return '/'
#     return url[url.find('/'):]

def host_from_url(url):
    """
    Returns host for Host header
    """
    url = url.replace('http://', '')
    if url.find('/') != -1:
        url = url[:url.find('/')]
    return url

def do_request(url, request):
    """
    sends the request as-is to the url
    returns the response
    """

    url = url.replace('http://', '')
    if url.find('/') != -1:
        url = url[:url.find('/')]

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if url.find(':') == -1:
        clientSocket.connect((url, 80))
    else:
        splitUrl = url.split(':')
        host, port = splitUrl[0], splitUrl[1]
        clientSocket.connect((host, int(port)))

    # print(request + '\n')
    clientSocket.sendall(str.encode(request, "utf-8"))

    return recvall(clientSocket)

def recvall(sock):
    buffer = bytearray()
    done = False
    while not done:
        part = sock.recv(1024)
        if (part):
            buffer.extend(part)
            if received_complete_response(buffer):
                break
        else:
            done = not part

    return buffer

def received_complete_response(buffer):
    """
    Fixes issue with sites returning 302 and keeping the conn open
    (recvall given to us will wait forever for conn close?)
    """
    buffer = buffer.decode("utf-8")
    print("buffer1",type(buffer),buffer)
    headers = buffer.split('\r\n')
    content_length = [h for h in headers if h[:15] == 'Content-Length:']
    if content_length == []:
        return False
    content_length = int(content_length[0][15:])

    if buffer.find('\r\n\r\n') == -1:
        return False

    split_buffer = buffer.split('\r\n\r\n')
    if (len(split_buffer) == 1 or split_buffer[1] == '') and content_length == 0:
        return True
    if len(split_buffer[1]) >= content_length:
        return True

    return False