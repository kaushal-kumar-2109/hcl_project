from __main__ import app



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
print(" Supplier File Connected To Database 😂😂")

#  ......................Function for adding the data into database

def getdata(key,id,table):
    cursor.execute(f'select * from {table} where {key}="{id}"') 
    # DBData=mydb.commit()
    DBData = cursor.fetchall() 
    return DBData

# ..........................function for check sesssion 

app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

def checksession():
    id=session.get('defid')
    if(id !=None and len(id)>2):
        return (session.get('defid'))
    else:
        return "1"





# ........................route for the supplier page 
@app.route("/supplier")
def supplier():
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    name='Daily.Shop..supplier'
    return render_template("supplier/supplier.html",defid=defid,name=name,topro=totalproduct)

# ...........................Router for priRegister page
@app.route("/user/priregister")
def priregister():
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    name='Daily.Shop..pri-register'
    return render_template("supplier/priRegister.html",defid=defid,name=name,topro=totalproduct)

# ..........................Route for the register page 
@app.route("/user/register",methods=["POST","GET"])
def register():
    data=[]
    data.append(request.form.get("number"))
    data.append(request.form.get("email"))
    data.append(randomkey.getotp())
    verifyemail.sendEmail(data[1],data[2])
    session['getotp']=data[2]
    # sms=randomkey.getotp()
    # verifyemail.send_otp(request.form.get("number"),sms)
    # cursor.execute(f'UPDATE otp SET otp = "{sms}" WHERE id=2;')
    # mydb.commit()
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    name='Daily.Shop..register'
    return render_template("supplier/register.html",data=data,defid=defid,name=name,topro=totalproduct)

# ............................Router for the login page 
@app.route("/user/login")
def login():
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    name='Daily.Shop..login'
    return render_template("supplier/login.html",defid=defid,nmae=name,topro=totalproduct)

# ............................Router for the varify the user 
@app.route("/user/enterlogin", methods=['GET', 'POST'])
def enterlogin():
    number=request.form.get("number")
    email=request.form.get("email")
    password=request.form.get("password")

    if(number==None and password==None):
        try:
            cursor.execute(f'select * from userlist where email="{email}";') 
            DBData = cursor.fetchall()
            if(DBData):
                otp=randomkey.getotp()
                verifyemail.sendEmail(email,otp)
                session['getotp']=otp
                defid=checksession()
                totalproduct=0
                if(defid != None and len(defid)>5):
                    cursor.execute(f'select * from cart where uid="{defid}";')
                    data=cursor.fetchall()
                    totalproduct=len(data)
                name='Daily.Shop..re-create-password'
                return render_template('supplier/recreatepass.html',gemail=email,defif=defid,name=name,topro=totalproduct)
            else:
                return 'Wrong Email'
            
        except:
            return 'SomeThing is Wrong !'
    error=None
    try:
        cursor.execute(f'select * from userlist where email="{email}" and phonenumber="{number}";') 
        DBData = cursor.fetchall()[0] 
        ps=str(DBData[6])
        if(bcrypt.check_password_hash(ps,password)):
            id=DBData[0]
            url='/admin/'+id
            flash('You were successfully logged in')
            return redirect(f'{url}')
        else:
            error = 'Invalid credentials'
            return 'Wrong Password !'
    except:
        return "You have Enter Wrong Information"
    
# ....................................router for change the password 
@app.route('/user/changingpass',methods=['GET','POST'])
def changingpass():
    otp=int(request.form.get('otp'))
    email=request.form.get('email')
    password=request.form.get("password")
    repass=request.form.get('repassword')
    DBData = int(session.get('getotp')) 
    if(otp==DBData):
        if(password==repass):
            password=bcrypt.generate_password_hash (password).decode('utf-8')
            print(password)
            cursor.execute(f'UPDATE userlist SET password = "{password}" WHERE email="{email}";')
            mydb.commit()
            return redirect('/user/login')
        else:
            return f"Both Password Field Must be Same."
    else:
        return 'Wrong OTP.'

    
