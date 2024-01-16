import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import random

sender_address = 'letussharebook@gmail.com'
sender_pass_0 = 'hello0this0'
sender_pass = 'izbigkxhlbjvjwro'


def mail(message, recv):
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, recv, text)
    session.quit()


def sendOTP(recv_address, num, sub, msg):
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = recv_address
    message['Subject'] = sub
    OTP = ''
    for i in range(num): 
        a = chr(random.randint(65,90))
        A = chr(random.randint(97,122))
        N = str(random.randint(0,9))
        b = random.randint(0,2)
        if b==0:
            OTP += a
        elif b==1:
            OTP += A
        else:
            OTP += N
    msg = msg + OTP
    message.attach(MIMEText(msg, 'plain'))
    mail(message, recv_address)
    return OTP

def sendTHANK(recv):
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = recv
    message['Subject'] = 'Thank You For Shopping With Shop.Drop'
    msg = 'Thank you for shopping with us. We hope to serve you again\nTeam Shop.Drop'
    message.attach(MIMEText(msg, 'plain'))
    mail(message, recv)
    
