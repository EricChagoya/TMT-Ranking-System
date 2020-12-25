import os
import math
import numpy as np
import pandas as pd

import graphsStaff as GS
import UserInterface as UI

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

# pip install plotly
# pip install -U kaleido
# Used for saving static images


CHARACTERS = {'Fox': '#ffbf80',     # Orange
              'Falco' : '#0000ff',  # Blue
              'Marth': '#0d0d0d',   # Black
              'Sheik': '#9933ff',   # Purple
              'Falcon': '#ff0000',  # Red
              'Puff': '#ff80ff',    # Pink
              'Peach': '#ffcc33',   # Gold
              'ICs' : '#99ccff'}    # Baby Blue
CHARORDER = ['Fox', 'Falco', 'Marth', 'Sheik',
             'Falcon',  'Puff', 'Peach', 'ICs']

MIDTIERS = {'Pikachu': '#ffff00',   # Piss Yellow
            'Samus': '#ff9900',     # Redish Orange
            'Doc': '#4d4d4d',       # White/ Gray
            'Yoshi': '#99ff66',     # Dark Green
            'Luigi': '#009933',     # Slippi Green
            'Ganon': '#660000',     # Maroon
            'DK': '#663300'}

MIDTIERORDER = ['Pikachu', 'Samus', 'Doc',
                'Yoshi', 'Luigi', 'Ganon',
                'DK']

COLOROTHER = '#808080'      # Gray


FORMAT = 0  # 0 is an iteractable HTML
            # 1 is a jpeg
DEBUGGING = False

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
    the values will be a set of players. A character's tier doesn't matter."""
    Mains = 'Data/PlayerMains.csv'
    Mains = pd.read_csv(Mains, encoding='utf-8-sig')    # Not sure why ISO encoding doesn't work    
    AllPlayerMains = dict()
    for index, row in Mains.iterrows():
        if row['Main'] in AllPlayerMains:
            AllPlayerMains[row['Main']].add(row['SmashTag'])
        else:
            AllPlayerMains[row['Main']] = {row['SmashTag']}
    return AllPlayerMains


def getPlayerMidTier(AllPlayerMains: {'Main': 'Tag'}) -> {'Tag': 'Main'} and {'Tag'}:
    """Find out mains a midtier and those players who we don't know their main or
    they main a low tier."""
    MidTiers = dict()
    Other = set()
    for k, v in AllPlayerMains.items():
        if k in MIDTIERS:
            for player in v:
                MidTiers[player] = k
        elif k not in CHARACTERS:
            Other = Other.union(v)
    return MidTiers, Other


def getMainsOfPlayer() -> {'Tag': 'Main'}:
    """We will return a dictionary with the key being the Tag and
    the value will be their main character."""
    Mains = 'Data/PlayerMains.csv'
    Mains = pd.read_csv(Mains, encoding = 'utf-8-sig')    # Not sure why ISO encoding doesn't work    
    PlayerMains = dict()
    for index, row in Mains.iterrows():
        if row['Main'] in CHARACTERS:
            PlayerMains[row['SmashTag']] = row['Main']
        elif row['Main'] in MIDTIERS:
            PlayerMains[row['SmashTag']] = row['Main']
        else:
            PlayerMains[row['SmashTag']] = 'Other'
    return PlayerMains


def appendRankLegend(legend: 'df', temp: {'player': int}, character: str) -> 'df':
    for k, v in sorted(temp.items(), key = lambda item: item[1]):
        row = {'SmashTag': k, 'Rank': v, 'Character': character}
        legend = legend.append(row, ignore_index= True)
    return legend

def appendPointsLegend(legend: 'df', temp: {'player': int}, character: str) -> 'df':
    for k, v in sorted(temp.items(), key = lambda item: -item[1]):
        row = {'SmashTag': k, 'Points': v, 'Character': character}
        legend = legend.append(row, ignore_index= True)
    return legend


# 1
def RankCharacter(season: int, week: int) -> None:
    """It plots every player's weekly rank up to that week for every week.
    Plots are separated by a player's main"""
    RankRecords = f'Data/Season{season}/Records/S{season}W{week}RankRecords.csv'
    RankRecords = pd.read_csv(RankRecords, encoding = 'ISO-8859-1')
    RankRecords = RankRecords.sort_values(f'RWeek{week}')
    AllPlayerMains = getPlayerMains()
    MidTierMains, Other = getPlayerMidTier(AllPlayerMains)
    legend = pd.DataFrame()
    
    for character, v in sorted(CHARACTERS.items(), key = lambda item: item[1]):
        if character in AllPlayerMains:
            temp = CharacterRankGraph(RankRecords, AllPlayerMains[character],
                                      CHARACTERS[character], character, season, week)
            legend = appendRankLegend(legend, temp, character)
    
    temp2 = CharacterMidTierRankGraph(RankRecords, MidTierMains, 'MidTiers', season, week)
    temp3 = CharacterRankGraph(RankRecords, Other, COLOROTHER, 'Other', season, week)
    legend = appendRankLegend(legend, temp2, "MidTiers")
    legend = appendRankLegend(legend, temp3, "Other")
    legend = legend[['Character', 'SmashTag', 'Rank']]
    rankLegendLocation = f'Data/Season{season}/PlotsWebsite/S{season}W{week}RankLegend.csv'
    legend.to_csv(rankLegendLocation, index=False, encoding = "ISO-8859-1")


