import json
import requests

# This is FTSTimSin's API key
HEADERS = {'Authorization': 'Bearer bbc80775130117d4ecb1b0eedc00db7d'}

# Sends the request to the API given the query and variables. Returns the json
def run_query(query, variables):
    request = requests.post('https://api.smash.gg/gql/alpha',
                            json={'query': query, 'variables': variables},
                            headers=HEADERS)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}"
                        .format(request.status_code, query))


# Gets page counts for both the number of valid players (1st item in the list)
# and sets (2nd item in the list) depending on the number of items per page.
def get_page_counts(eventId, perPage=100):
    query = '''
    query PageCounts($eventId: ID!, $perPage: Int!) {
      event(id: $eventId) {
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
    }'''
    variables = {
        'eventId': eventId,
        'perPage': perPage
    }
    result = run_query(query, variables)
    return [result['data']['event']['standings']['pageInfo']['totalPages'],
            result['data']['event']['sets']['pageInfo']['totalPages']]


# Returns a dict {player ID: [player name, placement, wins, losses]}
def get_event_standings(eventId, pageCounts, perPage=100):
    query = '''
    query EventStandings($eventId: ID!, $page: Int!, $perPage: Int!) {
      event(id: $eventId) {
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
            }
          }
        }
      }
    }'''
    variables = {
        'eventId': eventId,
        'perPage': perPage
    }
    standings = dict()

    # Loops 'pageCount' amount of times to ensure that all players are looped
    # through, not just the top ones.
    for i in range(pageCounts[0]):
        variables['page'] = (i + 1)
        playersList = run_query(query, variables)
        for player in playersList['data']['event']['standings']['nodes']:
            standings[player['entrant']['id']] = [player['entrant']['name'],
                                                  player['placement'], 0, 0]

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
    }'''

    # Loops 'pageCount' amount of times to ensure that all sets are looped
    # through, not just the top ones.
    for i in range(pageCounts[1]):
        variables['page'] = (i + 1)
        playersList = run_query(query, variables)
        for player in playersList['data']['event']['sets']['nodes']:
            winner = player['winnerId']
            entrants = [player['slots'][0]['entrant']['id'],
                        player['slots'][1]['entrant']['id']]
            if entrants[0] == winner:
                loser = entrants[1]
            else:
                loser = entrants[0]
            standings[winner][2] += 1
            standings[loser][3] += 1
    return standings


# Return a string of 0s and 1s that determine what tier a player is in by
# where the 1 is.
def get_tier(placement, pro, rookie):
    if placement <= pro:
        return '0\t0\t1'
    elif placement <= rookie:
        return '0\t1\t0'
    else:
        return '1\t0\t0'


if __name__ == '__main__':
    # 528834
    eventId = input('Enter the eventId: ')
    ladder = input('Is this a ladder event? (Y) or (N): ').upper()
    if ladder == 'Y':
        l = True
    elif ladder == 'N':
        l = False
    else:
        print('Not a valid response')
        quit()

    if l:
        pro = int(input(
            'Input the lowest placement with the Pro Rank (Roughly): '))
        rookie = int(input(
            'Input the lowest placement with the Rookie Rank (Roughly): '))

    pageCounts = get_page_counts(eventId)
    standings = (get_event_standings(eventId, pageCounts))
    f = open('WeeklyScoreLadderN.txt', 'w')
    f.write('SmasherID\tSmashTag\tWins\tLosses\t')
    if l:
        f.write('Prospect\tRookie\tPro\t')
    f.write('Placement\n')

    for key, element in standings.items():
        f.write(str(key) + '\t' +
                str(element[0]) + '\t' +
                str(element[2]) + '\t' +
                str(element[3]) + '\t')
        if l:
            f.write(get_tier(element[1], pro, rookie) + '\t')
        f.write(str(element[1]) + '\n')
