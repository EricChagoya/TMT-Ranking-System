# TMT-Ranking-System





 Each text file with have N to show what week it was created.
 
 Tim's File
 
    It gets the pure data from smash.gg without applying any formula to it. 
    
 WeeklyScoreLadderN.txt
 
        SmasherID   SmashTag    Wins    Losses (Future)     Prospect    Rookie  Pro Placement
        
 WeeklyScoreBracketN.txt
 
        SmasherID   SmashTag    Wins    Losses (Future)     Placement
 
 
 
 CreateRanks.py
 
    This will take this weeks scores from a text file. It will assign some type of formula to determine points. It will then 
    use those points and put it as a ranking.
    TotalsPointsN.txt will be used to calculated TotalRanks.txt.
 
    Maybe split this into files so if we ever want to change the formula, it doesn't have to do a bunch of steps.
 
 Output Files
 
 TotalPointsv1N.txt
 
    SmasherID   SmasherTag  Wins    Losses (Future) Prospect    Rookie  Pro TimesBracket    [AllPlacements]  NumberTourneysEntered
    
    It aggregates this week's data to previous.
    
 TotalPointsv2N.txt         (Future)
 
 TotalRanksv1N.txt
 
    SmasherID   SmasherTag  Rank    RankChange  TotalWins   TotalLosses (Future)    WinPercentage (Future)
    
    This is where the formula will be applied.
    
 TotalRanksv2N.txt          (Future)
 
 
 These will be posted on the website. It will be a subset of the columns for it was named after.
 
 SubsetWeeklyScoreN.txt
 
    SmashTag    Wins    Losses (Future)     Tier
    
 SubsetTotalRanksN.txt
 
    Rank    SmasherTag  RankChange  TotalWins   TotalLosses (Future)    WinPercentage (Future)
 
 
 
 
 
 
 
 
 

