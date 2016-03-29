# Provides access to the raw emg data off the sensor
# Useful to try and write your own classifier


# The raw sensor reading off of each of the 8 emg sensors
# note this reading is dependent on the rotation of the sensor
# on the arm
uint32[8] emg_data

# Was the sensor moving during this reading
bool     moving
