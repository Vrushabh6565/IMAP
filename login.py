import base64

from folders import *
from os import system
from socket import *
import ssl
from colorama import *
#import base64
clear = lambda: system('clear')

s = socket(AF_INET, SOCK_STREAM)
s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23)

def login(auth):
    try:
        ip = gethostbyname(auth[2])
    except:
        print("SERVER NOT RESPONDED PLEASE CHECK DOMAIN ELSE RETRY\n")
        return None
    try:
        s.connect((ip,993))
        resp = s.recv(1024).decode()
        list = resp.split()
        if(list[1] != 'OK'):
            print("CONNECTION REFUSED FROM SERVER\n")
            return None
    except:
        print("CONNECTION TIMEOUT\n")
        return None
    userName = auth[0]
    Password = auth[1]
    if(not authenticate(userName, Password, s)):
        return 0
    return 1


def authenticate(userName, Password, s):
    auth = 'a001 login {0} {1}\r\n'.format(userName, Password)
    auth = bytes(auth, 'utf-8')
    s.send(auth)
    resp = s.recv(1024).decode()
    list = resp.split()
    if('OK' in list):
        print(f'{Fore.GREEN}WELCOME{Style.RESET_ALL}')
        return 1
    else:
        print(f'{Fore.RED}LOGIN AUTHENTICATION FAILED PLEASE CHECK YOUR MAIL-ID AND PASSWORD{Style.RESET_ALL}')
        return 0

def MAILBOX():
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

def authenticated_state():
    folder_dict = MAILBOX()
    folder_dict['X'] = ' LOGOUT'
    print_dict(folder_dict)
    print("\n\n")
    for i in range(10):
        print('\t')
    select = str(input("ENTER CHOICE : "))
    return select_folder(select, folder_dict)


def select_folder(select, folder_dict):
    if(select == "X"):
        return logout(s)
    query = "a001 Select{0}\r\n".format(folder_dict.get(select))
    query = bytes(query, 'utf-8')
    if(True):
        s.send(query)
        resp = s.recv(4096)
        return open_folder(folder_dict.get(select), resp)
    else:
        print("UNABLE TO FETCH ",folder_dict.get(select),"\n")
        return None

def get_uid_list():
    UIDS = "a001 UID SEARCH ALL\r\n"
    UIDS = bytes(UIDS, 'utf-8')
    s.send(UIDS)
    all_uids = s.recv(4096).decode()
    while (True):
        if ('a001 OK' in all_uids):
            break
        elif ('a001 NO' in all_uids or 'a001 BAD' in all_uids):
            print("1. UNABLE TO FETCH\n")
            return None
        all_uids += s.recv(4096).decode()
    list = all_uids.split("\r\n")
    list = list[0].split(" ")
    list = list[2:]
    return list

def open_folder(folder_name, resp):
    #clear()
    resp = resp.decode()
    list = resp.split("\r\n")
    if ('NO' in list[-2] or 'BAD' in list[-2]):
        print("UNABLE TO WENT INTO",folder_name,"\n")
        return None
    print("\t\t\t\t\t-----------------",folder_name,"-----------------\n")
    if(True):
        list = get_uid_list()
        if(len(list) == 0):
            start_uid = -1
            end_uid = -1
        else:
            start_uid = int(list[0])
            end_uid = int(list[-1])
        return print_mail_headers(s, start_uid, end_uid)

    else:
        print("open folder SOMETHING WENT WRONG\n")
        return None

def print_mail_headers(s, start, end):
    if(start == -1 and end == -1):
        print("NO MAILS IN THIS FOLDER\n")
        print("R : RETURN TO MAIN MENU\t\tX : LOGOUT\n\n")
        while(True):
            choice = str(input("CHOICE : "))
            if(choice == 'R'):
                return unselect(s)
            elif(choice == 'X'):
                return logout(s)
            else:
                print("WRONG CHOICE!!!")
    query = "a001 UID FETCH {0}:{1} (UID BODY[HEADER.FIELDS (FROM DATE SUBJECT)])\r\n".format(start,end)
    query = bytes(query, 'utf-8')
    s.send(query)
    all_uids = s.recv(4096).decode()
    print(all_uids)
    while (True):
        if ('a001 OK ' in all_uids):
            break
        elif ('a001 NO ' in all_uids or 'a001 BAD ' in all_uids):
            print("1. UNABLE TO FETCH\n")
            return None
        all_uids = s.recv(4096).decode()
        print(all_uids)
    ret = 9
    while(ret == 9):
        ret = all_mail_next_window(start, end)
    return ret

