import os
import math
import numpy as np
import pandas as pd
import UserInterface as UI

import plotly.graph_objects as go
import plotly.express as px

# pip install plotly
# https://plotly.com/python/
# Really good documentation
# pip install -U kaleido
# Used for saving static images

FORMAT = 0  # 0 is an iteractable HTML
            # 1 is a png

CHARACTERS = {'Fox': 0,
              'Falco' : 1,
              'Marth': 2,
              'Sheik': 3,
              'Falcon': 4,
              'Puff': 5,
              'Peach': 6,
              'Pikachu' : 7,
              'Ganon': 8,
              'unknown': 9}

# Change these colors later
COLORS = ['#ffc34d', '#0000ff', '#1aff1a', '#ff1a1a', '#4d4d4d',
          '#6600cc', '#ff66ff', '#ffff00', '#000000', '#666699']
#        [Yellow/Orange, Blue, Lime Green, Red, Dark Gray,
#         Purple, Pink, Yellow, Black, Gray]

# Colors should be based off player's main


def SavingFormat(choice: int) -> None:
    """Changes a global variable so all graphs are put into HTML
    or into a png file"""
    global FORMAT
    if choice == 1: 
        FORMAT = 0  # HTML Version
    else:
        FORMAT = 1  # png Version
        if not os.path.exists("Plots"):
            os.mkdir("Plots")


def getPlayerMains() -> {'Main': 'Tag'}:
    """This will return a ditionary with the Character being the key and
    the values will be a set of players."""
    Mains = 'Records/PlayerMains.csv'
    Mains = pd.read_csv(Mains, encoding='utf-8-sig')    # Not sure why ISO encoding doesn't work    
    AllPlayerMains = dict()
    for index, row in Mains.iterrows():
        if row['Main'] in AllPlayerMains:
            AllPlayerMains[row['Main']].add(row['SmashTag'])
        else:
            AllPlayerMains[row['Main']] = {row['SmashTag']}
    return AllPlayerMains


def getMainsOfPlayer() -> {'Tag': 'Main'}:
    """We will return a dictionary with the key being the Tag and
    the value will be their main character."""
    Mains = 'Records/PlayerMains.csv'
    Mains = pd.read_csv(Mains, encoding='utf-8-sig')    # Not sure why ISO encoding doesn't work    
    PlayerMains = dict()
    for index, row in Mains.iterrows():
        PlayerMains[row['SmashTag']] = row['Main']
    return PlayerMains
    

def getCoastData(season: int, week: int) -> 'df':
    """Get the total number of combined, West Coast, and East Coast entrants
    for each week. The last column is for people we aren't sure of.
    [Total, WC, EC, NA]"""
    Features = f'Records/S{season}W{week}Features.csv'
    Features = pd.read_csv(Features, encoding = "ISO-8859-1")
    Placements = f'Records/S{season}W{week}Placements.csv'
    Placements = pd.read_csv(Placements, encoding = "ISO-8859-1")
    coasts= dict()
    for index, row in Features.iterrows():
        if row['Coast'] == "WC":
            region = 1
        elif row['Coast'] == "EC":
            region = 2
        else:
            region = 3
        coasts[row['SmasherID']] = region

    count = {i: [0, 0, 0, 0] for i in range(1, week + 1)}
    for _, row in Placements.iterrows():
        region = coasts[row['SmasherID']]
        placed = [row[f'PWeek{i}'] for i in range(1, week + 1)]
        attended = [i > -2 for i in placed]
        for index, i in enumerate(attended):
            count[index + 1][0] += i        # Update Tournament Entrant Count
            count[index + 1][region] += i   # Update Entrant Count for their region
    df = pd.DataFrame.from_dict(count, orient ='index')
    column_names = {0: 'Total',
                    1: 'West Coast',
                    2: 'East Coast',
                    3: 'NA'}
    df = df.rename(columns = column_names)
    return df[['Total', 'West Coast', 'East Coast']]


