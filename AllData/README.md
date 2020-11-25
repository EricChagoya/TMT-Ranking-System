# Output Files
All Output files will have S(N)W(n) as a prefix.

S(N) being what season we are on.

W(n) being which week is it.

CollectData.py Output Files
- WeeklyScoresLadder.csv
	- This will be done after Ladder finishes but before bracket
	- Column Names: SmasherID, SmashTag, Coast, Wins, Losses, Prospect, Rookie, Pro, AllStar, HallOfFame
		
- WeeklyScoresBracket.csv
	- Only lists wins, losses, and placement from bracket
	- Column Names: SmasherID, SmashTag, Wins, Losses, Placement
		


CreateRanks.py Output Files
- WeeklyTotalPoints.csv
	- It combines this week's lader and bracket results to one file
	- If a player did not make it into final bracket, their placement is -1
	- Column Names: SmasherID, SmashTag, Coast, Wins, Losses, LimitLadderWins, Prospect, Rookie, Pro, AllStar, HallOfFame, Floated, Placement
- TotalPoints.csv        CHANGE THIS TO FEATURES.CSV
	- It adds WeeklyTotalPoints.csv to last week's W(n-1)TotalPoints.csv
	- Column Names: SmasherID, SmashTag, Coast, Wins, Losses, LimitLadderWins, Prospect, Rookie, Pro, AllStar, HallOfFame, Floated
- Placements.csv
	- It saves a player's past bracket placements
	- If a player did not make it into final bracket, their placement is -1
	- If a player didn't enter that week, there placement is -2
	- Column Names: SmasherID, SmashTag, PWeek1, ..., PWeekN

- WeeklyRankLadder.csv
	- It applies the Ranking formula to this week's ladder
	- Column Names: SmasherID, SmashTag, Wins, Losses, LimitLadderWins, Prospect, Rookie, Pro, AllStar, HallOfFame, Placement, Rank, WinPercentage
- WeeklyRankBoth.csv
	- It applies the Ranking formula to this week's ladder and bracket
	- Column Names: SmasherID, SmashTag, Wins, Losses, Prospect, Rookie, Pro, AllStar, HallOfFame, Floated, Placement, Points, Rank, WinPercentage
- TotalRank.csv
	- It applies the Ranking formula to the whole season
	- Column Names: SmasherID, SmashTag, Coast, Wins, Losses, LimitLadderWins, Prospect, Rookie, Pro, AllStar, HallOfFame, Floated, PP, Points, Rank
 PastRanks.csv
 	- Column Names: SmasherID, RWeek1, ..., RWeekN, RankChange
	
- SubsetWeeklyLadderRank.csv
	- This goes on the Website
	- Rank, SmashTag, Wins, Losses, WinPercentage, BankRoll Bills, 
- SubsetWeeklyBracketRank.csv
	- This goes on the Website
	- Rank, SmashTag, Wins, Losses, WinPercentage, BankRoll Bills, 
- SubsetTotalRanks.csv
	- This goes on the Website
	- Column Names: Ranl, SmashTag, Coast, Wins, Losses, WinPercentage, RankChange, BankRoll Bills
