import os
import requests
import UserInterface as UI
#pip install requests

# The smash.gg API has 2 rate limits:
# 80 requests per minute
# 1000 objects per request
# At the top of each query, the number of objects per query will be shown in a
# comment (only an estimation).


# FTSTimSin's API Key
HEADERS = {'Authorization': 'Bearer bbc80775130117d4ecb1b0eedc00db7d'}

def CreateDirectories(season: int, week: int) -> None:
    """It will create a directory for a new season"""
    if week == 1:
        if not os.path.exists('Data'):
            os.mkdir('Data')
        if not os.path.exists(f'Data/Season{season}'):
            os.mkdir(f'Data/Season{season}')
            os.mkdir(f'Data/Season{season}/WeeklyLadderBracket')



def run_query(query: str, variables: {str, int or str}) -> dict:
    """Sends the request to the API given the query and variables. Returns the
    json response. If there is a problem, it raises an exception"""
    request = requests.post('https://api.smash.gg/gql/alpha',
                            json={'query': query, 'variables': variables},
                            headers=HEADERS)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}"
                        .format(request.status_code, query))


def get_event_info(slug: str) -> {str: int}:
    """Gets the id and name of all events in the tournament (given the smash.gg
    slug, and returns a dict with either 'East', 'West', or 'Bracket'
    (depending on which event), as the key and the eventID as the value. Prints
    information so the user can see what events are going to be returned."""
    # ESTIMATED NUMBER OF OBJECTS OBTAINED PER QUERY: 6
    query = '''
    query GetEventInfo($tourneySlug: String!){
      tournament(slug: $tourneySlug){
        events{
          id
          name
        }
      }
    }
    '''
    variables = {'tourneySlug': slug}
    result = run_query(query, variables)

    info = dict()
    for event in result['data']['tournament']['events']:
        if 'Melee Ladder East Coast' in event['name']:
            info['East'] = event['id']
            #print('East Coast Ladder Found!:', event['name'])
        elif 'Melee Ladder West Coast' in event['name']:
            info['West'] = event['id']
            #print('West Coast Ladder Found!:', event['name'])
        elif 'Melee Singles Main Bracket' in event['name']:
            info['Bracket'] = event['id']
            #print('Main Bracket Found!:', event['name'])
        else:
            pass
            #print('UNKNOWN EVENT:', event['name'])
    return info


def get_page_counts(eventId: int, perPage: int = 100) -> (int, int, int):
    """Gets page counts for both the number of valid players (1st item in the
    tuple) and sets (2nd item in the tuple) depending on the number of items
    per page. The 3rd item of the tuple is the number of items per page
    (perPage)."""
    # ESTIMATED NUMBER OF OBJECTS OBTAINED PER QUERY: 4
    query = '''
    query PageCounts($eventId: ID!, $perPage: Int!){
      event(id: $eventId){
        id
        name
        standings(query:{
          perPage: $perPage
        }){
          pageInfo{
            totalPages
          }
        }
        sets(perPage: $perPage){
          pageInfo{
            totalPages
          }
        }
      }
    }
    '''
    variables = { 'eventId': eventId, 'perPage': perPage}
    result = run_query(query, variables)

    return (result['data']['event']['standings']['pageInfo']['totalPages'],
            result['data']['event']['sets']['pageInfo']['totalPages'],
            perPage)


def get_event_stats(eventId: int, pageCounts: (int, int, int)) -> \
        {int: (str, int, int, int)}:
    """Gets the standings of all players in the event and information on every
    set played in the event and returns a dict in this format:
    {playerId (NOT entrantId): (gamertag, wins, losses, placement)}"""

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
        playersList = run_query(query, variables)
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
          sortType: RECENT
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

    for i in range(pageCounts[1]):
        variables['page'] = (i + 1)     # loops through pages to bypass 1000
                                        # objects per request limit
        playersList = run_query(query, variables)
        for player in playersList['data']['event']['sets']['nodes']:
            # Determines the entrantId of the winner and loser
            winner = player['winnerId']
            entrants = [player['slots'][0]['entrant']['id'],
                        player['slots'][1]['entrant']['id']]
            if entrants[0] == winner:
                loser = entrants[1]
            else:
                loser = entrants[0]
            try:
                stats[winner][2] += 1
                stats[loser][3] += 1
            except KeyError:
                pass

    playerIdDict = dict()
    for player in stats.values():
        playerIdDict[player[4]] = (player[0], player[2], player[3], player[1])

    return playerIdDict


