import numpy as np
import sys
from random import randrange

def showUtilityMatrixAveraged(gameBoard, numOfTrials):
    # Use vectorize to apply our lambda (division) function to each cell
    vectorizedFunction = np.vectorize(lambda element: element/numOfTrials)
    averagedGameBoard = vectorizedFunction(gameBoard)
    print(averagedGameBoard)

def getAvailablePositions(gameBoard):
    """
    :param gameBoard: the current 4x4x4 game board for the iteration
    :return: a list of tuples representing the indices of available spaces
    """
    positions = []
    # Iterate through the game board and search for spaces that are 0, representing available space
    for matrix in range(4):
        for row in range(4):
            for col in range(4):
                if gameBoard[matrix][row][col] == 0:
                    positions.append((matrix, row, col))
    return positions


def checkForThreeInARow(lastPlacedMatrix, gameBoard, player, lastPlacedRow, lastPlacedCol):
    """
    :param gameBoard:
    :param player: -1 or 1, representing current player turn
    :return: index of the winning cell or None if N/A
    """
    # check along current matrix's row
    rowSum = 0
    for col in range(4):
        rowSum += gameBoard[lastPlacedMatrix][lastPlacedRow][col]
    if rowSum == 3 * player:
        for col in range(4):
            if gameBoard[lastPlacedMatrix][lastPlacedRow][col] == 0:
                return lastPlacedMatrix, lastPlacedRow, col
    # check along current matrix's col
    colSum = 0
    for row in range(4):
        colSum += gameBoard[lastPlacedMatrix][row][lastPlacedCol]
    if colSum == 3 * player:
        for row in range(4):
            if gameBoard[lastPlacedMatrix][row][lastPlacedCol] == 0:
                return lastPlacedMatrix, row, lastPlacedCol
    # check along z axis
    zSum = 0
    for matrix in range(4):
        zSum += gameBoard[matrix][lastPlacedRow][lastPlacedCol]
    if zSum == 3 * player:
        for matrix in range(4):
            if gameBoard[matrix][lastPlacedRow][lastPlacedCol] == 0:
                return matrix, lastPlacedRow, lastPlacedCol
    currentMatrix = gameBoard[lastPlacedMatrix]
    # check the sum of a diagonal of a matrix, from top left to bottom right (the trace)
    zDiagonalSum1 = np.trace(currentMatrix)
    if zDiagonalSum1 == 3 * player:
        if currentMatrix[0][0] == 0:
            return lastPlacedMatrix, 0, 0
        elif currentMatrix[1][1] == 0:
            return lastPlacedMatrix, 1, 1
        elif currentMatrix[2][2] == 0:
            return lastPlacedMatrix, 2, 2
        elif currentMatrix[3][3] == 0:
            return lastPlacedMatrix, 3, 3
    # check the sum of a diagonal of a matrix, from top right to bottom left
    zDiagonalSum2 = currentMatrix[0][3] + currentMatrix[1][2] + currentMatrix[2][1] + currentMatrix[3][0]
    if zDiagonalSum2 == 3 * player:
        if currentMatrix[0][3] == 0:
            return lastPlacedMatrix, 0, 3
        elif currentMatrix[1][2] == 0:
            return lastPlacedMatrix, 1, 2
        elif currentMatrix[2][1] == 0:
            return lastPlacedMatrix, 2, 1
        elif currentMatrix[3][0] == 0:
            return lastPlacedMatrix, 3, 0
    # Checking across matrices for diagonals where one variable can be held constant (per iteration)
    for index in range(4):
        xDiagonalSum1 = gameBoard[0][index][0] + gameBoard[1][index][1] + gameBoard[2][index][2] + gameBoard[3][index][
            3]
        xDiagonalSum2 = gameBoard[3][index][0] + gameBoard[2][index][1] + gameBoard[1][index][2] + gameBoard[0][index][
            3]
        yDiagonalSum1 = gameBoard[0][3][index] + gameBoard[1][2][index] + gameBoard[2][1][index] + gameBoard[3][0][
            index]
        yDiagonalSum2 = gameBoard[0][0][index] + gameBoard[1][1][index] + gameBoard[2][2][index] + gameBoard[3][3][
            index]
    if xDiagonalSum1 == 3 * player:
        for index in range(4):
            if gameBoard[0][index][0] == 0:
                return 0, index, 0
            elif gameBoard[1][index][1] == 0:
                return 1, index, 1
            elif gameBoard[2][index][2] == 0:
                return 2, index, 2
            elif gameBoard[3][index][3] == 0:
                return 3, index, 3
    if xDiagonalSum2 == 3 * player:
        for index in range(4):
            if gameBoard[3][index][0] == 0:
                return 3, index, 0
            elif gameBoard[2][index][1] == 0:
                return 2, index, 1
            elif gameBoard[1][index][2] == 0:
                return 1, index, 2
            elif gameBoard[0][index][3] == 0:
                return 0, index, 3
    if yDiagonalSum1 == 3 * player:
        for index in range(4):
            if gameBoard[0][3][index] == 0:
                return 0, 3, index
            elif gameBoard[1][2][index] == 0:
                return 1, 2, index
            elif gameBoard[2][1][index] == 0:
                return 2, 1, index
            elif gameBoard[3][0][index] == 0:
                return 3, 0, index
    if yDiagonalSum2 == 3 * player:
        for index in range(4):
            if gameBoard[0][0][index] == 0:
                return 0, 0, index
            elif gameBoard[1][1][index] == 0:
                return 1, 1, index
            elif gameBoard[2][2][index] == 0:
                return 2, 2, index
            elif gameBoard[3][3][index] == 0:
                return 3, 3, index
    # Hardcoded to check for four different internal diagonals
    if gameBoard[0][0][0] + gameBoard[1][1][1] + gameBoard[2][2][2] + gameBoard[3][3][3] == 3 * player:
        if gameBoard[0][0][0] == 0:
            return 0, 0, 0
        elif gameBoard[1][1][1] == 0:
            return 1, 1, 1
        elif gameBoard[2][2][2] == 0:
            return 2, 2, 2
        elif gameBoard[3][3][3] == 0:
            return 3, 3, 3
    if gameBoard[0][0][3] + gameBoard[1][1][2] + gameBoard[2][2][1] + gameBoard[3][3][0] == 3 * player:
        if gameBoard[0][0][3] == 0:
            return 0, 0, 3
        elif gameBoard[1][1][2] == 0:
            return 1, 1, 2
        elif gameBoard[2][2][1] == 0:
            return 2, 2, 1
        elif gameBoard[3][3][0] == 0:
            return 3, 3, 0
    if gameBoard[0][3][3] + gameBoard[1][2][2] + gameBoard[2][1][1] + gameBoard[3][0][0] == 3 * player:
        if gameBoard[0][3][3] == 0:
            return 0, 3, 3
        elif gameBoard[1][2][2] == 0:
            return 1, 2, 2
        elif gameBoard[2][1][1] == 0:
            return 2, 1, 1
        elif gameBoard[3][0][0] == 0:
            return 3, 0, 0
    if gameBoard[0][3][0] + gameBoard[1][2][1] + gameBoard[2][1][2] + gameBoard[3][0][3] == 3 * player:
        if gameBoard[0][3][0] == 0:
            return 0, 3, 0
        elif gameBoard[1][2][1] == 0:
            return 1, 2, 1
        elif gameBoard[2][1][2] == 0:
            return 2, 1, 2
        elif gameBoard[3][0][3] == 0:
            return 3, 0, 3
    return None


