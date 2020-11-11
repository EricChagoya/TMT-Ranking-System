import numpy as np
import pandas as pd

# You need to pipinstall numpy and pandas
# pip install numpy
# pip install pandas


POINT_WIN = 1   # Need to change this so max is 20
POINT_PROSPECT = 1
POINT_ROOKIE = 5
POINT_PRO = 10
POINT_ALL_STAR = 15
POINT_HALL_OF_FAME = 20
POINT_FLOATED_PLAYER = 15

PLACEMENTS = {1: 200,
              2: 175,
              3: 150,
              4: 125,
              5: 95,
              7: 75,
              9: 45,
              13: 25,
              17: 10,
              25: 0}
# We need to manually change what placing 0-2 for final bracket
# Or else people in ladder can get points for being in final bracket


# Make some type of chart for abbreviations
# Placement. -1 means they didn't place that week. Any number above 0 is what they placed.
# Placements will have a string of all placeings. -2 means they didn't enter that week.
# Still need to make these changes
# I need to document it better.


def PrintWelcomeMessage() -> None:
    print("Hi There!")
    print("The Architect here! OmegaLUL\n")
    print("Which option would you like? (Press the number you want)")
    print("\t1. Update the Ladder Rankings")
    print("\t2. Update the Bracket Rankings")


def UserChoice() -> int:
    """The user decides what option they want"""
    while True:
        option = input("")
        try:
            option = int(option)
        except:
            pass
        if option in (1, 2):
            return option
        else:
            print("Choose 1 or 2\n")


def UserWeek() -> int:
    """The user decides what week it is"""
    while True:
        week = input("What week is it? (Week of the Season) ")
        try:
            week = int(week)
            if week > 0:
                return week
            else:
                print("Please choose an integer greater than 0")
        except:
            print("Please Choose an integer\n")       



def WeeklyScorePointsWeek1(WSLfile:str, WSBfile:str, WTPfile:str, TPfile:str) -> None:
    WSL = pd.read_csv(WSLfile, encoding = "ISO-8859-1")
    WSB = pd.read_csv(WSBfile, encoding = "ISO-8859-1")
    
    WTP = WSL
    WTP['SmasherID'] = WTP['SmasherID'].astype(str)
    WSB['SmasherID'] = WSB['SmasherID'].astype(str)

    # bandaid
    WTP['Placement'] = -1

    for i, SmashTag in enumerate(WSB['SmashTag']):    # I think this can be faster (future)
    #for i, SmasherID in enumerate(WSB['SmasherID']):    # I think this can be faster (future)
        #print(i, SmasherID)
        t= WTP[WTP['SmashTag'].isin([SmashTag])]
        #print(t, SmashTag)
        #t= WTP[WTP['SmasherID'].isin([SmasherID])]
        #print(t)
        index= t.index[0]
        WTP.at[index, 'Wins']= WTP['Wins'][index] + WSB['Wins'][i]
        WTP.at[index, 'Losses']= WTP['Losses'][index] + WSB['Losses'][i]
        WTP.at[index, 'Placement']= WSB['Placement'][i]

    WTP['WinPercentage'] = WTP['Wins']/ (WTP['Wins'] + WTP['Losses'])
    WTP.to_csv(WTPfile, index= False)
    
    # WTP['AllPlacements'] = WSL['Placement']     # Placement for that week
    # WTP['AllPlacements'] = WTP['AllPlacements'].astype(str)
    WTP.to_csv(TPfile, index= False)



def RankLadder(WSLfile:str, WRLfile:str) -> None:
    """Rank ladder for that week. """
    WSL = pd.read_csv(WSLfile)
    print(WSLfile)

    WSL['Points']= WSL.apply(lambda row: row.Wins + row.Prospect*POINT_PROSPECT + \
                             row.Rookie*POINT_ROOKIE + row.Pro*POINT_PRO + \
                             row.AllStar*POINT_ALL_STAR + row.HallOfFame*POINT_HALL_OF_FAME, axis= 1)
    WSL['Rank'] = (WSL['Points'] * -1).rank(method= 'max')
    WSL['WinPercentage'] = WSL['Wins']/ (WSL['Wins'] + WSL['Losses'])
    WSL.to_csv(WRLfile, index= False)


