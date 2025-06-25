from __main__ import app

import pandas as pd
import numpy as np
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
from datetime import date

# Get the current date
month = int(date.today().month)
todaydate = int(date.today().day)
year = int(date.today().year)


# Load environment variables from .env file
load_dotenv()

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


cursor=mydb.cursor()
print(" Admin Flie Connected To Database 😂😂")


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


def getTotalAmounts():
    amounts=[]
    for i in range(12):
        cursor.execute(f'select amount from orders where omonth="{i+1}" and oyear="{year}";')
        allorders = cursor.fetchall()
        if(len(allorders)==0):
            amounts.append(0)
        else:
            v=0
            for value in allorders:
                v=v+int(value[0])
            amounts.append(v)
    
    return amounts

def getCategoryProfit():
    amounts=[]
    category=['Fashion','Daily Use','Cosmatics','Toys']
    for cate in category:
        cursor.execute(f'select * from productlist where pcategory="{cate}";')
        allorders = cursor.fetchall()
        amounts.append(len(allorders))
    
    return amounts

from collections import Counter
import pandas as pd

def most_frequent_elements(lst):
    series = pd.Series(lst)
    value_counts = series.value_counts()
    max_count = value_counts.max()
    most_frequent = value_counts[value_counts == max_count].index.tolist()
    return most_frequent

def getTopProducts():
    getTopProductsList=[]
    ids=[]
    cursor.execute(f'select productid from orders where omonth="{month}";')
    allorders = cursor.fetchall()
    for data in allorders:
        ids.append(data[0])
    for i in range(5):
        t=[]
        series = pd.Series(ids)
        value_counts = series.value_counts()
        max_count = value_counts.max()
        most_frequent = value_counts[value_counts == max_count].index.tolist()
        for i in ids:
            if(i != most_frequent[0]):
                t.append(i)
        ids=t
        getTopProductsList.append(most_frequent[0])
    return getTopProductsList
    

def getTopalldata():
    finaldata=[]
    famousProduct=getTopProducts()
    for id in famousProduct:
        cursor.execute(f'select * from productlist where pid="{id}";;')
        allorders = cursor.fetchall()
        finaldata.append(allorders[0])
    return finaldata

def getTopalldatanumber():
    finaldata=[]
    famousProduct=getTopProducts()
    for id in famousProduct:
        temp=[]
        cursor.execute(f'select * from orders where productid="{id}";')
        allorders = cursor.fetchall()
        temp.append(len(allorders))
        cursor.execute(f'select pname from productlist where pid="{id}";')
        allor = cursor.fetchall()
        temp.append(allor[0][0])
        finaldata.append(temp)
    return finaldata
    
def getorders():
        cursor.execute(f'select * from orders;')
        allorders = cursor.fetchall()
        return allorders
    
def getTotalEle(totalAmount,orders):
    toele=[]
    te=0
    for i in totalAmount:
            te +=i
    lo=len(orders)
    toele.append(lo)
    toele.append(te)
    
    cursor.execute('select * from alluser;')
    user=cursor.fetchall()
    toele.append(len(user))
    cursor.execute('select * from productlist;')
    product=cursor.fetchall()
    toele.append(len(product))
    
    return toele
    
# ........................function for get all products
def getallproducts(key=0,id=0,f=0):
    if(f==0):
        cursor.execute('select * from orders;')
        orders=cursor.fetchall()
        return orders
    elif(f==1):
        cursor.execute(f'select * from orders where {key}="{id}" and oyear="{year}"')
        orders=cursor.fetchall()
        return orders
    else:
        cursor.execute(f'select * from orders where {key} !="{id}" and oyear="{year}"')
        orders=cursor.fetchall()
        return orders
#.........................function for orders image
def getAllProductImage(orders):
    name_image=[]
    for order in orders:
        tem=[]
        orders=getdata("pid",order[3],"productlist")
        tem.append(orders[0][2])
        tem.append(orders[0][7])
        name_image.append(tem)
    return name_image
    
# .......................router for the admin login page
@app.route('/<string:vid>/daily.shop.admin')
def adminpage(vid):
    if(session.get('checkAdmin')==True):
        totalAmount=getTotalAmounts()
        category=getCategoryProfit()
        famousProduct=getTopalldata()
        famousPn=getTopalldatanumber()
        orders=getorders()
        te=getTotalEle(totalAmount,orders)
        
        if(int(vid)==0):
            return render_template('admin/admin.html',te=te,ta=totalAmount,cp=category,fpn=famousPn,fp=famousProduct,od=orders)
        
        if(int(vid)==1):
            allproduct=getallproducts()
            name_image=getAllProductImage(allproduct)
            aleng=len(allproduct)
            
            newProduct=getallproducts('omonth',f'{month}',1)
            new_image=getAllProductImage(newProduct)
            nleng=len(newProduct)
            
            oldProduct=getallproducts('omonth',f'{month}',2)
            old_image=getAllProductImage(oldProduct)
            oleng=len(oldProduct)
            
            return render_template('admin/order&transection.html',te=te,alen=aleng,nlen=nleng,olen=oleng,ni=name_image,ap=allproduct,np=newProduct,nni=new_image,op=oldProduct,oni=old_image)
        
        if(int(vid)==2):
            cursor.execute(f'select * from alluser;')
            allproduct=cursor.fetchall()
            return render_template('admin/useranalysis.html',te=te,data=allproduct)
        
        if(int(vid)==3):
            cursor.execute(f'select * from productlist;')
            allproduct=cursor.fetchall()
            
            return render_template('admin/productanalysis.html',te=te,data=allproduct)
    
    else:
        return render_template('admin/adminlogin.html')
        
 
# .......................router for the admin login page
@app.route('/daily.shop.admin/login')
def adminpagelogin():
    if(session.get('checkAdmin')==True):
        return render_template('admin/admin.html')
    else:
        return render_template('admin/adminlogin.html')

# ........................router for check admin
@app.route('/check/admin',methods=['POST','GET'])
def checkadminlog():
    username=request.form.get('username')
    password=str(request.form.get('password'))
    ch0=str(os.getenv('ADMIN_USERNAME'))
    ch1=str(os.getenv('ADMIN_PASSWORD'))
    if(username==ch0):
        if(password==ch1):
            session['checkAdmin']=True
            return redirect('/0/daily.shop.admin')
        else:
            return 'Wrong Password'
    else:
        return 'Wrong Username'
    
# ............................logout from admin page

@app.route('/check/admin/logout')
def checkadminlogout():
    session['checkAdmin']=False
    return redirect('/')



