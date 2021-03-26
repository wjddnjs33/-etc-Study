import sys
import os.path  
import os

help = '''Help
ex) python3 upload.py url
'''
def save(u):
	result = 0
	try:
		os.system('wget -P /root/blog/source/_posts ' + u)
		os.system('wget -P /root/blog/public/backup_md ' + u)
		os.system('alias s=\'hex\'')
		os.system('cd /root/blog;hexo g; hexo d')
		result = 1
	except:
		pass
	return result

Filename = ''
def check(u):
	global Filename
	result = 0
	filename = u.split('/')
	for i in range(len(filename)):
		if ".md" in filename[i]:
			Filename = filename[i]
			if os.path.isfile('/root/blog/source/_posts/' + filename[i]):
				result = 2
			else:
				result = 1
		else:
			pass
	return result
def rm(n):
	result = 0
	try:
		print(n)
		os.system('rm /root/blog/source/_posts/' + n)
		os.system('rm /root/blog/public/backup_md/' + n)
		result = 1
	except:
		pass
	return result
def run():
	try:
		url = sys.argv[1]
		check_r = check(url)
		print("File name : " + Filename)
		if check_r == 1:
			check_i = input("[+] Do you want to upload a file? (Y/N) : ").lower()
			print(check_i)
			if check_i == 'y' or check_i == 'yes':
				if save(url):
					print("[+] Upload Success")
				else:
				 	print("[+] Upload Failed")
			else:
				print("[+] Not Upload")

		elif check_r == 2:
			check_i = input("[+] File upload already exists. Would you like to delete and download it? (Y/N) : ").lower()
			if check_i == 'y' or check_i == 'yes':
				if rm(Filename):
					print("[+] Delete Success")
					if save(url):
						print("[+] Upload Success")
					else:
						print("[+] Upload Failed")
				else:
					print("[+] Delete Failed")
			else:
				print("[+] Not Upload")
		else:
			print('[+] Please upload the markdown file.')
	except:
		print(help)

if __name__ == '__main__':
	run()