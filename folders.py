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


