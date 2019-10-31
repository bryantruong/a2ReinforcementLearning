import numpy as np
import sys


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
                    positions.append((matrix,row,col))
    return positions



if __name__ == '__main__':
    # Check to ensure the program was run correctly
    if len(sys.argv) != 4:
        print("incorrect number of arguments, exiting.")
    else:
        numOfTrials1 = int(sys.argv[1])
        numOfTrials2 = int(sys.argv[2])
        numOfTrials3 = int(sys.argv[3])
        utilityMatrix = np.zeros((4, 4, 4))  # initialize a utilityMatrix
        # 4 matrices, each with 4 rows and 4 columns
        print(utilityMatrix)
        for i in range(numOfTrials1):
            gameMatrix = np.zeros((4, 4, 4))  # initialize the game board
            # TODO: Do the reinforcement learning, then print utility values
            # Probably make a method for "playing a game"
            break

        for i in range(numOfTrials1, numOfTrials2):
            # TODO: Do the reinforcement learning, then print utility values
            break
        for i in range(numOfTrials2, numOfTrials3):
            # TODO: Do the reinforcement learning, then print utility values
            break

