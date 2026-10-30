import os
import warnings

# ---------------------------------------------------------
# 1. SUPPRESS WARNINGS (Must be done before importing mediapipe)
# ---------------------------------------------------------
# Disable Mediapipe/TensorFlow C++ Logs (XNNPACK / inference_feedback)
os.environ['GLOG_minloglevel'] = '2'  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Disable Protobuf Python warnings
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")
warnings.filterwarnings("ignore", message="SymbolDatabase.GetPrototype() is deprecated")
# ---------------------------------------------------------

import cv2
import time
from camera import WebcamStream
from tracker import FaceTracker
from controller import MouseController

def main():
    print("Loading Pro AI Models... (No more warnings!)")
    
    # Initialize our modular components
    stream = WebcamStream(src=0).start()
    tracker = FaceTracker()
    mouse = MouseController(smoothening=7, blink_threshold=6)
    
    print("\n🚀 PRO EYE TRACKING MOUSE IS RUNNING (Multi-threaded & Lag-free)!")
    print("👉 Move your HEAD to move the mouse cursor.")
    print("👉 BLINK your LEFT EYE to Click.")
    print("❌ Press 'q' on the camera window to safely stop.\n")
    
    # Wait for camera to warm up
    time.sleep(1.0)
    
    # FPS calculation variables
    pTime = 0
    
    while True:
        # Get frame instantly from the background thread (ZERO lag)
        frame = stream.read()
        if frame is None:
            continue
            
        # Mirror image for natural feeling
        frame = cv2.flip(frame, 1)
        
        # 1. Process AI Tracker
        frame, nose_point, blink_dist = tracker.process_frame(frame)
        
        # 2. Control Mouse (if face detected)
        if nose_point is not None:
            mouse.move_mouse(nose_point[0], nose_point[1])
            frame = mouse.process_click(blink_dist, frame, cv2)
            
        # FPS Calculation
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        
        # Show Output
        cv2.imshow("Pro Eye Tracker", frame)
        
        # Safely exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    print("Shutting down cleanly...")
    stream.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
