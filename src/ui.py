import dearpygui.dearpygui as dpg
from .brightness_controller import BrightnessController
from .system_tray import SystemTray
import threading
import time

class UI:
    def __init__(self):
        self.controller = BrightnessController()
        self.system_tray = SystemTray(self.show_window)
        self.running = True

    def setup_theme(self):
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                # Main background color (dark purple)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (40, 10, 40))
                # Title bar color (medium purple)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (130, 60, 180))
                # Button colors (light purple)
                dpg.add_theme_color(dpg.mvThemeCol_Button, (150, 70, 200))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (170, 90, 220))
                # Slider colors (bright purple)
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (180, 100, 230))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (200, 120, 250))
                # Text color (white)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))

        dpg.bind_theme(global_theme)

    def create_window(self):
        dpg.create_context()
        dpg.create_viewport(title="Screen Dimmer", width=400, height=500)
        dpg.set_viewport_resize_callback(self.resize_callback)

        with dpg.window(label="Screen Dimmer", tag="primary_window"):
            # Title with gradient effect using multiple text elements
            with dpg.group(horizontal=True):
                dpg.add_text("Screen", color=(255, 150, 255))
                dpg.add_text("Brightness", color=(230, 180, 255))
                dpg.add_text("Control", color=(200, 200, 255))
            
            dpg.add_spacer(height=20)
            
            # Sensitivity Control
            dpg.add_text("Sensitivity", color=(230, 180, 255))
            dpg.add_slider_int(
                default_value=7,
                min_value=1,
                max_value=10,
                callback=lambda s, a: self.controller.set_sensitivity(a),
                width=-1
            )
            
            dpg.add_spacer(height=10)
            
            # Maximum Brightness Control
            dpg.add_text("Maximum Brightness", color=(230, 180, 255))
            dpg.add_slider_int(
                default_value=80,
                min_value=0,
                max_value=100,
                callback=lambda s, a: self.controller.set_max_brightness(a),
                width=-1
            )
            
            dpg.add_spacer(height=20)
            
            # Control Buttons
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Pause",
                    callback=self.toggle_pause,
                    tag="pause_button",
                    width=150,
                    height=40
                )
                dpg.add_button(
                    label="Minimize to Tray",
                    callback=self.minimize_to_tray,
                    width=150,
                    height=40
                )
            
            dpg.add_spacer(height=20)
            
            # Status Display
            with dpg.group():
                dpg.add_text("Current Status:", color=(200, 200, 255))
                dpg.add_text("", tag="status_text", color=(255, 255, 255))

        self.setup_theme()
        
        dpg.set_primary_window("primary_window", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def resize_callback(self, sender, data):
        dpg.set_item_width("primary_window", data[0])
        dpg.set_item_height("primary_window", data[1])

    def update_status(self):
        while self.running:
            avg_brightness, target_brightness = self.controller.adjust_brightness()
            if avg_brightness is not None and target_brightness is not None:
                status_text = (
                    f"Average Brightness: {avg_brightness:.2f}\n"
                    f"Target Brightness: {target_brightness:.2f}%"
                )
                dpg.set_value("status_text", status_text)
            time.sleep(1)

    def toggle_pause(self):
        paused = self.controller.toggle_pause()
        dpg.set_item_label("pause_button", "Resume" if paused else "Pause")

    def minimize_to_tray(self):
        dpg.hide_item("primary_window")

    def show_window(self):
        dpg.show_item("primary_window")

    def run(self):
        self.system_tray.create_icon("glimmerlogo.png")
        self.system_tray.run_in_thread()

        update_thread = threading.Thread(target=self.update_status)
        update_thread.daemon = True
        update_thread.start()

        self.create_window()
        
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()

        self.running = False
        dpg.destroy_context()