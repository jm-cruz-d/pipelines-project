import pandas as pd
import numpy as np
import re as re
import requests
from bs4 import BeautifulSoup

url = "https://es.wikipedia.org/wiki/Trofeo_Pichichi"
#Open the Page
def getPage(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

pichi = getPage(url)

#Create pichichi table
def getPichichi(soup):
    table = soup.find_all('table')[1]
    rows = table.find_all('tr')[77:]
    pichichi = []
    for row in rows:
        cells = row.find_all('td')
        pichichi.append({
            "season": re.sub("[()\\n]", "", cells[0].find('a').text),
            "players": re.sub("[0-9]?[()\\n]", "", cells[1].text),
            "goals": int(re.sub("[()\\n]", "", cells[5].text)[:2])       
        })
    return pd.DataFrame(pichichi)

pc = getPichichi(pichi)

def subThings(DF, column, text):
    DF[column] = DF[column].replace('\[?[0-9]+\]?', text)
    return DF

subThings(pc, 'players', "")

#Select Capocannoniere (Pichichi Italy)
pichIt=getPage("http://www.lalanternadelpopolo.it/Calcio%20-%20Capocannonieri%20Campionato%20Italia%20Albo%20d'Oro%20Vincitori.htm")

def getCapo(soup):
    table = pichIt.find_all('table')[3]
    rows = table.select('tr')[78:97]
    capo = []
    for row in rows:
        cells = row.find_all('td')
        capo.append({
            "season": cells[0].text.strip(),
            "players": cells[1].text.strip(),
            "goals": cells[2].text.strip()})
    return pd.DataFrame(capo)

capoc = getCapo(pichIt)

#Delete Rows, just in case of two top scorers
def deleteRow(DF, row):
    DF = DF.drop(row)
    return DF

deleteRow(capoc, 16)

#Select Top score form Premier League
top = getPage('https://www.worldfootball.net/top_scorer/eng-premier-league/')
def getTop(soup):
    table = top.find_all('table')[0]
    rows = table.select('tr')[1:24]
    rows
    tp = []
    for row in rows:
        cells = row.find_all('td')
        tp.append({
            "season": cells[0].text.strip(),
            "players": cells[2].text.strip(),
            "goals": cells[5].text.strip()})
    return pd.DataFrame(tp)

topPL = getTop(top)
topPL = deleteRow(topPL, [1,2,11])

#Select top League 1, Eredivisie and Bundesliga(Refactorizando)
french = getPage('https://es.wikipedia.org/wiki/Anexo:M%C3%A1ximos_goleadores_de_la_Liga_Francesa')
holl = getPage('https://es.wikipedia.org/wiki/Anexo:M%C3%A1ximos_goleadores_de_la_Eredivisie')
bund = getPage('https://es.wikipedia.org/wiki/Anexo:Estad%C3%ADsticas_de_la_Bundesliga_de_Alemania')

def getWiki(soup, postable, posrows, posSeason, posPlayers, posGoals):
    table = soup.find_all('table')[postable]
    rows = table.find_all('tr')[posrows:]
    wiki = []
    for row in rows:
        cells = row.find_all('td')
        wiki.append({
            "season": cells[posSeason].text.strip(),
                "players": cells[posPlayers].text.strip(),
                "goals": cells[posGoals].text.strip()})
    return pd.DataFrame(wiki)

getWiki(holl, 0, 45, 0, 1, 2)
getWiki(french, 0, 63, 0, 1, 3)
getWiki(bund, 3, 38, 0, 1, 3)

