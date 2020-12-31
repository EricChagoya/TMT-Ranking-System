# Output Files
All Output files will have S(N)W(n) as a prefix

S(N) being what season we are on

W(n) being which week is it

## CollectData.py Output Files
##### WeeklyScoresLadder.csv
- It combines West and East Ladder results into one file
- Column Names: SmasherID, SmashTag, Coast, Wins, Losses, Prospect, Rookie, Pro, AllStar, HallOfFame
		
##### WeeklyScoresBracket.csv
- Results from that week's final bracket
- Column Names: SmasherID, SmashTag, Wins, Losses, Placement
		


## CreateRanks.py Output Files
##### WeeklyResults.csv
- Combines ladders and bracket results
- Column Names: SmasherID, SmashTag, Coast, Wins, Losses, LimitLadderWins, Prospect, Rookie, Pro, Allstar, HallOfFame, Floated, Placement
 
##### Features.csv
- It keeps track of what tier people ended in ladder
- Column Names: SmasherID, SmashTag, Coast, Wins, Losses, LimitLadderWins, Prospect, Rookie, Pro, AllStar, HallOfFame, Floated, Points, Rank

##### Placements.csv
- It list every player's placement in the final bracket
- If they did not TMT that week, it will be -2
- If they did not make it into final bracket, it will be -1
- Column Names: SmasherID, SmashTag, NumTMTEntered, NumInBracket, PWeek1, ..., PWeekN

##### WeeklyRankLadder.csv
- It ranks people for how well they did in ladder and only ladder
- Column Names: SmasherID, SmashTag, Coast, Wins, Losses, LimitLadderWins, Prospect, Rookie, Pro, AllStar, HallOfFame, Placement, Points, Rank

##### WeeklyRank.csv
- It ranks people based off ladder and bracket for that week
- Column Names: SmasherID, SmashTag, Coast, Wins, Losses, LimitLadderWins, Prospect, Rookie, Pro, AllStar, HallOfFame, Floated, Placement, PlacePoints, Points, Rank

##### RankRecords.csv
- It displays a player's rank on a week to week basis
- The last column displays how much they increase or decreased
- Column Names: SmasherID, SmashTag, RWeek1, ..., RWeekN, ChangeInRank

##### PastPoints.csv
- It displays a player's cummulative points for every week
- Column Names: SmasherID, SmashTag, BWeek1, ..., BWeekN
  
##### WebsiteWeeklyLadderRank.csv
- Column Names: Rank, SmashTag, Wins, Losses, WinPercentage, BankRollBills
  
##### WebsiteWeeklyRank.csv
- It displays how many points were earned that week for ladder and bracket
- Column Names: Rank, SmashTag, Wins, Losses, WinPercentage, BankRollBills

##### WebsiteTotalRanks.csv
- Everybody's points for the entire season
- Column Names: Rank, ChangeInRank, SmashTag, Coast, Wins, Losses, Win%, NumTMTEntered, NumInBracket, BankRoll Bills



## ArmadaNumber.py Output Files
##### PlayerSets.json
- Contains every player's head to head records for the season
- Attributes: SmasherID, WinningsSets, LosingSets

##### PlayerSetsTags.json
- Same as PlayerSets.json except it replaces SmasherID with SmashTag
- Mostly used for debugging
- Attributes: SmashTag, WinningsSets, LosingSets

##### ArmadaNumber.csv
- It contains everybody's Armada number and the shortest path to get there
- Column Names: SmashTag, Armada Number, Path

## UpdateWebsiteSpreadSheets.py Output Files
##### RanksforBracket.csv
- Column Names: Rank, SmashTag, EnteredTMT


## Manually Update Files
##### PlayerMains.csv
- A player's main. No dual main. Most played character
- Column Names: SmasherID, SmashTag, Main
  

##### TMTRevenue.csv
- The revenue, cost, and total profit for the entire series
- Column Names: Week, Amount, Reason
