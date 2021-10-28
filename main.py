import sys
from login import *
from folders import *
def flagChecker():
    u = f = p = d = 0
    userName = Password = domain = file_path = ''
    i = 1
    arg_len = len(sys.argv)
    while(i < arg_len):
        if(sys.argv[i] == '-u'):
            u = u + 1
            if(i+1 < arg_len):
                i = i + 1
                userName = sys.argv[i]
                i = i + 1
                continue
            else:
                print("NO USERNAME SPECIFIED\n")
                return
        elif (sys.argv[i] == '-p'):
            p = p + 1
            if (i + 1 < arg_len):
                i = i + 1
                Password = sys.argv[i]
                i = i + 1
                continue
            else:
                print("NO PASSWORD SPECIFIED\n")
                return
        elif (sys.argv[i] == '-f'):
            f = f + 1
            if (i + 1 < arg_len):
                i = i + 1
                file_path = sys.argv[i]
                i = i + 1
                continue
            else:
                print("NO FILE NAME SPECIFIED\n")
                return
        elif (sys.argv[i] == '-d'):
            d = d + 1
            if (i + 1 < arg_len):
                i = i + 1
                domain = sys.argv[i]
                i = i + 1
                continue
            else:
                print("NO DOMAIN NAME SPECIFIED\n")
                return
        else:
            print("WRONG ARGUMENTS PASSED\n")
            return

    bin = str(f)+str(u)+str(p)+str(d)
    log_auth = create_auth_table(bin,userName,Password,domain,file_path)
    return log_auth

def create_auth_table(bin, u, p, d, f):
    log_auth = []
    if(bin == '1001'):
        file = open(f, 'r')
        for i in file:
            log_auth = i.split(":")
            if(len(log_auth) != 2):
                print("PLEASE CHECK CREDENTIAL DETAILS FORMAT IN FILE")
                return None
            else:
                log_auth.append(d)
                return log_auth
    elif(bin == '0111'):
        log_auth.append(u)      #['userName', .Password', 'domain']
        log_auth.append(p)
        log_auth.append(d)
        return log_auth
    else:
        print("INAPPROPRIATE USE OF FLAGS")


if __name__ == '__main__':
    auth = flagChecker()
    if(auth == None):
        print("PLEASE CHECKS FLAG AND VALUES AGAIN\n")
        sys.exit()
    if(login(auth)):
        call_back = authenticated_state()
        while(call_back):
            call_back = authenticated_state()
