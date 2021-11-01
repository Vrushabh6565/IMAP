from inputs import *

mails = mail_ids()
subject = mail_subject()
body = mail_body()
s = connect()
if(set_sender_receiver(mails, s)):
    if(send_mail(mails, subject, body, s)):
        print("mail send successfully")