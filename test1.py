a = b'* SEARCH 29\r\na002 OK SEARCH completed (Success)\r\n'
a = a.decode()
list = a.split("\r\n")
list = list[0].split(" ")
print(list)
list = list[2:]
print(list)