def RankWeeklyBoth(WTPfile: str, WRBfile: str) -> None:
    """Rank Ladder and Bracket for that week."""
    WTP = pd.read_csv(WTPfile)
    WTP["PlacePoints"] = WTP['Placement']
    WTP["PlacePoints"] = WTP["PlacePoints"].map(PLACEMENTS)
    WTP["PlacePoints"] = WTP["PlacePoints"].fillna(0)

    WTP['Points']= WTP.apply(lambda row: row.Wins + row.Prospect*POINT_PROSPECT + \
                             row.Rookie*POINT_ROOKIE + row.Pro*POINT_PRO + \
                             row.AllStar*POINT_ALL_STAR + row.HallOfFame*POINT_HALL_OF_FAME + \
                             row.PlacePoints, axis= 1)

    WTP['Rank'] = (WTP['Points'] * -1).rank(method= 'max')
    WTP.to_csv(WRBfile, index= False)


def RankTotalPoints(TPfile:str, TRfile:str) -> None:
    """It will give value to each column to determine the ranks for
    the entire season."""
    pass
    


def WebsiteWeeklyRank(WRfile:str, SWRfile:str) -> None:
    """ It does not change anything about the data. It moves and removes columns
    so it is more presentable for the website. This is used by both the weekly
    ladder and bracket rank."""
    WR = pd.read_csv(WRfile)
    WR = WR.rename(columns = {'Points':'BankRoll Bills'})
    WR = WR[['Rank', 'BankRoll Bills', 'SmashTag',
             'Wins', 'Losses', 'WinPercentage']]
    WR= WR.sort_values(by= 'Rank')
    WR = WR.round(3)
    WR.to_csv(SWRfile, index= False)


def WebsiteWeeklyTotalRank(TRfile:str, STRfile:str) -> None:
    # Keep for now. We might want different columns for each file.
    # The total can include more information
    """ It does not change anything about the data. It moves and removes columns
    so it is more presentable for the website."""
    TR = pd.read_csv(TRfile)
    TR = TR.rename(columns = {'Points':'BankRoll Bills'})
    TR = TR[['Rank', 'BankRoll Bills', 'SmashTag',
             'Wins', 'Losses', 'WinPercentage']]
    TR= TR.sort_values(by= 'Rank')
    TR = TR.round(3)
    TR.to_csv(STRfile, index= False)




def main():
    #PrintWelcomeMessage()
    #choice = UserChoice()
    #week = UserWeek()
    choice = 2
    week = 1

    # Input files    
    WSL = "WeeklyScoresLadder" + str(week) + ".csv"     
    WSB = "WeeklyScoresBracket" + str(week) + ".csv"

    # Total Points
    WTP = "WeeklyTotalPoints" + str(week) + ".csv"   # It combines the points from Ladder and Bracket
    oldTP = "TotalPoints" + str(week - 1) + ".csv"   # Last week's Total Points
    TP = "TotalPoints" + str(week) + ".csv"          # Counts all the points from all cummulative weeks
    
    # These next two apply the ranking formula
    WRL = "WeeklyRankLadder" + str(week) + ".csv"   # Points for ladder that week's ladder
    WRB = "WeeklyRankBoth" + str(week) + ".csv"     # Points for ladder and bracket for the week
    TR = "TotalRank" + str(week) + ".csv"           # Points for the entire season

    # These three will go on the website
    SWLR = "SubsetWeeklyLadderRank" + str(week) + ".csv"
    SWBR = "SubsetWeeklyBracketRank" + str(week) + ".csv"
    STR = "SubsetTotalRanks" + str(week) + ".csv"
    


    if choice == 1:
        RankLadder(WSL, WRL)
        WebsiteWeeklyRank(WRL, SWLR)
    else:
        if week == 1:
            WeeklyScorePointsWeek1(WSL, WSB, WTP, TP)   # 2 inputs, 2 outputs
        else:
            #WeeklyScorePoints(WSL, WSB, oldTP, WTP, TP) # 3 inputs, 2 outputs   # Not Done
            pass

        RankWeeklyBoth(WTP, WRB)
        # RankTotalPoints(TP, TR)     # Not Done

        WebsiteWeeklyRank(WRB, SWBR)
        # WebsiteTotalRank(TR, STR)  # Not Done



main()


"""
These I need to work on\
1. WeeklyScorePoint() So I can add this week's ranking to the last couple
2. Document better
3. Make the code cleaner
4. Document the github better
5. List of terminology
6. Learn Github 
"""



