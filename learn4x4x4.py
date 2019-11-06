import numpy as np
import sys
from random import randrange


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
    maxUtility = 0
    bestPositions = []  # Stores the indices of the best positions, which may be multiple in case of ties
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
    winningPlayer = None
    while True:
        availablePositions = getAvailablePositions(newGameBoard)
        bestPosition = findBestPosition(existingUtilityMatrix, availablePositions)
        newGameBoard[bestPosition] = 1
        if checkIfWinner(newGameBoard, bestPosition[0], bestPosition[1], bestPosition[2]):
            winningPlayer = 1
            break
        availablePositions = getAvailablePositions(newGameBoard)
        bestPosition = findBestPosition(existingUtilityMatrix, availablePositions)
        newGameBoard[bestPosition] = -1
        if checkIfWinner(newGameBoard, bestPosition[0], bestPosition[1], bestPosition[2]):
            winningPlayer = -1
            break
    # Increase the squares of the winning player by one in the utility matrix
    if winningPlayer == 1:
        # Get the indices of the cells that the winningPlayer used
        winningSquares = np.argwhere(newGameBoard == 1)  # A list of cells indices [[matrix row col] [matrix row col]]
    if winningPlayer == -1:
        winningSquares = np.argwhere(newGameBoard == -1)  # A list of cells indices [[matrix row col] [matrix row col]]
    for winningIndex in winningSquares:
        existingUtilityMatrix[winningIndex[0]][winningIndex[1]][winningIndex[2]] += 1
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

        # Dummy values to test
        # utilityMatrix[0][0][2] = 1
        # utilityMatrix[0][0][1] = -1
        # utilityMatrix[3][2][1] = 1
        # utilityMatrix[2][3][0] = -1
        # utilityMatrix[1][1][1] = 1
        # print(utilityMatrix)

        for i in range(numOfTrials1):
            gameBoard = np.zeros((4, 4, 4))  # initialize a utilityMatrix
            utilityMatrix = playGame(utilityMatrix, gameBoard)

        # TODO: Divide each cell in utility matrix by numOfTrials1
        print("CURRENT UTILITY MATRIX AFTER " + str(numOfTrials1) + " " + "TRIALS")
        print(utilityMatrix)
        sys.exit()
        # TODO: Multiply each cell in utility matrix by numOfTrials1
        for i in range(numOfTrials1, numOfTrials2):
            gameBoard = np.zeros((4, 4, 4))  # initialize a utilityMatrix
            utilityMatrix = playGame(utilityMatrix, gameBoard)

        # TODO: Divide each cell in utility matrix by numOfTrials2
        print("CURRENT UTILITY MATRIX AFTER " + str(numOfTrials2) + " " + "TRIALS")
        print(utilityMatrix)
        # TODO: Multiply each cell in utility matrix by numOfTrials2

        for i in range(numOfTrials2, numOfTrials3):
            gameBoard = np.zeros((4, 4, 4))  # initialize a utilityMatrix
            utilityMatrix = playGame(utilityMatrix, gameBoard)

        # TODO: Divide each cell in utility matrix by numOfTrials3
        print("CURRENT UTILITY MATRIX AFTER " + str(numOfTrials3) + " " + "TRIALS")
        print(utilityMatrix)
