#!/usr/bin/python3
import os
import io
import uuid
import redis

class Session:
    '''
    Session
    '''
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    redis = redis.Redis(connection_pool=pool)
    sessionID = ""
    def __init__(self):
        pass
    def set(self, key, value):
        '''redis setter'''
        key = str(key)
        self.redis.set(self.sessionID+str(key),value)
    def get(self, key):
        '''redis getter'''
        key = str(key)
        ch = self.redis.get(self.sessionID+key)
        if ch is None:
            return None
        else:
            return (ch)

def print_to_string(*args, **kwargs):
    '''
    converts anything to string
    '''
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents

class HTTP:
    '''
    HTTP headers & post helper
    '''
    setcookie = {}
    cookie = {}
    post = {}
    get = {}
    out = ""
    method = ""
    def __init__(self) -> None:
        self.method = os.getenv("REQUEST_METHOD")
        # cookies parsing
        if os.getenv("HTTP_COOKIE"):
            rawcookie = os.getenv("HTTP_COOKIE").split('; ')
            if rawcookie != "":
                for coc in rawcookie:
                    key, val = coc.split('=')
                    self.cookie[key] = val
        # post data parsing
        if self.method == 'POST':
            rawpost = input().split('&')
            for i in rawpost:
                key, val = i.split('=')
                self.post[key] = val
        # get data parsing
        if os.getenv("QUERY_STRING"):
            rawget = os.getenv("QUERY_STRING").split('&')
            if rawget != "":
                for i in rawget:
                    key, val = i.split('=')
                    self.get[key] = val

    def print(self, *args, end='<br>'):
        '''
        sends args to out string adding <br>
        '''
        self.out += print_to_string(*args) + end

    def send_file(self,filename):
        '''
        reads file line-by-line and sends the result to out string
        '''
        with(open(filename,"r",encoding='utf8')) as f:
            while line := f.readline():
                line = str(line)
                self.print(line,end='')
    def send(self):
        '''
        sends http respond
        '''
        # header
        print("Content-Type: text/html; charset=utf-8")
        # for i in self.setcookie:

        # cookies
        for key, val in self.setcookie.items():
            print(f'Set-Cookie: {key}={val};')
        print()
        #response body
        print(self.out)

http = HTTP()
ses = Session()
http.print('<a href="./">Up</a>')
if http.cookie.get('session'):
    ses.sessionID = http.cookie['session']
else:
    ses.sessionID = str(uuid.uuid4())
    http.setcookie["session"] = ses.sessionID

if http.method == "POST":
    login = http.post.get('login')
    password = http.post.get('password')
    if login !="" and password !="":
        ses.set('login','true')
        if login == 'admin' and password == 'admin':
            ses.set('is_admin','true')
        else:
            ses.set('is_admin','false')

if (ses.get('login') is None) or (ses.get('login') == b'false'):
    http.send_file("login.html")
    http.send()
    exit(0)

if http.get.get("logout"):
    http.setcookie["session"] = ""
    ses.set('login','false')
    # http.send_file("login.html")
    http.print('logout')
    http.print('<a href="session.py">click to login</a>')
    http.send()
    exit(0)

http.print("you UID: ", ses.sessionID)

if ses.get('is_admin') == b'true':
    http.print("you are admin!:) ")
else:
    http.print("you are not admin!:( ")

# http.print("you UID: ",ses.sessionID)
http.print('<a href="session.py?logout=true">logout</a>')

http.send()