def getBracketNewData(season, week) -> 'df':
    """Get the total number of attendees, number of players in bracket, and
    number of unique players for each tournament in the season.
    [TotalnumAttendees, numBracket, newPlayers] """
    Placements = f'Records/S{season}W{week}Placements.csv'
    Placements = pd.read_csv(Placements, encoding = "ISO-8859-1")
    players = {row['SmasherID'] for index, row in Placements.iterrows()}
    # Used to determine new players

    count = {i: [0, 0, 0] for i in range(1, week + 1)}
    # Key is the Week number
    # Values are [TotalnumAttendees, numBracket, newPlayers]
    for _, row in Placements.iterrows():
        placed = [row[f'PWeek{i}'] for i in range(1, week + 1)]
        attended = [i > -2 for i in placed]     # Which tournaments did they enter
        madeBracket = [i > -1 for i in placed]  # Which tournaments did they make bracket

        for i in range(1, week + 1):
            count[i][0] += attended[i - 1]
            count[i][1] += madeBracket[i - 1]
            if (attended[i - 1] == 1) and (row['SmasherID'] in players): # New player
                count[i][2] += 1
                players.remove(row['SmasherID'])
    df = pd.DataFrame.from_dict(count, orient ='index')
    column_names = {0: 'Total',
                    1: 'Players In Bracket',
                    2: 'New Players'}
    return df.rename(columns = column_names)    


def SetupRank(season: int, week: int) -> None:
    """It plots every player's weekly rank up to that week for every week.
    Plots are separated by a player's main"""
    RankRecords = f'Records/S{season}W{week}RankRecords.csv'
    RankRecords = pd.read_csv(RankRecords, encoding = 'ISO-8859-1')
    RankRecords = RankRecords.sort_values(f'RWeek{week}')

    AllPlayerMains = getPlayerMains()
    
    for character, v in sorted(CHARACTERS.items(), key = lambda item: item[1]):
        if character in AllPlayerMains:
            CreateCharacterRankGraph(RankRecords, AllPlayerMains[character],
                            COLORS[v], character, season, week)

def SetupPoint(season: int, week: int) -> None:
    """It plots the number of Points every player for every week. Plots are
    separated by a player's main."""
    PastPoints = f'Records/S{season}W{week}PastPoints.csv'
    PastPoints = pd.read_csv(PastPoints, encoding = "ISO-8859-1")
    PastPoints = PastPoints.sort_values(f'BWeek{week}', ascending = False)

    AllPlayerMains = getPlayerMains()
    maxPoints = max(PastPoints[f'BWeek{week}']) + 30
    
    for character, v in sorted(CHARACTERS.items(), key = lambda item: item[1]):
        if character in AllPlayerMains:
            CreateCharacterPointsGraph(PastPoints, AllPlayerMains[character],
                              COLORS[v], character, season, week, maxPoints)


def CreateCharacterRankGraph(RankRecords: 'df', players: {'str'}, color: str,
                    character: str, season : int, week: int) -> None:
    """It plots the ranks of all the players of one character on
    a week to week basis."""
    x_range = [i for i in range(1, week + 1)]

    fig = go.Figure()
    for index, row in RankRecords.iterrows():
        playerTag = row[1]
        if playerTag in players:    # If player is an X main
            playerRank = [row[f'RWeek{i}'] for i in range(1, week + 1)]
            fig.add_trace(go.Scatter(x = x_range, y = playerRank, name = playerTag,
                             line = dict(color = color, width = 3)))

    print()
    fig.update_layout(title = f'Season {season} {character} Ranks')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    
    fig.update_layout(yaxis_title = 'Rank')
    fig.update_yaxes(range=[RankRecords.shape[0], 0])

    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    if FORMAT == 0:
        fig.show()
    else:
        fig.write_image(f"Plots/S{season}W{week}Rank{character}.png")


