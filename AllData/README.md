All Output files will have S(N)W(n) as a prefix.
S(N) being what season we are on.
W(n) being which week is it.

CollectData.py Output Files
- WeeklyScoresLadder.csv
	- This will be done after Ladder finishes but before bracket
	- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, AllStar, HallOfFame
		
- WeeklyScoresBracket.csv
	- Only lists wins, losses, and placement from bracket
	- Column Names: SmasherID, SmashTag, Wins, Losses, PlaceWeekN
		


CreateRanks.py Output Files
- WeeklyTotalPoints.csv
	- It combines this week's lader and bracket results to one file
	- If a player did not make it into final bracket, their placement is -1
	- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, AllStar, HallOfFame, Floated, PlaceWeekN, WinPercentage
- TotalPoints.csv
	- It adds WeeklyTotalPoints.csv to last week's W(n-1)TotalPoints.csv
	- If a player didn't enter that week, there placement is -2
	- Column Names: SmasherID, SmasherTag, Wins, Losses, Prospect, Rookie, Pro, AllStar, HallOfFame, Floated, PlaceWeek1, ..., PlaceWeekN, WinPercentage

- WeeklyRankLadder.csv
	- It applies the Ranking formula to this week's ladder
	- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, AllStar, HallOfFame, PlaceWeekN, Rank, WinPercentage
- WeeklyRankBoth.csv
	- It applies the Ranking formula to this week's ladder and bracket
	- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, AllStar, HallOfFame, Floated, PlaceWeek1, ..., PlaceWeekN, Points, Rank, WinPercentage
- TotalRank.csv
	- It applies the Ranking formula to the whole season
	- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, AllStar, HallOfFame, Floated, PlaceWeek1, ..., PlaceWeekN, Points, Rank, WinPercentage
	
- SubsetWeeklyLadderRank.csv
	- This goes on the Website
	- Rank, SmashTag, Wins, Losses, WinPercentage, BankRoll Bills, 
- SubsetWeeklyBracketRank.csv
	- This goes on the Website
	- Rank, SmashTag, Wins, Losses, WinPercentage, BankRoll Bills, 
- SubsetTotalRanks.csv
	- This goes on the Website