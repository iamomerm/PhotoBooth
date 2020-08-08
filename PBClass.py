from tkinter import *
from PIL import Image
from PIL import ImageTk
import threading
import datetime
import imutils
import cv2
import os

class PhotoBoothApp():
    
    def __init__(self, VideoStream, OutputPath): 

        self.VideoStream = VideoStream
        self.OutputPath = OutputPath
        self.Frame = None
        self.Thread = None
        self.StopEvent = None
        self.Root = Tk()
        self.Panel = None

        myButton = Button(self.Root, text='Snapshot', command=self.SnapShot)
        myButton.pack(side='bottom', fill='both', expand='yes', padx=10, pady=10)

        self.StopEvent = threading.Event()
        self.VideoThread = threading.Thread(target=self.VideoLoop, args=())
        self.VideoThread.start()

        self.Root.wm_title('PhotoBooth')
        self.Root.wm_protocol('WM_DELETE_WINDOW', self.OnClose)

    def VideoLoop(self):
        while not self.StopEvent.is_set():
            try:
                self.Frame = self.VideoStream.read()
                self.Frame = imutils.resize(self.Frame, width=300)
                self.myImage = cv2.cvtColor(self.Frame, cv2.COLOR_BGR2RGB)
                self.myImage = Image.fromarray(self.myImage)
                self.myImage = ImageTk.PhotoImage(image=self.myImage)
            
                if self.Panel is None:
                    self.Panel = Label(image=self.myImage)
                    self.Panel.image = self.myImage
                    self.Panel.pack(side='left', padx=10, pady=10)
                else:
                    self.Panel.configure(image=self.myImage)
                    self.Panel.image = self.myImage
                    
            except:
                pass

    def SnapShot(self):
        TimeStamp = datetime.datetime.now()
        File = '{}.jpg'.format(TimeStamp.strftime('%Y-%m-%d_%H_%M_%S'))
        Path = os.path.sep.join((self.OutputPath, File))
        cv2.imwrite(Path, self.Frame.copy())
        print('Snapshot captured {}'.format(File))

    def OnClose(self):
        print('Closing...')
        self.StopEvent.set()
        self.VideoStream.stop()
        self.Root.destroy()
                
