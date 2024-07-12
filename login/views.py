from django.shortcuts import redirect,render
from django.core.mail import send_mail
import mysql.connector as con
import random
def login(request):
	if request.method == "POST":
		var = request.POST
		print(var)
		request.session['loginid1'] = var['loginid']
		otp = random.randint(1000,9999)
		request.session['otp'] = otp
		signconnection = con.connect(host='localhost', user='root', password='rootpw', database='bleeeper',auth_plugin='mysql_native_password' )
		curse = signconnection.cursor()
		curse.execute('SELECT * from signup_users')
		checkin = curse.fetchall()
		signconnection.commit()
		checkingin = []
		for lt in checkin:
			checkingin.append(lt)
		z=0
		for  ll in checkingin :
			  if (int(var['loginid']) not in ll)  :
				  z=2
			  elif (int(var['loginid']) in ll):
				  z=6
				  mail = ll[2]
				  break
		if z==6:
			send_mail(
				'This is the otp for signing up and its just to confirm , ur the owner of this account ',
				'Pls dont share this otp with anybody except us' + str(otp),
				'noreplybleeeper557@gmail.com',
				[mail]
			 )
			return redirect('http://localhost:8000/l/lotp/')
	return render(request,'login/login.html')

def loginotp(request):
	li1 = request.session['loginid1']
	if request.method == "POST":
		var1 = request.POST
		otp1 = request.session['otp']
		if int(var1['otp1']) == otp1 :
			request.session['loggedin'] = request.session['loginid1']
			return redirect('http://localhost:8000/')
			#send to messaging page 
	return render(request,'login/loginotp.html')
# Create your views here.
