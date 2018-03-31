# home-calendar-api
The API for the Harveys' home calendar

## Quickstart
 1. Create a Python 3 virtual environment
```
$ mkvirtualenv home-calendar-api -p python3
```
 2. Add the following environment variables to `postactivate`
```
export FLASK_APP=app.py
export FLASK_DEBUG=1
export CALENDAR_ID=<google-calendar-id>
```
 3. Install Python requirements
```
$ pip install -r requirements.txt
```
 4. (re)Activate the virtual environment
```
$ deactivate
$ workon home-calendar-api
```
 5. Try to run the app, and follow the Google OAuth instructions in the output
```
$ python app.py
...
oauth2client.clientsecrets.InvalidClientSecretsError: Cannot find client_secret.json.
	1. Go to https://console.developers.google.com/apis/credentials
...
```
6. Run the app
```
$ python app.py
```