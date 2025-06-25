
import mysql.connector
import mysql
from datetime import date
from datetime import date
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

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

# Get the current date
month = int(date.today().month)
todaydate = int(date.today().day)
year = int(date.today().year)


import datetime as dt
d=f'{year}-{month}-{todaydate}'
day = dt.datetime.strptime(d,'%Y-%m-%d').date()

class getdays():

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

class todays(getdays):
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
    
# orderslist=[
#     {
#         'username':'kishore',
#         'address':'abcaddress',
#         'phonenumber':'9130234324',
#         'ToPay':2342,
#         'orderdate':'yyyy/mm/dd',
#         'delevery':'yyyy/mm/dd',
#         'status':'ordered',
#         'products':[[(34,234,24),(2)],[(34,234,24),(2)]],
#         'delevryagent':'ram',
#         'agentnumber':'91034324'
#     }
# ]