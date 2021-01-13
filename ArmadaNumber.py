import os
import json
import pandas as pd
import UserInterface as UI
import CollectTourneyData as CTData

# The smash.gg API has 2 rate limits:
# 80 requests per minute
# 1000 objects per request3
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

    # ESTIMATED NUMBER OF OBJECTS OBTAINED PER QUERY: ???
    query = '''
    query EventSets($eventId: ID!, $page: Int!, $perPage: Int!) {
          event(id: $eventId) {
            id
            name
            sets(
              page: $page
              perPage: $perPage
              sortType: RECENT
            ) {
              nodes {
                winnerId
                slots{
                  entrant{
                    id
                    name
                  }
                  standing{
                    stats{
                      score{
                        value
                      }
                    }
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

            # get winner, loser, and loser's score
            if entrants[0] == winner:
                loser = entrants[1]
            else:
                loser = entrants[0]
            loserScore = min(player['slots'][0]['standing']['stats']['score']
                ['value'], player['slots'][1]['standing']['stats']['score']
                ['value'])

            if (loserScore != -1):      # only add set if it is not a DQ
                winner = stats[winner][-1]
                loser = stats[loser][-1]
                if winner not in playerSets:
                    playerSets[winner] = [[], []]
                if loser not in playerSets:
                    playerSets[loser] = [[], []]

                playerSets[winner][0].append(loser)
                playerSets[loser][1].append(winner)
            else:
                print(f"DQ Found! {player['slots'][0]['entrant']['name']} vs. {player['slots'][1]['entrant']['name']} not added.")
    return playerSets


def getPlayerTags() -> {int: str}:
    """It gets the tag of every player with SmasherID as the key and the tag as a value"""
    Mains = f'Data/PlayerMains.csv'
    Mains = pd.read_csv(Mains, encoding = 'utf-8-sig')
    return {int(row['SmasherID']):row['SmashTag'] for _, row in Mains.iterrows()}


def findBestRankedPlayer(season, week) -> str and int:
    """Find who is ranked number one for the whole season"""
    Rank = f'Data/Season{season}/Records/S{season}W{week}RankRecords.csv'
    Rank = pd.read_csv(Rank, encoding = 'ISO-8859-1')
    for index, row in Rank.iterrows():
        if row[f'RWeek{week}'] == 1:
            return row['SmashTag'], row['SmasherID']


def CombineSetData(info: {str: int}, season: int, week: int) -> None:
    """It combines the sets from ladder and final bracket."""
    data = []
    for eventName, eventId in info.items():
        pageCounts = CTData.get_page_counts(eventId, 50)    # halved the number of items per page from normal to handle the extra query code that checks DQs
        data.append(getPlayerSets(eventId, pageCounts))    
    master = dict()
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
    """It will combine last week's cummulative sets with the current week."""
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
    total = []
    t= set()
    for player in previousSets:
        allPlayers[player['SmasherID']] = [player['WinningSets'], player['LosingSets']]
        t.add(player['SmasherID'])
    
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
            t.remove(player['SmasherID'])
                    
        temp= {'SmasherID': player['SmasherID'],
               'WinningSets': allPlayers[player['SmasherID']][0],
               'LosingSets': allPlayers[player['SmasherID']][1]}
        total.append(temp)
    for SmasherID in t:
        sets= allPlayers[SmasherID]
        temp= {'SmasherID': SmasherID,
               'WinningSets': sets[0],
               'LosingSets': sets[1]}
        total.append(temp)
    
    with open(newSets, "w") as outfile:
        jsonPlayer = json.dumps(total, indent = 2)
        outfile.write(jsonPlayer)


def SetDataWithSmashTag(season: int, week: int) -> None:
    """Make a Json file that is more readable for humans. It will now include
    a Smasher's Tag for the player and for each of their wins and losses.
    Mostly used for debugging purposes."""
    playerMains = getPlayerTags()
    playerSets = f'Data/Season{season}/ArmadaNumber/S{season}W{week}PlayerSets.json'
    with open(playerSets, "r") as file:
        playerSets = json.load(file)

    total = []
    for player in playerSets:
        wins = dict()
        for winsID, record in player['WinningSets'].items():
            wins[playerMains[int(winsID)]] = record
            
        losses = dict()
        for lossesID, record in player['LosingSets'].items():
            losses[playerMains[int(lossesID)]] = record

        SmashTagSets = {'SmashTag': playerMains[player['SmasherID']],
                        'SmasherID': player['SmasherID'],
                        'WinningSets': wins,
                        'LosingSets': losses}
        total.append(SmashTagSets)
    
    playerSetsTags = f'Data/Season{season}/ArmadaNumber/S{season}W{week}PlayerSetsTags.json'
    with open(playerSetsTags, "w") as outfile:
        jsonPlayer = json.dumps(total, indent = 2)
        outfile.write(jsonPlayer)


def getPlayerLosses(season: int, week: int) -> {'SmasherID': {'WinsID'}}:
    """Find out everybody's wins. The key being the player and the value being
    a set of the player ids of the people they beat."""
    playerSets = f'Data/Season{season}/ArmadaNumber/S{season}W{week}PlayerSets.json'
    with open(playerSets, "r") as file:
        playerSets = json.load(file)

    return {player['SmasherID']: {int(lossesID) for lossesID in player['LosingSets']} for player in playerSets}


def DijkstraTable(graphLosses: {int: {int}}, Armada: int) -> \
                    {'SmasherID': {'inTree': bool, 'parent': 'SmasherID', 'distance': int}}:
    """It will create the preliminary table for Dijkstra's Algorithm.
    inTree means whether we have "taken" that value.
    parent is the player that they they lost to.
    Distance will be infinity."""
    inTree = dict()
    parent = dict()
    distance = dict()
    for player in graphLosses.keys():
        inTree[player] = False
        parent[player] = ""
        distance[player] = float('inf')
    distance[Armada] = 0
    return inTree, parent, distance
    

def ShortestPath(graphLosses: {int: {int}}, Armada: int) -> {int:int}:
    """It tries to find the smallest Armada number for each player by naming
    the person who they beat.
    Parent = {Player: PlayerTheyBeat}
    Distance = {Player: ArmadaNumber}
    """
    inTree, parent, distance = DijkstraTable(graphLosses, Armada)
    playersLeft = {k:v for k, v in distance.items()}    # Players that not yet been choosen

    while True:
        # Determine next player arbitrarily
        nextPlayer = min(playersLeft, key = playersLeft.get)
        if playersLeft[nextPlayer] == float('inf'):
            break
        del playersLeft[nextPlayer]
        inTree[nextPlayer] = True
        
        for playerLosses in graphLosses[nextPlayer]:
            if (distance[nextPlayer] + 1) < distance[playerLosses]:
                distance[playerLosses] = distance[nextPlayer] + 1
                playersLeft[playerLosses] = distance[playerLosses]
                parent[playerLosses] = nextPlayer
    return parent, distance


def CompletePath(shortestPath: {int: int}, distance: {int: int}, Armada: int) -> None:
    """Input is the shortest Path. Now we want to know from any player, the exact
    path to reach Armada with the fewest amount of players. """
    fullPath = {Armada: []}
    del distance[Armada]

    for player, d in sorted(distance.items(), key = (lambda x: x[1]) ):
        if d == float('inf'):
            fullPath[player] = ['NA']
        else:
            fullPath[player] = fullPath[shortestPath[player]] + [shortestPath[player]]

    IdTags = getPlayerTags()
    data= {f'{IdTags[Armada]} Number': [0],
           'SmashTag': [str(IdTags[Armada])],
           'Path': ['']}
    df = pd.DataFrame(data)

    for player, d in sorted(distance.items(), key = (lambda x: x[1]) ):
        if fullPath[player] == ['NA']:
            path = 'NA'
            d = 'NA'
        else:
            path = f'{IdTags[Armada]}'
            for p in fullPath[player][1:]:
                path += f' < {IdTags[p]}'
        
        new_row = {f'{IdTags[Armada]} Number': d,
                   'SmashTag': IdTags[player],
                   'Path': path}
        df = df.append(new_row, ignore_index = True)
    return df[['SmashTag', f'{IdTags[Armada]} Number', 'Path']]


def ArmadaSolver(Armada: int, season: int, week: int):
    """It will find the shortest number of wins required to get to Armada
    for each player."""
    graphLosses = getPlayerLosses(season, week)
    shortestPath, distance = ShortestPath(graphLosses, Armada)
    df = CompletePath(shortestPath, distance, Armada)
    armadaNumber = f'Data/Season{season}/ArmadaNumber/S{season}W{week}ArmadaNumber.csv'
    df.to_csv(armadaNumber, index = False, encoding = 'ISO-8859-1')


def main():
    UI.PrintArmadaNumberWelcomeMessage()
    choice = UI.ArmadaGeneralOption()
    season = UI.UserSeason()
    week = UI.UserWeek()
    #choice = 2
    #season = 1
    #week = 6
    CreateDirectories(season)

    if choice == 1:         # Collect Player Set from Smash.gg
        slug = UI.UserSlug()
        #slug = 'training-mode-tournaments-6'
        info = CTData.get_event_info(slug)
        CombineSetData(info, season, week)
        SetDataWithSmashTag(season, week)
        
    elif choice == 2:       # Find Armada Number
        SmashTag, SmasherID = findBestRankedPlayer(season, week)
        Armada = UI.findArmada(SmashTag, SmasherID)
        ArmadaSolver(Armada, season, week)
        
    else:       # Collect Player Sets and Find Armada Number
        slug = UI.UserSlug()
        info = CTData.get_event_info(slug)
        CombineSetData(info, season, week)
        SetDataWithSmashTag(season, week)
        
        SmashTag, SmasherID = findBestRankedPlayer(season, week)
        Armada = UI.findArmada(SmashTag, SmasherID)
        ArmadaSolver(Armada, season, week)
    

main()
