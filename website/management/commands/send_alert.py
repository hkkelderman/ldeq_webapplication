import pandas as pd
from django_pandas.io import read_frame
import win32com.client as win32

from django.core.management.base import BaseCommand
from website.models import Permit

class Command(BaseCommand):
    help = 'Sends filtered, updated data to subscribers.'

    def handle(self, *args, **options):
	    #grabbing current table from database
	    qs = Permit.objects.all()
	    data = read_frame(qs)
	    newest_date = data.sort_values('date_uploaded', ascending=False)['date_uploaded'].unique()[0]

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




#function for sending data updates to Sasha
def send_updates(length):
    """Takes the CSV with updates from the permit status website and sends them to Sasha. 
    
    Params:
    length - the number of permit status updates
    
    Currently returns a dataframe."""
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'kkelderman@environmentalintegrity.org'
    mail.Subject = 'LDEQ Permit Status Updates'
    mail.Body = 'This is an automated message. Attached is a CSV with {} updates to permits you are tracking.'.format(length)

    attachment  = "C:/Users/kkelderman/Documents/00_Coding Projects/O&G/LA EDMS Alert/Alert/DataUpdates.csv"
    mail.Attachments.Add(attachment)

    mail.Send()

    #send grid plugin for heroku and scheduler plugin

    #python email message - add attachment