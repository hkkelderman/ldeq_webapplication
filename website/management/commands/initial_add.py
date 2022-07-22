import requests
from bs4 import BeautifulSoup
from csv import reader
import pandas as pd
from sqlalchemy import create_engine
from datetime import date

from django.core.management.base import BaseCommand
from website.models import Permit


class Command(BaseCommand):
    help = 'Scrape initial permit status data from LDEQ website.'

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
        df['date_uploaded'] = date.today()

        engine = create_engine('sqlite:///db.sqlite3')

        df.to_sql(Permit._meta.db_table, if_exists='replace', con=engine, index=True, index_label = 'id')