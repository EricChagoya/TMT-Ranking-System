import os
import math
import numpy as np
import pandas as pd

import graphsStaff as GS
import UserInterface as UI

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

#pio.kaleido.scope.default_height = 1200
#pio.kaleido.scope.default_width = 2400

# pip install plotly
# https://plotly.com/python/
# Really good documentation
# pip install -U kaleido
# Used for saving static images

CHARACTERS = {'Fox': 0,
              'Falco' : 1,
              'Marth': 2,
              'Sheik': 3,
              'Falcon': 4,
              'Puff': 5,
              'Peach': 6,
              'ICs' : 7,
              'Other': 8}

COLORS = ['#ffc34d', '#0000ff', '#1aff1a', '#ff1a1a', '#4d4d4d',
          '#6600cc', '#ff66ff', '#ffff00', '#000000', '#666699']
#        [Yellow/Orange, Blue, Lime Green, Red, Dark Gray,
#         Purple, Pink, Yellow, Black, Gray]



FORMAT = 0  # 0 is an iteractable HTML
            # 1 is a jpeg

def SavingFormat(choice: int, season: int) -> None:
    """Changes a global variable so all graphs are put into HTML
    or into a jpeg file"""
    global FORMAT
    if choice == 1: 
        FORMAT = 0
    else:
        FORMAT = 1
        if not os.path.exists(f'Data/Season{season}/PlotsWebsite'):
            os.mkdir(f'Data/Season{season}/PlotsWebsite')
        if not os.path.exists(f'Data/Season{season}/PlotsStaff'):
            os.mkdir(f'Data/Season{season}/PlotsStaff')


def getPlayerMains() -> {'Main': 'Tag'}:
    """This will return a ditionary with the Character being the key and
    the values will be a set of players."""
    Mains = 'Data/PlayerMains.csv'
    Mains = pd.read_csv(Mains, encoding='utf-8-sig')    # Not sure why ISO encoding doesn't work    
    AllPlayerMains = dict()
    for index, row in Mains.iterrows():
        if row['Main'] in AllPlayerMains:
            AllPlayerMains[row['Main']].add(row['SmashTag'])
        else:
            if row['Main'] in CHARACTERS:
                AllPlayerMains[row['Main']] = {row['SmashTag']}
            else:
                AllPlayerMains['Other'] = {row['SmashTag']}
    return AllPlayerMains


def getMainsOfPlayer() -> {'Tag': 'Main'}:
    """We will return a dictionary with the key being the Tag and
    the value will be their main character."""
    Mains = 'Data/PlayerMains.csv'
    #Mains = pd.read_csv(Mains, encoding='utf-8-sig')
    Mains = pd.read_csv(Mains, encoding='utf-8-sig')    # Not sure why ISO encoding doesn't work    
    PlayerMains = dict()
    for index, row in Mains.iterrows():
        if row['Main'] in CHARACTERS:
            PlayerMains[row['SmashTag']] = row['Main']
        else:
            PlayerMains[row['SmashTag']] = 'Other'
    return PlayerMains
    


def RankCharacter(season: int, week: int) -> None:
    """It plots every player's weekly rank up to that week for every week.
    Plots are separated by a player's main"""
    RankRecords = f'Data/Season{season}/Records/S{season}W{week}RankRecords.csv'
    RankRecords = pd.read_csv(RankRecords, encoding = 'ISO-8859-1')
    RankRecords = RankRecords.sort_values(f'RWeek{week}')
    AllPlayerMains = getPlayerMains()
    
    for character, v in sorted(CHARACTERS.items(), key = lambda item: item[1]):
        if character in AllPlayerMains:
            CharacterRankGraph(RankRecords, AllPlayerMains[character],
                               COLORS[v], character, season, week)

def CharacterRankGraph(RankRecords: 'df', players: {'str'}, color: str,
                       character: str, season : int, week: int) -> None:
    """It plots the ranks of all the players of one character on
    a week to week basis."""
    fig = go.Figure()
    x_range = [i for i in range(1, week + 1)]
    for index, row in RankRecords.iterrows():
        playerTag = row[1]
        if playerTag in players:    # If player is an X main
            playerRank = [row[f'RWeek{i}'] for i in range(1, week + 1)]
            fig.add_trace(go.Scatter(x = x_range, y = playerRank,
                                     name = playerTag + " Rank " + str(int(playerRank[-1])),
                                     line = dict(color = color, width = 3)))
            
    fig.update_layout(title = f'Season {season} {character} Ranks')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    
    fig.update_layout(yaxis_title = 'Rank')
    fig.update_yaxes(range=[RankRecords.shape[0], 0])

    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    GS.presentFile(fig, FORMAT, f'Data/Season{season}/PlotsWebsite/S{season}W{week}Rank{character}.jpeg')


