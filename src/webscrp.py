import pandas as pd
import numpy as np
import re as re
import requests
from bs4 import BeautifulSoup
import cleanWS as cw

url = "https://es.wikipedia.org/wiki/Trofeo_Pichichi"
#Open the Page
def getPage(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

pichi = getPage(url)

#Create pichichi table
def getPichichi(soup, postable, row, cellSeason, cellPlayers, cellGoals):
    table = soup.find_all('table')[postable]
    rows = table.find_all('tr')[row:]
    pichichi = []
    for row in rows:
        cells = row.find_all('td')
        pichichi.append({
            "season": re.sub("[()\\n]", "", cells[cellSeason].find('a').text),
            "players": re.sub("[0-9]?[()\\n]", "", cells[cellPlayers].text),
            "goals": int(re.sub("[()\\n]", "", cells[cellGoals].text)[:2])       
        })
    return pd.DataFrame(pichichi)

pc = getPichichi(pichi, 1, 76, 0, 1, 5)

def subThings(DF, column, text):
    DF[column] = DF[column].replace('\[?[0-9]+\]?', text)
    return DF

pc = subThings(pc, 'players', "")

def convSeas(DF, column, range1, range2):
    lista = list(range(range1,range2))
    DF[column]=lista
    return DF

pc = convSeas(pc, 'season', 2000, 2020)

#Select Capocannoniere (Pichichi Italy)
pichIt=getPage("http://www.lalanternadelpopolo.it/Calcio%20-%20Capocannonieri%20Campionato%20Italia%20Albo%20d'Oro%20Vincitori.htm")

def getCapo(soup):
    table = pichIt.find_all('table')[3]
    rows = table.select('tr')[77:97]
    capo = []
    for row in rows:
        cells = row.find_all('td')
        capo.append({
            "season": cells[0].text.strip(),
            "players": cells[1].text.strip(),
            "goals": cells[2].text.strip()})
    return pd.DataFrame(capo)

capo = getCapo(pichIt)

#Delete Rows, just in case of two top scorers
def deleteRow(DF, row):
    DF = DF.drop(row)
    return DF

capo = deleteRow(capo, 16)

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

premierT = getTop(top)
premierT = deleteRow(premierT, [1,2,11])
premierT = convSeas(premierT, 'season', 2000, 2020)

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

holland = getWiki(holl, 0, 44, 0, 1, 2)
frenchs = getWiki(french, 0, 62, 0, 1, 3)
bundSc = getWiki(bund, 3, 37, 0, 1, 3)
hollT = convSeas(holland, 'season', 2000, 2019)
frenchT = convSeas(frenchs, 'season', 2000, 2018)
bundT = convSeas(bundSc, 'season', 2000, 2019)

#Cleaning with cleanWS
bundT = cw.subChar(bundT, 'players', 'ž', 'z')
bundT = cw.subChar(bundT, 'players', ' Martin Max', '')
bundT = cw.subChar(bundT, 'players', ' Ebbe Sand', '')
bundT = cw.subChar(bundT, 'players', ' Thomas Christiansen', '')
frenchT = cw.subChar(frenchT, 'players', 'CisséPauleta', 'Cissé')
frenchT = cw.subChar(frenchT, 'players', 'ć', 'c')
frenchT = cw.subChar(frenchT, 'players', ' Nené', '')
hollT = cw.subChar(hollT, 'players', 'ž', 'z')
premierT = cw.subChar(premierT, 'players', 'Kun\s.+', 'Sergio Agüero')
premierT = cw.subChar(premierT, 'players', 'Su.+', 'Suárez')
premierT = cw.subChar(premierT, 'players', 'Ma.+', 'Mané')
spainT = cw.subChar(pc, 'players', '\s\[[0-9]+\]', '')
italyT = capo

#Change types with cleanWS
bundT = cw.changeType(bundT, 'season', str)
frenchT = cw.changeType(frenchT, 'season', str)
hollT = cw.changeType(hollT, 'season', str)
premierT = cw.changeType(premierT, 'season', str)
spainT = cw.changeType(spainT, 'season', str)
italyT = cw.changeType(italyT, 'season', str)

#Combine columns
bundT = cw.combCol(bundT, 'Comb', 'players', 'season')
frenchT = cw.combCol(frenchT, 'Comb', 'players', 'season')
hollT = cw.combCol(hollT, 'Comb', 'players', 'season')
premierT = cw.combCol(premierT, 'Comb', 'players', 'season')
spainT = cw.combCol(spainT, 'Comb', 'players', 'season')
italyT = cw.combCol(italyT, 'Comb', 'players', 'season')

#Import to csv
cw.impCsv(bundT, './output/bundT.csv')
cw.impCsv(frenchT, './output/frenchT.csv')
cw.impCsv(hollT, './output/hollT.csv')
cw.impCsv(premierT, './output/premierT.csv')
cw.impCsv(spainT, './output/spainT.csv')
cw.impCsv(italyT, './output/italyT.csv')



