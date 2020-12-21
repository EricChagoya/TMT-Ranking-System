import pandas as pd
import CollectTourneyData as CTData

# The smash.gg API has 2 rate limits:
# 80 requests per minute
# 1000 objects per request
# At the top of each query, the number of objects per query will be shown in a
# comment (only an estimation).


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


def CombineSetData(info: {str: int}, week: int) -> None:
    data = []
    count = 0
    for eventName, eventId in info.items():
        pageCounts = CTData.get_page_counts(eventId)
        data.append(getPlayerSets(eventId, pageCounts))
        if count >= 2:
            break
        count += 1
    
    master = dict()
    allPlayers = data[0].keys() | data[1].keys()
    #allPlayers = data[0].keys() | data[1].keys() | data[2].keys()

    for player in allPlayers:
        wins = []
        losses = []
        for event in data:
            if player in event:
                wins += event[player][0]
                losses += event[player][1]
        master[player] = [wins, losses]
    SetDataToJSON(master, week)

def SetDataToJSON(players:{'SmasherID': [['WinsID'], ['LossesID']]}, week: int) -> None:
    """It will append this week's data with the previous. """
    if week == 6:   # Change it back to 1
        pass
        return
    pass






def main():
    # ask for week and season
    #slug = input('Please input the smash.gg tournament slug: ')
    week = 6
    slug = 'training-mode-tournaments-6'
    info = CTData.get_event_info(slug)
    CombineSetData(info, week)

    # 3 output files
    # Sets with SmasherID
    # Sets with SmashTag
    # Dijkstra's Algorithm




main()

