#...................Explaination of Representations.................
'''
     The Sudoku Board:

  \ R  0  1  2    3  4  5    6  7  8
 C \
       bSquare6:  bSquare7:  bSquare8:
 8     72 73 74   75 76 77   78 79 80
 7     63 64 65   66 67 68   69 70 71
 6     54 55 56   57 58 59   60 61 62
       bSquare3:  bSquare4:  bSquare5:
 5     45 46 47   48 49 50   51 52 53
 4     36 37 38   39 40 41   42 43 44
 3     27 28 29   30 31 32   33 34 35
       bSquare0:  bSquare1:  bSquare2:
 2     18 19 20   21 22 23   24 25 26
 1     9  10 11   12 13 14   15 16 17
 0     0  1  2    3  4  5    6  7  8

 R = row
 C = column
 bSquare = big square
 square = individual little square (from 0 until 80 inclusive)
'''
import json
import datetime
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 40

#..........................User interface..................

def hardestSudokuInTheWorld():
    board = [0]*81
    board[72] = 8
    board[65] = 3
    board[66] = 6
    board[55] = 7
    board[58] = 9
    board[60] = 2
    board[46] = 5
    board[50] = 7
    board[40] = 4
    board[41] = 5
    board[42] = 7
    board[30] = 1
    board[34] = 3
    board[20] = 1
    board[25] = 6
    board[26] = 8
    board[11] = 8
    board[12] = 5
    board[16] = 1
    board[1] = 9
    board[6] = 4
    return board
def inputToBoard(board, boardIsEmpty):
    if boardIsEmpty:
        if input("Do you want to use the hardest board in the world?(y/n): ") == "y": board = hardestSudokuInTheWorld()
    lastSquareNumber = -1
    while True:
        print("\n\n\n\n\n\n\n\n\n\n")
        print("representation of the squares in the sudoku board:")
        printRepresentationOfPlaces()
        print("\n\nThis is how the board looks like in the meantime:")
        printBoard(board)
        print("")
        squareNumber = 0
        squareNumber = lastSquareNumber + 1
        if squareNumber == 81: squareNumber = 0
        correctInput = False
        valueToInput = 0
        while not(correctInput):
            correctInput = True
            try:
                valueToInput = int(input("What value do you want to input in square number " + str(squareNumber) + \
                                         "?\n(from 0 until 9 inclusive, or -1 for inputting somewhere else, or -2 for solve board): "))
            except ValueError:
                print("invalid input, not an integer")
                correctInput = False
                continue
            if valueToInput == -2:
                print("\nUsing this board:")
                printBoard(board)
                print("")
                return board
            elif valueToInput == -1:
                print("")
                correctInput1 = False
                while not(correctInput1):
                    correctInput1 = True
                    try:
                        squareNumber = int(input("What square number do you want to input to?\n(from 0 until 80 inclusive, or -1 or -2 for solve board): "))
                    except ValueError:
                        print("wrong input, not an integer")
                        correctInput1 = False
                        continue
                    if (squareNumber == -1) or (squareNumber == -2):
                        print("\nUsing this board:")
                        printBoard(board)
                        print("")
                        return board
                    if not((squareNumber >= 0) and (squareNumber <= 80)):
                        correctInput1 = False
                        print("wrong input, outside of range")
                    else:
                        print("")
                correctInput = False
            elif not((valueToInput >= 0) and (valueToInput <= 9)):
                correctInput = False
                print("invalid input, outside of range")
            else:
                boardC = board.copy()
                boardC[squareNumber] = valueToInput
                if not(isBoardValidBasedOnChangedSquare(boardC, squareNumber)):
                    if input("input is contradictory with existing board, are you sure it's correct?(y/n): ") == "n":
                        print("\nOk then, not using your last input")
                        correctInput = False
                    else: print("")
        lastSquareNumber = squareNumber
        board[squareNumber] = valueToInput
def createBoard():
    notFound = False
    try:
        lastBoard = open("lastBoardInputted.json")
        board = json.load(lastBoard)
        lastBoard.close()
    except FileNotFoundError:
        print("lastBoardInputted.json Not found! No worries. Making new board that you\'ll input to.")
        notFound = True
    if (notFound) or (input("Do you want to use your board from last time?(y/n): ") == "n"):
        board = [0]*81
        board = inputToBoard(board.copy(), True)
        lastBoard = open("lastBoardInputted.json", "w")
        json.dump(board, lastBoard)
        lastBoard.close()
        return board
    else:
        board = inputToBoard(board.copy(), False)
        lastBoard = open("lastBoardInputted.json", "w")
        json.dump(board, lastBoard)
        lastBoard.close()
        return board
