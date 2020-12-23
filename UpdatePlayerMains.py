import numpy as np
import pandas as pd

import UserInterface as UI

# This file is going to update annoying problems
# Find players who never entered TMT and add them to PlayerMains.csv
# Update Players when they have a new tag

def getNewPlayersSeason(season: int, week: int) -> {'SmasherID', 'SmashTag'}:
    """Find all the players who never TMT that season."""
    PastPoints = f'Data/Season{season}/Records/S{season}W{week}PastPoints.csv'
    PastPoints = pd.read_csv(PastPoints, encoding = 'ISO-8859-1')
    NewPlayers = dict()
    if week != 1:
        # If they didn't have any points in the second to last week,
        # they are new to the season
        for _, row in PastPoints.iterrows():
            if row[f'BWeek{week - 1}'] == "NAN":
                NewPlayers[row['SmasherID']] = row['SmashTag']
    else:
        for _, row in PastPoints.iterrows():
            NewPlayers[row['SmasherID']] = row['SmashTag']
    return NewPlayers


def UpdateNewPlayerMains(season: int, week: int, TMTNumber: int) -> None:
    """This will find players who have never entered a TMT
    and put their SmasherID, SmashTag, and what TMT was their
    first TMT into PlayerMains.csv"""
    Mainsfile = "Data/PlayerMains.csv"
    Mains = pd.read_csv(Mainsfile, encoding = 'utf-8-sig')
    newPlayers = getNewPlayersSeason(season, week)
    print(Mains.columns)
    oldPlayers = set(Mains['SmasherID'])
    for SmasherID, SmashTag in sorted(newPlayers.items(), key = lambda item: item[1]):
        if SmasherID not in oldPlayers:
            new_row = {'SmasherID': SmasherID, 'SmashTag': SmashTag,
                       'Main': '', 'FirstTMT': TMTNumber}
            Mains = Mains.append(new_row, ignore_index = True)    
    Mains.to_csv(Mainsfile, index = False, encoding='utf-8-sig')


def UpdateTags(season: int, week: int) -> None:
    Mainsfile = "Data/PlayerMains.csv"
    Mains = pd.read_csv(Mainsfile, encoding = 'utf-8-sig')
    PastPoints = f'Data/Season{season}/Records/S{season}W{week}PastPoints.csv'
    PastPoints = pd.read_csv(PastPoints, encoding = 'ISO-8859-1')

    t1 = {row['SmasherID']: row['SmashTag'] for _, row in Mains.iterrows()}
    t2 = {row['SmasherID']: row['SmashTag'] for _, row in PastPoints.iterrows()}

    k1 = set(t1.keys())
    k2 = set(t2.keys())
    common_keys = set(k1).intersection(set(k2))
    updatedTags = dict()

    for key in common_keys:
        if t1[key] != t2[key]:
            #print(str(key) + ":" + str(t2[key]) + " match " + str(t1[key]))
            updatedTags[key] = t2[key]

    for SmasherID, SmashTag in updatedTags.items():
        location = Mains.loc[Mains['SmasherID'] == SmasherID]
        Mains.at[location.index[0], 'SmashTag'] = SmashTag
    Mains.to_csv(Mainsfile, index = False, encoding = 'utf-8-sig')


def main():
    season = UI.UserSeason()
    week = UI.UserWeek()
    TMTNumber = UI.UserTMTNumber()
    #season = 1
    #week = 7
    #TMTNumber = 7
    UpdateNewPlayerMains(season, week, TMTNumber)
    UpdateTags(season, week)




main()
