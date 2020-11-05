import numpy as np
import pandas as pd

# You need to pipinstall numpy and pandas
# pip install numpy
# pip install pandas


# We will change this
# These are temporary values
POINT_WIN = 1
POINT_PROSPECT = 10
POINT_ROOKIE = 20
POINT_PRO = 50

PLACEMENTS = {1: 250,
              2: 200,
              3: 150,
              4: 125,
              5: 100,
              7: 75,
              9: 50,
              13: 30,
              17: 20,
              25: 10,
              33: 5}


# Make some type of chart for abbreviations
# Placement. -1 means they didn't place that week. Any number above 0 is what they placed.
# Placements will have a string of all placeings. -2 means they didn't enter that week.

# I need to document it better.


def TotalPointsFirstWeekLadder(WSL1file:str, TPv1file:str) -> None:
    """For the first week there hasn't been a TotalPoints so we create it."""
    WSL = pd.read_csv(WSL1file, sep = "\t")  # df- dataframe
    WSL['NumTimesBracket'] = 0
    WSL['Placement'] = -1
    WSL['NumTourneysEntered'] = 1
    #print(df.shape)
    #print(type(df))
    print(df)
    print(df.columns)
    df.to_csv(TPv1file, sep = "\t", index= False)


def TotalPointBracket(TPv1file:str, WSBfile:str, outputFile:str) -> None:
    """Add final bracket results to the points."""
    TPv1 = pd.read_csv(TPv1file, sep = "\t")
    WSB = pd.read_csv(WSBfile, sep = "\t")


    # append WSB to TPv1
    # If they are in bracket, identical SmasherID, then replace Wins, Placements,
    # increment NumTimesBracket
    TPv1.to_csv(outputFile, sep = "\t")


def RankLadder(WSLfile:str, WRLfile:str) -> None:
    """Rank ladder for that week. """
    WSL = pd.read_csv(WSLfile, sep = "\t")

    WSL['Points']= WSL.apply(lambda row: row.Wins + row.Prospect*POINT_PROSPECT + \
                             row.Rookie*POINT_ROOKIE + row.Pro*POINT_PRO, axis= 1)
    WSL['Rank'] = (WSL['Points'] * -1).rank(method= 'max')
    WSL['WinPercentage'] = WSL['Wins']/ (WSL['Wins'] + WSL['Losses'])
    WSL.to_csv(WRLfile, sep = "\t", index= False)


def WebsiteWeeklyLadderRank(WRLfile:str, SWRfile:str) -> None:
    """ It does not change anything about the data. It moves and removes columns
    so it is more presentable for the website."""
    WRL = pd.read_csv(WRLfile, sep = "\t")
    WRL = WRL[['Rank', 'SmashTag', 'Wins', 'Losses', 'WinPercentage']]
    WRL= WRL.sort_values(by= 'Rank')
    WRL = WRL.round(3)
    WRL.to_csv(SWRfile, sep = "\t", index= False)




def main():
    #week = int(input("What week is it? ") )
    # Make some type of interface when I only have ladder, or add ladder and bracket.


    week = 1
    
    WSL = "WeeklyScoresLadder" + str(week) + ".txt"
    WSB = "WeeklyScoresBracket" + str(week) + ".txt"

    WTP = "WeeklyTotalPoint" + str(week) + ".txt"   # It combines the points from Ladder and Bracket
    TP = "TotalPoint" + str(week) + ".txt"          # Counts all the points from all cummulative weeks
    oldTP = "TotalPoint" + str(week - 1) + ".txt"   # Last week's Total Points
    
    # These next two apply the ranking formula
    WRL = "WeeklyRankLadder" + str(week) + ".txt"
    WRB = "WeeklyRankBoth" + str(week) + ".txt"
    TR = "TotalRank" + str(week) + ".txt"

    # These next two will go on the website
    SWR = "SubsetWeeklyRank" + str(week) + ".txt"
    STR = "SubsetTotalRanks" + str(week) + ".txt"
    
    category = "both"
    changeRankOnly = False  # used if you only want to change the formula

    if category == "ladder":
        # I don't need to include changeRankOnly bc I can only a ranking formula to it. Nothing else
        RankLadder(WSL, WRL)
        WebsiteWeeklyLadderRank(WRL, SWR)

    elif (category == "both") and (week == 1) and (changeRankOnly == False):
        # WeeklyScorePointsWeek1(WSL, WSB, WTP, TP)  2 inputs, 2 outputs
        
        # RankWeeklyBoth(WTP, WRB)
        # RankTotalPoints(TP, TR)

        # WebsiteWeeklyRank(WRB, SWR)
        # WebsiteTotalRank(TR, STR)
        pass

    
    elif (category == "both") and (changeRankOnly == False):
        # WeeklyScorePoints(WSL, WSB, oldTP, WTP, TP)  3 inputs, 2 outputs
        
        # RankWeeklyBoth(WTP, WRB)
        # RankTotalPoints(TP, TR)

        # WebsiteWeeklyRank(WRB, SWR)
        # WebsiteTotalRank(TR, STR)
        pass

    elif (category == "both") and (changeRankOnly):     # Used for change Formula
        # RankWeeklyBoth(WTP, WRB)
        # RankTotalPoints(TP, TR)

        # WebsiteWeeklyRank(WRB, SWR)
        # WebsiteTotalRank(TR, STR)
        pass
        
    # I am going to fix this awful if elif





main()
