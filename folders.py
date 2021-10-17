def logout(s):
    msg = "a001 LOGOUT\r\n"
    msg = bytes(msg, 'utf-8')
    try:
        s.send(msg)
        resp = s.recv(1024).decode()
        print("LOGGED OUT SUCCESSFULLY\n")
        return 1
    except(ConnectionResetError):
        print("CONNECTION FORCEFULLY CLOSED BY SERVER\n")
        return 1

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
    list = s.recv(4096)
    list = list.decode()
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

def print_mail_headers(s, start, end):
    query = "a001 UID FETCH {0}:{1} (UID BODY[HEADER.FIELDS (FROM DATE SUBJECT)])\r\n".format(start,end)
    query = bytes(query, 'utf-8')
    s.send(query)
    all_uids = s.recv(4096).decode()
    while (True):
        if ('OK' in all_uids):
            break
        elif ('NO' in all_uids or 'BAD' in all_uids):
            print("1. UNABLE TO FETCH\n")
            return None
        all_uids += s.recv(4096).decode()
    print(all_uids)

