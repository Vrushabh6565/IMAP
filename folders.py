import base64
from os import mkdir

def MAILBOX(s):
    folders = list_folders(s)
    if(folders):
        folder_dict = {}
        alpha = 'A'
        for i in folders:
            folder_dict[alpha] = i
            alpha = chr(ord(alpha) + 1)
        return folder_dict

def print_dict(dict):
    for i,j in dict.items():
        for k in range(10):
            print('\t',end='')
        print(i, end=" : ")
        print(j)
    return None

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
    if (charset == "us-ascii" or charset == "7 bit" or charset == "quoted-printable" or charset == ''):
        file.write(c)
        return 1
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
    if(encoding == "quoted-printable" or encoding == "7bit" or encoding == "us-ascii" or encoding == '' or encoding == '8bit'):
        return content
    elif(encoding == "base64"):
        d = base64.standard_b64decode(content)
        return d

'''def mixed_body(s,x,uid):
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
    print(b)
    c = b.split("}")[1]
    a = b.find('}')
    c = b[a+3:]
    c = c.split("Content-Type: text/html; charset=")[1]
    charset = c.split("\r\n")[0]
    if("Content-Transfer-Encoding: " in c):
        encoding = c.split("Content-Transfer-Encoding: ")
        if ("filename=" in encoding[0]):
            encoding = ''
        else:
            encoding = encoding[1]
            encoding = encoding.split("\r\n")[0]
    else:
        encoding = ''
    content_index = c.find("\r\n\r\n")
    split_str = c[content_index+4:]
    split_str = split_str.split(x)[0]
    decoded_html = decode(encoding,split_str)
    html_files.append("main.html")
    html.append(decoded_html)
    if("Content-Disposition: " in b):
        files = b.split("Content-Disposition: ")
        files = files[1:]
        for i in files:
            file_type = i.split(";")[0]
            file_name = i.split("filename=")[1]
            file_name = file_name.split("\"")[1]
            #file_name = file_name[1:]
            #file_name = file_name[:-1]
            encode = i.split("Content-Transfer-Encoding: ")[1]
            encode = encode.split("\r\n")[0]
            content_index = i.find("\r\n\r\n")
            content = i[content_index+4:]
            split_str = "\r\n--"+x
            content = content.split(split_str)[0]
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
    return None'''

def sub_boundary_split(b):
    print("sub boundary called")
    print("sub split called")
    content_dict = {}
    boundary = b.split("boundary=")[1]
    boundary = boundary.split("\r\n")[0]
    boundary = boundary.split("\"")
    if(len(boundary) == 1):
        boundary = boundary[0]
    elif(len(boundary) == 3):
        boundary = boundary[1]
    boundary = "--"+boundary
    body = b.split(boundary)
    body = body[1:-1]
    for i in body:
        encoding = ""
        if("Content-Type: text/plain" in i):
            charset = i.split("charset=")[1].split("\r\n")[0]
            if("Content-Transfer-Encoding:" in i):
                encoding = i.split("Content-Transfer-Encoding: ")[1].split("\r\n")[0]
            content = i.split("\r\n\r\n")[1]
            decoded_content = decode(encoding, content)
            content_dict["text/plain"] = decoded_content
        elif("Content-Type: text/html" in i):
            charset = i.split("charset=")[1].split("\r\n")[0]
            if ("Content-Transfer-Encoding:" in i):
                encoding = i.split("Content-Transfer-Encoding: ")[1].split("\r\n")[0]
                print(encoding)
            content = i.split("\r\n\r\n")[1]
            decoded_content = decode(encoding, content)
            print("ok till here")
            content_dict["text/html"] = decoded_content
    return content_dict

def dict_maker(files, f_type):
    my_dict = {}
    for k, v in enumerate(files):
        key = f_type + str(k)
        my_dict[key] = v
    return my_dict