def RankTop10Graph(season: int, week: int) -> None:
    """It plots all players weekly rank"""
    RankRecords = f'Data/Season{season}/Records/S{season}W{week}RankRecords.csv'
    RankRecords = pd.read_csv(RankRecords, encoding = "ISO-8859-1")
    RankRecords = RankRecords.sort_values(f'RWeek{week}')

    lowestRank = 0
    PlayerMains = getMainsOfPlayer()
    x_range = [i for i in range(1, week + 1)]

    fig = go.Figure()
    count = 1
    for index, row in RankRecords.iterrows():
        playerTag = row[1]
        color = '#666699'
        if playerTag in PlayerMains:    # Find the color for the player's main
            color = COLORS[CHARACTERS[PlayerMains[playerTag]]]
        playerRank = [float(row[f'RWeek{i}']) for i in range(1, week + 1)]
        lowestRank = max(lowestRank, max(playerRank)) # Max because lowest rank means highest number
        fig.add_trace(go.Scatter(x = x_range, y = playerRank,
                                 name = str(playerTag) + " Rank " + str(int(playerRank[-1])),
                                 line = dict(color = color, width = 3)))
        if count >= 10:
            break
        count += 1

    fig.update_layout(title = f'Season {season} Ranks')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    
    fig.update_layout(yaxis_title = 'Rank')
    fig.update_yaxes(range=[14, 0])
    #fig.update_yaxes(range=[lowestRank + 3, 0])

    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    GS.presentFile(fig, FORMAT, f'Data/Season{season}/PlotsWebsite/S{season}W{week}RankTop10.jpeg')


def PointsCharacter(season: int, week: int) -> None:
    """It plots the number of Points every player for every week. Plots are
    separated by a player's main."""
    PastPoints = f'Data/Season{season}/Records/S{season}W{week}PastPoints.csv'
    PastPoints = pd.read_csv(PastPoints, encoding = "ISO-8859-1")
    PastPoints = PastPoints.sort_values(f'BWeek{week}', ascending = False)
    AllPlayerMains = getPlayerMains()
    maxPoints = max(PastPoints[f'BWeek{week}']) + 30
    
    for character, v in sorted(CHARACTERS.items(), key = lambda item: item[1]):
        if character in AllPlayerMains:
            CharacterPointsGraph(PastPoints, AllPlayerMains[character],
                                 COLORS[v], character, season, week, maxPoints)

    
def CharacterPointsGraph(PastPoints: 'df', players:{'str'}, color: str,
                         character:str, season: int, week: int, maxPoints:int) -> None:
    """It plots the cummulative points of all players of one character
    on a week to week basis."""
    fig = go.Figure()
    x_range = [i for i in range(1, week + 1)]

    for _, row in PastPoints.iterrows():
        playerTag = row[1]
        if playerTag in players:    # If player is an X main
            playerPoints = [row[f'BWeek{i}'] for i in range(1, week + 1)]
            #playerPoints = [math.log(float(row[f'BWeek{i}'])) for i in range(1, week + 1)] # Log Points
            fig.add_trace(go.Scatter(x = x_range, y = playerPoints,
                                     name = playerTag + " Bills " + str(int(playerPoints[-1])),
                                     line = dict(color = color, width = 3)))
    
    fig.update_layout(title = f'Season {season} {character} BankRoll Bills')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    
    fig.update_layout(yaxis_title = 'Bills')
    fig.update_yaxes(range=[0, maxPoints])

    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    GS.presentFile(fig, FORMAT, f'Data/Season{season}/PlotsWebsite/S{season}W{week}Points{character}.jpeg')


