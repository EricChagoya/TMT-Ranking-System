import os
import numpy as np
import pandas as pd
import UserInterface as UI
import RankingFormula as RF




def CreateDirectories(season: int) -> None:
    """If these directories don't exists, it will create them"""
    if not os.path.exists(f'Data/Season{season}/Debug'):
        os.mkdir(f'Data/Season{season}/Debug')
    if not os.path.exists(f'Data/Season{season}/Records'):
        os.mkdir(f'Data/Season{season}/Records')
    if not os.path.exists(f'Data/Season{season}/Website'):
        os.mkdir(f'Data/Season{season}/Website')
    if not os.path.exists(f'Data/Season{season}/WeeklyLadderBracket'):
        os.mkdir(f'Data/Season{season}/WeeklyLadderBracket')



def CreateWeeklyResults(WeeklyScoresLadderfile: str, WeeklyScoresBracketfile: str,
                        WeeklyResultsfile: str,week: int) -> None:
    """It combines the scores from ladder and bracket into one file."""
    WSL = pd.read_csv(WeeklyScoresLadderfile, encoding = "ISO-8859-1")
    WSB = pd.read_csv(WeeklyScoresBracketfile, encoding = "ISO-8859-1")
    WR = WSL    # WeeklyResults

    WR['Placement'] = -1
    WR['Floated'] = 0
    RF.LimitLadderWins(WR)

    count = 0
    for index, row in WSB.iterrows():   # Add bracket player results to ladder
        inLadder = WR[WR['SmasherID'].isin([row['SmasherID']])]
        if len(inLadder) > 0:   # Did the player enter ladder
            index = inLadder.index[0]
            WR.at[index, 'Wins'] = WR['Wins'][index] + row['Wins']
            WR.at[index, 'Losses'] = WR['Losses'][index] + row['Losses']
            WR.at[index, 'Placement'] = row['Placement']
        else:
            new_row = {'SmasherID': row['SmasherID'],   # Player did not enter ladder
                       'SmashTag': row['SmashTag'],
                       'Coast': 'NOTAV',
                       'Wins': row['Wins'],
                       'Losses': row['Losses'],
                       'LimitLadderWins': 0,
                       'Prospect': 0,
                       'Rookie': 0,
                       'Pro': 0,
                       'AllStar': 0,
                       'HallOfFame': 0,
                       'Floated': 1,
                       'Placement': row['Placement']}
            WR = WR.append(new_row, ignore_index=True)

    WR = WR[['SmasherID', 'SmashTag', 'Coast', 'Wins', 'Losses',
             'LimitLadderWins', 'Prospect', 'Rookie', 'Pro',
             'AllStar', 'HallOfFame', 'Floated', 'Placement']]
    WR = WR.sort_values(by = 'SmasherID')
    WR.to_csv(WeeklyResultsfile, index=False, encoding = "ISO-8859-1")



