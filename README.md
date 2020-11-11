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
- It will assign some type of formula to determine points. It will then use those points and put it as a ranking
- Output Files
	- WeeklyTotalPointsN.csv
		- It combines this week's lader and bracket results to one file
		- If a player did not make it into final bracket, their placement is -1
		- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, Placement
	- TotalPointsN.txt
		- It adds WeeklyTotalPointsN.txt to TotalPoints(N-1).txt
		- If a player didn't enter that week, there placement is -2
 		- Column Names: SmasherID, SmasherTag, Wins, Losses, Prospect, Rookie, Pro, PlaceWeekN

	- WeeklyRankLadderN.csv
		- It applies the Ranking formula to this week's ladder
		- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, Placement, Points, Rank, WinPercentage
	- WeeklyRankBothN.csv
		- It applies the Ranking formula to this week's ladder and bracket
		- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, Placement, Points, Rank, WinPercentage
	- TotalRankN.csv
		- It applies the Ranking formula to the whole season
		- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, PlaceWeek1, ..., PlaceWeekN, Points, Rank, WinPercentage
	
	- SubsetWeeklyLadderRankN.csv
		- This goes on the Website
		- Rank, BankRoll Bills, SmashTag, Wins, Losses, WinPercentage
	- SubsetWeeklyBracketRankn.csv
		- This goes on the Website
		- Rank, BankRoll Bills, SmashTag, Wins, Losses, WinPercentage
	- SubsetTotalRanksN.csv
		- This goes on the Website

 
 [To Do List and Future Feature Ideas](https://docs.google.com/document/d/1aHgE6YX5nf8FrP0W4hysDb9TuxMNkKI6R7AvGE5YeJI/edit?usp=sharing)
 
 [Ranking Website](https://ucimelee.wixsite.com/tmtmelee)
 :shipit:
 
 
 
 

