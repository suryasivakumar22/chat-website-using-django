from django.shortcuts import render,redirect
import mysql.connector as con
from datetime import datetime,date
signconnection = con.connect(host='localhost', user='root', password='rootpw', database='bleeeper',auth_plugin='mysql_native_password' )
curse = signconnection.cursor()
def search(request):
	if request.method == 'POST':
		var5 = request.POST
		print(var5)
		messageconnection = con.connect(host='localhost', user='root', password='rootpw', database=str(request.session['loggedin'])+'bleeep',auth_plugin='mysql_native_password' )
		cursem = messageconnection.cursor()
		curse.execute('SELECT * FROM signup_users')
		checkup = curse.fetchall()
		signconnection.commit()
		checkingup = []
		for r in checkup:
			checkingup.append(r)
		y = 0
		check = list(var5.values())
		print(check)
		for t in checkingup:
			if (int(check[1]) in t):
				y = 2
				results = t
				request.session['searchresult'] = results
				return redirect("http://localhost:8000/m/searchresults/")
				break
			elif (int(check[1]) not in t):
				y = 1
				results = "notfound"
				request.session['searchresult'] = results
		if y ==1:
			return redirect("http://localhost:8000/m/searchresults/")
	return render(request,'bleeeps/messearch.html')

def searchresult(request):
	if request.method == "POST":
		var6 = request.POST
		lkbal = list(var6.values())
		messageconnection = con.connect(host='localhost', user='root', password='rootpw', database=str(request.session['loggedin'])+'bleeep',auth_plugin='mysql_native_password' )
		cursem = messageconnection.cursor()
		cc = "CREATE TABLE "+str(request.session['loggedin'])+"_"+str(lkbal[1])+"(role varchar(255),date int,time varchar(255),sender varchar(255),receiver varchar(255),messgae varchar(255))"
		print(cc)
		cursem.execute(cc)
		cursem.execute("INSERT INTO bleeeps values(" +lkbal[1]+")")
		messageconnection.commit()
		messageconnection2 = con.connect(host='localhost', user='root', password='rootpw', database=str(lkbal[1])+'bleeep',auth_plugin='mysql_native_password' )
		cursem2 = messageconnection2.cursor()
		cc1 = "CREATE TABLE "+str(lkbal[1])+"_"+str(request.session['loggedin'])+"(role varchar(255),date int,time varchar(255),sender varchar(255),receiver varchar(255),messgae varchar(255))"		
		cursem2.execute(cc1)
		cursem2.execute("INSERT INTO bleeeps values(" + request.session['loggedin']+")")
		messageconnection2.commit()

		return redirect("http://localhost:8000/m/search/")
	#print(request.session['searchresult'])
	x =request.session['searchresult']
	if x == "notfound" :
		context = { 

		}
	else:
		context = { 
			"name" : x[1], 
			"number"  : x[3], 
		} 
	return render(request,'bleeeps/searchresults.html',context)
def empty(request):
	if request.method == "POST":
		gosu = request.POST
		gopi = list(gosu.values())
		gopi.pop(0)
		print(gopi)
		request.session['openbleeep'] = gopi[0]
		print(request.session['openbleeep'])
		return redirect("http://localhost:8000/m/bleeeps")
	messageconnection = con.connect(host='localhost', user='root', password='rootpw', database=str(request.session['loggedin'])+'bleeep',auth_plugin='mysql_native_password' )
	cursem   = messageconnection.cursor()
	create   = "SELECT * FROM bleeeps where bleeepnum <> 0"
	cursem.execute(create)
	bleeepsr = cursem.fetchall()
	messageconnection.commit()
	bl = {}
	for i in bleeepsr:
		for j in i:
			curse.execute('SELECT * from signup_users where number = ' + str(j))
			ft = curse.fetchall()
			messageconnection.commit()
			bl[str(j)] = ft[0]
	print(bl)
	context = { 
			 "names":bl,
		} 
	return render(request,'bleeeps/messtart.html',context)
def bleeeps(request):
	messageconnection2 = con.connect(host='localhost', user='root', password='rootpw', database=str(request.session['openbleeep'])+'bleeep',auth_plugin='mysql_native_password' )
	cursem2  = messageconnection2.cursor()
	messageconnection = con.connect(host='localhost', user='root', password='rootpw', database=str(request.session['loggedin'])+'bleeep',auth_plugin='mysql_native_password' )
	cursem = messageconnection.cursor()
	if request.method == "POST":
		pdata = request.POST
		print(pdata)
		print(list(pdata.values())[1])
		if list(pdata.values())[1] == "itsabutton":
			request.session['openbleeep'] = list(pdata.values())[2]
			print('bye')
		if list(pdata.values())[1] == 'itsamessageform':
			now = datetime.now()
			today = date.today()
			current_time = now.strftime("%H:%M")			
			op = request.session['openbleeep']
			curd = today.strftime("%B %d")
			mes = pdata['message']
			oi = str(request.session['loggedin'])+"_"+str(request.session['openbleeep'])
			ins= "INSERT INTO "+oi+" values('{}','{}','{}','{}','{}','{}')".format('sender',curd,current_time,request.session['loggedin'],op,mes)
			ins1= "INSERT INTO "+oi+" values('{}','{}','{}','{}','{}','{}')".format('receiver',curd,current_time,request.session['loggedin'],op,mes)
			print(ins)
			cursem.execute(ins)
			messageconnection.commit()
			cursem2.execute(ins1)
			messageconnection2.commit()
	create   = "SELECT * FROM bleeeps where bleeepnum <> 0"
	cursem.execute(create)
	bleeepsr = cursem.fetchall()
	messageconnection.commit()
	bl = {}
	for i in bleeepsr:
		for j in i:
			curse.execute('SELECT * from signup_users where number = ' + str(j))
			ft = curse.fetchall()
			messageconnection.commit()
			bl[str(j)] = ft[0]
	
	context = { 
			 "names":bl,
		}
	return render(request,'bleeeps/bleeeps.html',context)
# Create your views here.
