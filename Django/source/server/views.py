# -*- coding: utf-8 -*-

import hashlib
import psycopg2
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from .models import users

# Email Send Module
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token


# 마이 페이지
def mypage(request):
	Users = []
	sess = request.session.get('session')
	db = psycopg2.connect(host='localhost', dbname='admin', user='postgres', password='password', port='5432')
	sql = "select * from server_users where username = %s"
	cur = db.cursor()
	cur.execute(sql, [sess])
	Users.append('')
	Users[0] = cur.fetchone()
	if sess:
		return render(request, 'server/mypage.html', {'user_list':Users})
	else:
		return render(request, 'server/login.html', {'message':'Login Please'})


# 관리자 페이지
Users = []
def admin_page(request):
	global Users
	if request.method == 'GET':
		sess = request.session.get('session')
		db = psycopg2.connect(host='localhost', dbname='admin', user='postgres', password='password', port='5432')
		cur = db.cursor()
		cur.execute("select * from server_users where username = %s", [sess])
		data = cur.fetchone()
		if sess:
			if data[8] == '1':
				cur.execute("select count(*) from server_users")
				count = cur.fetchone()[0]
				# List 크기를 사용자 수만큼 늘림
				for i in range(count):
					Users.append('')
				for i in range(count):
					cur.execute("select * from server_users limit 1 offset " + str(i))
					Users[i] = cur.fetchone()
				name_list = ['jane', 'michael', 'justine']
				return render(request, 'server/admin.html', {'user_list':Users})
			else:
				return render(request, 'server/alert.html')
		else:
			return render(request, 'server/login.html', {'message':'Login Please'})
	elif request.method == 'POST':
		pass

# 아이디 중복 확인
def check(ID):
	db = psycopg2.connect(host='localhost', dbname='admin', user='postgres', password='password', port='5432')
	sql = "select * from server_users where username = %s"
	cur = db.cursor()
	cur.execute(sql, [ID])
	Check_ = cur.fetchone()
	if Check_ == None:
		return True
	else:
		return False

# 계정 탈퇴
data = []
def delete(request):
	global data
	sess = request.session.get('session')
	if request.method == 'GET':
		db = psycopg2.connect(host='127.0.0.1', dbname='admin', user='postgres', password='password', port='5432')
		cur = db.cursor()
		sql = "select * from server_users where username = %s"
		cur.execute(sql, [sess])
		data = cur.fetchone()
		return render(request, 'server/delete.html', {'name':data[1], 'id':data[2]})
	elif request.method == 'POST':
		password = request.POST['password']
		hash_pw = hashlib.sha256(password.encode()).hexdigest()
		user = users.objects.get(username=sess)
		if user.password == hash_pw:
			db = psycopg2.connect(host='127.0.0.1', dbname='admin', user='postgres', password='password', port='5432')
			cur = db.cursor()
			sql = "DELETE FROM server_users where username = %s"
			cur.execute(sql, [sess])
			db.commit()
			request.session.set_expiry(1)
			return render(request, 'server/login.html', { 'message':'다시 로그인 해주세요.'})
		else:
			return render(request, 'server/delete.html', {'name':data[1], 'id':data[2], 'message':'패스워드가 일치하지 않습니다.'})


# 회원 가입
Admin_Code = "122121"
def signup(request):
	if request.method == 'POST':
		name = request.POST['name']
		id = request.POST['username'].lower()
		pw = request.POST['password']
		re_pw = request.POST['re_password']
		hash_pw = hashlib.sha256(pw.encode()).hexdigest()
		age = request.POST['age']
		mail_to = request.POST['email']
		phone = request.POST['phone']
		belong = request.POST['belong']
		interests = request.POST['Interests']
		authority = request.POST['authority']

		if name and id and pw and age and age and phone and belong and interests:
			Check = check(id)
			if Check == True:
				if pw == re_pw:
					if authority:
						if Admin_Code == authority:
							Level = 1
						else:
							return render(request, 'server/signup1.html', {'incorrect':'관리자 코드가 일치하지 않습니다.'})
					else:
						Level = 0
					user = users.objects.create(
							name=name,
							username=id,
							password=hash_pw,
							age=age,
							phone=phone,
							belong=belong,
							interests=interests,
							authority = Level,
							is_activy = True,
							mail_activy = False,
							score = 0,
							challenge = '0'
					)
					user.save()
