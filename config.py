import os
import flask
import requests
import time

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
# import bot

from flask import Flask, session
from flask_session import Session

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


app = flask.Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = '008229561849532'

Session(app)


@app.route('/')
def index():
  return print_index_table()


@app.route('/start')
def start_process():
  if 'start' in session:
    return ("Bot is already running yo.")
  if 'credentials' not in session:
    return ('Credentials not available, authroization required first')

  session['start'] = 1
  # bot.start()


@app.route('/test')
def test_api_request():
  if 'credentials' not in flask.session:
    return flask.redirect('authorize')

  # Load credentials from the session.
  credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])

  drive = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials)

  files = drive.files().list().execute()

  # Save credentials back to session in case access token was refreshed.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  flask.session['credentials'] = credentials_to_dict(credentials)

  return flask.jsonify(**files)


@app.route('/authorize')
def authorize():

  if('authorized' in session):
    #Already authed
    return ("ALready authroized.")


  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

  # The URI created here must exactly match one of the authorized redirect URIs
  # for the OAuth 2.0 client, which you configured in the API Console. If this
  # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
  # error.
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  flask.session['state'] = state

  return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  creds_to_store = credentials_to_dict(credentials)
  f = open('credentials.txt','w')
  f.write(str(creds_to_store))
  f.close()
  flask.session['credentials'] = creds_to_store
  session['credentials'] = creds_to_store
  session['authorized'] = 1
  return "successfully authorized."
  # return flask.redirect(flask.url_for('test_api_request'))


@app.route('/revoke')
def revoke():
  if 'credentials' not in flask.session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
    **flask.session['credentials'])

  revoke = requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.' + print_index_table())
  else:
    return('An error occurred.' + print_index_table())


@app.route('/clear')
def clear_credentials():
  if 'credentials' in flask.session:
    del flask.session['credentials']
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())




def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def print_index_table():
  # tmp = ""
  # if 'authroized' in session:
  #   tmp+="Already authorized\n"
  # else:
  #   tmp+="Not authorized yet\n"
  # if 'start' in session:
  #   tmp+="Bot is running"
  # else:
  #   tmp+="Bot is not running yet"

  # return ('<h1>%s</h1><table>'%(tmp) +
  #         '<tr><td><a href="/test">Test an API request</a></td>' +
  #         '<td>Submit an API request and see a formatted JSON response. ' +
  #         '    Go through the authorization flow if there are no stored ' +
  #         '    credentials for the user.</td></tr>' +
  #         '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
  #         '<td>Go directly to the authorization flow. If there are stored ' +
  #         '    credentials, you still might not be prompted to reauthorize ' +
  #         '    the application.</td></tr>' +
  #         '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
  #         '<td>Revoke the access token associated with the current user ' +
  #         '    session. After revoking credentials, if you go to the test ' +
  #         '    page, you should see an <code>invalid_grant</code> error.' +
  #         '</td></tr>' +
  #         '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
  #         '<td>Clear the access token currently stored in the user session. ' +
  #         '    After clearing the token, if you <a href="/test">test the ' +
  #         '    API request</a> again, you should go back to the auth flow.' +
  #         '</td></tr></table>')


  return ('<a href="/authorize"> Authenticate with your Google Account</a>')




def start_server():
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  app.run('localhost', 8080, debug=True)

if __name__ == '__main__':
  # print("[*] Authenticate with your Google Account.")
  print("[*] Go to http://localhost:8080 in your browser to authenticate with your Google Account.")
  time.sleep(2)
  start_server()
  pass