def printBoard(board):
    print(createStringOfBoard(board))
def createStringOfBoard(board):
    strOfBoard = ""
    for row in range(8, -1, -1):
        for column in range(9):
            square = fromRowAndColumnToSquare(row, column)
            strOfBoard += str(board[square])
            if column == 8:
                if row != 0:
                    strOfBoard += "\n"
                if (row == 6) or (row == 3): strOfBoard += "\n"
            else:
                strOfBoard += " "
                if column == 2: strOfBoard += "  "
                elif column == 5: strOfBoard += "  "
    return strOfBoard
def printRepresentationOfPlaces():
    print("72 73 74   75 76 77   78 79 80\n63 64 65   66 67 68   69 70 71\n54 55 56   57 58 59   60 61 62\n\n45 46 47   48 49 50   51 52 53\n36 37 38   39 40 41   42 43 44\n27 28 29   30 31 32   33 34 35\n\n18 19 20   21 22 23   24 25 26\n9  10 11   12 13 14   15 16 17\n0  1  2    3  4  5    6  7  8 ")

#..................Functions For Actual Algorithm...............

def fromSquareToRow(square):
    return (square // 9)
def fromSquareToColumn(square):
    return (square % 9)
def fromSquareTobSquare(square):
    return ((square//27)*3 + (square%9)//3)
def fromRowAndColumnToSquare(row, column):
    return ((row*9) + column)
def bottomLeftSquareOfbSquare(bSquare):
    return ((bSquare//3)*27 + 3*(bSquare%3))
def frombSquareToSquares(bSquare):
    listOfSquares = [0]*9
    bottomLeftSquare = bottomLeftSquareOfbSquare(bSquare)
    counter = 0
    for skipUp in range(3):
        for skipRight in range(3):
            square = bottomLeftSquare + skipUp*9 + skipRight
            listOfSquares[counter] = square
            counter += 1
    return listOfSquares
def fromRowToSquares(row):
    listOfSquares = [0]*9
    leftSquare = fromRowAndColumnToSquare(row, 0)
    leftSquarePlus9 = leftSquare + 9
    counter = 0
    for square in range(leftSquare, leftSquarePlus9):
        listOfSquares[counter] = square
        counter += 1
    return listOfSquares
def fromColumnToSquares(column):
    listOfSquares = [0]*9
    bottomSquare = fromRowAndColumnToSquare(0, column)
    bottomSquarePlus73 = bottomSquare + 73
    counter = 0
    for square in range(bottomSquare, bottomSquarePlus73, 9):
        listOfSquares[counter] = square
        counter += 1
    return listOfSquares
def fromRowTobSquares(rowNum):
    listOfbSquares = [0]*3
    rnd3t3 = (rowNum//3)*3
    listOfbSquares[0] = rnd3t3
    rnd3t3 += 1
    listOfbSquares[1] = rnd3t3
    rnd3t3 += 1
    listOfbSquares[2] = rnd3t3
    return listOfbSquares
def isRowValid(board, rowNum):
    numbersTaken = [False]*10
    squaresOfRow = fromRowToSquares(rowNum)
    for square in squaresOfRow:
        value = board[square]
        if value == 0: continue
        if numbersTaken[value]: return False
        numbersTaken[value] = True
    return True
def isbSquareValid(board, bSquareNum):
    numbersTaken = [False]*10
    squaresOfbSquare = frombSquareToSquares(bSquareNum)
    for square in squaresOfbSquare:
        value = board[square]
        if value == 0: continue
        if numbersTaken[value]: return False
        numbersTaken[value] = True
    return True
def isColumnValid(board, columnNum):
    numbersTaken = [False]*10
    squaresOfColumn = fromColumnToSquares(columnNum)
    for square in squaresOfColumn:
        value = board[square]
        if value == 0: continue
        if numbersTaken[value]: return False
        numbersTaken[value] = True
    return True
def isBoardValidBasedOnChangedSquare(board, changedSquareNum):
    if not(isRowValid(board, fromSquareToRow(changedSquareNum))): return False
    if not(isColumnValid(board, fromSquareToColumn(changedSquareNum))): return False
    if not(isbSquareValid(board, fromSquareTobSquare(changedSquareNum))): return False
    return True
def isBoardValidBasedOnChangedRow(board, changedRowNum):
    for column in range(9):
        if not(isColumnValid(board, column)): return False
    listOfbSquares = fromRowTobSquares(changedRowNum)
    for bSquareNum in listOfbSquares:
        if not(isbSquareValid(board, bSquareNum)): return False
    return True
def listAllValidValuesForEachSquare(board):
    listOfValidValuesForEachSquare = [[] for _ in range(81)]
    boardC = board.copy()
    for square in range(81):
        bs = board[square]
        if bs != 0:
            listOfValidValuesForEachSquare[square].append(bs)
            continue
        for value in range(1, 10):
            boardC[square] = value
            if isBoardValidBasedOnChangedSquare(boardC, square): listOfValidValuesForEachSquare[square].append(value)
        boardC[square] = 0
    return listOfValidValuesForEachSquare
def listAllValidCombForRow(board, row, listOfValidValuesForEachSquare, squareNumsInRow):
    listOfAllValidCombForRow = []
    amountOfPossValuesForEachSquareInRow = [0]*9
    numSquare1To9 = 0
    for squareNum in squareNumsInRow:
        amountOfPossValuesForEachSquareInRow[numSquare1To9] = len(listOfValidValuesForEachSquare[squareNum])
        numSquare1To9 += 1
    currentNumPossForEachSquare = [0]*9
    currentSquareToChange = 0
    valuesUsed = [False]*10
    valuesUsedByStep = []
    while True: #replacement for a recursive algorithm
        possibilityNumber = currentNumPossForEachSquare[currentSquareToChange]
        if possibilityNumber >= amountOfPossValuesForEachSquareInRow[currentSquareToChange]:
            if currentSquareToChange == 0: break
            valuesUsed[valuesUsedByStep.pop()] = False
            currentNumPossForEachSquare[currentSquareToChange] = 0
            currentSquareToChange -= 1
            currentNumPossForEachSquare[currentSquareToChange] += 1
        else:
            currentValue = listOfValidValuesForEachSquare[squareNumsInRow[currentSquareToChange]][possibilityNumber]
            if valuesUsed[currentValue]: currentNumPossForEachSquare[currentSquareToChange] += 1
            else:
                if currentSquareToChange == 8:
                    valuesUsedByStep.append(currentValue)
                    listOfAllValidCombForRow.append(valuesUsedByStep.copy())
                    valuesUsedByStep.pop()
                    valuesUsed[valuesUsedByStep.pop()] = False
                    currentNumPossForEachSquare[currentSquareToChange] = 0
                    currentSquareToChange -= 1
                    currentNumPossForEachSquare[currentSquareToChange] += 1
                else:
                    valuesUsed[currentValue] = True
                    valuesUsedByStep.append(currentValue)
                    currentSquareToChange += 1
    return listOfAllValidCombForRow
def listAllValidCombForEachRow(board, squareNumsForEachRow):
    listOfAllValidCombForEachRow = []
    listOfValidValuesForEachSquare = listAllValidValuesForEachSquare(board)
    for row in range(9):
        listOfAllValidCombForEachRow.append(listAllValidCombForRow(board, row, listOfValidValuesForEachSquare, squareNumsForEachRow[row]))
    return listOfAllValidCombForEachRow
def calcPercentDone(amountOfPossCombForEachRow, currentCombNumForEachRow, currentRowToChange):
    multOfMax = 1
    sumOfMultOfMax = 0
    sumOfMultOfCurrent = Fraction(0, 1)
    for row in range(8, -1, -1):
        multOfMax *= amountOfPossCombForEachRow[row]
        sumOfMultOfMax += multOfMax
        if row <= currentRowToChange:
            sumOfMultOfCurrent += (Fraction((currentCombNumForEachRow[row]) / (amountOfPossCombForEachRow[row])))*multOfMax
    FractionAnswer = (sumOfMultOfCurrent / sumOfMultOfMax)*100
    DecimalAnswer = Decimal(FractionAnswer.numerator) / Decimal(FractionAnswer.denominator)
    return (DecimalAnswer)
def convertSecondsToString(numOfSeconds):
    numOfSecondsCopy = numOfSeconds
    Days = int(numOfSecondsCopy / 86400)
    numOfSecondsCopy -= Days*86400
    Hours = int(numOfSecondsCopy / 3600)
    numOfSecondsCopy -= Hours*3600
    Minutes = int(numOfSecondsCopy / 60)
    numOfSecondsCopy -= Minutes*60
    strSeconds = '{0:f}'.format(numOfSecondsCopy)
    lenStrSeconds = len(strSeconds)
    end = lenStrSeconds - 1
    start = 0
    if numOfSecondsCopy >= 10:
        start = 3
    else:
        start = 2
    for charNum in range(start, lenStrSeconds):
        if strSeconds[charNum] != "0":
            end = charNum + 1
            break
    strSeconds = strSeconds[:end]
    strToReturn = ""
    is60SecondsOrAbove = False
    if Days != 0:
        strToReturn += ("Days: " + str(Days) + ", ")
        is60SecondsOrAbove = True
    if (Hours != 0) or (Days != 0):
        strToReturn += ("Hours: " + str(Hours) + ", ")
        is60SecondsOrAbove = True
    if (Minutes != 0) or (Days != 0) or (Hours != 0):
        strToReturn += ("Minutes: " + str(Minutes) + ", ")
        is60SecondsOrAbove = True
    if numOfSecondsCopy < 0.0001 and (not(is60SecondsOrAbove)): strToReturn = "no_idea"
    else: strToReturn += ("Seconds: " + strSeconds)
    return(strToReturn)
def findSolutionToBoard(originalBoard):
    timeWastedOnUserInput = datetime.timedelta()
    solutionBoardToReturn = originalBoard.copy()
    allSolutionBoards = [] #just in case it's an invalid sudoku board with more than one solution
    squareNumsForEachRow = []
    for rowCounter in range(9):
        squareNumsForEachRow.append(fromRowToSquares(rowCounter))
    listOfAllValidCombForEachRow = listAllValidCombForEachRow(originalBoard, squareNumsForEachRow)
    amountOfPossCombForEachRow = [0]*9
    rowNumber = 0
    for rowCombinations in listOfAllValidCombForEachRow:
        lenOfRowComb = len(rowCombinations)
        if lenOfRowComb == 0: #is no solution to board
            return (allSolutionBoards, timeWastedOnUserInput, 100.0)
        amountOfPossCombForEachRow[rowNumber] = lenOfRowComb
        rowNumber += 1
    currentRowToChange = 0
    currentCombNumForEachRow = [0]*9
    aopcfer0 = amountOfPossCombForEachRow[0]
    askedUserToStop = False
    percentageToStopAt = Decimal(100)
    timeOfLastCheck = datetime.datetime.now()
    Seconds = datetime.timedelta(seconds = 2)
    counterOfWhile = 0
    timeStartOfWholeLoop = datetime.datetime.now()
    askedUserToStop1 = False
    while True:
        counterOfWhile += 1
        if counterOfWhile >= 100000:
            counterOfWhile = 0
            changeInTime = datetime.datetime.now() - timeOfLastCheck
            if changeInTime > Seconds:
                percentDone = calcPercentDone(amountOfPossCombForEachRow, currentCombNumForEachRow, currentRowToChange)
                if not(askedUserToStop):
                    timeUntilNowOfAlgWorking = (datetime.datetime.now() - timeStartOfWholeLoop) - timeWastedOnUserInput

                    numOfSecondsAltogether = (percentageToStopAt/percentDone)*(Decimal(timeUntilNowOfAlgWorking.total_seconds()))
                    estimatedTimeAltogether = datetime.timedelta(seconds = float(numOfSecondsAltogether))
                    timeUntilNowOfAlgWorkingSeconds = Decimal(timeUntilNowOfAlgWorking.total_seconds())
                    estimatedTimeRemainingSeconds = numOfSecondsAltogether - timeUntilNowOfAlgWorkingSeconds
                    estimatedTimeRemaining = convertSecondsToString(estimatedTimeRemainingSeconds)
                    numOfSolutions = len(allSolutionBoards)
                    print("Number of solutions so far: " + str(numOfSolutions) + "  " + str(percentDone) + "% done. ETA " + str(estimatedTimeRemaining))
                    if numOfSolutions >= 2:
                        startTimeUserInput = datetime.datetime.now()
                        askedUserToStop = True
                        inputIsValid = False
                        while not(inputIsValid):
                            inputIsValid = True
                            percentageToCompleteStr = input("\nThe program has already found " + str(numOfSolutions) + " solutions.\n" + \
                                     "Do you want to continue finding more solutions? (enter percentage of solutions to find, 0% for stop now, 100% for find all): ")
                            print("")
                            if len(percentageToCompleteStr) == 0:
                                print("invalid input for percentage, you inputted nothing.")
                                inputIsValid = False
                                continue
                            lastChar = percentageToCompleteStr[-1]
                            if lastChar == "%": percentageToCompleteStr = percentageToCompleteStr[:-1]
                            if len(percentageToCompleteStr) == 0:
                                print("invalid input for percentage. You didn\'t input any number.")
                                inputIsValid = False
                                continue
                            try:
                                percentageToStopAt = Decimal(percentageToCompleteStr)
                            except ValueError:
                                print("The percentage you entered isn\'t a floating poing number.")
                                inputIsValid = False
                                continue
                            if (percentageToStopAt < 0) or (percentageToStopAt > 100):
                                print("The percentage you entered is out of the 0-100 range.")
                                inputIsValid = False
                                continue
                        if percentageToStopAt == 0:
                            print("\nOk, stopping now.\nFinishing early, at " + str(percentDone) + "% done")
                            timeWastedOnUserInput = datetime.datetime.now() - startTimeUserInput
                            return (allSolutionBoards, timeWastedOnUserInput, percentDone)
                        elif percentageToStopAt == 100:
                            print("Ok, finding all solutions. this might take a while.\n")
                        else:
                            print("Ok, not exceeding finding " + str(percentageToStopAt) + "% of the solutions (not exact obviously)")
                        timeWastedOnUserInput = datetime.datetime.now() - startTimeUserInput
                    elif (numOfSolutions == 1) and not(askedUserToStop1):
                        askedUserToStop1 = True
                        startTimeUserInput1 = datetime.datetime.now()
                        if input("\nThe program has already found 1 solution.\nDo you want to continue trying to find more?(y/n): ") == "n":
                            timeWastedOnUserInput += (datetime.datetime.now() - startTimeUserInput1)
                            print("\nOk. Finishing early, at " + str(percentDone) + "% done.")
                            return (allSolutionBoards, timeWastedOnUserInput, percentDone)
                        else:
                            print("\nOk, Finding one more solution (and then asking you again to find more).")
                        print("")
                        timeWastedOnUserInput += (datetime.datetime.now() - startTimeUserInput1)
                else:
                    if percentDone > percentageToStopAt:
                        print("\nFinishing early, at " + str(percentDone) + "% done")
                        return (allSolutionBoards, timeWastedOnUserInput, percentDone)
                    else:
                        percentageToStopAtDividedByPercentDone = percentageToStopAt/percentDone
                        oneHundredDividedByPercentDone = Decimal(100)/percentDone
                        timeUntilNowOfAlgWorking = (datetime.datetime.now() - timeStartOfWholeLoop) - timeWastedOnUserInput
                        numOfSecondsAltogether = (percentageToStopAt/percentDone)*(Decimal(timeUntilNowOfAlgWorking.total_seconds()))
                        estimatedTimeAltogether = datetime.timedelta(seconds = float(numOfSecondsAltogether))
                        timeUntilNowOfAlgWorkingSeconds = Decimal(timeUntilNowOfAlgWorking.total_seconds())
                        estimatedTimeRemainingSeconds = numOfSecondsAltogether - timeUntilNowOfAlgWorkingSeconds
                        estimatedTimeRemaining = convertSecondsToString(estimatedTimeRemainingSeconds)
                        numOfSolutions = len(allSolutionBoards)
                        print("Number of solutions so far: " + str(numOfSolutions) + "  " + str(percentDone) + "% done. ETA " + estimatedTimeRemaining + \
                              "  Estimated total number of solutions: " + str(int(oneHundredDividedByPercentDone * numOfSolutions)))
                timeOfLastCheck = datetime.datetime.now()
        currentCombNum = currentCombNumForEachRow[currentRowToChange]
        if currentCombNum >= amountOfPossCombForEachRow[currentRowToChange]:
            if currentRowToChange == 0: break #exhausted all possibilities of row combinations
            currentCombNumForEachRow[currentRowToChange] = 0
            currentRowToChange -= 1
            squareNumsForCurrentRow = squareNumsForEachRow[currentRowToChange]
            for square in squareNumsForCurrentRow: solutionBoardToReturn[square] = originalBoard[square]
            currentCombNumForEachRow[currentRowToChange] += 1
        else:
            squareNum = 0
            loavcfercrtcccn = listOfAllValidCombForEachRow[currentRowToChange][currentCombNum]
            squareNumsForCurrentRow = squareNumsForEachRow[currentRowToChange]
            for square in squareNumsForCurrentRow:
                solutionBoardToReturn[square] = loavcfercrtcccn[squareNum]
                squareNum += 1
            if isBoardValidBasedOnChangedRow(solutionBoardToReturn, currentRowToChange):
                if currentRowToChange == 8:
                    allSolutionBoards.append(solutionBoardToReturn.copy())
                    squareNumsForCurrentRow = squareNumsForEachRow[currentRowToChange]
                    for square in squareNumsForCurrentRow: solutionBoardToReturn[square] = originalBoard[square]
                    currentCombNumForEachRow[currentRowToChange] = 0
                    currentRowToChange -= 1
                    squareNumsForCurrentRow7 = squareNumsForEachRow[currentRowToChange]
                    for square7 in squareNumsForCurrentRow7: solutionBoardToReturn[square7] = originalBoard[square7]
                    currentCombNumForEachRow[currentRowToChange] += 1
                else:
                    currentRowToChange += 1
            else:
                squareNumsForCurrentRow = squareNumsForEachRow[currentRowToChange]
                for square in squareNumsForCurrentRow: solutionBoardToReturn[square] = originalBoard[square]
                currentCombNumForEachRow[currentRowToChange] += 1
    print("\n100% done!!!" + "  Number of solutions so far: " + str(len(allSolutionBoards)))
    return (allSolutionBoards, timeWastedOnUserInput, 100.0)
board = createBoard()
startTime = datetime.datetime.now()
print("\nCalculating...")
allSolutionBoards, timeWastedOnUserInput, percentageOfSolutionCompleted = findSolutionToBoard(board)
timeTook = datetime.datetime.now() - startTime
timeTook -= timeWastedOnUserInput
numOfSolutions = len(allSolutionBoards)
toPrintToFile = False
print("Calculations completed in " + str(timeTook) + "  (Not including time of user input)\n" + \
      "                          H M  Seconds\n\n" + \
      "Percentage of solutions that the program checked: " + str(percentageOfSolutionCompleted) + "%\n\n" + \
      "Original board that I needed to solve:\n" + createStringOfBoard(board) + "\n\n")
print("Final Solution:\n")
if numOfSolutions == 0: print("No Solutions")
elif numOfSolutions == 1:
    if percentageOfSolutionCompleted == 100:
        print("Valid board, there\'s only one solution:")
    else:
        print("Whether the board is valid or invalid is unknown.\nOnly one solution was found, but that doesn't mean that it\'s the only one that exists:")
    printBoard(allSolutionBoards[0])
    print("")
    if input("do you want to write the solution into a text file?(y/n): ") == "y": toPrintToFile = True
else:
    print("Invalid board, it has " + str(len(allSolutionBoards)) + " solutions. for example:\nsolution 1:")
    printBoard(allSolutionBoards[0])
    print("\n\nsolution 2:")
    printBoard(allSolutionBoards[1])
    print("")
    if numOfSolutions > 2:
        if input("do you want to print the rest of the solutions?(y/n): ") == "y":
            for solutionNum in range(2, numOfSolutions):
                print("\n\nsolution " + str(solutionNum + 1) + ":")
                printBoard(allSolutionBoards[solutionNum])
                print("")
    if input("do you want to write all solutions into a text file?(y/n): ") == "y": toPrintToFile = True
if toPrintToFile:
    inputFileNameAgain = True
    nameOfFile = ""
    while inputFileNameAgain:
        inputFileNameAgain = True
        nameOfFile = input("what do you want to call the file?(with .txt): ")
        try:
            fileOfSolutionsTry = open(nameOfFile)
            fileOfSolutionsTry.close()
            print("\nThe file with the directory / file name:\n" + nameOfFile + "\nalready exists. Try using a different directory / file name.\n")
        except FileNotFoundError:
            inputFileNameAgain = False
    fileOfSolutions = open(nameOfFile, "w")
    fileOfSolutions.write("Calculations completed in " + str(timeTook) + "  (Not including time of user input)\n" + \
                          "                          H M  Seconds\n\n" + \
                          "Percentage of solutions that the program checked: " + str(percentageOfSolutionCompleted) + "%\n\n" + \
                          "Original board that I needed to solve:\n" + createStringOfBoard(board) + \
                          "\n\nNumber of solutions found: " + str(numOfSolutions) )
    if percentageOfSolutionCompleted == 0:
        fileOfSolutions.write("It is unknown whether the board is valid or invalid")
    for solutionNum in range(numOfSolutions):
        fileOfSolutions.write("\n\nsolution " + str(solutionNum + 1) + ":\n" + (createStringOfBoard(allSolutionBoards[solutionNum]) + "\n"))
    fileOfSolutions.close()
    print("\nFinished writing the solutions into the text file.")
input("\npress enter to exit program")
