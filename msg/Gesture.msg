## A Gesture message can be used in place of the built in EMGData message
## The gestures can either be trained using the myo_raw myo_classifier
## of builtins (for api version 1+)

# What a pose means if it's a builtin
int32 POSE_REST = 0
int32 POSE_FIST = 1
int32 POSE_WAVE_IN = 2
int32 POSE_WAVE_OUT = 3
int32 POSE_FINGERS_SPREAD = 4
int32 POSE_THUMB_TO_PINKY = 5
int32 POSE_UNKNOWN = 255

# Was the pose a builtin from the myo api and not a manually trained one
bool 	is_builtin

# Either the trained pose number or one of the built-ins
# note the default classifier only can have a pose number from 0 to 9
int32   pose_number
# float64 pose_number

# How confident was the built in classifier that this pose was accurate
# will be 0 if the pose was a builtin
float64 confidence
