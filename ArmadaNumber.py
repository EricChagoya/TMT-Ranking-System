import os
import json
import pandas as pd
import CollectTourneyData as CTData

# The smash.gg API has 2 rate limits:
# 80 requests per minute
# 1000 objects per request
# At the top of each query, the number of objects per query will be shown in a
# comment (only an estimation).


def CreateDirectories(season: int) -> None:
    """If these directories don't exists, it will create them"""
    if not os.path.exists(f'Data/Season{season}/ArmadaNumber'):
        os.mkdir(f'Data/Season{season}/ArmadaNumber')


def getPlayerSets(eventId: int, pageCounts: (int, int, int)) -> {int: [[int], [int]]}:
    """Gets data on who every player beat and lost to for this event.
    {'SmasherID': [['WinsID'], ['LossesID']]}"""

    # entrantId != playerId. entrantId is the ID of the player for a specific
    # event (a player's entrantId changes per event). A playerId is constant
    # for that particular player.

    # ESTIMATED NUMBER OF OBJECTS OBTAINED PER QUERY: 402 at most
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
            placement
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
        'eventId': eventId,
        'perPage': pageCounts[2]
    }

    # This dict is not the same dict that is returned. This dict is:
    # {entrantId: [gamertag, placement, wins, losses, playerID]}
    stats = dict()

    for i in range(pageCounts[0]):
        variables['page'] = (i + 1)     # loops through pages to bypass 1000
                                        # objects per request limit
        playersList = CTData.run_query(query, variables)
        for player in playersList['data']['event']['standings']['nodes']:
            stats[player['entrant']['id']] = [
                player['entrant']['name'], player['placement'], 0, 0,
                player['entrant']['participants'][0]['player']['id']
            ]
            
    # ESTIMATED NUMBER OF OBJECTS OBTAINED PER QUERY: 302 at most
    query = '''
    query EventSets($eventId: ID!, $page: Int!, $perPage: Int!) {
      event(id: $eventId) {
        id
        name
        sets(
          page: $page
          perPage: $perPage
          sortType: STANDARD
        ) {
          nodes {
            winnerId
            slots{
              entrant{
                id
              }
            }
          }
        }
      }
    }
    '''

    playerSets = dict()     # {'playerID': [[WinsID], [LossesID]]}

    for i in range(pageCounts[1]):
        variables['page'] = (i + 1)     # loops through pages to bypass 1000
                                        # objects per request limit
        playersList = CTData.run_query(query, variables)
        for player in playersList['data']['event']['sets']['nodes']:
            winner = player['winnerId']
            entrants = [player['slots'][0]['entrant']['id'],
                        player['slots'][1]['entrant']['id']]
            if entrants[0] == winner:
                loser = entrants[1]
            else:
                loser = entrants[0]

            winner = stats[winner][-1]
            loser = stats[loser][-1]
            if winner not in playerSets:
                playerSets[winner] = [[], []]
            if loser not in playerSets:
                playerSets[loser] = [[], []]

            playerSets[winner][0].append(loser)
            playerSets[loser][1].append(winner)
    return playerSets


def CombineSetData(info: {str: int}, season: int, week: int) -> None:
    """It combines the sets from ladder and final bracket."""
    data = []
    for eventName, eventId in info.items():
        pageCounts = CTData.get_page_counts(eventId)
        data.append(getPlayerSets(eventId, pageCounts))    
    master = dict()
    #allPlayers = data[0].keys() | data[1].keys()
    allPlayers = data[0].keys() | data[1].keys() | data[2].keys()

    for player in allPlayers:
        wins = []
        losses = []
        for event in data:
            if player in event:
                wins += event[player][0]
                losses += event[player][1]
        master[player] = [wins, losses]
    weeklySets = SetWeeklyDataToJSON(master, week)
    CombinePreviousSets(weeklySets, season, week)
    

def SetWeeklyDataToJSON(players:{'SmasherID': [['WinsID'], ['LossesID']]}, week: int) -> None:
    """It will convert this week's sets into JSON."""
    playersJSON = []
    for SmasherID, playerSets in players.items():
        wins = dict()
        for winID in playerSets[0]:
            if winID not in wins:
                wins[winID] = [week]
            else:
                wins[winID].append(week)
        losses = dict()
        for lossesID in playerSets[1]:
            if lossesID not in losses:
                losses[lossesID] = [week]
            else:
                losses[lossesID].append(week)

        player= dict()
        player['SmasherID'] = SmasherID
        player['WinningSets'] = wins
        player['LosingSets'] = losses
        playersJSON.append(player)
    return json.dumps(playersJSON, indent = 2)
    

def CombinePreviousSets(weeklySets: json, season: int, week: int) -> None:
    """It will combine previous's sets with the current week."""
    previousSets = f'Data/Season{season}/ArmadaNumber/S{season}W{week - 1}PlayerSets.json'
    newSets = f'Data/Season{season}/ArmadaNumber/S{season}W{week}PlayerSets.json'
    
    temp = f'Data/Season{season}/ArmadaNumber/tempPlayerSets.json'
    if week == 1:
        with open(newSets, "w") as outfile: 
            outfile.write(weeklySets)
            return

    with open(temp, "w") as outfile:    # Change this later
        outfile.write(weeklySets)
    with open(previousSets, "r") as f1:
        previousSets = json.load(f1)
    with open(temp, "r") as f2:
        updatedSets = json.load(f2)

    allPlayers = dict()
    for player in previousSets:
        allPlayers[player['SmasherID']] = [player['WinningSets'], player['LosingSets']]

    total = []
    for player in updatedSets:
        if player['SmasherID'] not in allPlayers:   # New Player
            allPlayers[player['SmasherID']] = [player['WinningSets'], player['LosingSets']]
            
        else:       # Returning Player
            for recentWinsID, times in player['WinningSets'].items():
                # The winner has never beaten this person before
                if recentWinsID not in allPlayers[player['SmasherID']][0]:
                    allPlayers[player['SmasherID']][0][recentWinsID] = times
                else:
                    # This player has beaten this player before
                    allPlayers[player['SmasherID']][0][recentWinsID] += times
            for recentLossID, times in player['LosingSets'].items():
                # The player has never lost to this person before
                if recentLossID not in allPlayers[player['SmasherID']][1]:
                    allPlayers[player['SmasherID']][1][recentLossID] = times
                else:
                    # This player has lost to this player already
                    allPlayers[player['SmasherID']][1][recentLossID] += times
                    
        temp= {'SmasherID': player['SmasherID'],
               'WinningSets': allPlayers[player['SmasherID']][0],
               'LosingSets': allPlayers[player['SmasherID']][1]}
        total.append(temp)
        
    with open(newSets, "w") as outfile:
        jsonPlayer = json.dumps(total, indent = 2)
        outfile.write(jsonPlayer)



def main():
    # ask for week and season
    #slug = input('Please input the smash.gg tournament slug: ')
    season = 1
    week = 6
    #slug = 'tournament/training-mode-tournaments-2-100-pot-bonus'
    slug = 'training-mode-tournaments-6'
    CreateDirectories(season)
    info = CTData.get_event_info(slug)
    CombineSetData(info, season, week)

    # 3 output files
    # Cummulative Sets with SmasherID
    # Cummulative Sets with SmashTag    # Just for fast checking
    # Dijkstra's Algorithm



main()