def checkIfWinner(gameBoard, lastPlacedMatrix, lastPlacedRow, lastPlacedCol):
    # check along current matrix's row
    rowSum = 0
    for col in range(4):
        rowSum += gameBoard[lastPlacedMatrix][lastPlacedRow][col]
    if rowSum == 4 or rowSum == -4:
        return True
    # check along current matrix's col
    colSum = 0
    for row in range(4):
        colSum += gameBoard[lastPlacedMatrix][row][lastPlacedCol]
    if colSum == 4 or colSum == -4:
        return True
    # check along z axis
    zSum = 0
    for matrix in range(4):
        zSum += gameBoard[matrix][lastPlacedRow][lastPlacedCol]
    if zSum == 4 or zSum == -4:
        return True

    currentMatrix = gameBoard[lastPlacedMatrix]
    # check the sum of a diagonal of a matrix, from top left to bottom right (the trace)
    zDiagonalSum1 = np.trace(currentMatrix)
    if zDiagonalSum1 == 4 or zDiagonalSum1 == -4:
        return True
    # check the sum of a diagonal of a matrix, from top right to bottom left
    zDiagonalSum2 = currentMatrix[0][3] + currentMatrix[1][2] + currentMatrix[2][1] + currentMatrix[3][0]
    if zDiagonalSum2 == 4 or zDiagonalSum2 == -4:
        return True

    # Checking across matrices for diagonals where one variable can be held constant (per iteration)
    for index in range(4):
        xDiagonalSum1 = gameBoard[0][index][0] + gameBoard[1][index][1] + gameBoard[2][index][2] + gameBoard[3][index][
            3]
        xDiagonalSum2 = gameBoard[3][index][0] + gameBoard[2][index][1] + gameBoard[1][index][2] + gameBoard[0][index][
            3]
        yDiagonalSum1 = gameBoard[0][3][index] + gameBoard[1][2][index] + gameBoard[2][1][index] + gameBoard[3][0][
            index]
        yDiagonalSum2 = gameBoard[0][0][index] + gameBoard[1][1][index] + gameBoard[2][2][index] + gameBoard[3][3][
            index]

    if xDiagonalSum1 == 4 or xDiagonalSum2 == 4 or yDiagonalSum1 == 4 or yDiagonalSum2 == 4 or \
            xDiagonalSum1 == -4 or xDiagonalSum2 == -4 or yDiagonalSum1 == -4 or yDiagonalSum2 == -4:
        return True

    # Hardcoded to check for four different internal diagonals
    if gameBoard[0][0][0] + gameBoard[1][1][1] + gameBoard[2][2][2] + gameBoard[3][3][3] == 4 or \
            gameBoard[0][0][0] + gameBoard[1][1][1] + gameBoard[2][2][2] + gameBoard[3][3][3] == -4:
        return True

    if gameBoard[0][0][3] + gameBoard[1][1][2] + gameBoard[2][2][1] + gameBoard[3][3][0] == 4 or \
            gameBoard[0][0][3] + gameBoard[1][1][2] + gameBoard[2][2][1] + gameBoard[3][3][0] == -4:
        return True

    if gameBoard[0][3][3] + gameBoard[1][2][2] + gameBoard[2][1][1] + gameBoard[3][0][0] == 4 or \
            gameBoard[0][3][3] + gameBoard[1][2][2] + gameBoard[2][1][1] + gameBoard[3][0][0] == -4:
        return True

    if gameBoard[0][3][0] + gameBoard[1][2][1] + gameBoard[2][1][2] + gameBoard[3][0][3] == 4 or \
            gameBoard[0][3][0] + gameBoard[1][2][1] + gameBoard[2][1][2] + gameBoard[3][0][3] == - 4:
        return True
    return False


