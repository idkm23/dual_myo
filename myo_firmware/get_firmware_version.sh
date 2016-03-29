#!/bin/bash
echo "Downloading thalmic labs beta device firmware version" $1
wget "https://s3.amazonaws.com/thalmicdownloads/firmware/myo-firmware-$1-revd.hex"