def CharacterRankGraph(RankRecords: 'df', players: {'str'}, color: str,
                       character: str, season : int, week: int) -> None:
    """It plots the ranks of all the players of one character on
    a week to week basis."""
    temp = dict()
    fig = go.Figure()
    x_range = [i for i in range(1, week + 1)]
    for _, row in RankRecords.iterrows():
        playerTag = row['SmashTag']
        if playerTag in players:    # If player is an X main
            playerRank = [row[f'RWeek{i}'] for i in range(1, week + 1)]
            fig.add_trace(go.Scatter(x = x_range, y = playerRank,
                                     name = playerTag + ": " + str(int(playerRank[-1])),
                                     line = dict(color = color, width = 3)))
            temp[playerTag] = int(playerRank[-1])
            
    fig.update_layout(title = f'Season {season} {character} Ranks')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    fig.update_layout(yaxis_title = 'Rank')
    fig.update_yaxes(range=[RankRecords.shape[0], 0])
    
    fig.update_layout(font = dict(size= 28))
    if DEBUGGING:
        fig.update_layout(showlegend = True)
        fig.update_layout(legend = dict(font_size = 20))
    else:
        fig.update_layout(showlegend = False)
    GS.presentFile(fig, FORMAT, f'Data/Season{season}/PlotsWebsite/S{season}W{week}Rank{character}.jpeg')
    return temp


def CharacterMidTierRankGraph(RankRecords: 'df', MidTierMains: {'Player': 'Main'},
                              character:str, season: int, week: int) -> None:
    """It graphs all the mid tiers mains into one plot."""
    temp = dict()
    fig = go.Figure()
    x_range = [i for i in range(1, week + 1)]
    for _, row in RankRecords.iterrows():
        playerTag = row['SmashTag']
        if playerTag in MidTierMains:    # If player is a Mid Tier Loser
            playerRank = [row[f'RWeek{i}'] for i in range(1, week + 1)] # Their Rank over the Season
            color = MIDTIERS[MidTierMains[playerTag]]   # Color for that Mid Tier
            fig.add_trace(go.Scatter(x = x_range, y = playerRank,
                                     name = playerTag + ": " + str(int(playerRank[-1])),
                                     line = dict(color = color, width = 3)))
            temp[playerTag] = int(playerRank[-1])
            
    fig.update_layout(title = f'Season {season} {character} Ranks')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    fig.update_layout(yaxis_title = 'Rank')
    fig.update_yaxes(range=[RankRecords.shape[0], 0])

    fig.update_layout(font = dict(size= 28))
    if DEBUGGING:
        fig.update_layout(showlegend = True)
        fig.update_layout(legend = dict(font_size = 20))
    else:
        fig.update_layout(showlegend = False)
    GS.presentFile(fig, FORMAT, f'Data/Season{season}/PlotsWebsite/S{season}W{week}Rank{character}.jpeg')
    return temp
    

