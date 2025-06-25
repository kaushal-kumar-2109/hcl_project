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
import random

# Load environment variables from .env file
load_dotenv()

#  .................creating flask app 

app=Flask(__name__)
bcrypt = Bcrypt(app) 
app.secret_key = os.getenv('SECRET_KEY')
current_year = date.today()
year=current_year.year

import z_router.user
import z_router.gettingdata.admin
import z_router.supplier
import z_router.shop
import z_router.gettingdata.manage

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
print(" Main File Connected To Database 😂😂")

#  ......................Function for adding the data into database

def getdata(key,id,table):
    cursor.execute(f'select * from {table} where {key}="{id}"') 
    # DBData=mydb.commit()
    DBData = cursor.fetchall() 
    return DBData


app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

def checksession():
    id=session.get('defid')
    if(id !=None and len(id)>2):
        return (session.get('defid'))
    else:
        return "1"

# ...................../ router
@app.route('/')
def render():
        
    return redirect('/home')

# ....................Home page routes 
@app.route("/home")
def home():
    defid=checksession()
    
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
        
    li=(1,2,3,4,5,11,22,12,13,15,17,9,10,8,7,6,14,16,18,19,20,21)
    ri =random.choice(li)
    fashion=getdata('pcategory','Fashion','productlist')
    dailyuse=getdata('pcategory','Daily Use','productlist')
    name='Daily.Shop..home'
    rating=[]
    cursor.execute(f'select * from previews where ratting >=4;') 
    DBData = cursor.fetchall() 
    p=random.choice(DBData)
    rating.append(p)
    cursor.execute(f'select * from productlist where pid="{p[1]}";') 
    product = cursor.fetchall()
    rating.append(product[0])
    
    return render_template("home/home.html",defid=defid,duse=dailyuse,fuse=fashion,ri=ri,name=name,rating=rating,topro=totalproduct)
    

# ..........................................Router for the contect page 
@app.route('/contect')
def contect():
    value='0'
    defid=checksession()
    
    totalproduct=0
    if(defid != None and len(defid)>5):
        cursor.execute(f'select * from cart where uid="{defid}";')
        data=cursor.fetchall()
        totalproduct=len(data)
        
    file=open('flag.text','r')
    value=file.read()
    file=open('flag.text','w')
    file.write('0')
    name='Daily.Shop..contect'
    return render_template('contect/contect.html',value=value,defid=defid,name=name,topro=totalproduct)

# ............................................Sending feedback to the plateform
@app.route('/sending',methods=['GET','POST'])
def contectsending():
    email=request.form.get('email')
    mess=request.form.get('Message')
    sendfeedback.send_feedback(email,mess)
    file=open('flag.text','w')
    file.write("1")
    defid=checksession()
    name='Daily.Shop..contect'
    return redirect('/contect')






app.run(debug=True)
