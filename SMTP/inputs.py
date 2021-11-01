from socket import *

def connect():
    ip = gethostbyname("new.toad.com")
    s = socket(AF_INET, SOCK_STREAM)
    resp = s.connect((ip, 25))
    msg = "HELO new.toad.com\r\n"
    s.send(msg.encode())
    resp = s.recv(8000).decode()
    a = resp.split(" ")[0]
    b = resp.split("\r\n")[1].split(" ")[0]
    if (a == "220" and b == "250"):
        return s
    else:
        print("UNABLE TO CONNECT\r\n")
        return 0


def mail_ids():
    sender = str(input("Enter your mail id : "))
    receiver = str(input("Enter receivers mail id :"))
    print("please enter \".\" if you do not want to add in CC\n")
    cc = str(input("Enter CC recipient: "))
    mails = [sender, receiver, cc]
    return mails


def mail_subject():
    subject = str(input("SUBJECT:"))
    return subject

def mail_body():
    print("------------enter body of th mail----------------\r\n")
    body = str(input())
    return body

def set_sender_receiver(mails, s):
    sender_flag = receiver_flag = 0
    mail_from = mails[0]
    rcpt_to = mails[1]
    mail_from = "mail from:<" + mail_from + ">\r\n"
    s.send(mail_from.encode())
    resp = s.recv(2048).decode()
    print(resp)                               #
    if("ok" in resp):
        sender_flag = 1
    rcpt_to = "rcpt to:<" + rcpt_to + ">\r\n"
    s.send(rcpt_to.encode())
    resp = s.recv(8000).decode()
    print(resp)                                          #
    if("ok" in resp):
        receiver_flag = 1
    if(sender_flag == 1 and receiver_flag == 1):
        return 1
    else:
        return 0

def send_mail(mails, subject, body, s):
    s.send("DATA".encode())
    resp = s.recv(2048).decode()
    if("Enter mail" not in resp):
        print("MAIL NOT SENT\n")
        return 0
    build_body = ""
    build_body = "Subject:" + subject +"\r\nFrom:" + mails[0] + "\r\nto:" + mails[1] + "\r\n"
    if(mails[2] != "."):
        build_body = "Cc:" + mails[2] + "\r\n"
    build_body = build_body + body + "\r\n"
    build_body = build_body + ".\r\n"
    print(build_body)
    s.send(build_body.encode())
    resp = s.recv(2048).decode()
    if("Message accepted" in resp):
        resp = resp.split(" ")[2]
        print("msg send with id ",resp)
        return 1
    else:
        print("msg not sent")
        return 0
