from socket import *
import ssl
s = socket(AF_INET, SOCK_STREAM)
s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23)
ip = gethostbyname("imap.gmail.com")
s.connect((ip,993))
resp = s.recv(1024)
print(resp)
print("connected")
UserName = ""
Pass = ""
auth = 'a001 login {0} {1}\r\n'.format(UserName,Pass)
print(auth)
auth = bytes(auth, 'utf-8')
s.send(auth)
b = s.recv(1024)
print(b)
auth1 = "a002 Select \"inbox\"\r\n"
auth1 = bytes(auth1, 'utf-8')
s.send(auth1)
print(s.recv(1024))
'''auth2 = "a003 SEARCH ALL\r\n"
auth2 = bytes(auth2, 'utf-8')
s.send(auth2)
print(s.recv(4096))
auth3 = "a003 UID SEARCH ALL\r\n"
auth3 = bytes(auth3, 'utf-8')
s.send(auth3)
print(s.recv(1024))
auth2 = "a004 UID FETCH 1555 (BODY[])\r\n"
s.send(auth2.encode())
a = s.recv(2048)
while(len(a) == 1024):
    print(a)
    a = s.recv(2048)
print("\n\n\nDONE DONE DONE\n\n\n")

s.send("a001 LOGOUT\r\n".encode('utf-8'))
print(s.recv(1024))'''

''''
auth1 = "a001 \"LOGOUT\"\r\n"
auth1 = "a002 LIST \"\" \"*\"\r\n"
auth1 = bytes(auth1, 'utf-8')
s.send(auth1)'''



