from django.db import models
class users(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	number = models.BigIntegerField()
# Create your models here.