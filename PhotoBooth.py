from __future__ import print_function
from PBClass import PhotoBoothApp
from imutils.video import VideoStream
import argparse
import time

Arguments = argparse.ArgumentParser()
Arguments.add_argument("-o", "--output", required=True, help="Snapshot output path")
Arguments.add_argument("-p", "--picamera", type=int, default=-1, help="Raspberry Pi camera")
myArguments = vars(Arguments.parse_args())

print("Initializing...")
myVideoStream = VideoStream(usePiCamera=myArguments["picamera"] > 0).start()

#Delay 2 Sec #
time.sleep(2.0)

#Start
App = PhotoBoothApp(myVideoStream, myArguments["output"])
App.Root.mainloop()
