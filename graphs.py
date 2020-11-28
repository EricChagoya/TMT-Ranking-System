import math
import numpy as np
import pandas as pd
import UserInterface as UI

import plotly.graph_objects as go
# pip install plotly


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
        fig.add_trace(go.Scatter(x= x_range, y= playerRank, name= playerTag,
                         line=dict(color= colors[index % len_colors], width=4)))

    fig.update_layout(title = f'Season {season} Ranks')
    fig.update_layout(xaxis_title='Week Number')
    fig.update_layout(yaxis_title='Rank')
    fig.update_layout(showlegend = True)
    fig.update_layout(legend=dict(font_size=16))
    
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
        fig.add_trace(go.Scatter(x= x_range, y= playerPoints, name= playerTag,
                         line=dict(color= colors[index % len_colors], width=4)))

    fig.update_layout(title = f'Season {season} BankRoll Bills')
    fig.update_layout(xaxis_title='Week Number')
    fig.update_layout(yaxis_title='Bills')
    fig.update_layout(showlegend = True)
    fig.update_layout(legend=dict(font_size=16))
    
    fig.update_xaxes(nticks = week)
    fig.show()


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
    return pd.DataFrame.from_dict(count, orient ='index')

    
def CreateEntrantsCoastGraph(season: int, week: int) -> None:
    Entrants = getCoastData(season, week)
    print(Entrants)

    

    

    
    

    




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
    else:
        CreateEntrantsCoastGraph(season, week)

    # Make graph all of these
    # Save them into a folder called Plots
    


    print("End")


main()
