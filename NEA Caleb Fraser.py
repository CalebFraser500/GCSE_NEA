import csv  # import python module for reading csv files
information = []    # Initialises information list outside of functions to allow global access
aircraftType = []   # Initialises aircraftType list outside of functions to allow global access


def airportDetails():   # Defines airportDetails function/subroutine
    localCode = input("Enter three digit airport code: ")   # User enters local airport 3-digit identifier
    if localCode.lower() != "lpl" and localCode.lower() != "boh":   # Checks that entered code is valid
        print("Error: Invalid code")
        menu()  # Calls the menu function
    information.append(localCode)   # Appends local airport code to information
    foreignCode = input("Enter three digit foreign airport code: ").upper()  # User enters foreign airport 3-digit identifier
    with open("airports.txt", "r") as f:    # Opens airports file in read mode
        reader = csv.reader(f, delimiter=",")
        for row in reader:  # For loop runs through all rows in file
            if foreignCode in row[0]:   # Checks if the foreign airport is in airports.txt
                print("Your destination airport is", row[1])
                break   # Ends the for loop
        else:
            print("Error: Airport not found")
        information.append(foreignCode.upper())     # Appends  foreign airport code to information
        f.close()   # Closes file
        menu()  # Calls menu function


def flightDetails():    # Defines flightDetails function/subroutine
    global firstClass   # Creates the variable firstClass, which can be accessed outside the function
    global standard

    aircraft = input("Enter aircraft type (medium narrow body, medium wide body, large narrow body): ")     # Allows user to enter the chosen aircraft type
    if aircraft.lower() != "medium narrow body" and aircraft.lower() != "medium wide body" and aircraft.lower() != "large narrow body":     # If statement checks if aircraft's syntax is correct
        print("Error: Invalid aircraft")
        menu()
    information.append(aircraft)    # Appends chosen aircraft type to information
    with open("airports.txt", "r") as f:    # Opens file
        reader = csv.reader(f, delimiter=",")
        for row in reader:  # For loop runs through all rows in file
            if aircraft in row[0]:  # Checks if aircraft is in current row
                aircraftType.append(row)    # Appends aircraft information to aircraftType list
                print("Cost per 100km =", row[1], "flight range =", row[2], "capacity (standard) =", row[3],
                      "minimum first class =", row[4])
                break
        else:
            print("Error: Aircraft type not found")     # Error displays if aircraft is not found

        firstClass = int(input("Please enter amount of first-class seats on aircraft: "))   # User enters the amount of first-class seats on aircraft
        if firstClass > 0:
            if firstClass < int(row[4]):    # Checks that amount of first-class seats exceeds minimum
                print("Error: First class seats less than minimum for", row[0], "aircraft")
                menu()
            elif firstClass > (int(row[3]) / 2):    # Checks that amount of first-class seats is less than maximum
                print("Error: First class seats surpass maximum for", row[0], "aircraft")
        information.append(firstClass)  # Appends amount of firstclass seats to information
        standard = int(row[3]) - (firstClass * 2)   # Calculates amount of standard seats available using amount of first-class seats
        information.append(standard)    # Appends amount of standard seats to information
        print("Standard seats on aircraft is", standard)
        menu()


def priceProfit():  # Defines priceProfit function/subroutine
    if information[0] == "":                        # Checks if all needed information has been entered
        print("Error: local airport not found")
        menu()
    elif information[1] == "":
        print("Error: foreign airport not found")
        menu()
    elif information[2] == "":
        print("Error: aircraft type not found")
        menu()
    elif information[3] == "":
        print("Error: no# first-class seats not found")
        menu()
    elif information[4] == "":
        print("Error: no# standard seats not found")
        menu()
    airportDistance = distanceCheck()   # Runs distanceCheck subroutine
    standardPrice = int(input("Enter price of standard seat: "))    # User enters price of standard seat
    firstClassPrice = int(input("Enter price of first-class seat: "))    # User enters price of first-class seat
    flightCostPerSeat = (int(aircraftType[0][1]) * int(airportDistance)) / 100  # Calculates flight cost per seat
    print("Flight cost per seat is", flightCostPerSeat)
    flightCost = flightCostPerSeat * (firstClass + standard)    # Calculates total flight cost
    print("Flight cost total is", flightCost)
    flightIncome = (firstClass * firstClassPrice) + (standard * standardPrice)  # Calculates total flight income
    print("Flight income is", flightIncome)
    flightProfit = flightIncome - flightCost    # Calculates flight profit
    print("Flight profit is", flightProfit.__round__())  # Outputs flight profit, rounds the sum to nearest integer
    menu()


def distanceCheck():    # Defines distanceCheck function/subroutine
    with open("airports.txt", "r") as f:    # Opens airports file in read mode
        reader = csv.reader(f, delimiter=",")
        if information[0].lower() == "lpl":     # Checks if local airport is lpl
            for row in reader:  # For loop running through all lines in airports file
                if information[1] in row:   # Checks if foreign airport is in row
                    airportDistance = row[2]    # Sets airportDistance using distance from local to foreign airport

                if information[2] in row:   # Checks if aircraft type max distance is in row
                    maxDistance = row[2]    # information[2] is max distance aircraft type can travel
        elif information[0].lower() == "boh":   # Checks if local airport is boh
            for row in reader:
                if information[1] in row:
                    airportDistance = row[3]

                if information[2] in row:
                    maxDistance = row[2]
        if maxDistance <= airportDistance:  # Checks if distance between airports exceeds aircraft travel distance
            print("Error: Distance exceeds maximum travel distance of", information[2])
            menu()


    f.close()   # Closes airports file
    return airportDistance  # Returns airportDistance variable to priceProfit()


def menu():     # Defines menu function/subroutine
    print(      # Outputs menu options to user (use of multi-line print)

        '''
1) Enter Airport Details
2) Enter flight Details
3) Enter price plan and calculate profit
4) Clear Data
5) Quit
        '''
    )

    choice = int(input("Enter Menu Choice (1-5): "))    # choice variable allows user to choose menu option in integer

    if choice == 1:     # If statement w/ elif and else
        airportDetails()    # Calls airportDetails function
    elif choice == 2:
        flightDetails()  # Calls flightDetails function
    elif choice == 3:
        priceProfit()   # Calls priceProfit function
    elif choice == 4:
        global information  # Allows information to be accessed outside menu function
        information = []    # Clears data in information
        print("Entered data has been cleared")
        menu()
    elif choice == 5:
        print("Thanks for using airport program")
        quit()  # Python function to end program
    else:
        print("Invalid Choice")
        menu()  # Calls menu function


menu()      # Calls menu function on startup