def UpdateTiers(WeeklyResultsfile: str, oldFeaturesfile: str, Featuresfile: str, week: int):
    """It updates a player's wins, losses, and number of times they were in
    Prospect, ..., Floated to previous weeks"""
    WR = pd.read_csv(WeeklyResultsfile, encoding = "ISO-8859-1")
    if week != 1:
        Features = pd.read_csv(oldFeaturesfile, encoding = "ISO-8859-1")
        for index, row in WR.iterrows():
            inThisWeek = Features[Features['SmasherID'].isin([row['SmasherID']])]
            if len(inThisWeek) > 0:     # Has the player entered before
                index = inThisWeek.index[0]
                Features.at[index, 'SmashTag'] = row['SmashTag']  # If someone changes their tag
                Features.at[index, 'Wins'] = Features['Wins'][index] + row['Wins']
                Features.at[index, 'Losses'] = Features['Losses'][index] + row['Losses']
                Features.at[index, 'LimitLadderWins'] = Features['LimitLadderWins'][index] + row['LimitLadderWins']
                Features.at[index, 'Prospect'] = Features['Prospect'][index] + row['Prospect']
                Features.at[index, 'Rookie'] = Features['Rookie'][index] + row['Rookie']
                Features.at[index, 'Pro'] = Features['Pro'][index] + row['Pro']
                Features.at[index, 'AllStar'] = Features['AllStar'][index] + row['AllStar']
                Features.at[index, 'HallOfFame'] = Features['HallOfFame'][index] + row['HallOfFame']
                Features.at[index, 'Floated'] = Features['Floated'][index] + row['Floated']
            else:
                new_row = {'SmasherID': row['SmasherID'],   # Player's first time entering
                           'SmashTag': row['SmashTag'],
                           'Coast': row['Coast'],
                           'Wins': row['Wins'],
                           'Losses': row['Losses'],
                           'LimitLadderWins': row['LimitLadderWins'],
                           'Prospect': row['Prospect'],
                           'Rookie': row['Rookie'],
                           'Pro': row['Pro'],
                           'AllStar': row['AllStar'],
                           'HallOfFame': row['HallOfFame'],
                           'Floated': row['Floated']}
                Features = Features.append(new_row, ignore_index=True)
    else:
        Features = WR[['SmasherID', 'SmashTag', 'Coast', 'Wins', 'Losses',
                       'LimitLadderWins', 'Prospect', 'Rookie', 'Pro',
                       'AllStar', 'HallOfFame', 'Floated']]
    Features = Features.sort_values(by = 'SmasherID')
    Features.to_csv(Featuresfile, index=False, encoding = "ISO-8859-1")


def FindTournamentEntrants(Placement: 'df', week: int) -> None:
    """Find out how many times a player entered the season and how
    many times they made it into final bracket.
    -1 if they entered ladder but didn't make bracket
    -2 if they didn't enter that week"""
    Placement['NumTMTEntered'] = 0
    Placement['NumInBracket'] = 0
    for index, row in Placement.iterrows():
        nTMTEntered = 0
        nInBracket = 0
        for i in range(1, week + 1):
            weeklyPlacement = row[f'PWeek{i}']
            if weeklyPlacement > -2:
                nTMTEntered += 1
            if weeklyPlacement > -1:
                nInBracket += 1
        Placement.at[index, 'NumTMTEntered'] = nTMTEntered
        Placement.at[index, 'NumInBracket'] = nInBracket


def UpdatePlacements(WeeklyResultsfile, oldPlacementsfile:str, Placementsfile:str, week:int):
    """Appends this week's bracket placement to previous weeks.
    -1 means they did not make bracket.
    -2 means they did not enter that week."""
    WR = pd.read_csv(WeeklyResultsfile, encoding = "ISO-8859-1")
    if week != 1:
        Placement = pd.read_csv(oldPlacementsfile, encoding = "ISO-8859-1")
        Placement[f'PWeek{week}'] = -2
        for index, row in WR.iterrows():
            oldPlayer = Placement[Placement['SmasherID'].isin([row['SmasherID']])]
            if len(oldPlayer) > 0:  # Have they entered before?
                index = oldPlayer.index[0]
                Placement.at[index, 'SmashTag'] = row['SmashTag']  # If someone changes their tag
                Placement.at[index, f'PWeek{week}'] = row['Placement']
            else:
                new_row = {'SmasherID': row['SmasherID'],   # New TMT Entrant
                           'SmashTag': row['SmashTag'],
                           f'PWeek{week}': row['Placement']}
                for i in range(1, week):
                    new_row[f'PWeek{i}'] = -2
                Placement = Placement.append(new_row, ignore_index = True)
    else:
        WR['NumTMTEntered'] = 0
        WR['NumInBracket'] = 0
        Placement = WR[['SmasherID', 'SmashTag', 'NumTMTEntered',
                        'NumInBracket', 'Placement']]
        Placement = Placement.rename(columns={'Placement': 'PWeek1'})
        
    FindTournamentEntrants(Placement, week)
    Placement = Placement.sort_values(by = 'SmasherID')
    Placement.to_csv(Placementsfile, index=False, encoding = "ISO-8859-1")


