import cv2
import numpy as np
from PIL import ImageGrab
import screen_brightness_control as sbc
from typing import Tuple, Optional

class BrightnessController:
    
    def __init__(self, parent):
        """Initialize the brightness controller with default settings."""
        self.parent = parent
        self.paused = False
        self.max_brightness_limit = 80  # Default maximum brightness
        self.min_brightness_limit = 20  # Default minimum brightness
        
    def set_brightness_limits(self, max_brightness: int, min_brightness: int) -> None:
        if not 0 <= min_brightness <= max_brightness <= 100:
            raise ValueError(
                "Invalid brightness limits. Must be: 0 <= min <= max <= 100"
            )
        
        self.max_brightness_limit = max_brightness
        self.min_brightness_limit = min_brightness
        
    def pause(self) -> None:
        self.paused = True
        
    def resume(self) -> None:
        self.paused = False
        
    def get_average_brightness(self) -> Optional[float]:
        try:
            screen = ImageGrab.grab()  # Capture the entire screen
            screen_np = np.array(screen)
            frame = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            avg_brightness = gray_frame.mean()
            
            self._last_captured_brightness = avg_brightness
            self._capture_error_count = 0  # Reset error count on successful capture
            return avg_brightness
            
        except Exception as e:
            self._capture_error_count += 1
            print(f"Error capturing screen (attempt {self._capture_error_count}): {e}")
            
            # Return last known good value if available and not too many errors
            if self._last_captured_brightness is not None and self._capture_error_count < 3:
                return self._last_captured_brightness
                
            return None
            
    def calculate_target_brightness(self, avg_brightness: float, sensitivity: float, min_brightness, max_brightness) -> Optional[float]:
        try:
            return min_brightness + (1 - (avg_brightness * sensitivity / 2550)) * (max_brightness - min_brightness)
            
        except Exception as e:
            print(f"Error calculating target brightness: {e}")
            return None
            
    def adjust_brightness(self, prev_target_brightness, sensitivity: int, max_brightness: int, min_brightness: int) -> Tuple[int, int]:
        if self.paused:
            return 0, 0

        # Get ambient brightness
        avg_brightness = self.get_average_brightness()
        if avg_brightness is None:
            return 0, 0
            
        # Calculate target brightness
        target_brightness = self.calculate_target_brightness(avg_brightness, sensitivity, min_brightness, max_brightness)
        prev_target_brightness = round(prev_target_brightness)
        current_brightness = sbc.get_brightness()[0]
        if abs(current_brightness - prev_target_brightness) > 5 and prev_target_brightness!=0:
            self.parent.toggle_pause()
            return 0,0
        if target_brightness is None:
            return 0, 0
            
        # Apply brightness limits
        target_brightness = min(max(target_brightness, min_brightness), max_brightness)
        
        try:
            sbc.set_brightness(int(target_brightness))
            return avg_brightness, target_brightness
            
        except Exception as e:
            print(f"Error setting brightness: {e}")
            return 0, 0
            
    def set_manual_brightness(self, brightness: int) -> None:
        if not 0 <= brightness <= 100:
            raise ValueError("Brightness must be between 0 and 100")
            
        try:
            sbc.set_brightness(brightness)
            self.current_manual_brightness = brightness
        except Exception as e:
            print(f"Error setting manual brightness: {e}")