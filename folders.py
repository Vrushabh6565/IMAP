import base64
from os import mkdir
def logout(s):
    msg = "a001 LOGOUT\r\n"
    msg = bytes(msg, 'utf-8')
    try:
        s.send(msg)
        resp = s.recv(1024).decode()
        print("LOGGED OUT SUCCESSFULLY\n")
        return 0
    except(ConnectionResetError):
        print("CONNECTION FORCEFULLY CLOSED BY SERVER\n")
        return 0

def unselect(s):
    msg = "a001 Close\r\n"
    msg = bytes(msg, 'utf-8')
    s.send(msg)
    resp = s.recv(1024).decode()
    print(resp)
    if('a001 OK' in resp):
        return 1
    else:
        return None

def inbox(s):
    msg = "a001 Select \"INBOX\"\r\n"
    msg = bytes(msg, 'utf-8')
    try:
        s.send(msg)
        resp = s.recv(4096).decode()
        return resp
    except:
        print("ERROR")
        return 0

def list_folders(s):
    list = "a002 LIST \"\" \"*\"\r\n"
    list = bytes(list, 'utf-8')
    s.send(list)
    list = s.recv(4096).decode()
    while (True):
        if ('a002 OK' in list):
            break
        elif ('a002 NO' in list or 'a002 BAD' in list):
            print("1. UNABLE TO FETCH\n")
            return None
        list += s.recv(4096).decode()
    list1 = list.split("\r\n")
    if('OK' in list1[-2]):
        list2 = []
        for i in list1[0:len(list1)-2]:
            if("HasChildren" in i):
                continue
            list2.append(i.split("\"/\"")[1])
        return list2
    else:
        print("UNABLE TO FETCH EXISTING FOLDERS...\n")
        return None

def content_html(s,file,charset, uid):
    auth2 = "a004 UID FETCH {0} (BODY[TEXT])\r\n".format(uid)
    s.send(auth2.encode())
    b = s.recv(8192).decode(charset)
    while ('a004 OK' not in b):
        b += s.recv(8192).decode(charset)
    c = b.split("}")[1]
    c = c.split("\r\n\r\n")[0]
    d = base64.standard_b64decode(c)
    file.write(d.decode())
    return 1

def content_plain(s,charset, uid):
    try:
        auth2 = "a004 UID FETCH {0} (BODY[TEXT])\r\n".format(uid)
        s.send(auth2.encode())
        b = s.recv(8192).decode(charset)
        while ('a004 OK' not in b):
            b += s.recv(8192).decode(charset)
        c = b.split("}")[1]
        c = c.split(")\r\n")[0]
        print(c)
        return 1
    except:
        print("WRONG IN CONTENT PLAIN")
        return 0

def decode(encoding,content):
    if(encoding == "quoted-printable"):
        return content
    elif(encoding == base64):
        d = base64.standard_b64decode(content)
        return d.decode()


def mixed_body(s,x,uid):
    print("mix called")
    html = []
    html_files = []
    inline_files = []
    inline = []
    attachment_files = []
    attachment = []
    auth2 = "a004 UID FETCH {0} (BODY[TEXT])\r\n".format(uid)
    s.send(auth2.encode())
    b = s.recv(8192).decode()
    while ('a004 OK' not in b):
        b += s.recv(8192).decode()
    c = b.split("}")[1]
    a = b.find('}')
    c = b[a+3:]
    if("Content-Type: text/html" in c):
        c = c.split("Content-Type: text/html; charset=")[1]
        charset = c.split("\r\n")[0]
        encoding = c.split("Content-Transfer-Encoding: ")[1]
        encoding = encoding.split("\r\n\r\n")[0]
        split_str = "Content-Transfer-Encoding: "+encoding+"\r\n\r\n"
        encoded_content = c.split(split_str)[1]
        encoded_content = encoded_content.split(x)[0]
        decoded_html = decode(encoding,encoded_content)
        html_files.append("main.html")
        html.append(decoded_html)
    if("Content-Disposition: " in b):
        files = b.split("Content-Disposition: ")
        files = files[1:]
        for i in files:
            file_type = i.split(";")[0]
            file_name = i.split("filename=")[1]
            file_name = file_name.split(";")[0]
            file_name = file_name[1:]
            file_name = file_name[:-1]
            encode = i.split("Content-Transfer-Encoding: ")[1]
            encode = encode.split("\r\n")[0]
            content = i.split("\r\n\r\n")[1]
            decoded_content = decode(encode,content)
            if(file_type == "inline"):
                inline.append(decoded_content)
                inline_files.append(file_name)
            elif(file_type == "attachment"):
                attachment.append(decoded_content)
                attachment_files.append(file_name)
    print(html_files,len(html))
    print(inline_files,len(inline))
    print(attachment_files,len(attachment))
    path = "C:/Users/VRUSHABH/Desktop/login/" + str(uid)
    mkdir(path)
    i = 0
    for i in range(0,len(html_files)):
        path1 = ''
        path1 = path + "/" + html_files[i]
        file1 = open(path1,"w")
        file1.write(html[i])
        file1.close()
    i = 0
    for i in range(0, len(inline_files)):
        path1 = ''
        path1 = path + "/" + inline_files[i]
        file1 = open(path1,"wb")
        file1.write(inline[i])
        file1.close()
    i = 0
    for i in range(0, len(attachment_files)):
        path1 = ''
        path1 = path + "/" + attachment_files[i]
        file1 = open(path1,"wb")
        file1.write(attachment[i])
        file1.close()
    return None