def findBestPosition(currentUtilityMatrix, listOfAvailablePositions):
    maxUtility = -sys.maxsize - 1
    bestPositions = []  # Stores the indices of the best positions, which may be multiple in case of ties
    # In the case of a tie, return
    if not listOfAvailablePositions:
        return None
    for position in listOfAvailablePositions:
        if currentUtilityMatrix[position[0]][position[1]][position[2]] > maxUtility:
            maxUtility = currentUtilityMatrix[position[0]][position[1]][position[2]]
            bestPositions = [position]  # If it is better than what we currently have, replace the list
        if currentUtilityMatrix[position[0]][position[1]][position[2]] == maxUtility:
            bestPositions.append(position)

    # Randomly pick an index of a max value
    bestPosition = (bestPositions[randrange(len(bestPositions))])
    return bestPosition


def playGame(existingUtilityMatrix, newGameBoard):
    winningPlayer = 0
    # We start with player -1 going first, outside of the while loop, since there is no need to check
    # for three in a row on the first move
    availablePositions = getAvailablePositions(newGameBoard)
    bestPosition = findBestPosition(existingUtilityMatrix, availablePositions)
    newGameBoard[bestPosition] = -1
    while True:
        # First, see if player 1 can win the game offensively
        if checkForThreeInARow(bestPosition[0], newGameBoard, 1, bestPosition[1], bestPosition[2]):
            bestPosition = checkForThreeInARow(bestPosition[0], newGameBoard, 1, bestPosition[1], bestPosition[2])
        # If player 1 cannot win the game offensively, see if it needs to block three -1's in a row
        elif checkForThreeInARow(bestPosition[0], newGameBoard, -1, bestPosition[1], bestPosition[2]):
            bestPosition = checkForThreeInARow(bestPosition[0], newGameBoard, -1, bestPosition[1], bestPosition[2])
        else:
            availablePositions = getAvailablePositions(newGameBoard)
            if not findBestPosition(existingUtilityMatrix, availablePositions):
                break
            # From the list of available positions, use findBestPosition to get the index of the best one
            bestPosition = findBestPosition(existingUtilityMatrix, availablePositions)
        newGameBoard[bestPosition] = 1
        if checkIfWinner(newGameBoard, bestPosition[0], bestPosition[1], bestPosition[2]):
            winningPlayer = 1
            break

        # Now, see if player -1 can win the game offensively
        if checkForThreeInARow(bestPosition[0], newGameBoard, -1, bestPosition[1], bestPosition[2]):
            bestPosition = checkForThreeInARow(bestPosition[0], newGameBoard, -1, bestPosition[1], bestPosition[2])
        # If player -1 cannot win the game offensively, see if it needs to block three 1's in a row
        elif checkForThreeInARow(bestPosition[0], newGameBoard, 1, bestPosition[1], bestPosition[2]):
            bestPosition = checkForThreeInARow(bestPosition[0], newGameBoard, 1, bestPosition[1], bestPosition[2])
        else:
            availablePositions = getAvailablePositions(newGameBoard)
            if not findBestPosition(existingUtilityMatrix, availablePositions):
                break
            # From the list of available positions, use findBestPosition to get the index of the best one
            bestPosition = findBestPosition(existingUtilityMatrix, availablePositions)
        newGameBoard[bestPosition] = -1
        if checkIfWinner(newGameBoard, bestPosition[0], bestPosition[1], bestPosition[2]):
            winningPlayer = -1
            break
    # Adjustthe squares of the winning player by one in the utility matrix
    winningSquares = []
    losingSquares = []
    if winningPlayer == 1:
        # Get the indices of the cells that the winningPlayer used
        winningSquares = np.argwhere(newGameBoard == 1)  # A list of cells indices [[matrix row col] [matrix row col]]
        losingSquares = np.argwhere(newGameBoard == -1)
    if winningPlayer == -1:
        winningSquares = np.argwhere(newGameBoard == -1)  # A list of cells indices [[matrix row col] [matrix row col]]
        losingSquares = np.argwhere(newGameBoard == +1)
    # Increase the utility values at the indices of the winning squares
    for winningIndex in winningSquares:
        existingUtilityMatrix[winningIndex[0]][winningIndex[1]][winningIndex[2]] += 1
    # Decrease the utility values at the indices of the losing squares
    for losingIndex in losingSquares:
        existingUtilityMatrix[losingIndex[0]][losingIndex[1]][losingIndex[2]] -= 1
    return existingUtilityMatrix


