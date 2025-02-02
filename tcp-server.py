#!/usr/bin/python3
'''
server, based on socket
'''
import socket
import sys
import subprocess
import os
from http import HTTPStatus
import mimetypes
import time
import datetime

DEBUG = 0
DEFAULTFILE = '/index.html'
SEARCHPATH = '.'
CGIEXT = ['.cgi','.py']
HTTPVERIN = 'HTTP/1.1'
HTTPVER = 'HTTP/1.0'
if sys.platform == "linux":
    PYTHON = 'python3'
elif sys.platform == "win32":
    PYTHON = 'py'

DEF404SENDDATA = b'''\
Content-Type: text/html; charset=utf-8


<html>
<body>
<a href="./">Up</a>
<p>File Not Found!</p>
</body>
</html>
'''



def getMainHeader(httpdata):
    '''
    get "GET", "/index.py?a=b","HTTP/1.1"
    '''
    httpdata = httpdata.replace('\r', '')
    httpdata = httpdata.split('\n')
    return httpdata[0].split(' ')

def parseHeaders(httpdata):
    '''
    Parsing HTTP Headers
    '''
    env = {}
    httpdata = httpdata.replace('\r', '')
    httpdata = httpdata.split('\n')
    method,url,version = httpdata[0].split(' ')
    # method,url,version = getMainHeader(httpdata)
    if version not in [HTTPVERIN, HTTPVER]:
        print(version.encode())
        return HTTPStatus.HTTP_VERSION_NOT_SUPPORTED, b"\r\n\r\n n"
    if '?' in url:
        path,getparams = url.split('?')
    else:
        path = url
        getparams = ''
    if path == '/exit':
        print("Server stopped")
        sys.exit()
    env["REQUEST_METHOD"] = method
    env['QUERY_STRING'] = getparams
    postdata = ''
    flag_post = 0
    lenthOfHttpData = len(httpdata)
    for itr, dataInHttp in enumerate(httpdata):
        if flag_post:
            if itr == lenthOfHttpData - 1:
                postdata += dataInHttp
            else:
                postdata += dataInHttp+'\n'
        elif dataInHttp == '':
            flag_post=1
        else:
            if ':' in dataInHttp:
                env_key, env_value = dataInHttp.split(":", maxsplit = 1)
                env_key = env_key.upper().replace("-","_")
                env_value = env_value[1:]
                if env_key == "COOKIE":
                    env_key = "HTTP_COOKIE"

                env[env_key] = env_value

    if os.path.isdir(SEARCHPATH+path):
        path += DEFAULTFILE
    if DEBUG:
        print('REQUESTING FILE: ', path.encode())
    else:
        # NOT DEBUG PRINT method + url
        print(method, url, end=' ',flush=True)

    if not os.path.exists('./'+path):
        return HTTPStatus.NOT_FOUND, DEF404SENDDATA
    ext = os.path.splitext(path)[-1].lower()
    if ext in CGIEXT:
        if DEBUG:
            print("POST to send: ", postdata)
        code, result_data = run_cgi(ext, SEARCHPATH+path, postdata, env)
    else:
        code, result_data = send_file(SEARCHPATH+path)
    return code, result_data
def run_cgi(ext, path, postdata, environ):
    '''exec requesting CGI program and return its output'''
    if DEBUG:
        print("ext ",ext)
    my_env = environ
    # my_env = os.environ.copy()
    if sys.platform == 'linux':
        sb = subprocess.Popen(path,stdout=subprocess.PIPE,stdin=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=my_env)
        out, err = sb.communicate(input=bytes(postdata,encoding='cp1251'))
    elif sys.platform == 'win32':
        if ext == '.py':
            if DEBUG:
                print("CGI PYTHON")
            sb = subprocess.Popen(PYTHON+' '+path,stdout=subprocess.PIPE,stdin=subprocess.PIPE,
                                  stderr=subprocess.PIPE, env=my_env)
            out, err = sb.communicate(input = bytes(postdata,encoding='cp1251'))
        else:
            if DEBUG:
                print('path ',path)
            sb = subprocess.Popen('wsl'+' '+path, shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,
                                  stderr=subprocess.PIPE,env=my_env)
            out, err = sb.communicate(input=bytes(postdata,encoding='cp1251'))
    # NOT DEBUG PRINT CGI
    print("CGI",end='')
    if sb.returncode == 0:
        ret = out
        return HTTPStatus.OK, ret
    else:
        # NOT DEBUG PRINT error
        print("\nerror! log:", err)
        return HTTPStatus.INTERNAL_SERVER_ERROR, b' '+bytes(abs(sb.returncode))

def send_file(path):
    '''return data from requesting file with Content-Type and charset'''
    mime = mimetypes.guess_type(path)[0]
    if not mime:
        mime = 'text/html'
    if DEBUG:
        print("SEND FILE "+mime)
    try:
        with(open(path,"rb")) as f:
            filedata = f.read()
    except FileNotFoundError:
        return HTTPStatus.NOT_FOUND, DEF404SENDDATA
    return HTTPStatus.OK, b'Content-Type: '+bytes(mime,encoding='utf8')+b'; charset=UTF-8\r\n\r\n'\
           +filedata

def main():
    '''main function'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('0.0.0.0', 5000)
    print(f'Старт сервера на {server_address[0]} порт {server_address[1]}')
    sock.bind(server_address)

    sock.listen(1)

    while True:
        print('waiting connection...',end='',flush=True)
        connection, client_address = sock.accept()
        try:
            now = datetime.datetime.now()
            print(f'\r            \r>{now} ', client_address, end=' ',flush=True)
            while True:
                datamas = []
                data = b''
                # drecv = connection.recv(2048)
                # method, _, _ = getMainHeader(drecv.decode())
                # data = drecv
                # if method != 'GET':
                while True:
                    connection.sendall(b'HTTP 100 Continue\n\n')
                    time.sleep(0.5) # waiting browser to send data
                    drecv = connection.recv(2048)
                    # time.sleep(0.5)
                    data += drecv
                    if DEBUG:
                        print("d", drecv)
                    if len(drecv) < 2048:
                        break
                if DEBUG:
                    print('Получено: ')
                    for i in datamas:
                        print(i)
                    print('END\n',flush=True)
                if data:
                    print('...',end=' ',flush=True)
                    code, senddata = parseHeaders(data.decode(encoding="cp1251"))
                    print('>>>>',end=' ',flush=True)
                    # HTTP/1.1 200 OK
                    retdata =  HTTPVER+' '+str(code.value)+' '+code.phrase+'\n'
                    retdata = retdata.encode('utf8')
                    retdata += senddata
                    print(code.value,code.phrase, datetime.datetime.now() - now ,end=' ',flush=True)
                    connection.sendall(retdata)
                    if DEBUG:
                        print(f'SEND: {len(retdata)}',flush=True)
                    print()
                    break
                else:
                    print('Нет данных от:', client_address,flush=True)
                    break

        finally:
            connection.close()
if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt as e:
            print("\nShutdown")
            sys.exit()