def mixed_body(s, boundary, uid):
    print("mixed body called")
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
    file = open("C:/Users/VRUSHABH/Desktop/login/c.txt", "w",errors='replace')
    file.write(b)
    boundary = "--"+boundary
    b = b.split(boundary)
    b = b[1:-1]
    if("boundary=" in b[0]):
        content_dict = sub_boundary_split(b[0])
        if(len(content_dict) != 0):
            for key, value in content_dict.items():
                if(key == "text/plain"):
                    print(value)
                elif(key == "text/html"):
                    html_files.append("main.html")
                    html.append(value)
    b = b[1:]
    for i in b:
        i = i.split("\r\n\r\n")
        if ("Content-Disposition: " in i[0]):
            position_type = i[0].split("Content-Disposition: ")[1]
            position_type = position_type.split(";")[0]
            filename = ""
            encoding = ""
            if ("filename=" in i[0]):
                filename = i[0].split("filename=")[1].split("\r\n")[0]
                filename = filename.split("\"")[1]
            elif ("name=" in i[0]):
                filename = i[0].split("name=")[1].split("\r\n")[0]
                filename = filename.split("\"")[1]
            else:
                filename = "unknown.txt"  # working
            if ("Content-Transfer-Encoding: " in i[0]):
                encoding = i[0].split("Content-Transfer-Encoding: ")[1].split("\r\n")[0]
            encoded_content = "\r\n\r\n"
            encoded_content = encoded_content.join(i[1:])
            decoded_content = decode(encoding, encoded_content)
            if (position_type == "attachment"):
                attachment_files.append(filename)
                attachment.append(decoded_content)
            elif (position_type == "inline"):
                inline_files.append(filename)
                inline.append(decoded_content)
        elif ("Content-Disposition: " not in i):
            encoding = ""
            if ("Content-Type: text/plain" in i[0]):
                charset = i[0].split("charset=")[1].split("\r\n")[0]
                if ("Content-Transfer-Encoding:" in i):
                    encoding = i[0].split("Content-Transfer-Encoding: ")[1].split("\r\n")[0]
                content = i[1]
                decoded_content = decode(encoding, content)
                print(decoded_content)
            elif ("Content-Type: text/html" in i[0]):
                print("i reached inside")
                charset = i[0].split("charset=")[1].split("\r\n")[0]
                if ("Content-Transfer-Encoding:" in i):
                    encoding = i[0].split("Content-Transfer-Encoding: ")[1].split("\r\n")[0]
                content = i[1]
                decoded_content = decode(encoding, content)
                html_files.append("main1.html")
                html.append(decoded_content)
    html_dict = dict_maker(html_files, 'h')
    inline_dict = dict_maker(inline_files, 'i')
    attachment_dict = dict_maker(attachment_files, 'a')
    if(len(html_dict) != 0):
        print("main mail : ")
        for k,v in html_dict.items():
            print("\t\t",k," : ",v,"\r\n")
    if (len(inline_dict) != 0):
        print("inline files : ")
        for k, v in inline_dict.items():
            print("\t\t", k, " : ", v, "\r\n")
    if (len(attachment_dict) != 0):
        print("attachment files : ")
        for k, v in attachment_dict.items():
            print("\t\t", k, " : ", v, "\r\n")

    print("if do not wnant to download any attachment then press \".\"\r\n *give all file names SPACE SEPERATED*")
    download_choice = str(input("enter files you want to download : "))
    if(download_choice == "."):
        return None
    download_html = []
    download_inline = []
    download_attachment = []
    download_choice = download_choice.split(" ")
    for i in download_choice:
        if(i[0] == 'h' and int(i[1]) < len(html_files)):
            download_html.append(int(i[1]))
        elif (i[0] == 'i' and int(i[1]) < len(inline_files)):
            download_inline.append(int(i[1]))
        elif (i[0] == 'a' and int(i[1]) < len(attachment_files)):
            download_attachment.append(int(i[1]))
        else:
            print(i,"is not downloadable")
            continue
    path = "C:/Users/VRUSHABH/Desktop/login/" + str(uid)
    mkdir(path)
    for i in download_html:
        path1 = ''
        path1 = path + "/" + html_files[i]
        file1 = open(path1, "w",errors='replace')
        file1.write(html[i])
        file1.close()
    for i in download_inline:
        path1 = ''
        path1 = path + "/" + inline_files[i]
        file1 = open(path1, "wb")
        file1.write(inline[i])
        file1.close()
    for i in download_attachment:
        path1 = ''
        path1 = path + "/" + attachment_files[i]
        file1 = open(path1, "wb")
        file1.write(attachment[i])
        file1.close()
    return None

def delete(s,uid):
    print("please check the details again\n")
    auth2 = "a004 UID FETCH {0} (BODY[HEADER.FIELDS (FROM TO DATE SUBJECT)])\r\n".format(uid)
    s.send(auth2.encode())
    b = s.recv(8192).decode()
    while ('a004 OK' not in b):
        b += s.recv(8192).decode()
    print(b)
    choice = str(input("WANT TO DELETE[Y/N] : "))
    if (choice == "Y" or choice == "y"):
        auth2 = "a004 UID STORE {0} +FLAGS (\Deleted)\r\n".format(uid)
        s.send(auth2.encode())
        b = s.recv(8192).decode()
        while ('a004 OK' not in b):
            b += s.recv(8192).decode()
        auth2 = "a004 EXPUNGE\r\n"
        s.send(auth2.encode())
        b = s.recv(8192).decode()
        while ('a004 OK' not in b):
            b += s.recv(8192).decode()
        print("mail deleted successfully")
        return 9
    elif (choice == "N" or choice == "n"):
        return 9
    else:
        print("wrong input")
        return 9

