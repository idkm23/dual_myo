'''
Created on Jan 11, 2016

@author: ymeng
'''

from sklearn.neighbors import KNeighborsClassifier
#from sklearn.cluster import KMeans
import numpy as np
import cPickle as pickle

class SignalClassifier(KNeighborsClassifier):
    '''
    classdocs
    '''

    def __init__(self, n_neighbors=5):
        '''
        Constructor
        '''
        super(SignalClassifier, self).__init__(n_neighbors=n_neighbors)
    
    def train(self, trainingFile, dim):
        data = np.genfromtxt(trainingFile, delimiter=',')
        X = data[:, 0:dim]
        y = data[:, dim]
        self.fit(X, y)
        
if __name__ == '__main__':
    imu_data = '../data/imu.dat'
    imu_classifier = SignalClassifier()
    imu_classifier.train(imu_data, 9)
    with open('../data/imu_classifier.pkl', 'w') as f:
        pickle.dump(imu_classifier, f)
