from __future__ import print_function
import httplib2
import os
import datetime
import logging

from flask import Flask, jsonify, request
from flask_cors import CORS
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.clientsecrets import InvalidClientSecretsError


app = Flask(__name__)
CORS(app)
app.config['CALENDAR_ID'] = os.environ['CALENDAR_ID']

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = "Harveys' Home Calendar"


logger = logging.getLogger(__name__)


def get_credentials():
    """Gets valid user credentials from storage.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.google_credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'harveys-home-calendar.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        
        try:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        except InvalidClientSecretsError as e:
            current_directory = os.getcwd()
            message = (
                'Cannot find client_secret.json.\n'
                '\t1. Go to https://console.developers.google.com/apis/credentials\n'
                '\t2. Select the correct project\n'
                '\t3. Download the correct OAuth 2.0 client IDs JSON\n'
                f'\t4. Save the file as {current_directory}/client_secret.json'
            )
            raise type(e)(message)
        
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags=None)
        logger.info('Storing credentials to ' + credential_path)
    
    return credentials


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)


@app.route("/", methods=['GET', 'OPTIONS'])
def get_events():
    """
    Create a Google Calendar API service object and output a list of the next
    10 events on the user's calendar.
    """
    start = request.args.get('start', None)
    if not start:
        start = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    end = request.args.get('end', None)

    kwargs = {
        'calendarId': app.config['CALENDAR_ID'], 
        'timeMin': start, 
        'maxResults': 100,
        'singleEvents': True,
        'orderBy': 'startTime'
    }
    if end:
        kwargs['timeMax'] = end

    eventsResult = service.events().list(**kwargs).execute()

    return jsonify(eventsResult)


if __name__ == "__main__":
    get_credentials()
    app.run()