def RankLadder(WeeklyScoresLadderfile: str, WeeklyRankLadderfile: str) -> None:
    """Rank ladder for that week. """
    WSLadder = pd.read_csv(WeeklyScoresLadderfile, encoding = "ISO-8859-1")
    RF.LimitLadderWins(WSLadder)
    RF.FormulaLadder(WSLadder)
    WSLadder['Rank'] = (WSLadder['Points'] * -1).rank(method = 'min')
    WSLadder.to_csv(WeeklyRankLadderfile, index = False, encoding = "ISO-8859-1")


def RankWeekly(WeeklyResultsfile: str, WeeklyRankfile: str) -> None:
    """Rank Ladder and Bracket for that week."""
    WeeklyResults = pd.read_csv(WeeklyResultsfile, encoding = "ISO-8859-1")
    RF.PlacementPointsWeekly(WeeklyResults)
    RF.FormulaWeekly(WeeklyResults)
    WeeklyResults['Rank'] = (WeeklyResults['Points'] * -1).rank(method = 'min')
    WeeklyResults.to_csv(WeeklyRankfile, index = False, encoding = "ISO-8859-1")


def RankSeason(Featuresfile: str, Placementsfile: str, week: int) -> None:
    """It will give value to each column to determine the ranks for
    the entire season."""
    Features = pd.read_csv(Featuresfile, encoding = "ISO-8859-1")
    Placements = pd.read_csv(Placementsfile, encoding = "ISO-8859-1")
    RF.PlacementPointsSeason(Placements, week)
    RF.FormulaTotalSeason(Features, Placements)
    Features['Rank'] = (Features['Points'] * -1).rank(method = 'min')
    Features.to_csv(Featuresfile, index = False, encoding = "ISO-8859-1")


def ChangeRank(Featuresfile: str, oldRankRecordsfile: str, week: int, RankRecordsfile: str):
    """It keeps track of someone's rank for each week."""
    Features = pd.read_csv(Featuresfile, encoding = "ISO-8859-1")
    if week != 1:
        RankRecords = pd.read_csv(oldRankRecordsfile, encoding = "ISO-8859-1")
        for index, row in Features.iterrows():
            oldPlayer = RankRecords[RankRecords['SmasherID'].isin([row['SmasherID']])]
            if len(oldPlayer) > 0:      # Have they entered before?
                index = oldPlayer.index[0]
                RankRecords.at[index, 'SmashTag'] = row['SmashTag']  # If someone changes their tag
                RankRecords.at[index, f'RWeek{week}'] = row['Rank']
                RankRecords.at[index, 'ChangeInRank'] = RankRecords.at[index, f'RWeek{week - 1}'] - \
                                                        RankRecords.at[index, f'RWeek{week}']
            else:
                new_row = {'SmasherID': row['SmasherID'],   # New TMT Entrant
                           'SmashTag': row['SmashTag'],
                           f'RWeek{week}': row['Rank'],
                           'ChangeInRank': 'NAN'}
                for i in range(1, week):
                    new_row[f'RWeek{i}'] = 'NAN'
                RankRecords = RankRecords.append(new_row, ignore_index = True)
        temp= RankRecords['ChangeInRank']     # Used to move a column
        RankRecords = RankRecords.drop(['ChangeInRank'], axis = 1)
        RankRecords['ChangeInRank'] = temp
    else:
        RankRecords = Features[['SmasherID', 'SmashTag', 'Rank']]
        RankRecords = RankRecords.rename(columns = {'Rank': 'RWeek1'})
        RankRecords['ChangeInRank'] = 'New'
    RankRecords = RankRecords.sort_values(by = 'SmasherID')
    RankRecords.to_csv(RankRecordsfile, index = False, encoding = "ISO-8859-1")


