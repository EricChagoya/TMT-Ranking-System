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
def getNewPlayerData(season: int, week: int, cummulativeWeek: int) -> 'df':
    """Get the total number of attendees, number of returning players, and
    number of unique players for each tournament.
    [TotalnumAttendees, oldPlayers, newPlayers] """
    # Need to completely change this function
    Placements = f'Data/Season{season}/Records/S{season}W{week}Placements.csv'
    Placements = pd.read_csv(Placements, encoding = "ISO-8859-1")

    Mains = 'Data/PlayerMains.csv'
    Mains = pd.read_csv(Mains, encoding = 'utf-8-sig')
    
    # Finds the cummulative weeks for the past N weeks
    display = 12
    startWeek = cummulativeWeek - display + 1
    if startWeek < 1:
        startWeek = 1
    weeksSeason = [i for i in range(startWeek, cummulativeWeek + 1)]
    count = {i: [0, 0, 0] for i in range(startWeek, cummulativeWeek + 1)}
    newPlayers = {row['SmasherID']:row['FirstTMT'] for index, row in Mains.iterrows() \
                                                      if row['FirstTMT'] in weeksSeason}

    for _, row in Placements.iterrows():
        placed = [row[f'PWeek{i}'] for i in range(1, week + 1)]
        attended = [i > -2 for i in placed]     # Which tournaments did they enter

        for i in range(1, week + 1):
            currentWeek = i + startWeek - 1
            count[currentWeek][0] += attended[i - 1]
            
            # New Player
            if (row['SmasherID'] in newPlayers) and (newPlayers[row['SmasherID']] == currentWeek):
                count[currentWeek][2] += 1
            else:                           # Returning Player
                if attended[i - 1] == 1:
                    count[currentWeek][1] += 1
##            A bug where we are counting wrong by 1 sometimes
##            Appears for cummulative weeks 1- 4
##            if count[currentWeek][0] != (count[currentWeek][1] + count[currentWeek][2]):
##                print(row['SmasherID'], row['SmashTag'], "Week:", currentWeek)
##                print(count[currentWeek][0])
##                print(count[currentWeek][1] + count[currentWeek][2])
##                print(count)
##                return

    df = pd.DataFrame.from_dict(count, orient ='index')
    column_names = {0: 'Total',
                    1: 'Returning Players',
                    2: 'New Players'}
    return df.rename(columns = column_names)



def NewPlayersGraph(season: int, week: int, cummulativeWeek: int, FORMAT: int) -> None:
    """Plots a bar graph of the total number of attendees, returning players,
    and players who have never entered a TMT. """
    Entrants = getNewPlayerData(season, week, cummulativeWeek)
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
    presentFile(fig, FORMAT, f"Data/Season{season}/PlotsStaff/S{season}W{week}NewPlayers.jpeg")



# 8
def getBarGraphDataEntrants(season: int, week: int) -> [int]:
    """It collects to see how often someone enters TMT 1 time, 2 times,...,
    for the whole season. """
    entrants = [0 for i in range(week)]
    Placements = f'Data/Season{season}/Records/S{season}W{week}Placements.csv'
    Placements = pd.read_csv(Placements, encoding = "ISO-8859-1")
    for _, row in Placements.iterrows():
        numTournamentEntered = sum([row[f'PWeek{i}'] >= -1 for i in range(1, week + 1)])
        entrants[numTournamentEntered - 1] += 1
    return entrants


def BarGraphEntrants(season: int, week: int, FORMAT: int) -> None:
    """It plots a histogram of how often someone enters TMT. Only does for
    the current season."""
    entrants = getBarGraphDataEntrants(season, week)
    x = [i for i in range(1, week + 1)]

    fig = go.Figure(data=[go.Bar(x=x, y= entrants,
                                 text= entrants,
                                 textposition='outside')])

    fig.update_layout(title = f'Number of Times People Entered in Season {season}')
    fig.update_layout(xaxis_title = 'Entered N Times')
    fig.update_layout(xaxis = dict(tickvals = [i for i in range(1, week + 1)],
                                   ticktext = [f'{i}' for i in range(1, week + 1)]))
                                   #ticktext = [f'Week {i}' for i in range(1, week + 1)]))
    fig.update_layout(yaxis_title = 'Entrants')

    fig.update_layout(font = dict(size= 30))
    fig.update_layout(showlegend = False)
    presentFile(fig, FORMAT, f"Data/Season{season}/PlotsStaff/S{season}W{week}BarGraphEntrants.jpeg")
    


# 9
def getRevenueData() -> 'df':
    Revenue = f'Data/TMTRevenue.csv'
    Revenue = pd.read_csv(Revenue, encoding = "ISO-8859-1")
    Total = dict()          # {Week Number: [Revenue, Loss, Overall Profit]}
    overallTotal = 0
    for _, row in Revenue.iterrows():
        if row['Week'] not in Total:
            Total[row['Week']] = [0, 0, overallTotal]
        if row['Amount'] >= 0:
            Total[row['Week']][0] += row['Amount']
        else:
            Total[row['Week']][1] += row['Amount']
        overallTotal += row['Amount']
        Total[row['Week']][2] = overallTotal
        
    df = pd.DataFrame()
    for k, v in sorted(Total.items()):
        new_row = {'Revenue': v[0], 'Loss': v[1] * -1, 'Overall Profit': v[2]}
        #new_row = {'Revenue': v[0], 'Loss': v[1], 'Overall Profit': v[2]}
        df = df.append(new_row, ignore_index = True)
    return df[['Revenue', 'Loss', 'Overall Profit']]
    

def Revenue(season, week, FORMAT) -> None:
    """Graphs how much revenue, loss, and profit we have"""
    Total = getRevenueData()
    numWeeks = Total.shape[0]
    Display = 12         # Only display the last 10 weeks
    Total = Total.tail(Display)
    t = Total.shape[0]


    weeks = [f'Week {i + 1}' for i in range(numWeeks - t, numWeeks)]

    fig = go.Figure()
    fig.add_trace(go.Bar(x = weeks, y = Total['Revenue'],
                         name = 'Revenue', marker_color = '#33cc33'))
    fig.add_trace(go.Bar(x = weeks, y = Total['Loss'],
                         name = 'Loss', marker_color = '#cc0000'))
    fig.add_trace(go.Bar(x = weeks, y = Total['Overall Profit'],
                         name = 'Overall Profit', marker_color = '#ffff4d'))
    fig.update_layout(title = f'Total Revenue')
    fig.update_layout(yaxis_title = 'Money')

    fig.update_layout(font = dict(size= 30))
    fig.update_layout(showlegend = True)
    fig.update_layout(legend = dict(font_size = 30))
    presentFile(fig, FORMAT, f"Data/Season{season}/PlotsStaff/S{season}W{week}Revenue.jpeg")



