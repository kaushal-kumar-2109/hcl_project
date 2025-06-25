import smtplib, ssl
import random
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from twilio.rest import Client
import random

# Load environment variables from .env file
load_dotenv()



class extractrequiddata():
    def returnReaquidData(data):
        getdata=[]
        getdata.append(data.get('name'))
        getdata.append(data.get('price'))
        getdata.append(data.get('catagory'))
        getdata.append(data.get('discount'))
        getdata.append(data.get('quantity'))
        getdata.append(data.get('image'))

        if(data.get('catagory')=='Fashion'):
            getdata.append(data.get('fashioncolor'))
            getdata.append(data.get('fashionsize'))
            getdata.append(data.get('fashioncompany'))
            getdata.append(data.get('fashionpcategory'))
            getdata.append("none")
            getdata.append("none")
            getdata.append("none")
            return getdata
        elif(data.get('catagory')=='Health-Care'):
            getdata.append("none")
            getdata.append("none")
            getdata.append(data.get('healthcompany'))
            getdata.append(data.get('healthpcategory'))
            getdata.append(data.get('healthweight'))
            getdata.append(data.get("healthusertype"))
            getdata.append("none")
            return getdata
        elif(data.get('catagory')=='Toys'):
            getdata.append("none")
            getdata.append("none")
            getdata.append(data.get('toycompany'))
            getdata.append(data.get('toypcategory'))
            getdata.append(data.get('toyweight'))
            getdata.append("none")
            getdata.append(data.get('toyagelimit'))
            return getdata
        elif(data.get('catagory')=='Daily Use'):
            getdata.append("none")
            getdata.append("none")
            getdata.append(data.get('dailycompany'))
            getdata.append("none")
            getdata.append(data.get('dailyweight'))
            getdata.append("none")
            getdata.append("none")
            return getdata
        else:
            return "false"


class randomkey():
    # ......................function for creating random id
    def getrandomid():
        li=('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0')
        string=''
        for i in range (15):
            string =string+random.choice(li)
        return string

    # .................................function for get random otp
    def getotp():
        li=('1','2','3','4','5','6','7','8','9','0')
        string=''
        for i in range (6):
            string =string+random.choice(li)
        return string


# ...................................function for verify email address

class verifyemail(randomkey):
    def sendEmail(receiver_email,otp,smtp_server="smtp.gmail.com",email_code=os.getenv('EMAIL_CODE'),port=465,sender_email=os.getenv('SENDER_EMAIL')):
        message = f"""\
Subject: One Time Password For Site

    This message is sent from Site.    Your One Time Password is : {otp} """
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, email_code)
            server.sendmail(sender_email,receiver_email, message)


    def send_otp(phonenumber,otp):
        client = Client(os.getenv('ACCOUNT_SID'),os.getenv('AUTH_TOKEN'))
        phone_number = phonenumber
    
        message = client.messages.create(
            body=f'Your OTP is {otp} ',
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            to=phone_number
        )

# ...................................For send feedBack 

class sendfeedback():
    def send_feedback(temail,tmess,receiver_email=os.getenv('SENDER_EMAIL'),smtp_server="smtp.gmail.com",email_code=os.getenv('EMAIL_CODE'),port=465,sender_email=os.getenv('SENDER_EMAIL')):
        message = f"""\
Subject: Feedback from site.

    This feedback from : {temail}             feedback : {tmess} """
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, email_code)
            server.sendmail(sender_email,receiver_email, message)
    
            

