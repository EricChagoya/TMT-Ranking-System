# TMT-Ranking-System


##### CollectTourneyData.py
- It gets the pure data from smash.gg without applying any formula to it
- These files produce every other file in CreateRanks.py
- Output Files
 	- WeeklyScoresLadder.csv
 	- WeeklyScoresBracket.csv
 
##### CreateRanks.py
- This will take this week's scores from CollectTourneyData.py and add it to the total
- It will assign some type of formula to determine points. It will then use those points to determine a ranking
- Output Files
	- WeeklyResults.csv
	- Features.csv
	- Placements.csv
	- WeeklyRankLadder.csv
	- WeeklyRank.csv
	- RankRecords.csv
	- PastPoints.csv
	- WebsiteWeeklyLadderRank.csv
	- WebsiteWeeklyRank.csv
	- WebsiteTotalRanks.csv
	

##### RankingFormula.py
- Details about the rankings


##### UpdatePlayerMains.csv
- It will update a player's tag if they change it
- It will keep track of a player's first TMT
- Someone needs to manually update each player's main


##### graphs.py
- Makes graphs about Ranks, Points, and Placements for the entire season
- These graphs go on the website
- The interface to get website and staff graphs


##### graphsStaff.py
- Graphs only for the TMT staff
- Plots graphs about number of entrants, new players, and revenue


## ArmadaNumber.py
- Collects data on everyone's wins and losses in ladder and bracket
- Determine everybody's "Armada" Number based off the highest ranked player


##### UserInterface.py
- Small interface details

 
 [To Do List and Future Feature Ideas](https://docs.google.com/document/d/1aHgE6YX5nf8FrP0W4hysDb9TuxMNkKI6R7AvGE5YeJI/edit?usp=sharing)
 
 [Past TMTs links](https://docs.google.com/document/d/1Ze3aTZklszRjjHdqVtS7hS2tbIED5M_s3A5Vy_1_P6k/edit?usp=sharing)
 
 [People's Mains](https://drive.google.com/file/d/1sordRvRwXjrGbftJNfb60wXZ1dC3yUD2/view?usp=sharing)
 
 [Getting People's Tiers](https://docs.google.com/document/d/1I6oSWfsJBWJcFOFvQEz96dwvCBstLog_ZrL8pxZSr4I/edit?usp=sharing)
 
 [Checklist for Updating the Website](https://docs.google.com/document/d/1dOn92pFcJPdpBYNX2bsFhm-R0J_Owpqmf8T3eZJ0kLE/edit?usp=sharing)
 
 [Ranking Website](https://ucimelee.wixsite.com/tmtmelee)
 :shipit:
 
 
