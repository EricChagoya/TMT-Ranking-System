import UserInterface as UI

import time
import numpy as np
import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

# pip install gspread
# pip install df2gspread
# pip install oauth2client


def getClient() -> 'client':
    """Get the credentials to allow us access to the Google Sheets."""

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    gc = gspread.authorize(credentials)
    time.sleep(1)
    return credentials

def addPlusSign(df: 'df') -> None:
    """For RankChange, if the number is positive, add a plus sign. I convert
    all the numbers into strings."""
    t= pd.DataFrame()
    for index, row in df.iterrows():
        try:
            float(row['RankChange'])
            num = row['RankChange']
            a= num.split('.')
            if '-' not in a[0]:
                new_row = {'RankChange': "+" + a[0]}
            else:
                new_row = {'RankChange': a[0]}
        except:
            new_row = {'RankChange': row['RankChange']}
            pass
        t = t.append(new_row, ignore_index = True)

    df['RankChange'] = t['RankChange']


def removeFloat(df: 'df') -> None:
    """Remove the float sign for the Armada Number"""
    ArmadaNumber = df.columns[1]
    t= pd.DataFrame()
    for index, row in df.iterrows():
        try:
            new_row = {'ArmadaNumber': int(row[1])}
        except:
            new_row = {'ArmadaNumber': 'NA'}
            
        t = t.append(new_row, ignore_index = True)

    df['ArmadaNumber'] = t['ArmadaNumber']
    df = df[['SmashTag', 'ArmadaNumber', 'Path']]
    df = df.rename(columns = {'ArmadaNumber': ArmadaNumber})
    df['Path'] = df['Path'].fillna("")
    return df

    

def updateWeeklyFiles(credentials: 'credentials', season: int, week: int) -> None:
    """Update the Website Google Sheets that only need one sheet. In this case it's only
    TotalRankings, WeeklyRankings, and ArmadaNumber"""
    spreadsheet_key = '1vkuvUasB_pgLFJtVFcmpIxXj8EfoxL0y-ms9rVw0R74'
    wks_name = 'WeeklyRankings'
    websiteSheets = ['TotalRankings', 'WeeklyRankings', 'ArmadaNumber']
    
    files = [f'Data/Season{season}/Website/S{season}W{week}WebsiteTotalRanks.csv',
             f'Data/Season{season}/Website/S{season}W{week}WebsiteWeeklyRank.csv',
             f'Data/Season{season}/ArmadaNumber/S{season}W{week}ArmadaNumber.csv']

    for i in range(len(files)):
        df = pd.read_csv(files[i], encoding = 'ISO-8859-1')
        if websiteSheets[i] == 'TotalRankings':
            df['Rank'] = df['Rank'].astype(int)
            df['Bankroll Bills'] = df['Bankroll Bills'].astype(int)
            addPlusSign(df)
        elif websiteSheets[i] == 'WeeklyRankings':
            df['Rank'] = df['Rank'].astype(int)
            df['Bankroll Bills'] = df['Bankroll Bills'].astype(int)
        else:
            ArmadaNumber = df.columns[1]
            t= pd.DataFrame()
            for index, row in df.iterrows():
                try:
                    new_row = {'ArmadaNumber': str(int(row[1]))}
                except:
                    new_row = {'ArmadaNumber': 'NA'}
                    
                t = t.append(new_row, ignore_index = True)

            df['ArmadaNumber'] = t['ArmadaNumber']
            df = df[['SmashTag', 'ArmadaNumber', 'Path']]
            df = df.rename(columns = {'ArmadaNumber': ArmadaNumber})
            df['Path'] = df['Path'].fillna("")
        
        d2g.upload(df, spreadsheet_key, websiteSheets[i], credentials = credentials, row_names = False)
        time.sleep(10)


def updateRanks(credentials: 'credentials', season: int, week: int) -> None:
    """Update the Website Google Sheets for all Ranks. This will update each character,
    the MidTiers, and Other"""
    spreadsheet_key = '1gwi2PAyjBA2peLLexP2NGO2mfh_J-AbH8uxkAf3xt_s'
    wks_name = 'Ranks'
    websiteSheets = ['Fox', 'Falco', 'Marth', 'Sheik', 'Falcon',
                     'Puff', 'Peach', 'ICs', 'MidTiers', 'Other']
    
    characters = f'Data/Season{season}/PlotsWebsite/S{season}W{week}RankLegend.csv'
    characters = pd.read_csv(characters, encoding = 'ISO-8859-1')

    for i in range(len(websiteSheets)):
        character = websiteSheets[i]
        df = characters[characters['Character'] == character]
        df = df[['SmashTag', 'Rank']]
        df['Rank'] = df['Rank'].astype(int)
        d2g.upload(df, spreadsheet_key, character, credentials = credentials, row_names = False)
        time.sleep(10)
        print(character)


def updatePoints(credentials: 'credentials', season: int, week: int) -> None:
    """Update the Website Google Sheets for all Bills. This will update each character,
    the MidTiers, and Other"""
    spreadsheet_key = '12Q-krFLMSpc-AuLH2KGjTz9SoAwC1ob1spxmVW7XSfY'
    wks_name = 'Bills'
    websiteSheets = ['Fox', 'Falco', 'Marth', 'Sheik', 'Falcon',
                     'Puff', 'Peach', 'ICs', 'MidTiers', 'Other']
    
    characters = f'Data/Season{season}/PlotsWebsite/S{season}W{week}PointsLegend.csv'
    characters = pd.read_csv(characters, encoding = 'ISO-8859-1')
    
    for i in range(len(websiteSheets)):
        character = websiteSheets[i]
        df = characters[characters['Character'] == character]
        df = df.rename(columns={'Points': 'Bills'})
        df['Bills'] = df['Bills'].astype(int)
        df = df[['SmashTag', 'Bills']]
        d2g.upload(df, spreadsheet_key, character, credentials = credentials, row_names = False)
        time.sleep(10)
        print(character)



def main():
    season = UI.UserSeason()
    week = UI.UserWeek()
    #season = 1
    #week = 8
    
    credentials = getClient()

    updateWeeklyFiles(credentials, season, week)
    time.sleep(100)
    updateRanks(credentials, season, week)
    time.sleep(100)
    updatePoints(credentials, season, week)

    
main()

