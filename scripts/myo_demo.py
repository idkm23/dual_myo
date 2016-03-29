#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty
from numpy import genfromtxt
from geometry_msgs.msg import Quaternion
import tf

pub = rospy.Publisher('/exercise/playback', Quaternion, queue_size=20)
    
data = genfromtxt('../myo_mdp/data/imu_sample.dat', delimiter=',')
orientation = data[:, 6:9]
print orientation.shape
quat = []
for euler in orientation:
    rotated_quat = tf.transformations.quaternion_from_euler(euler[2], euler[1], euler[0])
    quat.append(Quaternion(x=rotated_quat[0], 
                      y=rotated_quat[1], 
                      z=rotated_quat[2], 
                      w=rotated_quat[3]))
quat.append(Quaternion(x=-1337, y=-1337, z=-1337, w=-1337))

def callback(message):
    counter = 0
    rate = rospy.Rate(50) # 50hz
    for q in quat:
        pub.publish(q)
        counter += 1
        rate.sleep()
    print counter, "coordinates pulished."

def subscriber():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/exercise/playback_trigger', Empty, callback)
    rospy.spin()
    
if __name__ == '__main__':
    subscriber()
