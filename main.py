import sys
import argparse
import subprocess
import clean as df
import webscrp as wb


def recibeConfig():
    parser = argparse.ArgumentParser(description='¿Será el pichichi el fichaje del verano?')
    parser.add_argument('--summer',
                        help='Summer transfer market between 2000-2019',
                        '--league',
                        help='Select league Bundesliga, LaLiga, Premier League, League One, Serie A, Eredivisie
                        )
                        
    args = parser.parse_args()
    print(args)
    return args















if __name__=="__main__":
    main()