def PointsTop10Graph(season: int, week: int) -> None:
    """It plots a player's points through out the season. The color is
    related to their main."""
    PastPoints = f'Data/Season{season}/Records/S{season}W{week}PastPoints.csv'
    PastPoints = pd.read_csv(PastPoints, encoding = "ISO-8859-1")
    PastPoints = PastPoints.sort_values(f'BWeek{week}', ascending = False)

    count = 1
    fig = go.Figure()
    PlayerMains = getMainsOfPlayer()
    x_range = [i for i in range(1, week + 1)]

    for _, row in PastPoints.iterrows():
        playerTag = row[1]
        playerPoints = [row[f'BWeek{i}'] for i in range(1, week + 1)]
        #playerPoints = [math.log(float(row[f'BWeek{i}'])) for i in range(1, week + 1)]
        color = '#666699'
        if playerTag in PlayerMains:    # Find the color for the person's main
            color = COLORS[CHARACTERS[PlayerMains[playerTag]]]
        fig.add_trace(go.Scatter(x = x_range, y = playerPoints,
                                 name = str(playerTag) + " Bills " + str(int(playerPoints[-1])),
                                 line = dict(color = color, width = 3)))
        if count >= 10:
            break
        count += 1

    fig.update_layout(title = f'Season {season} BankRoll Bills')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    fig.update_layout(yaxis_title = 'Points')

    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    GS.presentFile(fig, FORMAT, f'Data/Season{season}/PlotsWebsite/S{season}W{week}PointsTop10.jpeg')


def getPointsCoast(season: int, week: int) -> [int, int]:
    """It gets the total amount of points for each coast and
    number of attendees for each coast"""
    Features = f'Data/Season{season}/Records/S{season}W{week}Features.csv'
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

    fig = go.Figure()
    fig.add_trace(go.Bar(x = [-0.5], y= [Points[0]],
                         name = 'West Coast', marker_color = '#428bca'))

    #fig.add_trace(go.Bar(x = [-0.5], y= [Points[0]],
    #                     name = 'West Coast', marker_color = '#428bca',
    #                     text= "West Coast", textposition = "inside"))

    fig.add_trace(go.Bar(x = [0.5], y= [Points[1]],
                         name = 'East Coast', marker_color = '#d9534f'))
    
    fig.update_layout(title = f'Season {season} Coast Total Points')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [""], ticktext = [""]))
    
    fig.update_layout(yaxis_title = 'Points')
    fig.update_yaxes(range=[0, max(Points) + 250])

    fig.update_layout(font = dict(size= 23))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 30))
    GS.presentFile(fig, FORMAT, f'Data/Season{season}/PlotsWebsite/S{season}W{week}CoastTotalPoints.jpeg')




def main():
    #UI.PrintGraphWelcomeMessage()
    #choice = UI.graphChoice()
    #save_graphs = UI.saveGraph()
    #season = UI.UserSeason()
    #week = UI.UserWeek()
    choice = 9
    save_graphs = 2
    season = 1
    week = 6
    
    SavingFormat(save_graphs, season)
    
    if choice == 1:
        # Plots every rank based off character
        RankCharacter(season, week)
        #SetupRank(season, week)
        
    elif choice == 2:
        # Plots the rank of the top 10
        RankTop10Graph(season, week)
        
    elif choice == 3:
        # Plots points for every character
        PointsCharacter(season, week)
        
    elif choice == 4:
        # Plots the points of the top 10
        PointsTop10Graph(season, week)

    elif choice == 5:
        # Points for each Coast
        CombinedPointsCoast(season, week)
        
    elif choice == 6:
        # Plots Total Entrants, WC Entrants, and EC Entrants
        GS.CoastEntrantsGraph(season, week, FORMAT)
        
    elif choice == 7:
        # Plots Total Entrants, Returning Players, and New Players
        GS.NewPlayersGraph(season, week, FORMAT)

    elif choice == 8:
        # Plots how many TMTs the average attendee entered for that season
        #GS.HistogramEntrants(season, week, FORMAT)
        pass

    elif choice == 9:
        # Plots Revenue for TMT
        #GS.Revenue(season, week, FORMAT)
        pass
        
    elif choice == 10:
        # All Website Plots
        RankCharacter(season, week)
        RankTop10Graph(season, week)
        PointsCharacter(season, week)
        PointsTop10Graph(season, week)
        CombinedPointsCoast(season, week)
        
    elif choice == 11:
        # Plots for Staff
        GS.CoastEntrantsGraph(season, week, FORMAT)
        GS.NewPlayersGraph(season, week, FORMAT)
        #GS.HistogramEntrants(season, week, FORMAT)
        
    print("End")

main()
