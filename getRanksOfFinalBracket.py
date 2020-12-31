import numpy as np
import pandas as pd

import UserInterface as UI
import CollectTourneyData as CTD


def getPlayers(bracketID, pageCounts) -> {int: str}:
    """Get every player that made it into final bracket. Return their
    SmasherID and SmashTag"""
    query = '''
    query EventStandings($eventId: ID!, $page: Int!, $perPage: Int!) {
      event(id: $eventId){
        id
        name
        standings(query:{
          page: $page,
          perPage: $perPage
        }){
          nodes{
            entrant{
              id
              name
              participants{
                player{
                  id
                }
              }
            }
          }
        }
      }
    }
    '''
    variables = {       # 'page' will be incremented in a for loop
        'eventId': bracketID,
        'perPage': pageCounts[2]
    }
    ids = dict()

    for i in range(pageCounts[0]):
        variables['page'] = (i + 1)     # loops through pages to bypass 1000
                                        # objects per request limit
        playersList = CTD.run_query(query, variables)
        for player in playersList['data']['event']['standings']['nodes']:
            ids[player['entrant']['participants'][0]['player']['id']] = player['entrant']['name']
    return ids


def getIDs(slug: str) -> {int: str}:
    """It finds the SmasherIDs of all the players who made it into final bracket.
    It returns a dictionary with the keys being the SmasherID and
    the value being their tag"""
    info = CTD.get_event_info(slug)
    bracketID = info['Bracket']
    pageCounts = CTD.get_page_counts(bracketID)
    return getPlayers(bracketID, pageCounts)


def outputPlayers(ids: {int: str}, season: int, week: int) -> None:
    """It will output a player's tag, their rank, and if they entered TMT
    that week. Also add the players for the top 10 in case they
    enter last minute."""
    RankRecords = f'Data/Season{season}/Records/S{season}W{week - 1}RankRecords.csv'
    RankRecords = pd.read_csv(RankRecords, encoding = "ISO-8859-1")
    RankRecords = RankRecords.sort_values(by = f'RWeek{week - 1}')

    df = pd.DataFrame()
    columns_names = ['Rank', 'SmasherID', 'SmashTag', 'EnteredTMT']
    for SmasherID, SmashTag in ids.items():
        oldPlayer = RankRecords[RankRecords['SmasherID'].isin([SmasherID])]
        if len(oldPlayer) > 0:  # Returning Player
            index = oldPlayer.index[0]
            rank = RankRecords.at[index, f'RWeek{week - 1}']
        else:
            rank = np.nan
        new_row = {'Rank': rank,
                   'SmasherID': SmasherID,
                   'SmashTag': SmashTag,
                   'EnteredTMT': 1}
        df = df.append(new_row, ignore_index = True)

    for index, row in RankRecords.iterrows():
        if row['SmasherID'] not in ids:
            new_row = {'Rank': row[f'RWeek{week - 1}'],
                       'SmasherID': row['SmasherID'],
                       'SmashTag': row['SmashTag'],
                       'EnteredTMT': 0}
            df = df.append(new_row, ignore_index = True)

        if row[f'RWeek{week - 1}'] >= 10:
            break
    
    df = df[['Rank', 'SmashTag', 'EnteredTMT']]
    df = df.sort_values(by = 'Rank')
    df['Rank'] = df['Rank'].fillna('NA')
    
    RanksBracket = f'Data/Season{season}/Debug/S{season}W{week}RanksforBracket.csv'
    df.to_csv(RanksBracket, index=False, encoding = "ISO-8859-1")


def main():
    season = UI.UserSeason()
    week = UI.UserWeek()
    slug = UI.UserSlug()
    #season = 1
    #week = 8
    #slug = 'training-mode-tournaments-8'
    ids = getIDs(slug)
    outputPlayers(ids, season, week)
    

main()

