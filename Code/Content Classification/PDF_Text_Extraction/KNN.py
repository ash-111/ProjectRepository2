
import math
import numpy as np


# https://www.youtube.com/watch?v=rTEtEy5o3X0&t=74s

def GetMostCommon(k_labels_array, k_val):
    """ 
    Find the most common element in list.
    If 2 or more labels have same number of frequency, expand the k_labels_list by 
    one and try again recursively 
    """
    
    k_labels_list = list(k_labels_array[:k_val])

    print("k_labels_list", k_labels_list)

    k_labels_set = set(k_labels_list)
    k_labels_freq = []

    for i in k_labels_set:
        k_labels_freq.append(k_labels_list.count(i))

    # print("k_labels_set", k_labels_set)
    # print("k_labels_freq", k_labels_freq)

    max_indexes = [index for (index, item) in enumerate(k_labels_freq) if item == max(k_labels_freq)]

    # print("max_indexes", max_indexes)


    if len(max_indexes) > 1:
        print("running again")
        return GetMostCommon(k_labels_array, k_val+1)
    else: 
        index = int(max_indexes[0])
        return list(k_labels_set)[index]





class KNN:
    def __init__(self, k, max_k):
        self.k = k
        self.max_k = max_k

    def load(self, X, y):
        self.X_train = X
        self.y_train = y

        self.totalNumOfDocuments = len(X)

    def predict(self, X):
        predictions = [self._predict(x) for x in X]
        return predictions

    def _predict(self, x):
        # Compute euclidean distances
        # distances = [math.dist(x, x_train) for x_train in self.X_train]
        
        x = np.tile(x, (self.totalNumOfDocuments, 1))

        distances = np.sqrt(np.sum(((x - self.X_train)**2), axis=1))

        # print("distances", distances)
        # print("len(distances)", len(distances))

        # Get the k nearest neighbors
        k_nearest_indices = np.argsort(distances)[:self.max_k]
        # print("k_nearest_indices", k_nearest_indices)
        k_labels = self.y_train[k_nearest_indices]
        # print("k_labels", k_labels)

        output = GetMostCommon(k_labels, self.k)

        print("output label", output)


        return k_labels