# 2
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
    for _, row in RankRecords.iterrows():
        playerTag = row[1]
        if (playerTag in PlayerMains) and (PlayerMains[playerTag] in CHARACTERS):   # Mains a Top Tier
            color = CHARACTERS[PlayerMains[playerTag]]
        elif (playerTag in PlayerMains) and (PlayerMains[playerTag] in MIDTIERS):   # Mains a Mid Tier
            color = MIDTIERS[PlayerMains[playerTag]]
        else:                   # Low Tier Main or NA
            color = '#666699'
        playerRank = [float(row[f'RWeek{i}']) for i in range(1, week + 1)]
        lowestRank = max(lowestRank, max(playerRank)) # Max because lowest rank means highest number
        fig.add_trace(go.Scatter(x = x_range, y = playerRank,
                                 name = str(playerTag) + ": " + str(int(playerRank[-1])),
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

    fig.update_layout(font = dict(size= 28))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 24))
    GS.presentFile(fig, FORMAT, f'Data/Season{season}/PlotsWebsite/S{season}W{week}RankTop10.jpeg')

# 3
def PointsCharacter(season: int, week: int) -> None:
    """It plots the number of Points every player for every week. Plots are
    separated by a player's main."""
    PastPoints = f'Data/Season{season}/Records/S{season}W{week}PastPoints.csv'
    PastPoints = pd.read_csv(PastPoints, encoding = "ISO-8859-1")
    PastPoints = PastPoints.sort_values(f'BWeek{week}', ascending = False)
    AllPlayerMains = getPlayerMains()
    MidTierMains, Other = getPlayerMidTier(AllPlayerMains)
    legend = pd.DataFrame()    
    
    for character, v in sorted(CHARACTERS.items(), key = lambda item: item[1]):
        if character in AllPlayerMains:
            temp = CharacterPointsGraph(PastPoints, AllPlayerMains[character],
                                        CHARACTERS[character], character, season, week)
            legend = appendPointsLegend(legend, temp, character)
            
    temp2 = CharacterMidTiersPointsGraph(PastPoints, MidTierMains, "MidTiers", season, week)
    temp3 = CharacterPointsGraph(PastPoints, Other, COLOROTHER, "Other", season, week)
    legend = appendPointsLegend(legend, temp2, "MidTiers")
    legend = appendPointsLegend(legend, temp3, "Other")
    legend = legend[['Character', 'SmashTag', 'Points']]
    pointsLegendLocation = f'Data/Season{season}/PlotsWebsite/S{season}W{week}PointsLegend.csv'
    legend.to_csv(pointsLegendLocation, index=False, encoding = "ISO-8859-1")
    

    
def CharacterPointsGraph(PastPoints: 'df', players:{'str'}, color: str,
                         character:str, season: int, week: int) -> None:
    """It plots the cummulative points of all players of one character
    on a week to week basis."""
    temp = dict()
    fig = go.Figure()
    x_range = [i for i in range(1, week + 1)]

    for _, row in PastPoints.iterrows():
        playerTag = row['SmashTag']
        if playerTag in players:    # If player is an X main
            playerPoints = [row[f'BWeek{i}'] for i in range(1, week + 1)]
            fig.add_trace(go.Scatter(x = x_range, y = playerPoints,
                                     name = playerTag + ": " + str(int(playerPoints[-1])),
                                     line = dict(color = color, width = 3)))
            temp[playerTag] = int(playerPoints[-1])
    
    fig.update_layout(title = f'Season {season} {character} BankRoll Bills')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    fig.update_layout(yaxis_title = 'Bills')
    values = [1, 5, 10, 50, 100, 500, 1000, 5000]
    fig.update_layout(yaxis = dict(tickmode = 'array', type = 'log',
                                   ticktext = values, tickvals = values))
    fig.update_layout(font = dict(size= 28))
    
    if DEBUGGING:
        fig.update_layout(showlegend = True)
        fig.update_layout(legend = dict(font_size = 20))
    else:
        fig.update_layout(showlegend = False)
    GS.presentFile(fig, FORMAT, f'Data/Season{season}/PlotsWebsite/S{season}W{week}Points{character}.jpeg')
    return temp