def all_mail_next_window(start, end):
    print("\n\nA : read message\tR : Back to main menu\tX : logout\n\n")
    choice = str(input("CHOICE : "))
    if(choice == 'X'):
        return logout(s)
    elif(choice == 'R'):
        return unselect(s)
    elif(choice == 'A'):
        list = get_uid_list()
        UID = int(input("Enter UID number : "))
        if(str(UID) in list):
            body_by_mime(UID,2)
            #query = "a001 UID FETCH {0} (BODY[HEADER.FIELDS (CONTENT-TYPE)])\r\n".format(UID)
            #query = bytes(query, 'utf-8')
            #s.send(query)
            #msg_uids = s.recv(4096).decode()
            #print(msg_uids)
            #query = "a001 UID FETCH {0} (BODY[])\r\n".format(UID)
            #query = bytes(query, 'utf-8')
            #s.send(query)
            #msg_uids = s.recv(4096).decode()
            # print(msg_uids)
            # while (True):
            #     if ('a001 OK ' in msg_uids):
            #         break
            #     elif ('a001 NO ' in msg_uids or 'a001 BAD ' in msg_uids):
            #         print("1. UNABLE TO FETCH\n")
            #         return None
            #     msg_uids += s.recv(4096).decode()
            # #msg = base64.decode(msg_uids)   #msg decoding part remaining
            # print(msg_uids)
            return 9

def get_bodystructure(UID):
    query = "a001 UID FETCH {0} (BODYSTRUCTURE)\r\n".format(UID)
    query = bytes(query, 'utf-8')
    s.send(query)
    msg_uids = s.recv(4096).decode()
    while (True):
        if ('a001 OK ' in msg_uids):
            break
        elif ('a001 NO ' in msg_uids or 'a001 BAD ' in msg_uids):
            print("1. UNABLE TO FETCH\n")
            return None
        msg_uids += s.recv(4096).decode()
    print(msg_uids)
    return 1

def get_bodyenvelope(UID):
    query = "a001 UID FETCH {0} (BODY ENVELOPE)\r\n".format(UID)
    query = bytes(query, 'utf-8')
    s.send(query)
    msg_uids = s.recv(4096).decode()
    while (True):
        if ('a001 OK ' in msg_uids):
            break
        elif ('a001 NO ' in msg_uids or 'a001 BAD ' in msg_uids):
            print("1. UNABLE TO FETCH\n")
            return None
        msg_uids += s.recv(4096).decode()
    print(msg_uids)
    return 1

def body_by_mime(UID,num):
    query = "a001 UID FETCH {0} (BODY[{1}])\r\n".format(UID,num)
    query = bytes(query, 'utf-8')
    s.send(query)
    msg_uids = s.recv(4096).decode()
    a = msg_uids.split("}")
    b = a[0].split("{")
    c = int(b[-1])
    file = open("C:/Users/VRUSHABH/Desktop/picture.jpg", "wb")
    msg_uids1 = bytes(b[1],'utf-8')
    file.write(msg_uids1)
    total = len(msg_uids)
    i = 0
    msg_uids = msg_uids.encode()
    while (True):
        if ('a001 OK ' in msg_uids.decode()):
            break
        elif ('a001 NO ' in msg_uids.decode() or 'a001 BAD ' in msg_uids.decode()):
            print("1. UNABLE TO FETCH\n")
            return None
        msg_uids = s.recv(4096)
        msg_uids1 = base64.b64decode(msg_uids, '-_')
        file.write(msg_uids1)
        file.flush()
        total += len(msg_uids)
        i = i + 1
        if(i%100 == 0):
            print("DOWNLOADED ==>",float(total/c)*100,"%\n")
    print("DOWNLOADED ==>",100, "%\n")
    file.close()
    return 1