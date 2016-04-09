#!/usr/bin/env python

import rospy
from std_msgs.msg import Header, Int32
from geometry_msgs.msg import Quaternion, Vector3, Pose, PoseStamped, Point
from myo_raw.msg import Gesture, EMGData, MyoArm, IMUData
from myo.myo import Myo, NNClassifier
from myo.myo_raw import MyoRaw

from time import sleep
from threading import Thread

import tf
import ctypes
import rospkg
import os
from math import pi

# Scale values for unpacking IMU data
# Accelerometer data. In units of g. Range of + -16. Values are multiplied by MYOHW_ACCELEROMETER_SCALE.
# Gyroscope data. In units of deg/s. Range of + -2000. Values are multiplied by MYOHW_GYROSCOPE_SCALE.
MYOHW_ORIENTATION_SCALE = 16384.0 
MYOHW_ACCELEROMETER_SCALE = 2048.0
MYOHW_GYROSCOPE_SCALE = 16.0

UPPER_ARM_DEVICE_NAME = "Winnie's Myo"

class MyoNode(object):
    """A ros wrapper for myo_raw"""
    def __init__(self):
        

        self.m = Myo(NNClassifier())
        self.connect(self.m)

        if self.m.device_name == UPPER_ARM_DEVICE_NAME:
            self.identifier  = 'u'
        else:
            self.identifier  = 'l'

        #might be necessary for some classification?
        #traning_data_directory = rospy.get_param('~training_data_dir', None)

        self.pub_imu     = rospy.Publisher('/myo/' + self.identifier + '/imu',     IMUData,     queue_size=10)
        self.pub_emg     = rospy.Publisher('/myo/' + self.identifier + '/emg',     EMGData,     queue_size=10)
        self.pub_pose    = rospy.Publisher('/myo/' + self.identifier + '/gesture', Gesture,     queue_size=10)
        self.pub_myo_arm = rospy.Publisher('/myo/' + self.identifier + '/arm',     MyoArm,      queue_size=10, latch=True)
        self.pub_ort     = rospy.Publisher('/myo/' + self.identifier + '/ort',     Quaternion,  queue_size=10)
        
        self.downsampler = 0
        self.baseRot = None 
        self.count = 0 
        self.keepScanning = True

        #might be necessary for some classification?
        #os.chdir(rospkg.RosPack().get_path('myo_raw')+'/training_data' if traning_data_directory == None else traning_data_directory)

    def connect(self, m):
        m.connect()

        m.vibrate(2)
        m.add_emg_handler(self.__on_emg)
        m.add_imu_handler(self.__on_imu)
        # m.add_pose_handler(self.__on_pose)
        m.add_raw_pose_handler(self.__on_raw_pose)
        m.add_arm_handler(self.__on_arm)

    def disconnect(self):
        self.m.disconnect()
    
    # builtin pose subscriber
    # def __on_pose(self, p):
    #     self.pub_pose.publish(is_builtin=True, pose_number=p, confidence=0.0)

    def __on_arm(self, arm, xdir):
        self.pub_myo_arm.publish(arm=arm, xdir=xdir)
    
    def __on_emg(self, emg, moving):
        self.pub_emg.publish(emg_data=emg, moving=moving)

    def __on_raw_pose(self, p):
        self.pub_pose.publish(is_builtin=False, pose_number=p, confidence=0.0)

    def __on_imu(self, quat, acc, gyro):
        # need to switch the yaw and the roll for some reason
        euler = tf.transformations.euler_from_quaternion((quat[0], quat[1], quat[2], quat[3])) # roll, pitch, yaw
        
        self.pub_imu.publish(header=Header(frame_id=rospy.get_param('frame_id', 'map'), stamp=rospy.get_param('stamp', None)),
                             orientation=Vector3(x=euler[0]*180/pi, y=euler[1]*180/pi, z=euler[2]*180/pi),
                             angular_velocity=Vector3(x=gyro[0], y=gyro[1], z=gyro[2]),
                             linear_acceleration=Vector3(x=acc[0]/MYOHW_ACCELEROMETER_SCALE, 
                             y=acc[1]/MYOHW_ACCELEROMETER_SCALE, z=acc[2]/MYOHW_ACCELEROMETER_SCALE))

        if self.baseRot == None:
            self.count += 1;

            # This subtraction '(60 * pi / 180.0)' is here to create an initial offset which matches a hand's natural initial offset
            if self.count > 360:
                self.baseRot = euler[0]# - ((60 * pi / 180.0) if self.identifier == 'u' else 0)
            return

        # need to switch the yaw and the roll for some reason   2    1     0
        rotated_quat = tf.transformations.quaternion_from_euler(-euler[2], euler[1], -euler[0] + self.baseRot)


        self.pub_ort.publish(Quaternion(x=rotated_quat[0], 
                                        y=rotated_quat[1], 
                                        z=rotated_quat[2], 
                                        w=rotated_quat[3]))

    def run(self): # note this function is EXTREMELY time sensitive... delay will cause a disconnect of the myo
        try:    
            while not rospy.is_shutdown() and self.keepScanning and not self.m.bt.disconnected:
                self.m.run()
        except rospy.ROSInterruptException or KeyboardInterrupt:
            self.m.disconnect()

        print("exiting cause: " + " " + str(not rospy.is_shutdown()) + " " + str(self.keepScanning) + " " + str(not self.m.bt.disconnected))

        self.m.initialized = False

        print "myo node shutting down"

