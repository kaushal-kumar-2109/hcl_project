from __main__ import app

import random
from flask import Flask
from flask import render_template,make_response,session
from flask import redirect
from flask import Flask, request,Response,flash
import mysql.connector
import mysql
from datetime import date
from function import verifyemail,randomkey,extractrequiddata,sendfeedback
from flask_bcrypt import Bcrypt 
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

month = int(date.today().month)
todaydate = int(date.today().day)
year = int(date.today().year)

import datetime as dt
d=f'{year}-{month}-{todaydate}'
day = dt.datetime.strptime(d,'%Y-%m-%d').date()



def getdays():
    days=[]
    
    for i in range(10):
        if(i>=7):
            d=day+dt.timedelta(days=i)
            # Getting the day name
            day_name = d.strftime("%A")
            dd=f'next {day_name}'
            days.append(dd)
        else:
            d=day+dt.timedelta(days=i)
            # Getting the day name
            day_name = d.strftime("%A")
            days.append(day_name)
    return days





#  .................creating flask app 

bcrypt = Bcrypt(app) 
app.secret_key = os.getenv('SECRET_KEY')
current_year = date.today()
year=current_year.year

import z_router.user

app.config['UPLOAD_FOLDER'] = 'uploads/'
# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

defid='1'

#....................connection to the database

mydb = mysql.connector.connect(
    host='localhost',
    user = 'root',
    password=os.getenv('PASSWORD'),
    database =os.getenv('DATABASE')
)
# a=bcrypt.generate_password_hash (str(21092003)).decode('utf-8')
# print('this is A : ',a)
# b=bcrypt.generate_password_hash (str(21092003)).decode('utf-8')
# print('this is B : ',b)
# c1=bcrypt.check_password_hash(a, str(21092003))
# print('check',c1)
# print('check',bcrypt.check_password_hash(b, str(21092003)))


cursor=mydb.cursor()
print(" Shop File Connected To Database 😂😂")


#  ......................Function for adding the data into database

def getdata(key,id,table):
    cursor.execute(f'select * from {table} where {key}="{id}"') 
    # DBData=mydb.commit()
    DBData = cursor.fetchall() 
    return DBData

# ........................Function for check the session
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

def checksession():
    id=session.get('defid')
    if(id !=None and len(id)>2):
        return (session.get('defid'))
    else:
        return "1"

# .........................................Router for the shop page 
@app.route('/shop')
def shop():
    fashion=getdata('pcategory','Fashion','productlist')
    dailyuse=getdata('pcategory','Daily Use','productlist')
    f=int(len(fashion)/2)
    li=[]
    for i in range(len(fashion)):
        li.append(i)
    lf =random.choice(li)
    pi=[]
    for i in range(len(dailyuse)):
        pi.append(i)
    ld =random.choice(pi)
    d=int(len(dailyuse)/4)
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    name='Daily.Shop..shop'
    return render_template('shop/shop.html',topro=totalproduct,fuse=fashion,duse=dailyuse,defid=defid,f=f,d=d,lf=lf,ld=ld,name=name)

# ..........................................Router for the view product 
@app.route('/shop/product/<string:pid>',methods=['POST','GET'])
def productdata(pid):
    dataa=getdata('pid',pid,'productlist')
    sdata=getdata('pcategory',dataa[0][4],'productlist')
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    if(defid==None or len(defid)<5):
        defid=1
    name='Daily.Shop..Product'
    return render_template('shop/productpage.html',topro=totalproduct,defid=defid,pdata=dataa,sdata=sdata,name=name)

# ..........................................Router for the add ratting 
@app.route('/<string:pid>/ratting',methods=['POST','GET'])
def ratting(pid):
    ratting=int(request.form.get('ratting'))
    cursor.execute(f"insert into previews values('{randomkey.getrandomid()}','{pid}',{ratting},'{request.form.get('reviewname')}','{request.form.get('reviewemail')}','{request.form.get('reviewtext')}');")
    mydb.commit()   
    url=f'/shop/product/{pid}'
    return redirect(url)

# ............................................Router for the shopcart
@app.route('/<string:pid>/cart' ,methods=['POST','GET'])
def shopcart(pid):
    quantity=int(request.form.get('quantity'))
    defid=checksession()
    if(defid==None or len(defid)<5):
        return redirect('/1/user')
    else:
        try:
            cursor.execute(f"insert into cart values('{randomkey.getrandomid()}','{defid}','{pid}',{quantity});")
            mydb.commit()
            return redirect('/cart')
        except:
            return 'May You Already Added This Product.'
    
# ..............................................Router for change quantity
@app.route('/<string:cid>/change/value',methods=['POST','GET'])
def changeQuantity(cid):
    quantity=int(request.form.get('quantity'))
    if(quantity==0):
        cursor.execute(f'DELETE FROM cart WHERE cartid="{cid}";')
        mydb.commit()
        return redirect('/cart')
    else:
        cursor.execute(f'UPDATE cart SET quantity ={quantity} WHERE cartid= "{cid}";')
        mydb.commit()
        return redirect('/cart')
    
    
