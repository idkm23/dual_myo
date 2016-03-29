## A MyoArm message can be used to determine the last known
## arm the myo was determined to be on (only sent for API version 1+)

int32 ARM_UNKNOWN = 0
int32 ARM_RIGHT = 1
int32 ARM_LEFT = 2

int32 XDIR_UNKNOWN = 0
int32 XDIR_TOWARD_WRIST = 1
int32 XDIR_TOWARD_ELBOW = 2


# Which arm is the myo currently on
int32 arm

# What is the determined x direction (is is the light up or down)
# In other words is the light pointing up or down?
int32 xdir