def get_tier(placement, hof, allstar, pro, rookie):
    """Return a string of 0s and 1s that determine what tier a player is in by
    where the 1 is."""
    if placement <= hof:
        return '0,0,0,0,1,'
    elif placement <= allstar:
        return '0,0,0,1,0,'
    elif placement <= pro:
        return '0,0,1,0,0,'
    elif placement <= rookie:
        return '0,1,0,0,0,'
    else:
        return '1,0,0,0,0,'


if __name__ == '__main__':
    season = UI.UserSeason()
    week = UI.UserWeek()

    CreateDirectories(int(season), int(week))
    ladderLink = f'Data/Season{season}/WeeklyLadderBracket/S{season}W{week}WeeklyScoresLadder.csv'
    bracketLink = f'Data/Season{season}/WeeklyLadderBracket/S{season}W{week}WeeklyScoresBracket.csv'

    

    slug = UI.UserSlug()
    print()
    info = get_event_info(slug)
    print()

    choice = UI.PrintCTDOptions()

    if choice != 2:
        print()
        hofE = int(input(
            'Input the lowest placement in East Coast Ladder with the Hall of Fame Rank (0 if NA): '))
        allstarE = int(input(
            'Input the lowest placement in East Coast Ladder with the All-Star Rank (Roughly): '))
        proE = int(input(
            'Input the lowest placement in East Coast Ladder with the Pro Rank (Roughly): '))
        rookieE = int(input(
            'Input the lowest placement in East Coast Ladder with the Rookie Rank (Roughly): '))

        print()
        hofW = int(input(
            'Input the lowest placement in West Coast Ladder with the Hall of Fame Rank (0 if NA): '))
        allstarW = int(input(
            'Input the lowest placement in West Coast Ladder with the All-Star Rank (Roughly): '))
        proW = int(input(
            'Input the lowest placement in West Coast Ladder with the Pro Rank (Roughly): '))
        rookieW = int(input(
            'Input the lowest placement in West Coast Ladder with the Rookie Rank (Roughly): '))

    print()
    ladderFile = open(ladderLink, 'w', encoding='utf-8')
    ladderFile.write('SmasherID,SmashTag,Wins,Losses,'
                     'Prospect,Rookie,Pro,AllStar,HallOfFame,Placement,Coast\n')
    for eventName, eventId in info.items():
        if eventName in {'East', 'West'} and choice in (1, 3):
            pageCounts = get_page_counts(eventId)
            stats = get_event_stats(eventId, pageCounts)
            for playerId, value in stats.items():
                ladderFile.write(str(playerId) + ',')
                ladderFile.write(value[0] + ',')
                ladderFile.write(str(value[1]) + ',')
                ladderFile.write(str(value[2]) + ',')
                if eventName == 'East':
                    ladderFile.write(
                        get_tier(value[3], hofE, allstarE, proE, rookieE))
                    ladderFile.write(str(value[3]) +',' + 'EC')
                else:
                    ladderFile.write(
                        get_tier(value[3], hofW, allstarW, proW, rookieW))
                    ladderFile.write(str(value[3]) + ',' + 'WC')

                ladderFile.write('\n')
            print(f'Inputted {eventName} Coast Ladder results to {ladderLink}')
        elif eventName == 'Bracket' and choice in (2, 3):
            pageCounts = get_page_counts(eventId)
            stats = get_event_stats(eventId, pageCounts)
            bracketFile = open(bracketLink, 'w', encoding='utf-8')
            bracketFile.write('SmasherID,SmashTag,Wins,Losses,Placement\n')
            for playerId, value in stats.items():
                bracketFile.write(str(playerId) + ',')
                bracketFile.write(value[0] + ',')
                bracketFile.write(str(value[1]) + ',')
                bracketFile.write(str(value[2]) + ',')
                bracketFile.write(str(value[3]) + '\n')
            bracketFile.close()
            print(f'Inputted Main Bracket results to {bracketLink}')

    ladderFile.close()
