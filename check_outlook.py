import base64
from socket import *
from sys import *
import ssl
s = socket(AF_INET, SOCK_STREAM)
s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23)
ip = gethostbyname("imap-mail.outlook.com")
s.connect((ip,993))
resp = s.recv(1024)
print(resp)
UserName = ""
Pass = ""
auth = 'a001 login {0} {1}\r\n'.format(UserName,Pass)
print(auth)
auth = bytes(auth, 'utf-8')
s.send(auth)
b = s.recv(1024)
print(b)
auth = 'a001 CAPABILITY\r\n'
print(auth)
auth = bytes(auth, 'utf-8')
s.send(auth)
b = s.recv(1024)
print(b)
