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
    t = df['Wins'] - LIMIT_LADDER_WINS
    df.insert(4, 'LimitLadderWins', t)
    df['LimitLadderWins'] = np.where((df.LimitLadderWins < 1), 0, df.LimitLadderWins)


def PlacementPointsWeekly(WeeklyResults: 'df') -> None:
    """It gives players points for their placement in bracket"""
    WeeklyResults["PlacePoints"] = WeeklyResults['Placement']
    WeeklyResults["PlacePoints"] = WeeklyResults["PlacePoints"].map(PLACEMENTS)
    WeeklyResults["PlacePoints"] = WeeklyResults["PlacePoints"].fillna(0)


def PlacementPointsSeason(P: 'df', week: int) -> None:
    """It gives players points for their placement in bracket
    for every tournament"""
    P['PlacePoints'] = 0
    temp= pd.DataFrame()
    for i in range(1, week + 1):
        temp['PlacePoints'] = P[f'PWeek{i}'].map(PLACEMENTS)
        temp['PlacePoints'] = temp['PlacePoints'].fillna(0)
        P['PlacePoints'] += temp['PlacePoints']


def FormulaLadder(WSLadder : 'df') -> None:
    """Ranking formula for ladder"""
    # WeeklyScoresLadder
    WSLadder['Points'] = WSLadder['Wins'] - WSLadder['LimitLadderWins'] + \
                         WSLadder['Prospect'] * POINT_PROSPECT + \
                         WSLadder['Rookie'] * POINT_ROOKIE + \
                         WSLadder['Pro'] * POINT_PRO + \
                         WSLadder['AllStar'] * POINT_ALL_STAR + \
                         WSLadder['HallOfFame'] * POINT_HALL_OF_FAME


def FormulaWeekly(WR : 'df') -> None:
    """Ranking formula for ladder and bracket for the week"""
    # WeeklyResults
    WR['Points'] = WR['Wins'] - WR['LimitLadderWins'] + \
                   WR['Prospect'] * POINT_PROSPECT + \
                   WR['Rookie'] * POINT_ROOKIE + \
                   WR['Pro'] * POINT_PRO + \
                   WR['AllStar'] * POINT_ALL_STAR + \
                   WR['HallOfFame'] * POINT_HALL_OF_FAME + \
                   WR['Floated'] * POINT_FLOATED_PLAYER + \
                   WR['PlacePoints']


def FormulaTotalSeason(TP : 'df', P: 'df') -> None:
    """Ranking formula for the entire season"""
    # We will add stuff to this later for a more complicated ranking formula
    # I'm assuming SmashID's will be in the same order for both
    TP['Points'] = TP['Wins'] - TP['LimitLadderWins'] + \
                   TP['Prospect'] * POINT_PROSPECT + \
                   TP['Rookie'] * POINT_ROOKIE + \
                   TP['Pro'] * POINT_PRO + \
                   TP['AllStar'] * POINT_ALL_STAR + \
                   TP['HallOfFame'] * POINT_HALL_OF_FAME + \
                   TP['Floated'] * POINT_FLOATED_PLAYER + \
                   P['PlacePoints']







