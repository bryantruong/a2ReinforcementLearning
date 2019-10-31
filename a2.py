import numpy as np
import sys

if __name__ == '__main__':
    # Check to ensure the program was run correctly
    if len(sys.argv) != 4:
        print("incorrect number of arguments, exiting.")
    else:
        numOfTrials1 = int(sys.argv[1])
        numOfTrials2 = int(sys.argv[2])
        numOfTrials3 = int(sys.argv[3])

    utilityMatrix = np.zeros((4, 4, 4))  # initialize a utilityMatrix
    print(utilityMatrix)

    for i in range(numOfTrials1):
        # TODO: Do the reinforcment learning, then print utility values
        break

    for i in range(numOfTrials1, numOfTrials2):
        # TODO: Do the reinforcment learning, then print utility values
        break
    for i in range(numOfTrials2, numOfTrials3):
        # TODO: Do the reinforcment learning, then print utility values
        break