def set_flag(s, uid):
    print("S : SET FLAGS\t\t R : REMOVE FLAGS\t\tC: Check flags\nAny other key to exit")
    choice = str(input("enter choice : "))
    if(choice == 'C' or choice == 'c'):
        auth2 = "a004 UID FETCH 39 FLAGS\r\n"
        s.send(auth2.encode())
        b = s.recv(8192).decode()
        while ('a004 OK' not in b):
            b += s.recv(8192).decode()
        b = b.split("a004 OK")[0]
        b = b.split("FETCH ")[1]
        print(b)
        return 9
    elif(choice == "S" or choice == "s" or choice == 'R' or choice == "r"):
        status = ""
        if(choice == "S" or choice == "s"):
            status = "+FLAGS"
        elif(choice == 'R' or choice == "r"):
            status = "-FLAGS"

        print("A: Answered\t\tB: Flagged\t\tC: Draft\t\tE: Seen\n any other key to exit")
        print("for two or more flags give space separated choice\n")
        choice = str(input("enter choice : "))
        choice = choice.split(" ")
        if(('A' in choice) or ('B' in choice) or ('C' in choice) or ('D' in choice)):
            flags = ""
            for i in range(len(choice)):
                if(choice[i] == 'A' or choice == 'a'):
                    if(i == 0):
                        flags = flags + "/Answered"
                    else:
                        flags = flags + " /Answered"
                elif (choice[i] == 'B' or choice == 'b'):
                    if (i == 0):
                        flags = flags + "/Flagged"
                    else:
                        flags = flags + " /Flagged"
                elif (choice[i] == 'C' or choice == 'c'):
                    if (i == 0):
                        flags = flags + "/Draft"
                    else:
                        flags = flags + " /Draft"
                elif (choice[i] == 'D' or choice == 'd'):
                    if (i == 0):
                        flags = flags + "/Seen"
                    else:
                        flags = flags + " /Seen"
                else:
                    print("wrong choice {0} . skipped...".format(choice[i]))
            auth2 = "a004 UID STORE {0} {1} ({2})\r\n".format(uid, status, flags)
            s.send(auth2.encode())
            b = s.recv(8192).decode()
            while ('a004 OK' not in b):
                b += s.recv(8192).decode()
            print(b)
            print("flags set/removed successfully")
            return 9

    else:
        print("returning back")
        return 9


def create_folder(s):
    print("R : return to main menu C: CREATE D : DELETE\n")
    choice = str(input("enter choice :"))
    if(choice == "R" or choice == 'r'):
        return 1
    elif(choice == "C" or choice == "c"):
        f_name = str(input("Enter folder name : "))
        auth1 = "a002 CREATE {0}\r\n".format(f_name)
        s.send(auth1.encode())
        resp =  s.recv(1024).decode()
        if("a002 OK" in resp):
            print("folder created successfully\n")
        else:
            print("unable to create folder(May folder with entered name already exist)\n")
        return 1

    elif(choice == "D" or choice == "d"):
        folder_dict1 = MAILBOX(s)
        print_dict(folder_dict1)
        print("select the folder you want to delete")
        choice = str(input("Enter choice : "))
        folder = folder_dict1.get(choice)
        if(folder):
            print("Do you really want to delete folder", folder, " [Y/N]: ")
            confirm = str(input("confirm : "))
            if(confirm == "Y" or confirm == "y"):
                folder = folder.split("\"")[1]
                auth1 = "a002 DELETE {0}\r\n".format(folder)
                s.send(auth1.encode())
                resp = s.recv(1024).decode()
                if("a002 OK" in resp):
                    print("folder deleted successfully")
                else:
                    print("selected internal folder which cannot be deleted")
                return 1
            else:
                return 1
        else:
            print("Wrong folder choice")
            return 1
    else:
        return 1

def copy(s, id):
    folder_dict1 = MAILBOX(s)
    print_dict(folder_dict1)
    print("select the destination folder")
    choice = str(input("Enter choice : "))
    folder = folder_dict1.get(choice)
    if (folder):
        folder = folder.split("\"")[1]
        auth1 = "a002 COPY {0} {1}\r\n".format(id, folder)
        auth1 = bytes(auth1, 'utf-8')
        s.send(auth1)
        resp = s.recv(1024).decode()
        if("a002 OK" in resp):
            print("mail copied to folder ", folder)
        else:
            print("unable to copy mail")
        return 9
    else:
        print("wrong choice")
        return 9
