




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
    print("\t1. Update the Ladder Rankings")
    print("\t2. Update the Bracket Rankings")


def rankChoice() -> int:
    """The user decides whether they want to create the ranks
    for ladder or ladder and bracket"""
    while True:
        option = input("1 For ladder only. 2 for ladder and bracket: ")
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
    print("I was wondering if you want to create a graph for:")
    print("\t1 Ranks")
    print("\t2 Points")
    print("\t3 Placements")
    

def graphChoice() -> int:
    """The user decides what type of graph they want to create
    based off Ranks, Points, or Placements"""
    while True:
        option = input("")
        try:
            option = int(option)
        except:
            pass
        if option in (1, 2, 3):
            return option
        else:
            print("Choose 1, 2, or 3\n")


