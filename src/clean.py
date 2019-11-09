import pandas as pd
import numpy as np
import re as re
import chardet   #Character encoding auto-detection in Python

lfile = '../input/top250-00-19.csv'

#Open DataFrame
def openDf(x):
    with open(x, 'rb') as f:
        result = chardet.detect(f.read())
    return pd.read_csv(x, encoding=result['encoding'])

df = openDf(lfile)

#Delete columns with more than 1000 nulls
def nullOut(x):
    null_cols = x.isnull().sum()
    return x.drop((list(null_cols[null_cols>1000].index)), axis=1)

df=nullOut(df)

#Delete columns of any DF, parameter "x" is DF and the parameter "y" must be a list
def dropCol(x, y):
    return x.drop(columns=y)

df=dropCol(df,['Position','League_to', 'Age'])

#Converter to millions, parameter "x" is DF and the parameter "y" is a column
def convMill(x, y):
    x[y]=x[y]/10**6
    return x

df = convMill(df, 'Transfer_fee')

#Makes filters, parameter "x" is DF, the parameter "y" is a column name and "ligas" is a list with the elements that
#you want to filter in column "y"
def generaFiltros(x, y, ligas):
    prob = x[(x[y].isin(ligas))]
    return prob

slclig = ['Bundesliga','LaLiga','Premier League','League One', 'Serie A', 'Eredivisie']
df = generaFiltros(df, 'League_from', slclig)

#Import DF to csv
def impCsv(x):
    return x.to_csv('../output/TransferLigas.csv', header=True, index=False)

impCsv(df)