def CreateAllPlayersRankGraph(season : int, week: int) -> None:
    """It plots all players weekly rank"""
    RankRecords = f'Records/S{season}W{week}RankRecords.csv'
    RankRecords = pd.read_csv(RankRecords, encoding = "ISO-8859-1")
    RankRecords = RankRecords.sort_values(f'RWeek{week}')

    x_range = [i for i in range(1, week + 1)]
    PlayerMains = getMainsOfPlayer()

    fig = go.Figure()
    for index, row in RankRecords.iterrows():
        playerTag = row[1]
        color = '#666699'
        if playerTag in PlayerMains:    # Find the color for the person's main
            color = COLORS[CHARACTERS[PlayerMains[playerTag]]]
        playerRank = [row[f'RWeek{i}'] for i in range(1, week + 1)]
        fig.add_trace(go.Scatter(x = x_range, y = playerRank, name = playerTag,
                         line = dict(color = color, width = 3)))

    print()
    fig.update_layout(title = f'Season {season} Ranks')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    
    fig.update_layout(yaxis_title = 'Rank')
    fig.update_yaxes(range=[RankRecords.shape[0], 0])

    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    if FORMAT == 0:
        fig.show()
    else:
        fig.write_image(f"Plots/S{season}W{week}RankAllPlayers.png")

    
def CreateCharacterPointsGraph(PastPoints: 'df', players:{'str'}, color: str,
                      character:str, season: int, week: int, maxPoints:int) -> None:
    """It plots the cummulative points of all players of one character
    main on a week to week basis."""
    x_range = [i for i in range(1, week + 1)]

    fig = go.Figure()
    for _, row in PastPoints.iterrows():
        playerTag = row[1]
        if playerTag in players:    # If player is an X main
            playerPoints = [row[f'BWeek{i}'] for i in range(1, week + 1)]
            #playerPoints = [math.log(float(row[f'BWeek{i}'])) for i in range(1, week + 1)] # Log Points
            fig.add_trace(go.Scatter(x = x_range, y = playerPoints, name = playerTag,
                             line = dict(color = color, width = 3)))
    print()
    fig.update_layout(title = f'Season {season} {character} BankRoll Bills')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    
    fig.update_layout(yaxis_title = 'Bills')
    fig.update_yaxes(range=[0, maxPoints])

    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    if FORMAT == 0:
        fig.show()
    else:
        fig.write_image(f"Plots/S{season}W{week}Points{character}.png")


def CreateAllPlayersPointsGraph(season: int, week: int) -> None:
    """It plots a player's points through out the season. The color is
    related to their main."""
    PastPoints = f'Records/S{season}W{week}PastPoints.csv'
    PastPoints = pd.read_csv(PastPoints, encoding = "ISO-8859-1")
    PastPoints = PastPoints.sort_values(f'BWeek{week}', ascending = False)

    x_range = [i for i in range(1, week + 1)]
    PlayerMains = getMainsOfPlayer()

    fig = go.Figure()
    for _, row in PastPoints.iterrows():
        playerTag = row[1]
        playerPoints = [row[f'BWeek{i}'] for i in range(1, week + 1)]
        #playerPoints = [math.log(float(row[f'BWeek{i}'])) for i in range(1, week + 1)]
        color = '#666699'
        if playerTag in PlayerMains:    # Find the color for the person's main
            color = COLORS[CHARACTERS[PlayerMains[playerTag]]]
        fig.add_trace(go.Scatter(x = x_range, y = playerPoints, name = playerTag,
                         line = dict(color = color, width = 3)))

    print()
    fig.update_layout(title = f'Season {season} BankRoll Bills')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    
    fig.update_layout(yaxis_title = 'Points')

    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    if FORMAT == 0:
        fig.show()
    else:
        fig.write_image(f"Plots/S{season}W{week}PointsAllPlayers.png")


def CreateEntrantsCoastGraph(season: int, week: int) -> None:
    """Plot a bar graph of the total number of attendees, number of
    West Coast and number of East Coast attendees for each week"""
    Entrants = getCoastData(season, week)

    fig = go.Figure()
    fig = px.bar(Entrants, barmode='group')

    print()
    fig.update_layout(title = f'Season {season} Entrant For Coasts')
    
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    fig.update_layout(yaxis_title = 'Entrants')

    max_y= max(Entrants['Total'])
    yticks = [5*i for i in range(5 + math.floor(max_y/5))]      # Ticks at every 5
    ytickstext = [5*i if (i % 2) == 0 else ' ' for i in range(5 + math.floor(max_y/5))]    # Text at every 10
    fig.update_layout(yaxis = dict(tickvals = yticks, ticktext = ytickstext))

    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    if FORMAT == 0:
        fig.show()
    else:
        fig.write_image(f"Plots/S{season}W{week}EntrantsCoasts.png")


