import requests
from bs4 import BeautifulSoup
from csv import reader
import pandas as pd
from sqlalchemy import create_engine
from datetime import date
from django_pandas.io import read_frame

from django.core.management.base import BaseCommand
from website.models import Permit

class Command(BaseCommand):
    help = 'Scrape new permit status data from LDEQ website and compare to current database.'

    def handle(self, *args, **options):
	    #permit status url
	    url = 'https://internet.deq.louisiana.gov/portal/ONLINESERVICES/CHECK-PERMIT-STATUS'
	    #form values that don't change
	    payload = {"__EVENTTARGET": "dnn$ctr489$dnn", "__EVENTARGUMENT": "CSV,Export,,M"}
	    #form values to be retrieved from get request
	    headers = ["__VIEWSTATE","__VIEWSTATEGENERATOR","__VIEWSTATEENCRYPTED","__EVENTVALIDATION",]

	    #retrieving payload from website
	    r = requests.get(url)
	    soup = BeautifulSoup(r.text, 'html.parser')
	    
	    #returning payload values
	    for head in headers:
	        val = soup.find(id=head)['value']
	        payload[head] = val

	    #retrieving permit status data
	    q = requests.post('https://internet.deq.louisiana.gov/portal/ONLINESERVICES/CHECK-PERMIT-STATUS', data=payload)
	    
	    #splitting text into rows
	    text = q.text.splitlines()
	    rows = []

	    for line in reader(text, skipinitialspace=True):
	        rows.append(line)

	    data = rows[1:]
	    columns = rows[0]
	    df = pd.DataFrame(data,columns=columns)
	    df.MASTER_AI_ID = pd.to_numeric(df.MASTER_AI_ID)
	    df.RECEIVED_DATE = pd.to_datetime(df.RECEIVED_DATE)
	    df.STATUS_DATE = pd.to_datetime(df.STATUS_DATE)
	    df.EFFECTIVE_START_DATE = pd.to_datetime(df.EFFECTIVE_START_DATE)
	    df.EXPIRATION_DATE = pd.to_datetime(df.EXPIRATION_DATE)

	    #grabbing current table from database
	    qs = Permit.objects.all()
	    old = read_frame(qs)

	    #comparing to new scrape
	    cols = ['MASTER_AI_ID', 'MASTER_AI_NAME', 'ACT_TRACKING_NO', 'MEDIA', 'PARISH', 'WRITER', 'PERMIT_NO',
	    'ACTION_TYPE', 'STATUS', 'RECEIVED_DATE', 'STATUS_DATE', 'EFFECTIVE_START_DATE', 'EXPIRATION_DATE']
	    differences = pd.concat([old,df]).drop_duplicates(subset=cols, keep=False)

	    #ids to drop from current db
	    ids = differences['id'].dropna().unique()

	    for id_ in ids:
	    	Permit.objects.filter(id=id_).delete()

	    #creating dataframe for updates and appending to database model
	    updates = differences.loc[differences['id'].isnull(), cols]
	    updates['date_uploaded'] = date.today()

	    engine = create_engine('sqlite:///db.sqlite3')
	    updates.to_sql(Permit._meta.db_table, if_exists='append', con=engine, index=True, index_label = 'id')