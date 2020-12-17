
# Added some comments



def UserSeason() -> int:
    """The user decides what Season it is"""
    while True:
        season = input("What week Season is it? ")
        try:
            season = int(season)
            if season >= 0:
                return season
            else:
                print("Please choose an integer 0 or greater")
        except:
            print("Please Choose an integer\n")


def UserWeek() -> int:
    """The user decides what Week it is"""
    while True:
        week = input("What week is it? (Week of the Season) ")
        try:
            week = int(week)
            if week > 0:
                return week
            else:
                print("Please choose an integer greater than 0")
        except:
            print("Please Choose an integer\n")

############# Rank #############

def PrintRankWelcomeMessage() -> None:
    print("Hi There!")
    print("The Architect here! OmegaLUL\n")
    print("Which option would you like? (Press the number you want)")
    print("1. Update the Ladder Rankings")
    print("2. Update the Bracket Rankings")


def rankChoice() -> int:
    """The user decides whether they want to create the ranks
    for ladder or ladder and bracket"""
    while True:
        option = input("User choice: ")
        try:
            option = int(option)
        except:
            pass
        if option in (1, 2):
            return option
        else:
            print("Choose 1 or 2\n")

############# Graphs #############

def PrintGraphWelcomeMessage() -> None:
    print("Hello, it's me")
    print("I was wondering if you wanted to create some graphs:")
    print("1. Ranks for each character Line Graph")
    print("2. Ranks for all entrants Line Graph")
    print("3. Points for each character Line Graph")
    print("4. Points for all entrants Line Graph")
    print("5. Coast Entrants Bar Graph")
    print("6. Number of Entrants and New Players Bar Graph")
    print("7. All Website Graphs")
    print("8. All TMT Details graphs")
    print()
    

def graphChoice() -> int:
    """The user decides what type of graph they want to create
    based off Ranks, Points, or Placements"""
    while True:
        option = input("User Choice: ")
        try:
            option = int(option)
        except:
            pass
        if option in range(1, 9):
            return option
        else:
            print("Choose an integer from 1 to 8\n")


def saveGraph() -> int:
    """The user decides whether to view the graphs as HTML or png."""
    print("How would you like to save the graphs?")
    print("1. Interactable Online Version")
    print("2. Save them as png")
    print()
    while True:
        option = input("User Choice: ")
        try:
            option = int(option)
        except:
            pass
        if option in (1, 2):
            return option
        else:
            print("Choose 1 or 2\n")