def CreateEntrantBracketNewGraph(season: int, week: int) -> None:
    """Plots a bar graph of the total number of attendees, players in bracket,
    and new players that season."""
    Entrants = getBracketNewData(season, week)
    fig = px.bar(Entrants, barmode='group',
                 color_discrete_sequence = px.colors.qualitative.Dark24)

    fig.update_layout(title = f'Season {season} Entrants')
    
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    fig.update_layout(yaxis_title = 'Entrants')

    print()
    max_y= max(Entrants['Total'])
    yticks = [5*i for i in range(5 + math.floor(max_y/5))]      # Ticks at every 5
    ytickstext = [5*i if (i % 2) == 0 else ' ' for i in range(5 + math.floor(max_y/5))]    # Text at every 10
    fig.update_layout(yaxis = dict(tickvals = yticks, ticktext = ytickstext))

    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    if FORMAT == 0:
        fig.show()
    else:
        fig.write_image(f"Plots/S{season}W{week}TMTDetails.png")


def getPointsCoast(season: int, week: int) -> [int, int]:
    """It gets the total amount of points for each coast and
    number of attendees for each coast"""
    Features = f'Records/S{season}W{week}Features.csv'
    Features = pd.read_csv(Features, encoding = "ISO-8859-1")
    Points = [0, 0] # [WC, EC]
    for index, row in Features.iterrows():
        if row['Coast'] == 'WC':
            Points[0] += row['Points']
        elif row['Coast'] == 'EC':
            Points[1] += row['Points']
    return Points


def CombinedPointsCoast(season: int, week: int) -> None:
    """It plots how many combined points each coast has."""
    Points = getPointsCoast(season, week)
    print(Points)

    # Fix how the plot looks like.
    fig = go.Figure()
    '#d9534f'
    fig.add_trace(go.Bar(x = [-0.5], y= [Points[0]],
                         name = 'West Coast', marker_color = 'indianred'))

    '#428bca'
    fig.add_trace(go.Bar(x = [0.5], y= [Points[1]],
                         name = 'East Coast', marker_color = 'indianred'))

    print()
    fig.update_layout(title = f'Season {season} Coast Total Points')
    
    fig.update_layout(xaxis_title = '')
    #fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
    #                               ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    fig.update_layout(yaxis_title = 'Points')



    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    if FORMAT == 0:
        fig.show()
    else:
        fig.write_image(f"Plots/S{season}W{week}TotalPointsCoast.png")




def main():
    #UI.PrintGraphWelcomeMessage()
    #choice = UI.graphChoice()
    #save_graphs = UI.saveGraph()
    #season = UI.UserSeason()
    #week = UI.UserWeek()
    choice = 9
    save_graphs = 1
    season = 1
    week = 3
    
    SavingFormat(save_graphs)
    
    if choice == 1:
        SetupRank(season, week)
    elif choice == 2:
        CreateAllPlayersRankGraph(season, week)
    elif choice == 3:
        SetupPoint(season, week)
    elif choice == 4:
        CreateAllPlayersPointsGraph(season, week)
    elif choice == 5:
        CreateEntrantsCoastGraph(season, week)
    elif choice == 6:
        CreateEntrantBracketNewGraph(season, week)
    elif choice == 7:
        SetupRank(season, week)     # Website Graphs
        CreateAllPlayersRankGraph(season, week)
        SetupPoint(season, week)
        CreateAllPlayersPointsGraph(season, week)
    elif choice == 8:
        CreateEntrantsCoastGraph(season, week)      # TMT details
        CreateEntrantBracketNewGraph(season, week)
    elif choice == 9:
        # Website
        # Points for each Coast
        CombinedPointsCoast(season, week)

    print("End")

main()








