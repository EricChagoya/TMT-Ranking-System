


def PrintWelcomeMessage() -> None:
    print("Hi There!")
    print("The Architect here! OmegaLUL\n")
    print("Which option would you like? (Press the number you want)")
    print("\t1. Update the Ladder Rankings")
    print("\t2. Update the Bracket Rankings")


def UserChoice() -> int:
    """The user decides what option they want"""
    while True:
        option = input("")
        try:
            option = int(option)
        except:
            pass
        if option in (1, 2):
            return option
        else:
            print("Choose 1 or 2\n")


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





