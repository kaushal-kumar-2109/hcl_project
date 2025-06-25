from __main__ import app


from flask import Flask
from flask import render_template,make_response,session
from flask import redirect
from flask import Flask, request,Response,flash
import mysql.connector
import mysql
from datetime import date
from function import verifyemail,randomkey,extractrequiddata,sendfeedback
from z_router.gettingdata.fuctions.managefunction import getdays,todays
from flask_bcrypt import Bcrypt 
from dotenv import load_dotenv
import os
from datetime import date
import datetime


# Get the current date
month = int(date.today().month)
todaydate = int(date.today().day)
year = int(date.today().year)


import datetime as dt
d=f'{year}-{month}-{todaydate}'
day = dt.datetime.strptime(d,'%Y-%m-%d').date()



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
print(" Manage File Connected To Database 😂😂")


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


# ..........................Router for the checking and redirect login or home
@app.route('/manage.daily.shop')
def managepagelogin():
    
    if(session.get('checkManage')==True):
        days=getdays.getdays()
        cursor.execute(f'select purchaseid from orders where deleverydate="{days[0]}" and status="ReadyForDeliver";')
        pdata=cursor.fetchall()
        cursor.execute(f'select purchaseid from orders where deleverydate="{days[1]}" and status="confirmed";')
        tpdata=cursor.fetchall()
        cursor.execute(f'select purchaseid from orders where deleverydate="{days[1]}" and status="orderplace";')
        tpdata_1=cursor.fetchall()
        cursor.execute(f'select purchaseid from orders where status="cancelled";')
        cencelOrders=cursor.fetchall()
        cursor.execute(f'select purchaseid from orders;')
        allOrders=cursor.fetchall()
        package=todayorders(pdata)
        tomoackage=todayorders(tpdata)
        tomoackage_1=todayorders(tpdata_1)
        cancel=todayorders(cencelOrders)
        allorder=todayorders(allOrders)
        
        return render_template('manage/managehome.html',days=days,pk=package,tpk=tomoackage,tpk_1=tomoackage_1,co=cancel,al=allorder)
    
    else:
        
        return render_template('manage/managelogin.html')
    
# ........................Router for the confirm order 
@app.route('/confirm/<string:oid>')
def confirmOrder(oid):
    cursor.execute(f'update orders set status="confirmed" where purchaseid="{oid}";')
    mydb.commit()
    return redirect('/manage.daily.shop')
# ........................Router for the Deliver order 
@app.route('/deliver/done/ok/<string:oid>')
def DeliveredOrder(oid):
    cursor.execute(f'update orders set status="delivered" where purchaseid="{oid}";')
    mydb.commit()
    return redirect('/manage.daily.shop')

# .........................Router for the redy for delever 
@app.route('/Redy/deiver/<string:oid>')
def readyToDeliver(oid):
    cursor.execute(f'update orders set status="ReadyForDeliver" where purchaseid="{oid}";')
    mydb.commit()
    return redirect('/manage.daily.shop')
# ........................router for check admin
@app.route('/check/manage',methods=['POST','GET'])
def checkmanagelog():
    username=request.form.get('username')
    password=str(request.form.get('password'))
    ch0=str(os.getenv('MANAGE_USERNAME'))
    ch1=str(os.getenv('MANAGE_PASSWORD'))
    if(username==ch0):
        if(password==ch1):
            session['checkManage']=True
            return redirect('/manage.daily.shop')
        else:
            return 'Wrong Password'
    else:
        return 'Wrong Username'
   
# ........................router for check admin
@app.route('/logout/manage/done')
def checkmanagelogOut():
    session['checkManage']=None
    return redirect('/')
  
  

#  ....................function from function file

def todayorders(data):
    days=getdays.getdays()
    dataa=getids(data)
    package=getorders(dataa)
    return package


def getids(data):
    uniqeid=[]
    for id in data:
        f=0
        for i in uniqeid:
            if(i==id[0]):
                f=1
        if(f==0):
            uniqeid.append(id[0])
    return uniqeid

def getorders(dataa):
    allorders=[]
    for i in dataa:
        cursor.execute(f'select * from orders where purchaseid="{i}";')
        data=cursor.fetchall()
        topay=data[0][11]
        orderdate=f'{data[0][9]}-{data[0][7]}-{data[0][8]}'
        delivery=data[0][12]
        status=data[0][13]
        deliveryagent='Nothing One'
        agentnumber='+917065676082'
        allproducts=[]
        for daa in data:
            temp=[]
            cursor.execute(f'select * from productlist where pid="{daa[3]}";')
            product=cursor.fetchall()
            temp.append(product[0])
            temp.append(daa[4])
            allproducts.append(temp)
            
        cursor.execute(f'select * from alluseraddress where id="{data[0][2]}";')
        dataa=cursor.fetchall()
        username=f'{dataa[0][4]} {dataa[0][5]}'
        number=dataa[0][3]
        address=f'{dataa[0][8]} {dataa[0][7]} {dataa[0][9]} {dataa[0][11]}-{dataa[0][10]}'
        
        da={
            'username':username,
            'address':address,
            'phonenumber':number,
            'topay':topay,
            'orderdate':orderdate,
            'delivery':delivery,
            'status':status,
            'products':allproducts,
            'deliveryagent':deliveryagent,
            'agentnumber':agentnumber,
            'purchaseid':i
        }
        allorders.append(da)
    return allorders
    