class MyThread(Thread):
    t1 = None
    t2 = None

    def __init__(self, myo = None):
        Thread.__init__(self)
        self.m = myo

        if(self.m == None):
            self.m = MyoNode()

    def run(self):
        self.m.run()

    @staticmethod
    def isInitialized(thread):
        return not (thread == None or thread.m == None or not thread.m.m.initialized)

    @staticmethod
    def calibrateMyo(myoCount):
        if MyThread.isInitialized(MyThread.t1):
            MyThread.t1.m.baseRot = None
        if MyThread.isInitialized(MyThread.t2):
            MyThread.t2.m.baseRot = None

    @staticmethod
    def startMyo(myoCount):
        myoCount = myoCount.data



        if(MyThread.t1 == None):
            MyThread.t1 = MyThread()
            MyThread.t1.daemon = True
            MyThread.t1.start();        
            sleep(1)
        elif(MyThread.t1.m != None):
            MyThread.t1.m.m.initialized = False

        if(MyThread.t2 == None):
            MyThread.t2 = MyThread()
            MyThread.t2.daemon = True
            MyThread.t2.start();
            sleep(1)
        elif(MyThread.t2.m != None):
            MyThread.t2.m.m.initialized = False

        while not MyThread.isInitialized(MyThread.t1) or (myoCount > 1 and not MyThread.isInitialized(MyThread.t2)):

            if not MyThread.isInitialized(MyThread.t1):
                MyThread.t1.m.keepScanning = False
                sleep(1)
                MyThread.t1.m.disconnect()
                sleep(1)

                print("aftersleep1")
                MyThread.t1.join()
                MyThread.t1.m.keepScanning = True
                MyThread.t1 = MyThread(MyThread.t1.m)
                MyThread.t1.m.m.connect()
                MyThread.t1.start()
                sleep(1)

            if not MyThread.isInitialized(MyThread.t2):
                MyThread.t2.m.keepScanning = False
                sleep(1)
                MyThread.t2.m.disconnect()
                sleep(1)

                if myoCount > 1:
                    MyThread.t2.join()
                    MyThread.t2.m.keepScanning = True
                    MyThread.t2 = MyThread(MyThread.t2.m)
                    MyThread.t2.m.m.connect()
                    MyThread.t2.start()
                    sleep(1)

        MyThread.calibrateMyo(myoCount)
        print("leftcallback")


if __name__ == '__main__':
    rospy.init_node('controllable_myo_node', anonymous=True)

    start_myo_sub = rospy.Subscriber("/myo/launch", Int32, MyThread.startMyo)
    calibrate_myo_sub = rospy.Subscriber('/myo/calibrate', Int32, MyThread.calibrateMyo)

    rospy.spin()

    if MyThread.t1 != None:
        MyThread.t1.join()
    if MyThread.t2 != None:
        MyThread.t2.join()