if __name__ == '__main__':
    # Check to ensure the program was run correctly
    if len(sys.argv) != 4:
        print("incorrect number of arguments, exiting.")
        sys.exit()
    else:
        numOfTrials1 = int(sys.argv[1])
        numOfTrials2 = int(sys.argv[2])
        numOfTrials3 = int(sys.argv[3])
        utilityMatrix = np.zeros((4, 4, 4))  # initialize a utilityMatrix
        # 4 matrices, each with 4 rows and 4 columns

        # Run until first break point
        for i in range(numOfTrials1):
            gameBoard = np.zeros((4, 4, 4))  # initialize a utilityMatrix
            utilityMatrix = playGame(utilityMatrix, gameBoard)

        print("CURRENT UTILITY MATRIX AFTER " + str(numOfTrials1) + " " + "TRIALS")
        showUtilityMatrixAveraged(utilityMatrix, numOfTrials1)

        # Continue to run until second break point
        for i in range(numOfTrials1, numOfTrials2):
            gameBoard = np.zeros((4, 4, 4))  # initialize a utilityMatrix
            utilityMatrix = playGame(utilityMatrix, gameBoard)
        print("CURRENT UTILITY MATRIX AFTER " + str(numOfTrials2) + " " + "TRIALS")
        showUtilityMatrixAveraged(utilityMatrix, numOfTrials2)

        # Continue to run until third break point
        for i in range(numOfTrials2, numOfTrials3):
            gameBoard = np.zeros((4, 4, 4))  # initialize a utilityMatrix
            utilityMatrix = playGame(utilityMatrix, gameBoard)
        print("CURRENT UTILITY MATRIX AFTER " + str(numOfTrials3) + " " + "TRIALS")
        showUtilityMatrixAveraged(utilityMatrix, numOfTrials3)