def getDataForCart(data):
    finaldata=[]
    for d in data:
        temp=[]
        cursor.execute(f'select pimage from productlist where pid="{d[2]}"') 
        DBData = cursor.fetchall() 
        temp.append(DBData[0][0])
        cursor.execute(f'select pprice from productlist where pid="{d[2]}"') 
        DBData = cursor.fetchall()
        temp.append(int(DBData[0][0]))
        finaldata.append(temp)
    return finaldata
    
# ..............................................Router for render cart page

@app.route('/cart')
def cart():
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    if(defid==None or len(defid)<5):
        return redirect('/1/user')
    data=getdata('uid',defid,'cart')
    length=len(data)
    fdata=getDataForCart(data)
    v=0
    for i in range(length):
        v=v+(fdata[i][1]*data[i][3])
    sbv=(v*10)/100
        
    return render_template('shop/shopcart.html',defid=defid,topro=totalproduct,pdata=data,fdata=fdata,length=length,v=v,sbv=sbv)


# .............................................Router for the checkout

@app.route('/<string:id>/<string:total>/checkOut',methods=['POST','GET'])
def checkout(id,total):
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    data=getdata('uid',defid,'cart')
    length=len(data)
    
    fdata=getDataForCart(data)
    cursor.execute(f'select * from alluseraddress;') 
    allad = cursor.fetchall() 
    
    if(len(id)<10):
        addid=False
    else:
        addid=id
    days=getdays()
    return render_template('shop/checkout.html',defid=defid,days=days,topro=totalproduct,ad=allad,len=length,fdata=fdata,pdata=data,total=total,addid=addid)

#............................................Router for atech address
@app.route('/<string:id>/<string:total>/addadress')
def attech(id,total):
    url=f'/{id}/{total}/checkOut'
    return redirect(url)
# ...........................................Router for add new address

@app.route('/add/new/address',methods=['POST','GET'])
def addNewAddress():
    defid=checksession()
    cursor.execute(f'insert into alluseraddress values ("{defid}","{randomkey.getrandomid()}","active","{request.form.get('number')}","{request.form.get('first-name')}","{request.form.get('last-name')}","{request.form.get('company')}","{request.form.get('house_street')}","{request.form.get('apartment')}","{request.form.get('city')}","{request.form.get('zip')}","{request.form.get('state')}","{request.form.get('notes')}");')
    mydb.commit()
    return redirect('/1dg2/000/checkOut')

#.................................Router for place order
@app.route('/<string:cid>/orderplaced',methods=['POST','GET'])
def orderplaced(cid):
    defid=checksession()
    data=getdata('uid',defid,'cart')
    length=len(data)
    fdata=getDataForCart(data)
    v=0
    delevry=request.form.get('delevery')
    
    for i in range(length):
        v=v+(fdata[i][1]*data[i][3])
    sbv=(v*10)/100
    
    purchaseid=randomkey.getrandomid()
    
    for i in range(length):
        cursor.execute(f'insert into orders values ("{randomkey.getrandomid()}","{defid}","{cid}","{data[i][2]}","{data[i][3]}",{fdata[i][1]},"Cash on delivery","{month}","{todaydate}","{year}",{v},{v-sbv},"{delevry}","orderplace","{purchaseid}");')
        mydb.commit()
    
    invoiceid=randomkey.getrandomid()
    invoice_data=getInvoiceData(defid,v-sbv,invoiceid)
    dat=f'{todaydate}-{month}-{year}'
    path=f"./invoices/invoice-{dat}-{invoiceid}-{defid}.pdf"
    session['invoicePath']=path
    create_invoice(invoice_data, path)
    
    cursor.execute(f'DELETE FROM cart WHERE uid ="{defid}" ;')
    mydb.commit()
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    cursor.execute(f'select email from alluser where id="{defid}";')
    email=cursor.fetchall()
    send_email(
    sender_email=os.getenv('SENDER_EMAIL'),  # Your email address
    receiver_email=email[0][0],  # Recipient's email address
    subject='Here Is Your Order Invoice File',
    body='Please find the attached PDF file.',
    pdf_file_path=path,  # Path to the PDF file
    smtp_server='smtp.gmail.com',  # SMTP server for Gmail (use the appropriate server for other email providers)
    smtp_port=587,  # Port number for Gmail's SMTP server
    smtp_user=os.getenv('SENDER_EMAIL'),  # Your email address (again, for login)
    smtp_password=os.getenv('EMAIL_CODE')  # Your email account password
    )
    return render_template('shop/order_complete.html',topro=totalproduct,defid=defid,date=dat,path=path)

# .............................router for send invoice to email