def UpdatePoints(Featuresfile: str, oldPastPoints: str, PastPointsfile: str, week: int) -> None:
    """It keeps tracks of how many points everybody got every week"""
    Features = pd.read_csv(Featuresfile, encoding = "ISO-8859-1")
    if week != 1:
        PastPoints = pd.read_csv(oldPastPoints, encoding = "ISO-8859-1")
        for index, row in Features.iterrows():
            oldPlayer = PastPoints[PastPoints['SmasherID'].isin([row['SmasherID']])]
            if len(oldPlayer) > 0:      # Have they entered before?
                index = oldPlayer.index[0]
                PastPoints.at[index, 'SmashTag'] = row['SmashTag']  # If someone changes their tag
                PastPoints.at[index, f'BWeek{week}'] = row['Points']
            else:
                new_row = {'SmasherID': row['SmasherID'],   # New TMT Entrant
                           'SmashTag': row['SmashTag'],
                           f'BWeek{week}': row['Points']}
                for i in range(1, week):
                    new_row[f'BWeek{i}'] = 'NAN'
                PastPoints = PastPoints.append(new_row, ignore_index = True)
    else:
        PastPoints = Features[['SmasherID', 'SmashTag', 'Points']]
        PastPoints = PastPoints.rename(columns = {'Points': 'BWeek1'})
    PastPoints = PastPoints.sort_values(by = 'SmasherID')
    PastPoints.to_csv(PastPointsfile, index = False, encoding = "ISO-8859-1")

    
def WebsiteWeeklyRank(WeeklyRankfile: str, WebWeeklyRankfile: str) -> None:
    """ It does not change anything about the data. It moves and removes columns
    so it is more presentable for the website. This is used by both the weekly
    ladder and bracket rank."""
    WeeklyRank = pd.read_csv(WeeklyRankfile, encoding = "ISO-8859-1")
    WeeklyRank = WeeklyRank.rename(columns={'Points': 'Bankroll Bills'})
    WeeklyRank['Win%'] = 100*WeeklyRank['Wins'] / (WeeklyRank['Wins'] + WeeklyRank['Losses'])
    WeeklyRank = WeeklyRank.rename(columns={'SmashTag': 'Tag'})
    WeeklyRank = WeeklyRank[['Rank', 'Tag', 'Wins', 'Losses',
                             'Win%', 'Bankroll Bills']]
    
    WeeklyRank = WeeklyRank.sort_values(by='Rank')
    WeeklyRank = WeeklyRank.round(2)
    WeeklyRank.to_csv(WebWeeklyRankfile, index=False, encoding = "ISO-8859-1")


def WebsiteChangeInRank(Features: 'df') -> None:
    """Make stylistic changes to ChangeInRank so it looks better for the website"""
    Features.loc[(Features.ChangeInRank == '0.0'), 'ChangeInRank'] = "-"
    Features.loc[(Features.ChangeInRank == 'NAN'), 'ChangeInRank'] = "New"
    for index, row in Features.iterrows():
        try:
            change = float(row['ChangeInRank'])
            if change > 0:
                Features.at[index, 'ChangeInRank'] = row['ChangeInRank']
                #Features.at[index, 'ChangeInRank'] = "++ " + row['ChangeInRank']
            elif change < 0:
                Features.at[index, 'ChangeInRank'] = str(change)
                #Features.at[index, 'ChangeInRank'] = "-- " + str(-1 * change)
        except:
            pass


def WebsiteTotalRank(Featuresfile: str, RankRecordsfile: str,
                     Placementsfile:str, WebTotalRankfile: str) -> None:
    # Keep for now. We might want different columns for each file.
    # The total can include more information
    """It moves and removes columns. Changes how values are displayed
    so it is more presentable for the website."""
    Features = pd.read_csv(Featuresfile, encoding = "ISO-8859-1")
    RankRecords = pd.read_csv(RankRecordsfile, encoding = "ISO-8859-1")
    Placements = pd.read_csv(Placementsfile, encoding = "ISO-8859-1")

    Features['ChangeInRank'] = RankRecords['ChangeInRank']
    WebsiteChangeInRank(Features)

    Features['NumTMTEntered'] = Placements['NumTMTEntered']
    Features['NumInBracket'] = Placements['NumInBracket']
        
    Features = Features.rename(columns={'Points': 'Bankroll Bills'})
    Features = Features.rename(columns={'ChangeInRank': 'RankChange'})
    Features = Features.rename(columns={'SmashTag': 'Tag'})
    Features['Win%'] = 100*Features['Wins'] / (Features['Wins'] + Features['Losses'])
