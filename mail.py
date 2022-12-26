import os
from unittest import result
import csv
import datetime
import time
import mysql.connector as msql
from mysql.connector import Error

import smtplib,ssl
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

#from datetime import date, timedelta
import time
print("\n\n\n\n")
print("you're about to see the status of your webservices")
#get current time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)

#get cureent date
CurrentDate=datetime.date.today()  
days = datetime.timedelta(0)

new_date = CurrentDate - days
final_date= new_date.strftime('%Y-%m-%d')
#%d is for date  
#%m is for month  
#Y is for Year  
print(final_date) 
CurrentDate1=datetime.date.today()  
days1 = datetime.timedelta(0)

new_date1 = CurrentDate1 - days1
final_date1= new_date1.strftime('%Y-%m-%d')


path1='C:/python_work/agent_billing/App/agents.txt'
with open(path1, 'r') as file_object:
    lines=file_object.read()
        #print(lines)
    contents1=lines.split()
    #print(contents1)
for code in contents1[:]:
    path2='C:/python_work/agent_billing/App/email.csv'
    with open(path2, 'r') as file_object:
        lines=file_object.read()
            #print(lines)
        contents1=lines.split()
    #     print(contents1)
    #print(contents1)
    email_list=[*csv.DictReader(open('C:/python_work/agent_billing/App/email.csv'))]
    #print(email_list)


    #calling the webservices dictionary to confirm the status
    
    #for bank_code in contents1[:]:
    for emails in email_list[:]:
        
        #print(emails)
        #if emails['bankName']==code:
            bankName=emails['bankName']
            #dest=emails['dest']
            email=emails['email']
            
            #print(bankName)
            #print(code)
            print(email)
        
            

    #Here i want to sent Billing reports to the recipients.
        
            from_addr = 'atalktolade@gmail.com'
            to_addr = f"{email}"
            subject = F'{bankName} BVN_NIN_FRSC_Phone Validation Billing Report'
            content = f'Kindly find your billing report attached between {final_date} and {final_date1}'
            msg = MIMEMultipart()
            msg['From'] = from_addr
            msg['To'] = to_addr
            msg['Subject'] = subject
            body = MIMEText(content, 'plain')
            msg.attach(body)
            filename = f"C:/python_work/agent_billing/AGENT_SPLIT/{bankName}/{bankName}_week_ending_{final_date}.txt"
            filename1 = f"C:/python_work/agent_billing/AGENT_SPLIT/{bankName}/{bankName}_week_ending_{final_date}.txt.csv"
            print(filename)   
            context=ssl.create_default_context()
            filenames=[filename,filename1]
            for file in filenames:    
                
                with open(file, 'r') as f:
                    part = MIMEApplication(f.read(), Name=basename(file))
                    part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(file))
                    msg.attach(part)
            server = smtplib.SMTP('smtp.gmail.com', 587) 
            server.starttls(context=context)
            server.login(from_addr, 'jniowfhqttnzurzd')
            server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])
            print(f"Mail has been sent to {bankName} with their file")




