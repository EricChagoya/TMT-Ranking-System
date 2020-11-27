import numpy as np
import pandas as pd
import UserInterface as UI
import RankingFormula as RF

# In order to run this script you will need the folders
# Debug
# Records
# Website
# WeeklyLadderBracket
# Maybe programm it to create this directory if they don't exist

def CreateWeeklyResults(WeeklyScoresLadderfile: str, WeeklyScoresBracketfile: str,
                        WeeklyResultsfile: str,week: int) -> None:
    """It combines the scores from ladder and bracket into one file."""
    WSL = pd.read_csv(WeeklyScoresLadderfile, encoding="ISO-8859-1")
    WSB = pd.read_csv(WeeklyScoresBracketfile, encoding="ISO-8859-1")
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
    WR.to_csv(WeeklyResultsfile, index=False)



def UpdateTiers(WeeklyResultsfile: str, oldFeaturesfile: str, Featuresfile: str, week: int):
    """It updates a player's wins, losses, and number of times they were in
    Prospect, ..., Floated to previous weeks"""
    WR = pd.read_csv(WeeklyResultsfile, encoding="ISO-8859-1")
    if week != 1:
        Features = pd.read_csv(oldFeaturesfile, encoding="ISO-8859-1")
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
    Features.to_csv(Featuresfile, index=False)


def UpdatePlacements(WeeklyResultsfile, oldPlacementsfile:str, Placementsfile:str, week:int):
    """Appends this week's bracket placement to previous weeks.
    -1 means they did not make bracket.
    -2 means they did not enter that week."""
    WR = pd.read_csv(WeeklyResultsfile, encoding="ISO-8859-1")
    
    if week != 1:
        Placement = pd.read_csv(oldPlacementsfile, encoding="ISO-8859-1")
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
        Placement = WR[['SmasherID', 'SmashTag', 'Placement']]
        Placement = Placement.rename(columns={'Placement': 'PWeek1'})
    Placement = Placement.sort_values(by = 'SmasherID')
    Placement.to_csv(Placementsfile, index=False)



def RankLadder(WeeklyScoresLadderfile: str, WeeklyRankLadderfile: str) -> None:
    """Rank ladder for that week. """
    WSLadder = pd.read_csv(WeeklyScoresLadderfile, encoding="ISO-8859-1")
    RF.LimitLadderWins(WSLadder)
    RF.FormulaLadder(WSLadder)
    WSLadder['Rank'] = (WSLadder['Points'] * -1).rank(method = 'min')
    WSLadder.to_csv(WeeklyRankLadderfile, index = False)



def RankWeekly(WeeklyResultsfile: str, WeeklyRankfile: str) -> None:
    """Rank Ladder and Bracket for that week."""
    WeeklyResults = pd.read_csv(WeeklyResultsfile)
    RF.PlacementPointsWeekly(WeeklyResults)
    RF.FormulaWeekly(WeeklyResults)
    WeeklyResults['Rank'] = (WeeklyResults['Points'] * -1).rank(method = 'min')
    WeeklyResults.to_csv(WeeklyRankfile, index = False)


def RankSeason(Featuresfile: str, Placementsfile: str, week: int) -> None:
    """It will give value to each column to determine the ranks for
    the entire season."""
    Features = pd.read_csv(Featuresfile)
    Placements = pd.read_csv(Placementsfile)
    RF.PlacementPointsSeason(Placements, week)
    RF.FormulaTotalSeason(Features, Placements)
    Features['Rank'] = (Features['Points'] * -1).rank(method = 'min')
    Features.to_csv(Featuresfile, index = False)


def ChangeRank(Featuresfile: str, oldRankRecordsfile: str, week: int, RankRecordsfile: str):
    """It keeps track of someone's rank for each week."""
    Features = pd.read_csv(Featuresfile)
    if week != 1:
        RankRecords = pd.read_csv(oldRankRecordsfile)
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
                           'ChangeInRank': 'New'}
                for i in range(1, week):
                    new_row[f'RWeek{i}'] = 'NAN'
                RankRecords = RankRecords.append(new_row, ignore_index = True)
        temp= RankRecords['ChangeInRank']     # Used to move a column
        RankRecords = RankRecords.drop(['ChangeInRank'], axis = 1)
        RankRecords['ChangeInRank'] = temp
    else:
        RankRecords = Features[['SmasherID', 'SmashTag', 'Rank']]
        RankRecords = RankRecords.rename(columns={'Rank': 'RWeek1'})
        RankRecords['ChangeInRank'] = 'New'
    RankRecords = RankRecords.sort_values(by = 'SmasherID')
    RankRecords.to_csv(RankRecordsfile, index = False)

    
