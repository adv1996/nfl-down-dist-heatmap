import json
import requests
import csv
from bs4 import BeautifulSoup
import time

def scrape(player, espn_id):
  player_url = "https://www.espn.com/nfl/player/splits/_/id/{1}/{0}".format(player, espn_id)
  page_response = requests.get(player_url, timeout=5)
  page_content = BeautifulSoup(page_response.content, "html.parser")
  table_body = page_content.find('table', attrs={'class': "Table Table--align-right"})
  
  # get left side of table
  left_headers = page_content.find('tbody', attrs={"class": "Table__TBODY"})
  leftRows = left_headers.findAll('tr')
  leftdata = []
  for r in leftRows:
    items = r.findAll('td')
    dataItems = []
    for i in items:
      dataItems.append(i.text)
    leftdata.append(dataItems)
  rows = table_body.findAll('tr')
  #assign headers for json keys
  headers = []
  for h in rows[1:2]:
    items = h.findAll('td')
    for i in items[:10]:
      headers.append(i.text)

  # assemble data items and seam headers and left headers
  data = {}
  for r in range(1, len(rows)):
    items = rows[r].findAll('td')
    dataItems = {}
    for i in range(0, 10):
      dataItems[headers[i]] = items[i].text
    
    data[leftdata[r-1][0]] = dataItems
  filename = '/Users/advaithvenkatakrishnan/Projects/new_era/nfl-down-dist-heatmap/players/' + player + '-week3-2019.json'
  saveJson(filename, data)

def saveJson(filename, data):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile)
  outfile.close()
  print('Completed Web Scraping ' + str(len(data)) + ' Items')

def playersToScrape():
  with open('active_quarterbacks.json') as json_file:
    data = json.load(json_file)
    for p in data['rows']:
      print('Name: ' + p[4] + "-" + p[3] + 'ESPN_ID ' + p[0])
      name = p[4] + "-" + p[3]
      espnid = p[0]
      scrape(name, espnid)
      time.sleep(5)
      print('Successfully Retrieved Player Splits')
  json_file.close()

def assembleCleanedDataHeatMap():
  playerFiles = []
  data = []
  with open('active_quarterbacks.json') as json_file:
    data = json.load(json_file)
    for p in range(0, len(data['rows'])):
      name = data['rows'][p][4] + "-" + data['rows'][p][3]
      espnid = data['rows'][p][0]
      extractFile = '/Users/advaithvenkatakrishnan/Projects/new_era/nfl-down-dist-heatmap/players/' + name + '-'+ 'week3-2019.json'
      playerFiles.append(extractFile)
  json_file.close()
  
  fieldsToCollect = [
    "1st and <=5",
    "2nd and <=5",
    "3rd and <=5",
    "4th and <=5",
    "1st and 6+",
    "2nd and 6+",
    "3rd and 6+",
    "4th and 6+"
  ]
  
  columns = ['CMP', 'ATT', 'YDS', 'CMP%', 'AVG', 'TD', 'INT', 'LNG', 'SACK', 'RTG']
  playersJsonData = {}
  playersJsonData["players"] = {}
  for f in range(0, len(playerFiles)):
    with open(playerFiles[f]) as json_file:
      playerData = json.load(json_file)
      fieldData = {}
      for field in fieldsToCollect:
        fieldData[field] = {}
        if field in playerData:
          for key in playerData[field]:
            fieldData[field][key] = float(playerData[field][key])
        else:
          for key in columns:
            fieldData[field][key] = 0
      # fieldData["firstName"] = data['rows'][f][4]
      # fieldData["lastName"] = data['rows'][f][3]
      down_dist = {}
      down_dist["down_dist"] = fieldData
      down_dist["sleeper_id"] = data["rows"][f][5]
      playersJsonData["players"][data['rows'][f][4] + "-" + data['rows'][f][3] + "-"+ data['rows'][f][0]] = down_dist
    json_file.close()
  saveJson("playerData.json", playersJsonData)
scrape("kyle-allen", 3115293)
assembleCleanedDataHeatMap()