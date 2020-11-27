import numpy as np
import pandas as pd
import UserInterface as UI

import plotly.graph_objects as go
# pip install plotly


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
        playerRank = [row[i] for i in range(2, week + 2)]
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





def main():
    #UI.PrintGraphWelcomeMessage()
    #choice = UI.graphChoice()
    #season = UI.UserSeason()
    #week = UI.UserWeek()
    choice = 0
    season = 1
    week = 3
    
    if choice == 1:
        CreateRankGraph(season, week)
    elif choice == 2:
        pass
    else:
        pass
    


    print("End")


main()
