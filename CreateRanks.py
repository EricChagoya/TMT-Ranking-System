import numpy as np
import pandas as pd
import UserInterface as UI
import RankingFormula as RF


def WeeklyScorePoints(WSLfile: str, WSBfile: str, WTPfile: str,
                      week: int) -> None:
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

    WTP['WinPercentage'] = WTP['Wins'] / (WTP['Wins'] + WTP['Losses'])
    WTP = WTP[['SmasherID', 'SmashTag', 'Wins', 'Losses', 'LimitLadderWins',
               'Prospect', 'Rookie', 'Pro', 'AllStar', 'HallOfFame',
               'Floated', 'WinPercentage', 'Placement']]
    WTP.to_csv(WTPfile, index=False)


def TotalScorePoints(WTPfile: str, oldTPfile: str, TPfile: str, week: int):
    WTP = pd.read_csv(WTPfile, encoding="ISO-8859-1")
    if week != 1:
        TP = pd.read_csv(oldTPfile, encoding="ISO-8859-1")
        TP[f'PlaceWeek{week}'] = -2

        for index, row in WTP.iterrows():
            inThisWeek = TP[TP['SmasherID'].isin([row['SmasherID']])]
            print(TP[TP['SmasherID'].isin([row['SmasherID']])])
            if len(inThisWeek) > 0:
                index = inThisWeek.index[0]
                TP.at[index, 'Wins'] = \
                    TP['Wins'][index] + row['Wins']
                TP.at[index, 'Losses'] = \
                    TP['Losses'][index] + row['Losses']
                TP.at[index, 'LimitLadderWins'] = \
                    TP['LimitLadderWins'][index] + row['LimitLadderWins']
                TP.at[index, 'Prospect'] = \
                    TP['Prospect'][index] + row['Prospect']
                TP.at[index, 'Rookie'] = \
                    TP['Rookie'][index] + row['Rookie']
                TP.at[index, 'Pro'] = \
                    TP['Pro'][index] + row['Pro']
                TP.at[index, 'AllStar'] = \
                    TP['AllStar'][index] + row['AllStar']
                TP.at[index, 'HallOfFame'] = \
                    TP['HallOfFame'][index] + row['HallOfFame']
                TP.at[index, 'Floated'] = \
                    TP['Floated'][index] + row['Floated']
                TP.at[index, f'PlaceWeek{week}'] = \
                    row['Placement']
            else:
                new_row = {'SmasherID': row['SmasherID'],
                           'SmashTag': row['SmashTag'],
                           'Wins': row['Wins'],
                           'Losses': row['Losses'],
                           'LimitLadderWins': row['LimitLadderWins'],
                           'Prospect': row['Prospect'],
                           'Rookie': row['Rookie'],
                           'Pro': row['Pro'],
                           'AllStar': row['AllStar'],
                           'HallOfFame': row['HallOfFame'],
                           'Floated': row['Floated'],
                           f'PlaceWeek{week}': row['Placement']}
                for i in range(1, week):
                    new_row[f'PlaceWeek{i}'] = -2
                TP = TP.append(new_row, ignore_index=True)

        TP['WinPercentage'] = TP['Wins'] / (TP['Wins'] + TP['Losses'])
    else:
        TP = WTP.rename({'Placement': 'PlaceWeek1'}, axis='columns')

    TP.to_csv(TPfile, index=False)


def RankLadder(WSLfile: str, WRLfile: str) -> None:
    """Rank ladder for that week. """
    WSL = pd.read_csv(WSLfile, encoding="ISO-8859-1")
    RF.LimitLadderWins(WSL)
    RF.FormulaLadder(WSL)
    WSL['Rank'] = (WSL['Points'] * -1).rank(method='max')
    WSL['WinPercentage'] = WSL['Wins'] / (WSL['Wins'] + WSL['Losses'])
    WSL.to_csv(WRLfile, index=False)