#current_site = get_current_site(request)
#domain = current_site.domain
#message = render_to_string('server/activity_email.html', {
#'user' = user
#'domain': current_site.domain,
#'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#'token': account_activation_token.make_token(user)
#})
#mail_title = "이메일 인증을 완료해주세요."
#email = EmailMessage(mail_title, message, to=[mail_to])
#email.send()
					return redirect('../login')
				else:
					return render(request, 'server/signup1.html', {'msg':'비밀번호가 일치하지 않습니다.'})
			else:
				return render(request, 'server/signup1.html', {'id':'이미 사용 중인 ID 입니다.'})
		else:
			return render(request, 'server/signup1.html', {'message':'빈 칸이 있으면 안 됩니다.'})
	elif request.method == 'GET':
		return render(request, 'server/signup1.html', {'m1':'이름', 'm2':'아이디', 'm3':'비밀번호','m4':'나이', 'm5':'이메일 주소', 'm6':'휴대폰 번호', 'm7':'소속', 'm8':'관리자 코드'})


# 이메일 인증
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = users.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user:
        user.is_activy = True
        user.save()
        return redirect("/login")
    else:
        return render(request, '/server/login.html', {'message' : '계정 활성화 오류'})
    return

# 패스워드 이메일 인증
def pw_activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = users.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError):
		user = None
	if user:
	 	user.mail_activy = True
	 	user.save()
	 	return change_pw(request, uid)
	else:
		return render(request, "server/forgot.html", {'message':'계정 활성화 오류'})
	return

# 로그인
@csrf_exempt
def login(request):
	sess = request.session.get('session')
	if request.method == 'POST':
		username = request.POST['username'].lower()
		password = request.POST['password']
		hash_pw = hashlib.sha256(password.encode()).hexdigest()
		try:
			user  = users.objects.get(username=username)
#success = cur.execute(sql)
#user = authenticate(username=username, password=hash_pw)
			if user.is_activy == 'True':
				if user.password == hash_pw:
					request.session['session'] = username
					return redirect('../mypage')
				else:
					return render(request, 'server/login.html', {'message':'가입되지 않은 아이디이거나, 패스워드가 일치하지 않습니다.'})
			else:
				return render(request, 'server/login.html', {'message':'가입되지 않은 아이디 입니다. 회원가입을 하셨다면 이메일 인증을 해주세요.'})
		except:
			return render(request, 'server/login.html', {'message':'가입되지 않은 아이디이거나, 패스워드가 일치하지 않습니다.'})
	elif request.method == 'GET':
		if sess:
			return redirect('../mypage')
		else:
			return render(request, 'server/login.html')


# SQL CLI
def sqlcli(request):
	if request.method == 'GET':
		sess = request.session.get('session')
		db = psycopg2.connect(host='localhost', dbname='admin', user='postgres', password='password', port='5432')
		sql = "select * from server_users where username = %s"
		cur = db.cursor()
		cur.execute(sql, [sess])
		data = cur.fetchone()
		if sess:
			if data[8] == '1':
				return render(request, 'server/sql.html')
			else:
				return render(request, 'server/mypage.html', {'msg':'Your not admin','message': sess + '님 안녕하세요.', 'name':data[1], 'id':data[2], 'age':data[4], 'phone':data[7],'belong':data[5], 'interests':data[6]})
		else:
			return render(request, 'server/login.html', {'message':'Login Please'})
	elif request.method == 'POST':
		pay = request.POST.get('payload')
		db = psycopg2.connect(host='127.0.0.1', dbname='admin', user='postgres', password='password', port='5432')
		curr = db.cursor()
		if "SELECT" in pay.upper():
			try:
				curr.execute(pay)
				data = curr.fetchone()
				if data:
					return render(request, 'server/sql.html', {'query':'Query : ' + pay, 'result': data})
				else:
					return render(request, 'server/sql.html', {'message':'Incorrect Value'})
			except:
				return render(request, 'server/sql.html', {'message':'Incorrect Value'})
		elif "SELECT " not in pay.upper():
			try:
				success = curr.execute(pay)
				db.commit()
				return render(request, 'server/sql.html', {'message':'OK'})
			except:
				return render(request, 'server/sql.html', {'message':'Incorrect Value'})



# 로그아웃
def logout(request):
	sess = request.session.get('session')
	if request.method =='GET':
		try:
			if sess:
				request.session.set_expiry(1)
				return render(request, 'server/login.html')
			else:
				return redirect('../login')
		except:
			return render(request, 'server/login.html')


# 아이디 찾는 함수
def find_id(req, name, phone):
	db = psycopg2.connect(host='127.0.0.1', dbname='admin', user='postgres', password='password', port='5432')
	cur = db.cursor()
	sql = "select * from server_users where name = %s and phone = %s"
	try:
		success = cur.execute(sql, [name, phone])
		data = cur.fetchone()
		if success != False:
			return data[2]
	except:
		return False

