#!/usr/bin/env python
import os
import rospy
import rospkg


rospy.init_node('myo_classifier', anonymous=True)
traning_data_directory = rospy.get_param('~training_data_dir', None)

module_path = rospkg.RosPack().get_path('myo_raw')

if traning_data_directory is not None:
	os.chdir(traning_data_directory)

else:

	os.chdir(module_path+'/training_data')

os.execlp("python", module_path+"/scripts/myo/classify_myo.py", module_path+"/scripts/myo/classify_myo.py")
