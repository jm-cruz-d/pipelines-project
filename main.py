import sys
import argparse
import subprocess
import chardet 
import pandas as pd
from fpdf import FPDF


def openDf(file):
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())
    return pd.read_csv(file, encoding=result['encoding'])

transfers = openDf('./output/TransferLeagues.csv')
Bundesliga = openDf('./output/bundT.csv')
LaLiga = openDf('./output/spainT.csv')
Premier_League = openDf('./output/premierT.csv')
League_One = openDf('./output/frenchT.csv')
Serie_A = openDf('./output/italyT.csv')
Eredivisie = openDf('./output/hollT.csv')

def recibeConfig():
    parser = argparse.ArgumentParser(description='¿Será el pichichi el fichaje del verano?')
    parser.add_argument('--summer',
                        help='Summer transfer market between 2000-2019')
    parser.add_argument('--league',
                        help='Select league Bundesliga: "./output/bundT.csv", LaLiga: "./output/spainT.csv", Premier_League: "./output/premierT.csv", League_One: "./output/frenchT.csv", Serie_A: "./output/italyT.csv", Eredivisie: "./output/hollT.csv"')
    args = parser.parse_args()
    #print(args)
    return args

def main(): 
    config = recibeConfig() 
    newDF=transfers[0:0]
    league = openDf(config.league)
    year = int(config.summer)
    for name in transfers['Comb']:
        for player in league['Comb']:
            if name == player:  
                newDF = newDF.append(transfers.loc[transfers['Comb'] == name])
    if newDF.empty:
        return 'Not coincidence'
    else:
        return newDF[newDF['Summer']==year]
       
#def createPDF(x):
#    pdf = FPDF()
#    pdf.add_page()
#    pdf.image("./output/castolo.jpeg", x=60, y=30, w=100)
#    pdf.set_font("Arial", size=12)
#    pdf.ln(85)  # move 85 down
#    pdf.cell(200, 5, txt=x, ln=1, align="C")
#    return pdf.output("./output/result.pdf")

#createPDF(main())

if __name__=="__main__":
    print(main())