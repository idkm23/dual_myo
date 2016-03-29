#!/usr/bin/env python

import rospy
import pylab as plt
import numpy as np
import collections
from myo.myo_raw import MyoRaw
from myo_raw.msg import MyoImu, Gesture, EMGData
import ctypes
import struct
from threading import Lock

class MyoPlotter(object):
    def __init__(self):
        rospy.init_node('myo_plotter', anonymous=True)

        self.imu_data = {'x': collections.deque(np.zeros(50), maxlen=50),
                         'y': collections.deque(np.zeros(50), maxlen=50),
                         'z': collections.deque(np.zeros(50), maxlen=50),
                         'w': collections.deque(np.zeros(50), maxlen=50)}
        self.emg_data = [collections.deque(np.zeros(50), maxlen=50) for i in xrange(8)]

        self.available_update_lock = Lock()
        self.available_update = True

        plt.ion()
        emg_fig = plt.figure("EMG Data")
        self.emg_plot = [emg_fig.add_subplot(421),
                         emg_fig.add_subplot(422),
                         emg_fig.add_subplot(423),
                         emg_fig.add_subplot(424),
                         emg_fig.add_subplot(425),
                         emg_fig.add_subplot(426),
                         emg_fig.add_subplot(427),
                         emg_fig.add_subplot(428)]
        self.emg_plot_axes = [self.emg_plot[i].plot(self.emg_data[i])[0] for i in xrange(8)]

        def emg_subscriber(emg_msg):
            for i in xrange(8):
                self.emg_data[i].append(emg_msg.emg_data[i])
                self.emg_plot_axes[i].set_ydata(self.emg_data[i])
                # self.emg_plot[i].set_ylim([min(self.emg_data[i]), max(self.emg_data[i])])
                self.emg_plot[i].set_ylim([0, 1000])
                
            self.available_update_lock.acquire()            
            self.available_update = True
            self.available_update_lock.release()



        self.emg_sub = rospy.Subscriber("/emg", EMGData, emg_subscriber)


    def spin(self):
        try: 
            r = rospy.Rate(50)  
            while not rospy.is_shutdown():
                self.available_update_lock.acquire()
                
                if self.available_update:
                    # plt.figure("EMG Data")
                    plt.draw()
                    # plt.figure("Imu Data - Quaternion")
                    # plt.draw()
                    self.available_update = False
                self.available_update_lock.release()
                r.sleep()
        except rospy.ROSInterruptException:
            pass



if __name__ == '__main__':
    m = MyoPlotter()
    m.spin()