def WebsiteWeeklyRank(WeeklyRankfile: str, WebWeeklyRankfile: str) -> None:
    """ It does not change anything about the data. It moves and removes columns
    so it is more presentable for the website. This is used by both the weekly
    ladder and bracket rank."""
    WeeklyRank = pd.read_csv(WeeklyRankfile)
    WeeklyRank = WeeklyRank.rename(columns={'Points': 'BankRoll Bills'})
    WeeklyRank['Win%'] = 100*WeeklyRank['Wins'] / (WeeklyRank['Wins'] + WeeklyRank['Losses'])
    WeeklyRank = WeeklyRank[['Rank', 'SmashTag', 'Wins', 'Losses',
                             'Win%', 'BankRoll Bills']]
    
    WeeklyRank = WeeklyRank.sort_values(by='Rank')
    WeeklyRank = WeeklyRank.round(2)
    WeeklyRank.to_csv(WebWeeklyRankfile, index=False)


def WebsiteTotalRank(Featuresfile: str, RankRecordsfile: str, WebTotalRankfile: str) -> None:
    # Keep for now. We might want different columns for each file.
    # The total can include more information
    """ It does not change anything about the data. It moves and removes columns
    so it is more presentable for the website."""
    Features = pd.read_csv(Featuresfile)
    RankRecords = pd.read_csv(RankRecordsfile)

    Features['ChangeInRank'] = RankRecords['ChangeInRank']
    Features = Features.rename(columns={'Points': 'BankRoll Bills'})
    Features['Win%'] = 100*Features['Wins'] / (Features['Wins'] + Features['Losses'])
    Features = Features[['Rank', 'ChangeInRank', 'SmashTag', 'Coast',
                         'Wins', 'Losses', 'Win%', 'BankRoll Bills', ]]
    
    Features = Features.sort_values(by='Rank')
    Features = Features.round(2)
    Features.to_csv(WebTotalRankfile, index=False)


def main():
    #UI.PrintRankWelcomeMessage()
    #choice = UI.rankChoice()
    #season = UI.UserSeason()
    #week = UI.UserWeek()
    choice = 2
    season = 1
    week = 3

    # Input files
    WSL = f'WeeklyLadderBracket/S{season}W{week}WeeklyScoresLadder.csv'
    WSB = f'WeeklyLadderBracket/S{season}W{week}WeeklyScoresBracket.csv'

    WeeklyResults= f'Debug/S{season}W{week}WeeklyResults.csv'    # It combines the results of Ladders and Bracket
    oldFeatures = f'Records/S{season}W{week - 1}Features.csv'
    Features = f'Records/S{season}W{week}Features.csv'

    oldPlacements = f'Records/S{season}W{week - 1}Placements.csv'
    Placements = f'Records/S{season}W{week}Placements.csv'

    WeeklyRankLadder = f'Debug/S{season}W{week}WeeklyRankLadder.csv'  # Points for that week's ladder
    WeeklyRank = f'Debug/S{season}W{week}WeeklyRank.csv'
    
    oldRankRecords = f'Records/S{season}W{week - 1}RankRecords.csv'
    RankRecords = f'Records/S{season}W{week}RankRecords.csv'

    # These three will go on the website
    WebWLR = f'Website/S{season}W{week}WebsiteWeeklyLadderRank.csv'
    WebWR = f'Website/S{season}W{week}WebsiteWeeklyRank.csv'    # Ladders and Bracket Ranks
    WebTR = f'Website/S{season}W{week}WebsiteTotalRanks.csv'    # Rank for the entire season

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
        
        WebsiteWeeklyRank(WeeklyRank, WebWR)
        WebsiteTotalRank(Features, RankRecords, WebTR)



main()