def RankWeekly(WTPfile: str, WRBfile: str) -> None:
    """Rank Ladder and Bracket for that week."""
    WTP = pd.read_csv(WTPfile)
    RF.PlacementPointsWeekly(WTP)
    RF.FormulaWeekly(WTP)
    WTP['Rank'] = (WTP['Points'] * -1).rank(method='min')
    WTP.to_csv(WRBfile, index=False)


def RankTotalPoints(TPfile: str, week: int, TRfile: str) -> None:
    """It will give value to each column to determine the ranks for
    the entire season."""
    TP = pd.read_csv(TPfile)
    RF.PlacementPointsSeason(TP, week)
    RF.FormulaTotalSeason(TP)
    TP['Rank'] = (TP['Points'] * -1).rank(method='min')
    TP.to_csv(TRfile, index=False)


def WebsiteWeeklyRank(WRfile: str, SWRfile: str) -> None:
    """ It does not change anything about the data. It moves and removes columns
    so it is more presentable for the website. This is used by both the weekly
    ladder and bracket rank."""
    WR = pd.read_csv(WRfile)
    WR = WR.rename(columns={'Points': 'BankRoll Bills'})
    WR = WR[['Rank', 'SmashTag', 'Wins', 'Losses',
             'WinPercentage', 'BankRoll Bills']]
    WR = WR.sort_values(by='Rank')
    WR = WR.round(3)
    WR.to_csv(SWRfile, index=False)


def WebsiteTotalRank(TRfile: str, STRfile: str) -> None:
    # Keep for now. We might want different columns for each file.
    # The total can include more information
    """ It does not change anything about the data. It moves and removes columns
    so it is more presentable for the website."""
    TR = pd.read_csv(TRfile)
    TR = TR.rename(columns={'Points': 'BankRoll Bills'})
    TR = TR[['Rank', 'SmashTag', 'Wins', 'Losses',
             'WinPercentage', 'BankRoll Bills', ]]
    TR = TR.sort_values(by='Rank')
    TR = TR.round(3)
    TR.to_csv(STRfile, index=False)


def main():
    # UI.PrintWelcomeMessage()
    # choice = UI.UserChoice()
    # season = UI.UserSeason()
    # week = UI.UserWeek()
    choice = 2
    season = 0
    week = 2

    # Input files
    WSL = f'S{season}W{week}WeeklyScoresLadder.csv'  # Placement
    WSB = f'S{season}W{week}WeeklyScoresBracket.csv'  # Placement

    # Total Points
    # WTP should also be Placement
    WTP = f'S{season}W{week}WeeklyTotalPoints.csv'  # It combines the points from Ladder and Bracket
    oldTP = f'S{season}W{week - 1}TotalPoints.csv'  # Last week's Total Points
    TP = f'S{season}W{week}TotalPoints.csv'  # Counts all the points from all cummulative weeks

    # These next two apply the ranking formula
    WRL = f'S{season}W{week}WeeklyRankLadder.csv'  # Points for ladder that week's ladder
    WRB = f'S{season}W{week}WeeklyRankBoth.csv'  # Points for ladder and bracket for the week
    TR = f'S{season}W{week}TotalRank.csv'  # Points for the entire season

    # These three will go on the website
    SWLR = f'S{season}W{week}SubsetWeeklyLadderRank.csv'  # Placement
    SWBR = f'S{season}W{week}SubsetWeeklyBracketRank.csv'  # Placement
    STR = f'S{season}W{week}SubsetTotalRanks.csv'

    if choice == 1:
        RankLadder(WSL, WRL)
        WebsiteWeeklyRank(WRL, SWLR)
    else:
        WeeklyScorePoints(WSL, WSB, WTP, week)
        TotalScorePoints(WTP, oldTP, TP,
                         week)  # Update LimitLadderWins column for non week 1

        RankWeekly(WTP, WRB)
        RankTotalPoints(TP, week, TR)

        WebsiteWeeklyRank(WRB, SWBR)
        WebsiteTotalRank(TR, STR)


main()

# Add LadderWinsLimit to Github ReadMe
# Split this file into 3 files. Another for UserInterface and Rankings





