from django.db import models

class users(models.Model):
	name = models.CharField(max_length = 50)
	username = models.TextField()
	password = models.TextField()
	age = models.CharField(max_length = 5)
	phone = models.CharField(max_length = 20)
	belong = models.CharField(max_length = 50)
	interests = models.CharField(max_length = 50)
	authority = models.CharField(max_length = 50, null = True)
	is_activy = models.CharField(max_length = 50, null = True)
	mail_activy = models.CharField(max_length = 50, null = True)
	score = models.CharField(max_length = 50, null = True)
	challenge = models.CharField(max_length = 5000, null = True) 