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
# a=bcrypt.generate_password_hash (str(21092003)).decode('utf-8')
# print('this is A : ',a)
# b=bcrypt.generate_password_hash (str(21092003)).decode('utf-8')
# print('this is B : ',b)
# c1=bcrypt.check_password_hash(a, str(21092003))
# print('check',c1)
# print('check',bcrypt.check_password_hash(b, str(21092003)))


cursor=mydb.cursor()
print(" User File Connected To Database 😂😂")


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




# ............................................Router for the user page login
@app.route('/<string:fid>/user')
def USER(fid):
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
        
    if(len(fid)<5):
        flag=int(fid)
        name='Daily.Shop..login'
        return render_template('/user/login.html',flag=flag,defid=defid,name=name,topro=totalproduct)
    else:
        udata=getdata("id",fid,"alluser")
        adata=getdata("uid",fid,"alluseraddress")
        length=len(adata)
        name='Daily.Shop..user'
        return render_template('/user/user.html',data=udata[0],adata=adata,length=length,defid=defid,name=name,topro=totalproduct)
    
# .............................................Router for the logout session 
@app.route('/<string:fid>/user/logout/session')
def logoutseession(fid):
    session['defid']=None
    url=f'/1/user'
    return redirect(url)

# .............................................Router for if forget password
@app.route('/forget',methods=['GET','POST'])
def forget():
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    email=request.form.get('email')
    if(email):
        cursor.execute(f'Select * from alluser where email="{email}"')
        data=cursor.fetchall()
        if(len(data)>0):
            otp=randomkey.getotp()
            verifyemail.sendEmail(email,otp)
            session['getotp']=otp
            name='Daily.Shop..re-create-password'
            return render_template('/user/recreatepass.html',email=email,defid=defid,name=name,topro=totalproduct)
        else:
            return 'No Email Found In Data Base'
        
    else:
        name='Daily.Shop..Send-email'
        return render_template('/user/sendemail.html',defid=defid,name=name,topro=totalproduct)

# .............................................Router for change password
@app.route('/change/old/password',methods=['GET','POST'])
def changeinpass():
    otp=int(request.form.get('otp'))
    email=request.form.get('email')
    password=str(request.form.get('password'))
    repassword=str(request.form.get('repassword'))
    if(password==repassword):
        cursor.execute('select * from otp')
        data=session.get('getotp')
        if(otp==int(data)):
            # cursor.execute(f'select * from alluser where email="{email}"')
            # data=cursor.fetchall()
            data=getdata("email",email,'alluser')
            id=data[0][0]
            password=bcrypt.generate_password_hash (password).decode('utf-8')
            cursor.execute(f'UPDATE alluser SET password = "{password}" WHERE email="{email}";')
            mydb.commit()
            url=f'/{id}/user'
            return redirect(url)
    else:
        return "The Password Fields Must Be Have Same Value"

#..............................................Router for login user
@app.route('/loginuser/userpage',methods=['POST','GET'])
def loger():
    email=request.form.get('email')
    password=request.form.get('password')
    # cursor.execute(f'Select * from alluser where email="{email}"')
    # data=cursor.fetchall()
    data=getdata("email",email,"alluser")
    if(len(data)>0):
        ps=data[0][5]
        id=data[0][0]
        if(bcrypt.check_password_hash(ps,password)):
            url=f'/{id}/user'
            session['defid']=id
            return redirect(url)
    else:
        return 'Wrong Email Entered'

# .............................................router for emailverification user data insert in database 
@app.route('/addUSER',methods=['GET','POST'])
def addUSER():
    password=request.form.get('password')
    email=request.form.get('email')
    if(password):
        data=session.get('getotp')
        otp=int(request.form.get('otp'))
        if(otp==int(data)):
            password=bcrypt.generate_password_hash (str(password)).decode('utf-8')
            username=request.form.get('username')
            gender=request.form.get('gender')
            f=open('templates/user/temp.txt','r')
            email=f.read()
            number=request.form.get('number')
            city=request.form.get('city')
            pincode=request.form.get('pincode')
            age=request.form.get('age')
            uid=randomkey.getrandomid()
            try:
                cursor.execute(f"insert into alluser values('{uid}','https://cdn.pixabay.com/photo/2023/02/18/11/00/icon-7797704_1280.png','{username}','{email}','{number}','{password}','{gender}','{city}','{pincode}','{age}','{month}','{todaydate}','{year}');")
                mydb.commit()
                # cursor.execute(f"insert into alluseraddress values('{uid}','{randomkey.getrandomid()}','Home','{username}','{number}','{city}','{pincode}','{address}');")
                # mydb.commit()
                return redirect('1/user')
            except Exception as e:
                print("exception :",e)
                return "Data already in use"
        else:
            return 'Envalid OTP'
    
    else:
        f=open('templates/user/temp.txt','w')
        f.write(email)
        otp=randomkey.getotp()
        verifyemail.sendEmail(email,otp)
        session['getotp']=otp
        return redirect('/3/user')

    # if 'image' not in request.files:
    #     return 'No file part'
    # file = request.files['image']
    # if file.filename == '':
    #     return 'No selected file'
    # if file:
    #     filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    #     file.save(filepath)
    #     return f'File successfully uploaded to {filepath}'