# 비밀번호 바꾸는 함수
def change_pw(request, user_id):
	user = users.objects.get(pk=user_id)
	username = user.username
	if request.method == 'GET':
		if user.mail_activy == 'True':
			return render(request, 'server/pw_change.html', {'name':user.name, 'id':user.username})
		else:
			return render(request, 'server/forgot.html')
	elif request.method =='POST':
		password = request.POST['new_password']
		check = request.POST['re_pw']
		hash_pw = hashlib.sha256(password.encode()).hexdigest()
		if password == check:
			user.password = hash_pw
			user.mail_activy = False
			user.save()
			return redirect('../../../login')
		else:
			return render(request, 'server/pw_change.html', {'name':user.name, 'id':user.username, 'message':'비밀번호가 일치하지 않습니다.'})

# 아이디 or 비밀번호 바꾸기
def forgot(request):
	if request.method =='GET':
		return render(request, 'server/forgot.html')
	elif request.method =='POST':
		if (request.POST['name'] and request.POST['phone']) or request.POST['name'] or request.POST['phone']:
			Name = request.POST['name']
			Phone = request.POST['phone']
			if Name and Phone:
				id = find_id(request, Name, Phone)
				if id != False:
                	return render(request, 'server/forgot.html' ,{'username': Name + "님의 아이디는 " + id + "입니다."})
				else: 
					return render(request, 'server/forgot.html',{'message':'회원 정보가 일치하지 않습니다.'})
			else:
				return render(request, 'server/forgot.html', {'message':'회원 정보를 모두 입력해주세요.'})
		elif (request.POST['username'] and request.POST['phone1']) or request.POST['username'] or request.POST['phone1']:
			username = request.POST['username']
			phone = request.POST['phone1']
			if username and phone:
				email = request.POST['email']
				user = users.objects.get(username = username)
				current_site = get_current_site(request)
				domain = current_site.domain
				if user:
					message = render_to_string('server/pw_activity_email.html', {
						'user': user,
						'domain': current_site.domain,
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'token': account_activation_token.make_token(user)
					})
					mail_title = "이메일 인증을 완료해주세요. (비빌번호 찾기)"
					email = EmailMessage(mail_title, message, to=[email])
					email.send()
					return render(request, 'server/forgot.html', {'message1':'이메일을 확인해주세요.'})
				else:
					return render(request,'server/forgot.html', {'message1':'회원 정보가 일치하지 않습니다.'})
			else:
					return render(request, 'server/forgot.html', {'message1':'구현 중 입니다'})
		else:
			return render(request, 'server/forgot.html', {'message':'회원 정보를 모두 입력해주세요.','message1':'회원 정보를 모두 입력해주세요.'})



# 내 정보 변경
def update(request):
	db = psycopg2.connect(host='127.0.0.1', dbname='admin', user='postgres', password='password', port='5432')
	cur = db.cursor()
	sess = request.session.get('session')
	sql = "select * from server_users where username = %s"
	cur.execute(sql, [sess])
	data = cur.fetchone()
	if request.method == 'GET':
		sess = request.session.get('session')
		if sess:
			return render(request, 'server/update.html', {'name':data[1], 'id':data[2], 'age':data[4], 'phone':data[5], 'belong':data[6], 'interests':data[7]})
		else:
			return render(request, 'server/login.html', {'message':'login please'})
	elif request.method == 'POST':
		password = request.POST['password']
		hash_pw = hashlib.sha256(password.encode()).hexdigest()
		new_password = request.POST['new_password']
		hash_newpw = hashlib.sha256(new_password.encode()).hexdigest()
		new_belong = request.POST['new_belong']
		new_interests = request.POST['new_interests']
		# data[3] = 패스워드
		# data[5] = 소속
		# data[6] = 관심 분야
		if password or new_password or new_belong or new_interests:
			if data[3] == hash_pw:
				if new_password:
					pass
				else:
					hash_newpw = data[3]
				if new_belong:
					pass
				else:
					new_belong = data[6]
				if new_interests:
					pass
				else:
					new_interests = data[7]
#DB = psycopg2.connect(host='127.0.0.1', dbname='admin', user='postgres', password='password', port='5432')
				sql = "update server_users set password = %s, belong = %s, interests = %s where username = %s"
				cur.execute(sql, [hash_newpw, new_belong, new_interests, data[2]])
				db.commit()
				if hash_newpw != data[3]:
					request.session.set_expiry(1)
					return render(request, 'server/login.html', {'message':'다시 로그인을 해주세요'})
				return redirect('../mypage')

			else:
				return render(request, 'server/update.html', {'name':data[1], 'id':data[2], 'age':data[4], 'phone':data[5], 'belong':data[6], 'interests':data[7], 'message':'비밀번호가 일치하지 않습니다'})
		else:
			return render(request, 'server/update.html', {'name':data[1], 'id':data[2], 'age':data[4], 'phone':data[5], 'belong':data[6], 'interests':data[7], 'message':'값이 입력 되지 않았습니다'}) 