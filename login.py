from socket import *
import ssl
from colorama import Fore, Style
from folders import *
from os import system
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
    print(folder_dict)
    folder_dict['X'] = ' LOGOUT'
    print_dict(folder_dict)
    print("\n\n")
    for i in range(10):
        print('\t')
    select = str(input("ENTER CHOICE : "))
    select_folder(select, folder_dict)


def select_folder(select, folder_dict):
    query = "a001 Select{0}\r\n".format(folder_dict.get(select))
    query = bytes(query, 'utf-8')
    try:
        s.send(query)
        resp = s.recv(4096)
        open_folder(folder_dict.get(select), resp)
        return None
    except:
        print("UNABLE TO FETCH ",folder_dict.get(select),"\n")
        return None


def open_folder(folder_name, resp):
    #clear()
    resp = resp.decode()
    list = resp.split("\r\n")
    if ('NO' in list[-2] or 'BAD' in list[-2]):
        print("UNABLE TO WENT INTO INBOX RETURNED\n")
        return None
    print("\t\t\t\t\t-----------------",folder_name,"-----------------\n")
    try:
        UIDS = "a001 UID SEARCH ALL\r\n"
        UIDS = bytes(UIDS, 'utf-8')
        s.send(UIDS)
        all_uids = s.recv(4096).decode()
        while(True):
            if ('a001 OK' in all_uids):
                break
            elif('a001 NO' in all_uids or 'a001 BAD' in all_uids):
                print("1. UNABLE TO FETCH\n")
                return None
            all_uids += s.recv(4096).decode()
        list = all_uids.split("\r\n")
        list = list[0].split(" ")
        list = list[2:]
        start_uid = int(list[0])
        end_uid = int(list[-1])
        print_mail_headers(s, start_uid, end_uid)
        return None

    except:
        print("SOMETHING WENT WRONG\n")
        return None
