# This is a message to hold data from an IMU (Inertial Measurement Unit)
#
# Accelerations should be in g, and angular velocity should be in rad/sec

Header header

#geometry_msgs/Quaternion orientation # user quaternion coordinates
#float64[9] orientation_covariance # Row major about x, y, z axes
geometry_msgs/Vector3 orientation # use euler angles

geometry_msgs/Vector3 angular_velocity
#float64[9] angular_velocity_covariance # Row major about x, y, z axes

geometry_msgs/Vector3 linear_acceleration
#float64[9] linear_acceleration_covariance # Row major x, y z 
