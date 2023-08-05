import pandas as pd
import requests
import json
from datetime import datetime
from IPython.display import clear_output


def json_col_to_df(df,col_name,drop_col=True):
  df2 = pd.DataFrame([i if type(i)==dict else {} for i in df[col_name].values])
  df2.columns = [f"{col_name}>{i}" for i in df2.columns]
  df3 = pd.concat([df,df2],axis=1)
  if drop_col:
    df3 = df3.drop(columns=[col_name])
  return df3

def list_col_to_df(df,col_name,key='name',value='value',drop_col=True):
  df[col_name] = [{i[key]:i[value] for i in j} for j in df[col_name]]
  df = json_col_to_df(df,col_name,drop_col=drop_col)
  return df

def expand_df(df,key='',value=''):

  while True:
    no_of_dicts=0
    for i in df.columns:
      if type(df[i][0])==dict:
        no_of_dicts+=1
        df = json_col_to_df(df,i)
      elif type(df[i][0])==list and key:
        no_of_dicts+=1
        df = list_col_to_df(df,i,key=key,value=value)
    if no_of_dicts==0:
      break
    
  return df

def get_fixtures(no_results=100,page=0,compSeasons=0,gameweeks=0,teams='',statuses='U,L,C',startDate='',endDate='',sort='asc'):

  url = "https://footballapi.pulselive.com/football/fixtures"

  params = {
      "comps":1,
      "pageSize":no_results,
      "page":page,
      "statuses":statuses,
      "sort":sort
  }

  if startDate and endDate:
    params['startDate'] = startDate
    params['endDate'] = endDate

  if compSeasons:
    params['compSeasons'] = compSeasons
  
  if gameweeks:
    params['gameweeks'] = gameweeks

  if teams:
    params['teams'] = teams


  payload = {}
  headers = {
    'authority': 'footballapi.pulselive.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'accept': '*/*',
    'origin': 'https://draft.premierleague.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://draft.premierleague.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload,params=params)

  try:
    response = json.loads(response.text.encode('utf8'))
  except:
    
    response = {
        "error":"Unknown",
        "response": response.text.encode('utf8')
    }

  return response

def get_match_stats(match_id):

  url = f"https://footballapi.pulselive.com/football/stats/match/{match_id}"

  payload = {}
  headers = {
    'authority': 'footballapi.pulselive.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': '*/*',
    'origin': 'https://www.premierleague.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.premierleague.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload)

  try:
    response = json.loads(response.text.encode('utf8'))
  except:
    
    response = {
        "error":"Unknown",
        "response": response.text.encode('utf8')
    }

  return response

def get_teams(compSeasons=363):
  url = f"https://footballapi.pulselive.com/football/compseasons/{compSeasons}/teams"

  payload = {}
  headers = {
    'authority': 'footballapi.pulselive.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'account': 'premierleague',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': '*/*',
    'origin': 'https://www.premierleague.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.premierleague.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload)

  try:
    response = json.loads(response.text.encode('utf8'))
  except:
    
    response = {
        "error":"Unknown",
        "response": response.text.encode('utf8')
    }

  return response

def get_standings(compSeasons=363):
  url = f"https://footballapi.pulselive.com/football/standings?compSeasons={compSeasons}"

  payload = {}
  headers = {
    'authority': 'footballapi.pulselive.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': '*/*',
    'origin': 'https://www.premierleague.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.premierleague.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload)

  try:
    response = json.loads(response.text.encode('utf8'))
  except:
    
    response = {
        "error":"Unknown",
        "response": response.text.encode('utf8')
    }

  return response

def get_team_stats(team_id=10,compSeasons=363):
  url = f"https://footballapi.pulselive.com/football/stats/team/{team_id}?comps=1&compSeasons={compSeasons}"

  payload = {}
  headers = {
    'authority': 'footballapi.pulselive.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': '*/*',
    'origin': 'https://www.premierleague.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.premierleague.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload)

  try:
    response = json.loads(response.text.encode('utf8'))
  except:
    
    response = {
        "error":"Unknown",
        "response": response.text.encode('utf8')
    }

  return response

def get_squad(compseasons=363,current=False):

  url = f"https://footballapi.pulselive.com/football/teams/26/compseasons/{compseasons}/staff?altIds=false&compCodeForActivePlayer=EN_PR&date=2019-09-03"

  params = {
      "altIds":"false",
      "compCodeForActivePlayer":"EN_PR", 
  }

  if current:
    params['date'] = str(datetime.today())[:10]


  payload = {}
  headers = {
    'authority': 'footballapi.pulselive.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': '*/*',
    'origin': 'https://www.premierleague.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.premierleague.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload,params=params)

  try:
    response = json.loads(response.text.encode('utf8'))
  except:
    
    response = {
        "error":"Unknown",
        "response": response.text.encode('utf8')
    }

  return response

def get_players(compSeasons=363,pageSize=1000):
  url = f"https://footballapi.pulselive.com/football/players?pageSize={pageSize}&compSeasons={compSeasons}&altIds=false&page=&type=player&id=-1"

  payload = {}
  headers = {
    'authority': 'footballapi.pulselive.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': '*/*',
    'origin': 'https://www.premierleague.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.premierleague.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload)

  try:
    response = json.loads(response.text.encode('utf8'))
  except:
    
    response = {
        "error":"Unknown",
        "response": response.text.encode('utf8')
    }

  return response

def get_player_stats(id,compSeasons=363):

  url = f"https://footballapi.pulselive.com/football/stats/player/{id}"

  params = {
      "comps":1,
  }

  if compSeasons!=0:
    params['compSeasons'] = compSeasons

  payload = {
  }

  headers = {
    'authority': 'footballapi.pulselive.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': '*/*',
    'origin': 'https://www.premierleague.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.premierleague.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload,params=params)

  try:
    response = json.loads(response.text.encode('utf8'))
  except:
    
    response = {
        "error":"Unknown",
        "response": response.text.encode('utf8')
    }

  return response

def get_fpl_data():
  url = "https://fantasy.premierleague.com/api/bootstrap-static/"

  payload = {}
  headers = {
    'authority': 'fantasy.premierleague.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://fantasy.premierleague.com/statistics',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload)

  try:
    response = json.loads(response.text.encode('utf8'))
  except:
    
    response = {
        "error":"Unknown",
        "response": response.text.encode('utf8')
    }

  return response

def get_fpl_player_stats(id):

  url = f"https://fantasy.premierleague.com/api/element-summary/{id}/"

  payload = {}
  headers = {
    'authority': 'fantasy.premierleague.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://fantasy.premierleague.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
    }

  response = requests.get(url, headers=headers, data = payload)

  try:
    response = json.loads(response.text.encode('utf8'))
  except:
    
    response = {
        "error":"Unknown",
        "response": response.text.encode('utf8')
    }

  return response

