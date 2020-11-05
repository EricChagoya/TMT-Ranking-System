# TMT-Ranking-System





 Each text file with have N to show what week it was created.
 
 Tim's File
 
    It gets the pure data from smash.gg without applying any formula to it. 
    
 WeeklyScoresLadderN.txt
 
        SmasherID   SmashTag    Wins    Losses     Prospect    Rookie  Pro Placement
	This will be done after Ladder finishes but before bracket.
		
 Option 1- Only lists wins from Bracket.
 WeeklyScoresBracketN.txt
 
        SmasherID   SmashTag    Wins    Losses     Placement

 Option 2 - Used if wins from Ladder and Bracket are combined. Like 4 wins from ladder and 4 wins brackets make it 8 wins.
 WeeklyScoresBoth.txt
 	
	SmasherID   SmashTag    Wins    Losses (Future)     Prospect    Rookie  Pro Placement
 
 
 
 
 CreateRanks.py
 
    This will take this weeks scores from a text file and aggregate to the total. 
	It will assign some type of formula to determine points. It will then 
    use those points and put it as a ranking.
    TotalsPointsN.txt will be used to calculated TotalRanksN.txt.
    Maybe split this into files so if we ever want to change the formula, it doesn't have to do a bunch of steps.

 
 Output Files
 
 TotalPointN.txt
 
 	SmasherID   SmasherTag  Wins    Losses Prospect    Rookie  Pro TimesBracket    [AllPlacements]  NumberTourneysEntered
	
 	It aggregates this week's ladder and bracket data and adds to TotalPoints(N-1).txt.
 
 WeeklyRankLadderN.txt
 
    SmasherID   SmasherTag  Rank    RankChange  TotalWins   TotalLosses    WinPercentage
    
    This is where the formula will be applied. It will take WeeklyScoreLadder.txt.
	We will only look at Ladder.
    
 TotalRanksN.txt
 
 	SmasherID   SmasherTag  Rank    RankChange  TotalWins   TotalLosses    WinPercentage
	It will take as input TotalPointN.txt. It will then create the Cumulative Rankings up to this week.
 
 
 
 These will be posted on the website. It will be a subset of the columns for it was named after.
 
 SubsetWeeklyRankScoreN.txt -  
 Maybe v1 and v2 for knowing which one is ladder.
 
    SmashTag    Wins    Losses (Future)     Tier
	It's input is WeeklyRankLadderN.txt.
	
    
 SubsetTotalRanksN.txt
 
    Rank    SmasherTag  RankChange  TotalWins   TotalLosses (Future)    WinPercentage (Future)
	It's input is TotalRanksN.txt.
 
 
 
 
 
 
 
 
 