@app.route('/send/invoice')
def sendinvoice():
    defid=checksession()
    dat=f'{todaydate}/{month}/{year}'    
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    cursor.execute(f'select email from alluser where id="{defid}";')
    email=cursor.fetchall()
    path=session.get('invoicePath')
    send_email(
    sender_email=os.getenv('SENDER_EMAIL'),  # Your email address
    receiver_email=email[0][0],  # Recipient's email address
    subject='Here Is Your Order Invoice File',
    body='Please find the attached PDF file.',
    pdf_file_path=path,  # Path to the PDF file
    smtp_server='smtp.gmail.com',  # SMTP server for Gmail (use the appropriate server for other email providers)
    smtp_port=587,  # Port number for Gmail's SMTP server
    smtp_user=os.getenv('SENDER_EMAIL'),  # Your email address (again, for login)
    smtp_password=os.getenv('EMAIL_CODE')  # Your email account password
    )
    
    return render_template('shop/order_complete.html',topro=totalproduct,date=dat,defid=defid,path=path)


def getInvoiceData(defid,total,invoiceid):
    cursor.execute(f'select * from cart WHERE uid ="{defid}" ;')
    DBData = cursor.fetchall()
    cursor.execute(f'select * from alluser WHERE id ="{defid}" ;')
    Data = cursor.fetchall()
    finalData=[]
    for data in DBData:
        cursor.execute(f'select * from productlist WHERE pid ="{data[2]}" ;')
        pData = cursor.fetchall()
        temp={'description':f'{pData[0][2]} ({pData[0][0]})','quantity':data[3],'price':int(pData[0][3]),'total':int(pData[0][3])*int(data[3])}
        
        finalData.append(temp)
    
    invoice_data = {
    'invoice_number': f'{invoiceid}-{defid}',
    'date': f'{year}-{month}-{todaydate}',
    'due_date': 'XXXX-XX-XX',
    'bill_to': f'{Data[0][2]} - {Data[0][4]}',
    'items': finalData,
    'total_amount': int(total) }
    
    
    return invoice_data



from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_invoice(invoice_data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, height - 50, "Invoice")

    # Invoice Information
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Invoice Number: {invoice_data['invoice_number']}")
    c.drawString(50, height - 120, f"Date: {invoice_data['date']}")
    c.drawString(50, height - 140, f"Due Date: {invoice_data['due_date']}")

    # Billing Information
    c.drawString(50, height - 180, "Bill To:")
    c.drawString(50, height - 200, invoice_data['bill_to'])

    # Items
    c.drawString(50, height - 240, "Product Name")
    c.drawString(300, height - 240, "Quantity")
    c.drawString(400, height - 240, "Price")
    c.drawString(500, height - 240, "Total")

    y = height - 260
    for item in invoice_data['items']:
        c.drawString(50, y, item['description'])
        c.drawString(300, y, str(item['quantity']))
        c.drawString(400, y, f"${item['price']:.2f}")
        c.drawString(500, y, f"${item['total']:.2f}")
        y -= 20

    # Total Amount
    c.drawString(400, y - 20, "Total Amount:")
    c.drawString(500, y - 20, f"${invoice_data['total_amount']:.2f}")

    c.save()

# Example data


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(sender_email, receiver_email, subject, body, pdf_file_path, smtp_server, smtp_port, smtp_user, smtp_password):
    # Create the MIMEMultipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    # Attach the body with the msg
    msg.attach(MIMEText(body, 'plain'))  # Attach the body as plain text
    
    # Attach the PDF file
    if os.path.isfile(pdf_file_path):
        with open(pdf_file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_file_path)}')
            msg.attach(part)
    else:
        print(f"Error: The file {pdf_file_path} does not exist.")

    # Establish a secure session with Gmail's SMTP server
    try:
        # Establish the connection to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection using TLS
            server.login(smtp_user, smtp_password)  # Login to the SMTP server
            
            # Send the email
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
# send_email(
#     sender_email='kaushal21092003kumar@gmail.com',  # Your email address
#     receiver_email='kaushal21092003kumar@gmail.com',  # Recipient's email address
#     subject='Here is your PDF file',
#     body='Please find the attached PDF file.',
#     pdf_file_path='./invoices/invoice-gNpEV854ihY2bs4.pdf',  # Path to the PDF file
#     smtp_server='smtp.gmail.com',  # SMTP server for Gmail (use the appropriate server for other email providers)
#     smtp_port=587,  # Port number for Gmail's SMTP server
#     smtp_user='kaushal21092003kumar@gmail.com',  # Your email address (again, for login)
#     smtp_password='gtpv zbey aqwy aqpz'  # Your email account password
# )




# from pathlib import Path

# file_path = Path('./invoice.pdf')

# try:
#     file_path.unlink()
#     print(f"{file_path} has been deleted successfully.")
# except FileNotFoundError:
#     print(f"{file_path} does not exist.")
# except PermissionError:
#     print(f"Permission denied: {file_path}")
# except Exception as e:
#     print(f"Error occurred: {e}")
