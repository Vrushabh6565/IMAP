import sys
from os import system
a = b'* FLAGS (\\Answered \\Flagged \\Draft \\Deleted \\Seen $NotPhishing $Phishing)\r\n* OK [PERMANENTFLAGS (\\Answered \\Flagged \\Draft \\Deleted \\Seen $NotPhishing $Phishing \\*)] Flags permitted.\r\n* OK [UIDVALIDITY 1] UIDs valid.\r\n* 76 EXISTS\r\n* 0 RECENT\r\n* OK [UIDNEXT 1629] Predicted next UID.\r\n* OK [HIGHESTMODSEQ 177044]\r\na001 OK [READ-WRITE] INBOX selected. (Success)\r\n'
a = a.decode()
list = a.split("\r\n")
print("\n\n")
for i in list:
    print(i)
if('OK' in list[1] and 'OK' in list[-2]):
    print("followings flags are possible\n")
    a = list[1].split("\\")
    for i in a[1:len(a) - 1]:
        print("@ ",i)