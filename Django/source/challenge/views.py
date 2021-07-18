from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import psycopg2

# 문제 중복 체크
def check(user):
	db1 = psycopg2.connect(host='localhost', dbname='admin', user='postgres', password='password', port='5432')
	cur1 = db1.cursor()
	cur1.execute("select * from server_users where username = %s", [user])
	data = cur1.fetchone()
	result = data[12]
	return result

# 문제 점수 추가
def score(S, C, user):
	db1 = psycopg2.connect(host='localhost', dbname='admin', user='postgres', password='password', port='5432')
	cur1 = db1.cursor()
	cur1.execute("select * from server_users where username = %s", [user])
	data = cur1.fetchone()
	data1 = int(data[11]) + int(S)
	data2 = data[12] + C
	cur1.execute("update server_users set score = %s, challenge = %s where username = %s", [str(data1), data2, user])
	db1.commit()

def challenge(request):
	if request.method == 'GET':
		return render(request,'challenge/challenge.html')

# 1번 문제
@csrf_exempt
def chall1(request):
	filters = ["hex", "ascii", "group", "strcmp"," ","'or", "' or", "'||", "union", "exp", "in(", "like", "=", "sleep", "sl", "eep","exists", "between", ">=", "<=", "is null", "is not null", "<=>", "as", "concat", "alias", ":", "@", 'limit']
	sess = request.session.get('session')
	if request.method == 'POST':
		db = psycopg2.connect(host='localhost', dbname='flag', user='postgres', password='password', port='5432')
		cur = db.cursor()
		username = request.POST.get('username').lower()
		password = request.POST.get('password').lower()
		flag = request.POST.get('flag')

		if username or password:
			for s in filters:
				if s in username:
					return render(request, 'challenge/chall1.html', {'message':'SQL Injection Firewall'})
				if s in password:
					return render(request, 'challenge/chall1.html', {'message':'SQL Injection Firewall'})
			try:
				success = cur.execute("select * from users where id = %s and pw = %s", [username, password])
				data = cur.fetchone()
				if data:
					return render(request, 'challenge/chall1.html', {'message':'good'})
				else:
					return render(request, 'challenge/chall1.html', {'message':'don\'t'})
			except:
				pass
		elif flag:
			if flag == "py{t1m2_b@s2d_b1i4d_s91_i4ection}":
				chall = check(sess)
				if "c1" not in chall:
					score('100', 'c1', sess)
					return render(request, 'challenge/solve.html',{'level':'1'})
				else:
					return render(request, 'challenge/solve.html', {'level':'1'})
			else:
				return render(request, 'challenge/chall1.html', {'message1':'Incorrect'})
	elif request.method == 'GET':
		if sess:
			return render(request, 'challenge/chall1.html')
		else:
			return render(request, 'server/login.html', {'message':'Login Please'})

# 2번 문제
@csrf_exempt
def chall2(request):
	sess = request.session.get('session')
	if request.method == 'GET':
		if sess:
			return render(request, 'challenge/chall2.html')
		else:
			return render(request, 'server/login.html', {'message':'Login Please'})
	elif request.method == 'POST':
		flag = request.POST.get('flag')

		if flag == "py{php_0bjec4_1n3ec4ion!!!!!!3o_8@sy}":
			chall = check(sess)
			if "c2" not in chall:
				score('100', 'c2', sess)
				return render(request, 'challenge/solve.html', {'level':'2'})
			else:
				return render(request, 'challenge/solve.html', {'level':'2'})
		else:
			return render(request, 'challenge/chall2.html', {'message1':'Incorrect'})


# 3번 문제
@csrf_exempt
def chall3(request):
	sess = request.session.get('session')
	if request.method == 'GET':
		if sess:
			return render(request, 'challenge/chall3.html')
		else:
			return render(request, 'server/login.html', {'message':'Login Please'})
	elif request.method == 'POST':
		flag = request.POST.get('flag')

		if flag == "py{e@sy_XxS_W@7_b7p@ss_Poc???}":
			chall = check(sess)
			if "c3" not in chall:
				score('100', 'c3', sess)
				return render(request, 'challenge/solve.html', {'level':'3'})
			else:
				return render(request, 'challenge/solve.html', {'level':'3'})
		else:
			return render(request, 'challenge/chall3.html', {'message1':'Incorrect'}) 