#  ...................................router for the adding new suplier user data to database 
@app.route("/user/submit", methods=['GET', 'POST'])
def submit():
    id=randomkey.getrandomid()
    name=request.form.get("name")
    surname=request.form.get('surname')
    company=request.form.get('company')
    number=request.form.get("number")
    email=request.form.get("email")
    password= bcrypt.generate_password_hash (request.form.get("password")).decode('utf-8') 
    emailotp=request.form.get("emailotp")
    numberotp=request.form.get("numberotp")
    comadd1=request.form.get('comadd1')
    comadd2=request.form.get('comadd2')
    amount='0'
    DBData =session.get('getotp')
    if(int(emailotp)==int(DBData)):
        if(int(numberotp)):
            try:
                cursor.execute(f'insert into userlist values ("{id}","{name}","{surname}","{company}","{number}","{email}","{password}","{amount}","{comadd1}","{comadd2}");') 
                DBData=mydb.commit()
                url='/admin/'+id
                return redirect(f'{url}')
            except Exception as e:
                return e
        else:
            return "Invalid Sms OTP."
    else:
        return "Invalid Email OTP."
    

# .................................router for the admin suplier user named as admin 
@app.route('/admin/<string:id>')
def admin(id):
    userdata=getdata("id",id,"userlist")
    # udata=userdata[0]
    productdata=getdata("id",id,"productlist")
    length=len(productdata)
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    name='Daily.Shop..user'
    return render_template("saller/user.html",data=userdata,pdata=productdata,length=length,defid=defid,name=name,topro=totalproduct)

# .................................router for the add new product page 
@app.route('/product/<string:id>')
def product(id):
    userdata=getdata("id",id,"userlist")
    length=0
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    name='Daily.Shop..add-product'
    return render_template("saller/addproduct.html",data=userdata,length=length,defid=defid,name=name,topro=totalproduct)

# .................................Router for the add new product data into database 
@app.route('/admin/<string:id>/adding',methods=['GET', 'POST'])
def addingproduct(id):
    pid=randomkey.getrandomid()
    d=extractrequiddata.returnReaquidData(request.form)
    cursor.execute(f'insert into productlist values ("{pid}","{id}","{d[0]}","{d[1]}","{d[2]}","{d[3]}","{d[4]}","{d[5]}","{d[6]}","{d[7]}","{d[8]}","{d[9]}","{d[10]}","{d[11]}","{d[12]}",4);') 
    DBData=mydb.commit()
    url='/admin/'+id
    return redirect(f'{url}')

# ..............................roter for the product edit page 
@app.route('/<string:id>/<string:pid>')
def productEdit(id,pid):
    userdata=getdata("id",id,"userlist")
    product=[["Empty"]]
    pdata=getdata("pid",pid,"productlist")
    li=[]
    for item in pdata[0]:
        li.append(item)
    product.append(li)
    length=len(product)
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    name='Daily.Shop..add-product'
    return render_template("saller/addproduct.html",topro=totalproduct,data=userdata,pdata=product,length=length,defid=defid,name=name)

# .................................Router for the edit in the product 

@app.route('/admin/<string:id>/edit/<string:pid>',methods=['GET', 'POST'])
def editproduct(id,pid):
    d=extractrequiddata.returnReaquidData(request.form)
    cursor.execute(f'update productlist set pname="{d[0]}",pprice="{d[1]}",pcategory="{d[2]}",pdiscount="{d[3]}",pquantity="{d[4]}",pimage="{d[5]}",pcolor="{d[6]}",psize="{d[7]}",pcompany="{d[8]}",pusercategory="{d[9]}",pweight="{d[10]}",pproducttype="{d[11]}",pagelimit="{d[12]}"where pid="{pid}";')
    DBData=mydb.commit()
    url='/admin/'+id
    return redirect(f'{url}')

# ..................................Router for delete product conformation page 
@app.route('/del/product/<string:pid>')
def Delete(pid):
    userdata=getdata("pid",pid,"productlist")
    defid=checksession()
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
    name='Daily.Shop..delete'
    return render_template("saller/delete.html",topro=totalproduct,data=userdata,defid=defid,name=name)

# .....................................Router for delete product from database

@app.route('/delted/<string:pid>/<string:id>')
def Deleteproduct(pid,id):
    
    cursor.execute(f'DELETE FROM productlist WHERE pid="{pid}";')
    DBData=mydb.commit()
    url='/admin/'+id
    return redirect(f'{url}')
