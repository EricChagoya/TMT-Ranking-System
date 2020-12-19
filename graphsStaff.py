import math
import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

pio.kaleido.scope.default_height = 1200
pio.kaleido.scope.default_width = 2400



def presentFile(fig: 'Plotly', FORMAT: int, location:str) -> None:
    """We either display on HTML or save it as a picture."""
    if FORMAT == 0:
        fig.show()
    else:
        fig.write_image(location)


# 6
def getCoastData(season: int, week: int) -> 'df':
    """Get the total number of combined, West Coast, and East Coast entrants
    for each week. The last column is for people we aren't sure of.
    [Total, WC, EC, NA]"""
    Features = f'Data/Season{season}/Records/S{season}W{week}Features.csv'
    Features = pd.read_csv(Features, encoding = "ISO-8859-1")
    Placements = f'Data/Season{season}/Records/S{season}W{week}Placements.csv'
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


def CoastEntrantsGraph(season: int, week: int, FORMAT:int) -> None:
    """Plot a bar graph of the total number of attendees, number of
    West Coast and number of East Coast attendees for each week"""
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
    presentFile(fig, FORMAT, f"Data/Season{season}/PlotsStaff/S{season}W{week}EntrantsCoasts.jpeg")


# 7
def getNewPlayerData(season, week) -> 'df':
    """Get the total number of attendees, number of returning players, and
    number of unique players for each tournament.
    [TotalnumAttendees, oldPlayers, newPlayers] """
    # Need to completely change this function
    
    Placements = f'Data/Season{season}/Records/S{season}W{week}Placements.csv'
    Placements = pd.read_csv(Placements, encoding = "ISO-8859-1")
    players = {row['SmasherID'] for index, row in Placements.iterrows()}
    # Used to determine new players. Change this later for season 2

    count = {i: [0, 0, 0] for i in range(1, week + 1)}
    # Key is the Week number
    # Values are [TotalnumAttendees, oldPlayers, newPlayers]
    t= 0
    for _, row in Placements.iterrows():
        placed = [row[f'PWeek{i}'] for i in range(1, week + 1)]
        attended = [i > -2 for i in placed]     # Which tournaments did they enter
        #madeBracket = [i > -1 for i in placed]  # Which tournaments did they make bracket

        for i in range(1, week + 1):
            count[i][0] += attended[i - 1]
            #count[i][3] += madeBracket[i - 1]
            if row['SmasherID'] in players:     # New Player
                if attended[i - 1] == 1:
                    count[i][2] += 1
                    players.remove(row['SmasherID'])
            else:                               # Returning Player
                if attended[i - 1] == 1:
                    count[i][1] += 1
                
    df = pd.DataFrame.from_dict(count, orient ='index')
    column_names = {0: 'Total',
                    1: 'Returning Players',
                    2: 'New Players'}
                    #3: 'Players In Bracket'}
##    0   1   2
##1   60   0  60
##2   54  19  35
    return df.rename(columns = column_names)


def NewPlayersGraph(season: int, week: int, FORMAT: int) -> None:
    """Plots a bar graph of the total number of attendees, returning players,
    and players who have never entered a TMT. """
    Entrants = getNewPlayerData(season, week)
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

    fig.update_layout(font = dict(size= 30))
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 30))
    presentFile(fig, FORMAT, f"Data/Season{season}/PlotsStaff/S{season}W{week}TMTDetails.jpeg")



