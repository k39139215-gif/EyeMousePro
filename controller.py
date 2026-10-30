import pyautogui

class MouseController:
    def __init__(self, smoothening=7, blink_threshold=6):
        # Disable failsafe to prevent corner crashes
        pyautogui.FAILSAFE = False
        
        # Screen dimensions
        self.screen_w, self.screen_h = pyautogui.size()
        
        self.smoothening = smoothening
        self.plocX, self.plocY = 0, 0
        self.clicking = False
        self.blink_threshold = blink_threshold

    def move_mouse(self, nose_normalized_x, nose_normalized_y):
        """
        Maps normalized coordinates (0.0 to 1.0) to screen and moves mouse with smoothing.
        """
        # Map to Screen resolution
        # Multiply by 2.0 and subtract offset so the user doesn't have to move head to screen edges
        mouse_x = int((nose_normalized_x - 0.25) * 2.0 * self.screen_w)
        mouse_y = int((nose_normalized_y - 0.25) * 2.0 * self.screen_h)
        
        # Clamp coordinates to valid screen bounds
        mouse_x = max(0, min(self.screen_w - 1, mouse_x))
        mouse_y = max(0, min(self.screen_h - 1, mouse_y))
        
        # Smoothing algorithm (exponential moving average)
        clocX = self.plocX + (mouse_x - self.plocX) / self.smoothening
        clocY = self.plocY + (mouse_y - self.plocY) / self.smoothening
        
        pyautogui.moveTo(clocX, clocY)
        
        # Save previous locations
        self.plocX, self.plocY = clocX, clocY

    def process_click(self, blink_distance, img, cv2):
        """
        Checks blink distance and clicks if below threshold.
        """
        if blink_distance is not None and blink_distance < self.blink_threshold:
            # Visual feedback on camera window
            cv2.putText(img, "BLINK (CLICK)!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            if not self.clicking:
                pyautogui.click()
                self.clicking = True
        else:
            self.clicking = False
        
        return img