# ............................................Router for the user page login
@app.route('/<string:fid>/change/data', methods=['POST','GET'])
def change(fid):
    if(request.form.get('username') and request.form.get('gender')):
        cursor.execute(f'UPDATE alluser SET username = "{request.form.get('username')}",gender="{request.form.get('gender')}" WHERE id="{fid}";')
        mydb.commit()
    if(request.form.get('email')):
        cursor.execute(f'UPDATE alluser SET email = "{request.form.get('email')}" WHERE id="{fid}";')
        mydb.commit()
    if(request.form.get('number')):
        cursor.execute(f'UPDATE alluser SET phonenumber = "{request.form.get('number')}" WHERE id="{fid}";')
        mydb.commit()
    url=f'/{fid}/user'
    return redirect(url)

# ............................................Router for the user page login
@app.route('/<string:fid>/change/address', methods=['POST','GET'])
def changeaddress(fid):
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    m=1
    name='Daily.Shop..new-address'
    return render_template('/user/newaddress.html',id=fid,m=m,name=name,topro=totalproduct)
    
# ...........................................Router for the add new address
@app.route('/<string:m>/<string:fid>/addnew/address', methods=['POST','GET'])
def newaddress(m,fid):
    if(len(m)<4):
        if(request.form.get('validationCustom01') and request.form.get('number') and request.form.get('address') and request.form.get('city') and request.form.get('type') and request.form.get('zip')):
            cursor.execute(f"insert into alluseraddress values('{fid}','{randomkey.getrandomid()}','{request.form.get('type')}','{request.form.get('validationCustom01')}','{request.form.get('number')}','{request.form.get('city')}','{request.form.get('zip')}','{request.form.get('address')}');")
            mydb.commit()
            url=f'/{fid}/user'
            return redirect(url)
        else:
            return 'Missing Data'
    else:
        cursor.execute(f"UPDATE alluseraddress SET atype='{request.form.get('type')}',name='{request.form.get('validationCustom01')}',number='{request.form.get('number')}',city='{request.form.get('city')}',pincode='{request.form.get('zip')}',address='{request.form.get('address')}' WHERE id='{m}';")
        mydb.commit()
        url=f'/{fid}/user'
        return redirect(url)
        
   
# ...........................................Router for the delete address
@app.route('/<string:m>/<string:fid>/delete/<string:aid>/address', methods=['POST','GET'])
def deleteaddress(m,fid,aid):
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    m=int(m)
    if (m==1):
        cursor.execute(f"DELETE FROM alluseraddress WHERE id='{aid}' and uid='{fid}';")
        a=mydb.commit()
        url=f'/{fid}/user'
        return redirect(url)
    elif(m==2):
        data=getdata('id',aid,'alluseraddress')
        data=data[0]
        name='Daily.Shop..new-address'
        return render_template('/user/newaddress.html',id=fid,m=m,data=data,name=name,topro=totalproduct)
        
  
#    ...................... Router for the  User orders page 

@app.route('/user/<string:uid>/Orders')
def placed_orders(uid):
    defid=uid
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    name='Daily.Shop..My Orders'
    cursor.execute(f'select purchaseid from orders where userid="{defid}";')
    allOrders=cursor.fetchall()
    allorder=todayorders(allOrders)
    return render_template('user/myOrders.html',name=name,topro=totalproduct,defid=defid,al=allorder)

# ......................... Router for the cancel the order 

@app.route('/cancel/<string:oid>')
def cancelOrder(oid):
    defid=checksession()
    cursor.execute(f'update orders set status="cancelled" where purchaseid="{oid}";')
    mydb.commit()
    url=f'/user/{defid}/Orders'
    return redirect(url)


# ...............................Functions from the functions file

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
    