##    Features = Features[['Rank', 'RankChange', 'Tag', 'Coast', 'Wins', 'Losses',
##                         'Win%', 'NumTMTEntered', 'NumInBracket', 'Bankroll Bills']]
    Features = Features[['Rank', 'RankChange', 'Tag', 'Wins',
                         'Losses', 'Win%', 'Bankroll Bills']]
    
    Features = Features.sort_values(by='Rank')
    Features = Features.round(2)
    Features.to_csv(WebTotalRankfile, index=False, encoding = "ISO-8859-1")


def main():
    UI.PrintRankWelcomeMessage()
    choice = UI.rankChoice()
    season = UI.UserSeason()
    week = UI.UserWeek()
    #choice = 2
    #season = 1
    #week = 3

    CreateDirectories(season)

    # Input files
    WSL = f'Data/Season{season}/WeeklyLadderBracket/S{season}W{week}WeeklyScoresLadder.csv'
    WSB = f'Data/Season{season}/WeeklyLadderBracket/S{season}W{week}WeeklyScoresBracket.csv'

    # It combines the results of Ladders and Bracket
    WeeklyResults= f'Data/Season{season}/Debug/S{season}W{week}WeeklyResults.csv'
    oldFeatures = f'Data/Season{season}/Records/S{season}W{week - 1}Features.csv'
    Features = f'Data/Season{season}/Records/S{season}W{week}Features.csv'

    oldPlacements = f'Data/Season{season}/Records/S{season}W{week - 1}Placements.csv'
    Placements = f'Data/Season{season}/Records/S{season}W{week}Placements.csv'

    # Points for that week's ladder
    WeeklyRankLadder = f'Data/Season{season}/Debug/S{season}W{week}WeeklyRankLadder.csv'
    WeeklyRank = f'Data/Season{season}/Debug/S{season}W{week}WeeklyRank.csv'
    
    oldRankRecords = f'Data/Season{season}/Records/S{season}W{week - 1}RankRecords.csv'
    RankRecords = f'Data/Season{season}/Records/S{season}W{week}RankRecords.csv'

    oldPastPoints = f'Data/Season{season}/Records/S{season}W{week - 1}PastPoints.csv'
    PastPoints = f'Data/Season{season}/Records/S{season}W{week}PastPoints.csv'

    # These three will go on the website
    WebWLR = f'Data/Season{season}/Website/S{season}W{week}WebsiteWeeklyLadderRank.csv'
    # Ladders and Bracket Ranks
    WebWR = f'Data/Season{season}/Website/S{season}W{week}WebsiteWeeklyRank.csv'
    # Rank for the entire season
    WebTR = f'Data/Season{season}/Website/S{season}W{week}WebsiteTotalRanks.csv'


    if choice == 1:
        RankLadder(WSL, WeeklyRankLadder)
        WebsiteWeeklyRank(WeeklyRankLadder, WebWLR)
    else:
        CreateWeeklyResults(WSL, WSB, WeeklyResults, week)
        
        UpdateTiers(WeeklyResults, oldFeatures, Features, week)
        UpdatePlacements(WeeklyResults, oldPlacements, Placements, week)
        
        RankWeekly(WeeklyResults, WeeklyRank)
        RankSeason(Features, Placements, week)

        ChangeRank(Features, oldRankRecords, week, RankRecords)
        UpdatePoints(Features, oldPastPoints, PastPoints, week)
        
        WebsiteWeeklyRank(WeeklyRank, WebWR)
        WebsiteTotalRank(Features, RankRecords, Placements, WebTR)
    
        

main()




