import cv2
from threading import Thread
import time

class WebcamStream:
    def __init__(self, src=0):
        # Initialize the video camera stream
        self.stream = cv2.VideoCapture(src)
        
        # Optimize camera settings for lower latency (optional, depends on webcam)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.stream.set(cv2.CAP_PROP_FPS, 30)
        
        (self.grabbed, self.frame) = self.stream.read()
        
        # Thread control flag
        self.stopped = False

    def start(self):
        # Start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True # Daemon thread so it closes when main program closes
        t.start()
        return self

    def update(self):
        # Keep looping infinitely until the thread is stopped
        while True:
            if self.stopped:
                self.stream.release()
                return

            # Read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # Return the most recent frame
        return self.frame

    def stop(self):
        # Indicate that the thread should be stopped
        self.stopped = True
