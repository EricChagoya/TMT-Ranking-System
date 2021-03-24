import requests
import json
#pip install requests

# The smash.gg API has 2 rate limits:
# 80 requests per minute
# 1000 objects per request
# At the top of each query, the number of objects per query will be shown in a
# comment (only an estimation).


# FTSTimSin's API Key
HEADERS = {'Authorization': 'Bearer bbc80775130117d4ecb1b0eedc00db7d'}

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
        if 'East' in event['name']:
            info['East'] = event['id']
            print('East Coast Ladder Found!:', event['name'])
        elif 'West' in event['name']:
            info['West'] = event['id']
            print('West Coast Ladder Found!:', event['name'])
        elif 'Main' in event['name']:
            info['Bracket'] = event['id']
            print('Main Bracket Found!:', event['name'])
        else:
            print('UNKNOWN EVENT:', event['name'])
    return info


def get_page_counts(eventId: int, perPage: int = 100) -> (int, int):
    """Gets page counts for both the number of valid players (1st item in the
    tuple) and sets (2nd item in the tuple) depending on the number of items
    per page. The 3rd item of the tuple is the number of items per page
    (perPage)."""
    # ESTIMATED NUMBER OF OBJECTS OBTAINED PER QUERY: 3
    query = '''
    query PageCounts($eventId: ID!, $perPage: Int!){
      event(id: $eventId){
        id
        name
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

    return (result['data']['event']['sets']['pageInfo']['totalPages'], perPage)


def get_event_sets(eventId: int, pageCounts: (int, int),
                   countDQ: bool = false) -> {int: ([str], [str])}:
    # ESTIMATED NUMBER OF OBJECTS OBTAINED PER QUERY: 502 at most
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
    variables = {  # 'page' will be incremented in a for loop
        'eventId': eventId,
        'perPage': pageCounts[1]
    }

    stats = dict()

    for i in range(pageCounts[0]):
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
            loserScore = player['slots'][1]['standing']['stats']['score']
            ['value']
        else:
            loser = entrants[0]
            loserScore = player['slots'][0]['standing']['stats']['score']
            ['value']

        if (countDQ or loserScore != -1):
            if winner in stats:
                   stats[winner][0].append(loser)
            else:
                stats[winner] = ([loser], [])
            if loser in stats:
                stats[loser][1].append(winner)
            else:
                stats[loser] = ([], [winner])

    return stats


if __name__ == '__main__':
    week = input('Please input the week number: ')

    jsonThisWeek = f'S1W{week}SetData.json'
    jsonPastWeek = f'S1W{week - 1}SetData.json'

    slug = input('Please input the smash.gg tournament slug: ')
    print()
    info = get_event_info(slug)
    print()

    if week == 1:
        data = dict()
    else:
        with open(jsonPastWeek) as json_file:
            data = json.load(json_file)

    for eventName, eventId in info.items():
        pageCounts = get_page_counts(eventId)
        stats = get_event_stats(eventId, pageCounts, false)

        for playerId, listTuple in stats.items():
            if playerId in data:
                data[playerId]
                # never mind

