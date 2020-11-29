import math
import numpy as np
import pandas as pd
import UserInterface as UI

import plotly.graph_objects as go
import plotly.express as px
# pip install plotly
# https://plotly.com/python/
# Really good documentation


CHARACTERS = {'Fox': 0,
              'Falco' : 1,
              'Marth': 2,
              'Sheik': 3,
              'Falcon': 4,
              'Puff': 5,
              'Peach': 6,
              'Pikachu' : 7,
              'NA': 8}

COLORS = []

# Colors should be based off player's main
# Should be gray if we don't know their main


def getCoastData(season: int, week: int) -> 'df':
    """Get the total number of combined, West Coast, and East Coast entrants
    for each week. The last column is for people we aren't sure of.
    [Total, WC, EC, NA]"""
    Features = f'Records/S{season}W{week}Features.csv'
    Features = pd.read_csv(Features)
    Placements = f'Records/S{season}W{week}Placements.csv'
    Placements = pd.read_csv(Placements)
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
    Placements = pd.read_csv(Placements)
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


def CreateRankGraph(season : int, week: int) -> None:
    """It plots all players weekly rank"""
    RankRecords = f'Records/S{season}W{week}RankRecords.csv'
    RankRecords = pd.read_csv(RankRecords)
    RankRecords = RankRecords.sort_values(f'RWeek{week}')

    colors = ['aquamarine', 'crimson', 'hotpink', 'goldenrod', 'navy']
    len_colors= len(colors)

    x_range = [i for i in range(1, week + 1)]

    fig = go.Figure()
    for index, row in RankRecords.iterrows():
        playerTag = row[1]
        playerRank = [row[f'RWeek{week}'] for i in range(1, week + 1)]
        fig.add_trace(go.Scatter(x = x_range, y = playerRank, name = playerTag,
                         line = dict(color = colors[index % len_colors], width = 4)))

    fig.update_layout(title = f'Season {season} Ranks')
    fig.update_layout(xaxis_title = 'Week Number')
    fig.update_layout(yaxis_title = 'Rank')
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 16))
    
    fig.update_xaxes(nticks = week)
    fig.update_yaxes(range=[RankRecords.shape[0], 0])
    fig.show()



def CreatePointsGraph(season: int, week: int) -> None:
    """It plots a player's points through out the season"""
    PastPoints = f'Records/S{season}W{week}PastPoints.csv'
    PastPoints = pd.read_csv(PastPoints)
    PastPoints = PastPoints.sort_values(f'BWeek{week}', ascending = False)

    colors = ['aquamarine', 'crimson', 'hotpink', 'goldenrod', 'navy']
    len_colors= len(colors)
    x_range = [i for i in range(1, week + 1)]

    fig = go.Figure()
    for index, row in PastPoints.iterrows():
        playerTag = row[1]
        playerPoints = [row[f'BWeek{i}'] for i in range(1, week + 1)]
        #playerPoints = [math.log(float(row[f'BWeek{i}'])) for i in range(1, week + 1)]
        fig.add_trace(go.Scatter(x = x_range, y = playerPoints, name = playerTag,
                         line = dict(color = colors[index % len_colors], width = 4)))

    fig.update_layout(title = f'Season {season} BankRoll Bills')
    fig.update_layout(xaxis_title = 'Week Number')
    fig.update_layout(yaxis_title = 'Bills')
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 16))
    
    fig.update_xaxes(nticks = week)
    fig.show()



def CreateEntrantsCoastGraph(season: int, week: int) -> None:
    """Plot the total number of attendees, number of West Coast and number
    of East Coast attendees for each week"""
    Entrants = getCoastData(season, week)

    fig = go.Figure()
    fig = px.bar(Entrants, barmode='group')

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
    fig.show()



def CreateEntrantBracketNewGraph(season: int, week: int) -> None:
    """Plots the total number of attendees, players in bracket, and
    new players that season."""
    Entrants = getBracketNewData(season, week)
    fig = px.bar(Entrants, barmode='group',
                 color_discrete_sequence = px.colors.qualitative.Dark24)

    fig.update_layout(title = f'Season {season} Entrants')
    
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

    fig.show()




def main():
    #UI.PrintGraphWelcomeMessage()
    #choice = UI.graphChoice()
    # Update choice to get new options
    #season = UI.UserSeason()
    #week = UI.UserWeek()
    choice = 3
    season = 1
    week = 3
    
    if choice == 1:
        CreateRankGraph(season, week)
    elif choice == 2:
        CreatePointsGraph(season, week)
    elif choice == 3:
        CreateEntrantsCoastGraph(season, week)
    else:
        CreateEntrantBracketNewGraph(season, week)

    # Make graph all of these
    # I might now even need a choice option.
    # Save them into a folder called Plots
    
    print("End")


main()
