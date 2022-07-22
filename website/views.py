from django.shortcuts import render
from .models import Permit
import datetime

def home(request):
	context = {}
	return render(request, 'home.html', context)

def recent(request):
	recent_upload_date = Permit.objects.latest('date_uploaded').date_uploaded
	last_two = list(Permit.objects.values_list('date_uploaded', flat = True).distinct())[-2:]
	last_date = last_two[0]
	next_date = recent_upload_date + datetime.timedelta(days=7)
	recent_data = Permit.objects.filter(date_uploaded = recent_upload_date)
	num_updates = len(recent_data)
	check = Permit.objects.latest('RECEIVED_DATE').RECEIVED_DATE
	context = {'recent': recent_data,
	'recent_date': recent_upload_date,
	'num_updates' : num_updates,
	'next_date' : next_date,
	'last_date': last_date,
	'check': check
	}
	return render(request, 'recent.html', context)
