#!/usr/bin/python3
'''show requesting files'''
import os
import base64
import mimetypes

print("Content-Type: text/html; charset=utf-8\r\n\r\n")
print()
print()
print()
print("<a href='./'>Up</a><br>")
# exit()
FILESPATH = './usrfiles'
os.chdir(FILESPATH)
files = [f for f in os.listdir('.') if os.path.isfile(f)]
if os.getenv("REQUEST_METHOD").lower() == 'post':
    file = input().split('=')[1]
    print("DELETE FILE: ", file)
    if file in files:
        os.remove(file)

files = [f for f in os.listdir('.') if os.path.isfile(f)]
if files == []:
    print("<h4>folder is empty:(</h4>")

for file in files:
    print("<h4>filename:",file,"</h4>")
    print(f'''
    <form action="watch_files.py" id="Form" enctype="application/x-www-form-urlencoded" method="post">
        <input id="keyinpgetall" name="delete" value="{file}" hidden="hidden">
        <input type="submit" value="Delete this file">
    </form>
    ''')
    data = ""
    if mimetypes.guess_type(file)[0]:
        if mimetypes.guess_type(file)[0].split("/", 1)[0] == 'image':
            with(open(file,"rb")) as f:
                data = f.read()
            b64encode_data = base64.b64encode(data)
            base64_str = b64encode_data.decode('utf-8')
            src = 'data: ' + mimetypes.guess_type(file)[0] + ';base64,' + base64_str
            print(f'<img src="{src}">')
            continue

    with(open(file,"r",encoding='utf8')) as f:
        contents = []
        while line := f.readline():
            for i in [["\"","\\&quot;"], ["<","&lt;"], [">","&gt;"]]:
                line = str(line).replace(i[0],i[1])
            print(line+'</br>')
