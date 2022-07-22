from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Parameter(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	organization = models.CharField(max_length=100)
	ais = models.TextField()

	def __str__(self):
		return str(self.user)

	def get_absolute_url(self):
		return reverse('home') #when filling out form for this model, this makes sure the button to submit data works
	
class Permit(models.Model):
	MASTER_AI_ID = models.IntegerField()
	MASTER_AI_NAME = models.CharField(max_length=150)
	ACT_TRACKING_NO = models.CharField(max_length=50)
	MEDIA = models.CharField(max_length=25)
	PARISH = models.CharField(max_length=30)
	WRITER = models.CharField(max_length=35)
	PERMIT_NO = models.CharField(max_length=60)
	ACTION_TYPE = models.CharField(max_length=75)
	STATUS = models.CharField(max_length=15)
	RECEIVED_DATE = models.DateField(null=True, blank=True)
	STATUS_DATE = models.DateField(null=True, blank=True)
	EFFECTIVE_START_DATE = models.DateField(null=True, blank=True)
	EXPIRATION_DATE = models.DateField(null=True, blank=True)
	date_uploaded = models.DateField(auto_now=True)

	def __str__(self):
		return f'{self.MASTER_AI_ID} - {self.ACT_TRACKING_NO}'