def CharacterMidTiersPointsGraph(PastPoints: 'df', MidTierMains: {'Player': 'Main'},
                                 character:str, season: int, week: int) -> None:
    """It plots the cummulative points of all players of one character
    on a week to week basis."""
    temp = dict()
    fig = go.Figure()
    x_range = [i for i in range(1, week + 1)]

    for _, row in PastPoints.iterrows():
        playerTag = row['SmashTag']
        if playerTag in MidTierMains:    # If player is a Mid Tier Loser
            playerPoints = [row[f'BWeek{i}'] for i in range(1, week + 1)]
            color = MIDTIERS[MidTierMains[playerTag]]   # Color for that Mid Tier
            fig.add_trace(go.Scatter(x = x_range, y = playerPoints, 
                                     name = playerTag + ": " + str(int(playerPoints[-1])),
                                     line = dict(color = color, width = 3)))
            temp[playerTag] = int(playerPoints[-1])

    fig.update_layout(title = f'Season {season} {character} BankRoll Bills')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    fig.update_layout(yaxis_title = 'Bills')
    values = [1, 5, 10, 50, 100, 500, 1000, 5000]
    fig.update_layout(yaxis = dict(tickmode = 'array', type = 'log',
                                   ticktext = values, tickvals = values))
    fig.update_layout(font = dict(size= 28))

    if DEBUGGING:
        fig.update_layout(showlegend = True)
        fig.update_layout(legend = dict(font_size = 20))
    else:
        fig.update_layout(showlegend = False)
    GS.presentFile(fig, FORMAT, f'Data/Season{season}/PlotsWebsite/S{season}W{week}Points{character}.jpeg')
    return temp


# 4
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
        playerTag = row['SmashTag']
        playerPoints = [row[f'BWeek{i}'] for i in range(1, week + 1)]
        if (playerTag in PlayerMains) and (PlayerMains[playerTag] in CHARACTERS):   # Mains a Top Tier
            color = CHARACTERS[PlayerMains[playerTag]]
        elif (playerTag in PlayerMains) and (PlayerMains[playerTag] in MIDTIERS):   # Mains a Mid Tier
            color = MIDTIERS[PlayerMains[playerTag]]
        else:                   # Low Tier Main or NA
            color = '#666699'
        fig.add_trace(go.Scatter(x = x_range, y = playerPoints,
                                 name = str(playerTag) + ": " + str(int(playerPoints[-1])),
                                 line = dict(color = color, width = 3)))
        if count >= 10:
            break
        count += 1

    fig.update_layout(title = f'Season {season} BankRoll Bills')
    fig.update_layout(xaxis_title = '')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)], 
                                   ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    fig.update_layout(yaxis_title = 'Points')

    fig.update_layout(font = dict(size= 28))    
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

# 5
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

    fig.update_layout(font = dict(size= 28))    
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 30))
    GS.presentFile(fig, FORMAT, f'Data/Season{season}/PlotsWebsite/S{season}W{week}CoastTotalPoints.jpeg')




def main():
    UI.PrintGraphWelcomeMessage()
    choice = UI.graphChoice()
    save_graphs = UI.saveGraph()
    season = UI.UserSeason()
    week = UI.UserWeek()
    cummulativeWeek = UI.UserTMTNumber()
    #choice = 10
    #save_graphs = 2
    #season = 1
    #week = 6
    
    SavingFormat(save_graphs, season)
    
    if choice == 1:
        # Plots every rank based off character
        RankCharacter(season, week)
        
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
        GS.NewPlayersGraph(season, week, cummulativeWeek, FORMAT)

    elif choice == 8:
        # Plots how many TMTs the average attendee entered for that season
        GS.BarGraphEntrants(season, week, FORMAT)
        
    elif choice == 9:
        # Plots Revenue for TMT
        GS.Revenue(season, week, FORMAT)
        
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
        GS.BarGraphEntrants(season, week, FORMAT)
        GS.Revenue(season, week, FORMAT)
        
    print("End")

main()
