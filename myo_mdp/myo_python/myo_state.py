'''
Created on Jan 14, 2016

@author: ymeng
'''

import cPickle as pickle
import rospy
from std_msgs.msg import String, Float64
from myo_raw.msg import IMUData
import classifier
import numpy as np
import sys
import time

state_map = {'s1':'twisting clockwise', 's4':'reaching limit counter-clockwise', 's2':'starting/ending position', 's3':'twisting counter-clockwise'}


class Progress(object):
    
    def __init__(self):
        self.classifier = classifier.SignalClassifier()
        self.classifier = pickle.load(open('../data/imu_classifier.pkl'))
        self.pub = rospy.Publisher('/exercise/progress', Float64, queue_size=10)
        self.pub1 = rospy.Publisher('/exercise/state', String, queue_size=10)
        self.progress = 0.0
        self.count_down = 10
        self.getTask()
        self.subscribe()
    
    def getTask(self):
        with open('../data/state_sequence.dat') as f:
            self.task = [x.strip() for x in f]
            self.n_states = len(self.task)
        print self.task
        time.sleep(2)
    
    def callback(self, imu):
        self.getProgress(imu)
    
    def subscribe(self):
        rospy.init_node('state_receiver')
        rospy.Subscriber('/myo/imu', IMUData, self.callback)
        rospy.spin()
    
    def getProgress(self, imu):
        imu_array = np.array([imu.linear_acceleration.x, imu.linear_acceleration.y, imu.linear_acceleration.z,
                      imu.angular_velocity.x, imu.angular_velocity.y, imu.angular_velocity.z,
                      imu.orientation.x, imu.orientation.y, imu.orientation.z])
#        print imu_array
        imu_array[3:6] = imu_array[3:6]/500
        imu_array[6:9] = imu_array[6:9]/180
        state = 's'+str(int(self.classifier.predict(imu_array)[0]))
        self.pub1.publish(state)
        self.pub.publish(self.progress)
        if self.task == []:
            print "Task completed!"
            self.pub.publish(1.0)
            sys.exit()
        if state == self.task[0]:
            self.count_down -= 1
            if self.count_down == 0:
                print "current state", state, state_map[state]
                self.task.pop(0)
                self.progress = 1 - 1.0*len(self.task)/self.n_states
                self.pub.publish(self.progress)
                self.count_down = 10

if __name__ == '__main__':
    progress = Progress()

    