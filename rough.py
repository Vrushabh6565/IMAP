from socket import *
import ssl
s = socket(AF_INET, SOCK_STREAM)
s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23)
ip = gethostbyname("imap.gmail.com")
s.connect((ip,993))
resp = s.recv(1024)
print(resp)
print("connected")
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



