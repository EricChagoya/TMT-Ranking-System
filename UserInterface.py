




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
    print("2. Update the Ladder and Bracket Rankings")


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
    print("1. Ranks for each character")
    print("2. Top 10 Ranked Players")
    print("3. Points for each character")
    print("4. Points of the Top 10 Players")
    print("5. Combined Points for both Coasts")
    print("6. Coast Entrants Bar Graph")
    print("7. Number of New Graph")
    print("8. All Website Graphs")
    print("9. All TMT Staff Graphs")
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
        if option in range(1, 10):
            return option
        else:
            print("Choose an integer from 1 to 9\n")


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










