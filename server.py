from attack_prediction import predict
from datetime import datetime
from hashlib import md5
import pandas as pd
import yagmail
import socket
import time


print("-------------------------------------")

print("[SERVER STARTED] Server started ..")

print()

ip_address = socket.gethostbyname(socket.gethostname())

print("[IP ADDRESS] Server running at ip address : ", ip_address)

print()

port = 5002

print("[PORT] Server running on port number : ", port)

print()

s = socket.socket()
s.bind((ip_address, port))
s.listen(5)

print("[LISTENING] Waiting for connection ..")


def check_ip_address(ip):
    r1 = pd.read_excel('responsive_blocked_ip.xlsx')
    flag = False
    for index, row in r1.iterrows():
        if row["ip_address"] == str(ip):
            flag = True
    return flag


def insert_into_excel(file, address, res):
    date = datetime.today()
    r2 = pd.read_excel(file)
    new_row = [date, address, res]
    r2.loc[-1] = new_row
    r2 = r2.reset_index(drop=True)
    r2.to_excel(file, index=False)

while True:
    c, addr = s.accept()
    client_ip = addr[0]
    checking = check_ip_address(client_ip)
    if not checking:
        print('[CONNECTED] Connection got from ' + str(client_ip))
        print()
        msg = c.recv(20480)
        print('[RECEIVING] Receiving file from client')
        print()
        f = open('in_folder/test.xlsx', 'wb')
        f.write(msg)
        f.close()
        time.sleep(10)  
        print('[PREDICTION] Predicting...')
        print()

        try:
            result = predict()
            print('[RESULT] Predicted result is ', result)
            print("-------------------------------------")
            print()

            insert_into_excel('responsive_ip_log.xlsx', client_ip, result)

            if result != "normal":
                insert_into_excel('responsive_blocked_ip.xlsx', client_ip, result)

                user = yagmail.SMTP(user='guru22ca@gmail.com', password='xqcvhyfdcvctgyly')
                user.send(to='guru22ca@gmail.com', subject='ALERT',
                        #   contents=f"{result}  intrusion has been found.")
                        contents=f"Dear Customer, We have recently detected a suspicious activity on our network that indicates a potential probe attack. This type of attack is an attempt by an attacker to gather information about our network to identify potential vulnerabilities.It is important that you remain vigilant and report any suspicious activity that you may come across. ATTACK TYPE: {result}")
                print("Email sent successfully")
                with open("in_folder/test.xlsx", 'rb') as f:
                    word = f.read()
                hashed = md5(word).hexdigest()

                r1 = pd.read_excel("responsive_signature.xlsx")
                for index, row in r1.iterrows():
                    if row["signature"] == hashed:
                        print("already presented")
                        break
                else:
                    insert_into_excel('responsive_signature.xlsx', client_ip, hashed)
                    print("signature added")

        except Exception as e:
            print('[ERROR] from server', e)
            print("-------------------------------------")

        # os.remove('in_folder/test.xlsx')
        c.close()
        print("[LISTENING] Waiting for new connection ..")
    else:
        print("[WARNING] Blocked Client Found....")
        c.close()
        print('-----------------------------------------')
        print("[LISTENING] Waiting for new connection ..")


