import numpy as np
import pandas as pd

POINT_WIN = 1
POINT_PROSPECT = 1
POINT_ROOKIE = 5
POINT_PRO = 10
POINT_ALL_STAR = 15
POINT_HALL_OF_FAME = 20
POINT_FLOATED_PLAYER = 10
LIMIT_LADDER_WINS = 20

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


def LimitLadderWins(df: 'df') -> None:
    """It limits how many points a player can get by grinding wins on ladder"""
    #df['LimitLadderWins']
    t = df['Wins'] - LIMIT_LADDER_WINS
    df.insert(4, 'LimitLadderWins', t)
#    df['LimitLadderWins'] = df['Wins'] - LIMIT_LADDER_WINS
    df['LimitLadderWins'] = np.where((df.LimitLadderWins < 1), 0, df.LimitLadderWins)


def PlacementPointsWeekly(WTP: 'df') -> None:
    """It gives players points for their placement in bracket"""
    WTP["PlacePoints"] = WTP['Placement']
    WTP["PlacePoints"] = WTP["PlacePoints"].map(PLACEMENTS)
    WTP["PlacePoints"] = WTP["PlacePoints"].fillna(0)


def PlacementPointsSeason(TP: 'df', week: int) -> None:
    """It gives players points for their placement in bracket
    for every tournament"""
    TP['PlacePoints'] = 0
    for i in range(1, week + 1):
        TP[f"PlacePoints{i}"] = TP[f'PlaceWeek{i}']
        TP[f"PlacePoints{i}"] = TP[f"PlacePoints{i}"].map(PLACEMENTS)
        TP[f"PlacePoints{i}"] = TP[f"PlacePoints{i}"].fillna(0)
        TP['PlacePoints'] += TP[f"PlacePoints{i}"]


def FormulaLadder(WSL : 'df') -> None:
    """Ranking formula for ladder"""
    WSL['Points'] = WSL['Wins'] - WSL['LimitLadderWins'] + \
                    WSL['Prospect'] * POINT_PROSPECT + \
                    WSL['Rookie'] * POINT_ROOKIE + \
                    WSL['Pro'] * POINT_PRO + \
                    WSL['AllStar'] * POINT_ALL_STAR + \
                    WSL['HallOfFame'] * POINT_HALL_OF_FAME


def FormulaWeekly(WTP : 'df') -> None:
    """Ranking formula for ladder and bracket for the week"""
    WTP['Points'] = WTP['Wins'] - WTP['LimitLadderWins'] + \
                    WTP['Prospect'] * POINT_PROSPECT + \
                    WTP['Rookie'] * POINT_ROOKIE + \
                    WTP['Pro'] * POINT_PRO + \
                    WTP['AllStar'] * POINT_ALL_STAR + \
                    WTP['HallOfFame'] * POINT_HALL_OF_FAME + \
                    WTP['Floated'] * POINT_FLOATED_PLAYER + \
                    WTP['PlacePoints']


def FormulaTotalSeason(TP : 'df') -> None:
    """Ranking formula for the entire season"""
    # We will add stuff to this later for a more complicated ranking formula
    TP['Points'] = TP['Wins'] - TP['LimitLadderWins'] + \
                   TP['Prospect'] * POINT_PROSPECT + \
                   TP['Rookie'] * POINT_ROOKIE + \
                   TP['Pro'] * POINT_PRO + \
                   TP['AllStar'] * POINT_ALL_STAR + \
                   TP['HallOfFame'] * POINT_HALL_OF_FAME + \
                   TP['Floated'] * POINT_FLOATED_PLAYER + \
                   TP['PlacePoints']







