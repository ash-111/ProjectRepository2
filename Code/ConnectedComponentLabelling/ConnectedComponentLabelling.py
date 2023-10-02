import numpy as np
import sys


def ConnectedComponents(testImageOriginal):
    sys.setrecursionlimit(320000)
    testImage = np.array(testImageOriginal)

    def dfs(i, j, label):
        if 0 <= i < len(testImage) and 0 <= j < len(testImage[0]) and testImage[i][j] == True:
             testImage[i][j] = label

             dfs(i, j-1, label) # left
             dfs(i, j+1, label) # right
             dfs(i-1, j, label) # top
             dfs(i+1, j, label) # bottom
             dfs(i-1, j-1, label) # NW
             dfs(i-1, j+1, label) # NE
             dfs(i+1, j-1, label) # SW
             dfs(i+1, j+1, label) # SE

    label = 2
    for i in range(len(testImage)):
        for j in range(len(testImage[0])):
            if testImage[i][j] == True:
                dfs(i, j, label)
                label += 1


    testImage = testImage - 1
    testImage[testImage == -1] = 0
    totalNumOfLabels = np.max(testImage) + 1


    return totalNumOfLabels, testImage

















