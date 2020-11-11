# TMT-Ranking-System





 Each text file with have N to show what week it was created.
 
 CollectData.py
 - It gets the pure data from smash.gg without applying any formula to it. 
 - Output Files
 	- WeeklyScoresLadderN.txt
		- This will be done after Ladder finishes but before bracket.
		- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, Placement
		
 	- WeeklyScoresBracketN.txt - Option 1	
		- Only lists wins from Bracket.
		- Column Names: SmasherID, SmashTag, Wins, Losses, Placement
		
	- WeeklyScoresBoth.txt - Option 2
		- Used if wins from Ladder and Bracket are combined. Like 4 wins from ladder and 4 wins brackets make it 8 wins.
		- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, Placement
 
 
 
 
 CreateRanks.py
 
- This will take this weeks scores from a text file and aggregate to the total. 
- It will assign some type of formula to determine points. It will then use those points and put it as a ranking.
- TotalsPointsN.txt will be used to calculated TotalRanksN.txt.
- Maybe split this into files so if we ever want to change the formula, it doesn't have to do a bunch of steps.
- Output Files
	- WeeklyTotalPointsN.csv
	- TotalPointsN.txt
		- It aggregates this week's ladder and bracket data and adds to TotalPoints(N-1).txt.
 		- Column Names: SmasherID, SmasherTag, Wins, Losses, Prospect, Rookie, Pro, PlaceWeekN
	- WeeklyRankLadderN.csv
	- WeeklyRankBothN.csv
	- TotalRankN.csv
	
	- SubsetWeeklyLadderRankN.csv
	- SubsetWeeklyBracketRankn.csv
	- SubsetTotalRanksN.csv

 
 [Future Feature Ideas](https://docs.google.com/document/d/1aHgE6YX5nf8FrP0W4hysDb9TuxMNkKI6R7AvGE5YeJI/edit?usp=sharing)
 
 [Ranking Website](https://ucimelee.wixsite.com/tmtmelee)
 :shipit:
 
 
 
 

