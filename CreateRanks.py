import numpy as np
import pandas as pd
import UserInterface as UI
import RankingFormula as RF


def CreateWeeklyResults(WSLfile: str, WSBfile: str, WTPfile: str,week: int) -> None:
    """It combines the scores from ladder and bracket into one file."""
    WSL = pd.read_csv(WSLfile, encoding="ISO-8859-1")
    WSB = pd.read_csv(WSBfile, encoding="ISO-8859-1")
    WTP = WSL

    WTP['Placement'] = -1
    WTP['Floated'] = 0
    RF.LimitLadderWins(WTP)

    count = 0
    for index, row in WSB.iterrows():
        inLadder = WTP[WTP['SmasherID'].isin([row['SmasherID']])]
        if len(inLadder) > 0:
            index = inLadder.index[0]
            WTP.at[index, 'Wins'] = WTP['Wins'][index] + row['Wins']
            WTP.at[index, 'Losses'] = WTP['Losses'][index] + row['Losses']
            WTP.at[index, 'Placement'] = row['Placement']
        else:
            new_row = {'SmasherID': row['SmasherID'],
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
            WTP = WTP.append(new_row, ignore_index=True)

    WTP = WTP[['SmasherID', 'SmashTag', 'Coast', 'Wins', 'Losses',
               'LimitLadderWins', 'Prospect', 'Rookie', 'Pro',
               'AllStar', 'HallOfFame', 'Floated', 'Placement']]
    WTP = WTP.sort_values(by = 'SmasherID')
    WTP.to_csv(WTPfile, index=False)


def UpdateTiers(WTPfile: str, oldTPfile: str, TPfile: str, week: int):
    WTP = pd.read_csv(WTPfile, encoding="ISO-8859-1")
    if week != 1:
        TP = pd.read_csv(oldTPfile, encoding="ISO-8859-1")
        for index, row in WTP.iterrows():
            inThisWeek = TP[TP['SmasherID'].isin([row['SmasherID']])]
            if len(inThisWeek) > 0:
                index = inThisWeek.index[0]
                TP.at[index, 'SmashTag'] = row['SmashTag']  # If someone changes their tag
                TP.at[index, 'Wins'] = TP['Wins'][index] + row['Wins']
                TP.at[index, 'Losses'] = TP['Losses'][index] + row['Losses']
                TP.at[index, 'LimitLadderWins'] = TP['LimitLadderWins'][index] + row['LimitLadderWins']
                TP.at[index, 'Prospect'] = TP['Prospect'][index] + row['Prospect']
                TP.at[index, 'Rookie'] = TP['Rookie'][index] + row['Rookie']
                TP.at[index, 'Pro'] = TP['Pro'][index] + row['Pro']
                TP.at[index, 'AllStar'] = TP['AllStar'][index] + row['AllStar']
                TP.at[index, 'HallOfFame'] = TP['HallOfFame'][index] + row['HallOfFame']
                TP.at[index, 'Floated'] = TP['Floated'][index] + row['Floated']
            else:
                new_row = {'SmasherID': row['SmasherID'],
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
                TP = TP.append(new_row, ignore_index=True)
    else:
        TP = WTP[['SmasherID', 'SmashTag', 'Coast', 'Wins', 'Losses',
                  'LimitLadderWins', 'Prospect', 'Rookie', 'Pro',
                  'AllStar', 'HallOfFame', 'Floated']]
    TP = TP.sort_values(by = 'SmasherID')
    TP.to_csv(TPfile, index=False)


def UpdatePlacements(WTPfile, oldPfile:str, Pfile:str, week:int):
    """It updates everybody's placements to include this weeks.
    -1 means they did not make bracket.
    -2 means they did not enter that week."""
    WTP = pd.read_csv(WTPfile, encoding="ISO-8859-1")
    
    if week != 1:
        oldP = pd.read_csv(oldPfile, encoding="ISO-8859-1")
        oldP[f'PWeek{week}'] = -2
        for index, row in WTP.iterrows():
            oldPlayer = oldP[oldP['SmasherID'].isin([row['SmasherID']])]
            if len(oldPlayer) > 0:
                index = oldPlayer.index[0]
                oldP.at[index, 'SmashTag'] = row['SmashTag']  # If someone changes their tag
                oldP.at[index, f'PWeek{week}'] = row['Placement']
            else:
                new_row = {'SmasherID': row['SmasherID'],   # New TMT Entrant
                           'SmashTag': row['SmashTag'],
                           f'PWeek{week}': row['Placement']}
                for i in range(1, week):
                    new_row[f'PWeek{i}'] = -2
                oldP = oldP.append(new_row, ignore_index = True)
    else:
        oldP = WTP[['SmasherID', 'SmashTag', 'Placement']]
        oldP = oldP.rename(columns={'Placement': 'PWeek1'})
    oldP = oldP.sort_values(by = 'SmasherID')
    oldP.to_csv(Pfile, index=False)


def RankLadder(WSLfile: str, WRLfile: str) -> None:
    """Rank ladder for that week. """
    WSL = pd.read_csv(WSLfile, encoding="ISO-8859-1")
    RF.LimitLadderWins(WSL)
    RF.FormulaLadder(WSL)
    WSL['Rank'] = (WSL['Points'] * -1).rank(method = 'min')
    WSL.to_csv(WRLfile, index = False)


def RankWeekly(WTPfile: str, WRBfile: str) -> None:
    """Rank Ladder and Bracket for that week."""
    WTP = pd.read_csv(WTPfile)
    RF.PlacementPointsWeekly(WTP)
    RF.FormulaWeekly(WTP)
    WTP['Rank'] = (WTP['Points'] * -1).rank(method = 'min')
    WTP.to_csv(WRBfile, index = False)


def RankSeason(TPfile: str, Pfile: str, week: int, TRfile: str) -> None:
    """It will give value to each column to determine the ranks for
    the entire season."""
    TP = pd.read_csv(TPfile)
    P = pd.read_csv(Pfile)
    RF.PlacementPointsSeason(P, week)
    RF.FormulaTotalSeason(TP, P)
    TP['Rank'] = (TP['Points'] * -1).rank(method = 'min')
    TP.to_csv(TRfile, index = False)


def ChangeRank(TRfile: str, oldPRfile: str, week: int, PRfile: str):
    """It keeps track of someone's rank for each week."""
    TR = pd.read_csv(TRfile)
    if week != 1:
        oldPR = pd.read_csv(oldPRfile)
        for index, row in TR.iterrows():
            oldPlayer = oldPR[oldPR['SmasherID'].isin([row['SmasherID']])]
            if len(oldPlayer) > 0:
                index = oldPlayer.index[0]
                oldPR.at[index, 'SmashTag'] = row['SmashTag']  # If someone changes their tag
                oldPR.at[index, f'RWeek{week}'] = row['Rank']
                oldPR.at[index, 'RankChange'] = oldPR.at[index, f'RWeek{week - 1}'] - oldPR.at[index, f'RWeek{week}']
            else:
                new_row = {'SmasherID': row['SmasherID'],   # New TMT Entrant
                           'SmashTag': row['SmashTag'],
                           f'RWeek{week}': row['Rank'],
                           'RankChange': 'New'}
                for i in range(1, week):
                    new_row[f'RWeek{i}'] = 'NAN'
                oldPR = oldPR.append(new_row, ignore_index = True)
        t= oldPR['RankChange']
        oldPR = oldPR.drop(['RankChange'], axis = 1)
        oldPR['RankChange'] = t
    else:
        oldPR = TR[['SmasherID', 'SmashTag', 'Rank']]
        oldPR = oldPR.rename(columns={'Rank': 'RWeek1'})
        oldPR['RankChange'] = 'New'
    oldPR = oldPR.sort_values(by = 'SmasherID')
    oldPR.to_csv(PRfile, index = False)


def WebsiteWeeklyRank(WRfile: str, SWRfile: str) -> None:
    """ It does not change anything about the data. It moves and removes columns
    so it is more presentable for the website. This is used by both the weekly
    ladder and bracket rank."""
    WR = pd.read_csv(WRfile)
    WR = WR.rename(columns={'Points': 'BankRoll Bills'})
    WR['Win%'] = 100*WR['Wins'] / (WR['Wins'] + WR['Losses'])
    WR = WR[['Rank', 'SmashTag', 'Wins', 'Losses',
             'Win%', 'BankRoll Bills']]
    
    WR = WR.sort_values(by='Rank')
    WR = WR.round(2)
    WR.to_csv(SWRfile, index=False)


def WebsiteTotalRank(TRfile: str, PRfile: str, STRfile: str) -> None:
    # Keep for now. We might want different columns for each file.
    # The total can include more information
    """ It does not change anything about the data. It moves and removes columns
    so it is more presentable for the website."""
    TR = pd.read_csv(TRfile)
    PR = pd.read_csv(PRfile)

    TR['RankChange'] = PR['RankChange']
    TR = TR.rename(columns={'Points': 'BankRoll Bills'})
    TR['Win%'] = 100*TR['Wins'] / (TR['Wins'] + TR['Losses'])
    TR = TR[['Rank', 'RankChange', 'SmashTag', 'Coast',
             'Wins', 'Losses', 'Win%', 'BankRoll Bills', ]]
    
    TR = TR.sort_values(by='Rank')
    TR = TR.round(2)
    TR.to_csv(STRfile, index=False)


def main():
    # UI.PrintWelcomeMessage()
    # choice = UI.UserChoice()
    # season = UI.UserSeason()
    # week = UI.UserWeek()
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

    WRankLadder = f'Debug/S{season}W{week}WeeklyRankLadder.csv'  # Points for that week's ladder
    WeeklyRank = f'Debug/S{season}W{week}WeeklyRank.csv'
    
    oldRankRecords = f'Records/S{season}W{week - 1}RankRecords.csv'
    RankRecords = f'Records/S{season}W{week}RankRecords.csv'

    # These three will go on the website
    WebWLR = f'Website/S{season}W{week}WebsiteWeeklyLadderRank.csv'
    WebWR = f'Website/S{season}W{week}WebsiteWeeklyRank.csv'    # Ladders and Bracket Ranks
    WebTR = f'Website/S{season}W{week}WebsiteTotalRanks.csv'    # Rank for the entire season

    if choice == 1:
        RankLadder(WSL, WRankLadder)
        WebsiteWeeklyRank(WRankLadder, WebWLR)
    else:
        CreateWeeklyResults(WSL, WSB, WeeklyResults, week)
        
        UpdateTiers(WeeklyResults, oldFeatures, Features, week)
        UpdatePlacements(WeeklyResults, oldPlacements, Placements, week)
        
        RankWeekly(WeeklyResults, WeeklyRank)
        RankSeason(Features, Placements, week, Features)

        ChangeRank(Features, oldRankRecords, week, RankRecords)
        
        WebsiteWeeklyRank(WeeklyRank, WebWR)
        WebsiteTotalRank(Features, RankRecords, WebTR)



main()




# Update functions parameters
