import cv2
import numpy as np
from PIL import ImageGrab
import screen_brightness_control as sbc

class BrightnessController:
    def __init__(self):
        self.paused = False
        self.sensitivity = 7
        self.max_brightness = 80  # 0-100

    def get_average_brightness(self):
        try:
            screen = ImageGrab.grab()
            screen_np = np.array(screen)
            frame = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return gray_frame.mean()
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None

    def calculate_target_brightness(self, avg_brightness):
        try:
            res = 1 - (avg_brightness * self.sensitivity / 2550)
            target = res * 100
            return min(target, self.max_brightness)
        except Exception as e:
            print(f"Error calculating target brightness: {e}")
            return None

    def adjust_brightness(self):
        if self.paused:
            return None, None

        avg_brightness = self.get_average_brightness()
        if avg_brightness is None:
            return None, None

        target_brightness = self.calculate_target_brightness(avg_brightness)
        if target_brightness is not None:
            sbc.set_brightness(target_brightness)
            return avg_brightness, target_brightness

        return None, None

    def set_sensitivity(self, value):
        self.sensitivity = value

    def set_max_brightness(self, value):
        self.max_brightness = value

    def toggle_pause(self):
        self.paused = not self.paused
        return self.paused