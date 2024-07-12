from django.shortcuts import redirect,render
from django.core.mail import send_mail
import mysql.connector as con
import random
signconnection = con.connect(host='localhost', user='root', password='rootpw', database='bleeeper',auth_plugin='mysql_native_password' )
curse = signconnection.cursor()
def signup(request):
	if request.method == 'POST':
		var2 = request.POST
		request.session['sform'] = var2
		curse.execute('SELECT * from signup_users')
		checkup = curse.fetchall()
		signconnection.commit()
		checkingup = []
		for r in checkup:
			checkingup.append(r)
		y = 0
		for t in checkingup:
			if (var2['signupmail'] in t) or (var2['signupnumber'] in t):
				y = 2
				break
			elif (var2['signupmail'] not in t) or (var2['signupnumber'] not in  t):
				y = 1
		if y == 1:
			sotp = random.randint(1000,9999)
			request.session['signupotp'] = sotp
			send_mail(
				'This is the otp for signing up and its just to confirm , ur the owner of this account ',
				'Pls dont share this otp with anybody except us' + str(sotp),
				'noreplybleeeper557@gmail.com',
				[var2['signupmail']]
			 )
			return redirect('http://localhost:8000/s/sotp/')
	return render(request,'signup/signup.html')
def signupotp(request):
		if request.method == 'POST':
			var4 = request.POST
			print(request.session['signupotp'])
			if int(var4['otp2']) == request.session['signupotp']:
				var3 = request.session['sform']
				insert = "INSERT INTO signup_users(name,email,number) values('{}','{}',{})".format(var3['signupname'],var3['signupmail'],var3['signupnumber'])
				curse.execute(insert)
				signconnection.commit()
				curse.execute("CREATE database  " + str(var3['signupnumber']) + "bleeep")
				signconnection.commit()
				userconnection = con.connect(host='localhost', user='root', password='rootpw', database=str(var3['signupnumber']) + 'bleeep',auth_plugin='mysql_native_password' )
				curso = userconnection.cursor()
				curso.execute("CREATE TABLE bleeeps(bleeepnum bigint)")
				curso.execute("INSERT INTO bleeeps values(0)")
				userconnection.commit()
				return redirect("http://localhost:8000/l")
		return render(request,'signup/signupotp.html')
# Create your views here.
