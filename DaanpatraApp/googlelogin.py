import os, sys
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.file import Storage
import requests


def return_token(): 
  return get_oauth2_token()


def disable_stout():
  o_stdout = sys.stdout 
  o_file = open(os.devnull, 'w')
  sys.stdout = o_file
  return (o_stdout, o_file)


def enable_stout(o_stdout, o_file):
  o_file.close()
  sys.stdout = o_stdout


def get_oauth2_token():
  CLIENT_ID = '1075097280260-sorptfjmrivp3i0oom42bl268dag0in9.apps.googleusercontent.com'
  CLIENT_SECRET = 'DnFSC6L1MoC0JXShsu3h1jDI'
  SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
  REDIRECT_URI = "http://localhost:8080/"
  
  o_stdout, o_file = disable_stout()

  flow = OAuth2WebServerFlow(
   client_id=CLIENT_ID,
   client_secret=CLIENT_SECRET,
   scope=SCOPE,
   redirect_uri=REDIRECT_URI)

  storage = Storage('creds.data')
  credentials = run_flow(flow, storage)
  enable_stout(o_stdout, o_file)

  token = credentials.access_token
  f = open("token.txt", "w")
  f.write(token)
  f.close()


if __name__ == "__main__":
  return_token()


