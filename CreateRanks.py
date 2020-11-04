import numpy as np
import pandas as pd

# You need to pipinstall numpy and pandas
# pip install numpy
# pip install pandas


# Global Variables for the points
# GetdatafromSmash.py
# Create_Ranks

# Make some type of chart for abbreviations
# Placement. -1 means they didn't place that week. Any number above 0 is what they placed.
# Placements will have a string of all placeings. -2 means they didn't enter that week.

# I need to document it better.


def TotalPointsFirstWeekLadder(inputFile:str, outputFile:str) -> None:
    """For the first week there hasn't been a TotalPoints so we create it."""
    df = pd.read_csv(inputFile, sep = "\t")  # df- dataframe
    df['NumTimesBracket'] = 0
    df['Placement'] = -1
    df['NumTourneysEntered'] = 1
    #print(df.shape)
    #print(type(df))
    print(df)
    print(df.columns)
    df.to_csv(outputFile, sep = "\t", index= False)
    
def TotalPointBracket(TPv1file:str, WSBfile:str, outputFile:str) -> None:
    """Add final bracket results to the points."""
    TPv1 = pd.read_csv(TPv1file, sep = "\t")
    WSB = pd.read_csv(WSBfile, sep = "\t")


    # append WSB to TPv1
    # If they are in bracket, identical SmasherID, then replace Wins, Placements,
    # increment NumTimesBracket
    TPv1.to_csv(outputFile, sep = "\t")






def main():
    #week = int(input("What week is it? ") )
    # Did you want to add ladder or final bracket scores?
    # Final Bracket
    # Make some type of interface when I only have ladder, add only bracket, or add both.
    
    week = 1
    if week == 1:
        WSL1 = "WeeklyScoresLadder1.txt"
        TPv1 = "TotalPoints1v1.txt"
        TotalPointsFirstWeekLadder(WSL1, TPv1)

        WSB1 = "WeeklyScoresBracket1.txt"
        TPv2 = "TotalPoints1v1.txt"
        #TotalPointBracket(TPv1, WSB1, TPv2)
        #f2= "WeeklyScoresBracket1.txt"
    else:
        pass

    



main()
