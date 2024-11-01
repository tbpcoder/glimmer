import dearpygui.dearpygui as dpg
from .brightness_controller import BrightnessController
import threading
import time

class UI:
    def __init__(self):
        self.controller = BrightnessController()
        self.running = True
        self.icon_path = "icons/glimmerlogo.png"
        self.font_path = "fonts/OpenSans-Regular.ttf"
        self.window_visible = True

    def setup_theme(self):
        """Set up the application theme."""
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                # Window styling
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 3, 35))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (45, 10, 60))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (70, 20, 90))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (40, 8, 50))
                
                # Button styling
                dpg.add_theme_color(dpg.mvThemeCol_Button, (140, 60, 180, 200))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (160, 80, 200, 220))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (180, 100, 220, 255))
                
                # Slider styling
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (200, 100, 255, 200))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (220, 120, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (50, 15, 65, 200))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (60, 20, 75, 220))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (70, 25, 85, 255))
                
                # Text styling
                dpg.add_theme_color(dpg.mvThemeCol_Text, (240, 240, 245))
                
                # Additional styling
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 8)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
                dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 15, 15)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8)

        dpg.bind_theme(global_theme)

    def show_window(self):
        dpg.show_item("primary_window")
    
    def center_align(self, sender, app_data):
        window_width = dpg.get_item_width("primary_window")
        
        # Calculate half the remaining space on either side of the group
        button_group_width = 300  # Total width of the buttons (150 each)
        text_width = dpg.get_text_size("Glimmer")[0]  # Width of the "Glimmer" text
        
        button_spacer_width = max((window_width - button_group_width - 50) // 2, 0)
        text_spacer_width = max((window_width - text_width - 50) // 2, 0)

        # Set spacer widths dynamically
        dpg.configure_item("button_spacer", width=button_spacer_width)
        dpg.configure_item("text_spacer", width=text_spacer_width)

    def create_window(self):
        """Create the main application window."""
        dpg.create_context()
        dpg.create_viewport(
            title="Glimmer",
            width=500,
            height=600,
            min_width=400,
            min_height=500
        )

        # Register the font
        with dpg.font_registry():
            default_font = dpg.add_font(self.font_path, size=20)

        # Create the primary window
        with dpg.window(label="Glimmer", tag="primary_window", no_collapse=True):
            # Title text with horizontal centering
            with dpg.group(horizontal=True):
                dpg.add_spacer(tag="text_spacer", width=0)
                dpg.add_text("Glimmer", color=(230, 180, 255))

            dpg.add_spacer(height=20)  # Vertical space

            # Center-aligned buttons group
            with dpg.group(horizontal=True):
                dpg.add_spacer(tag="button_spacer", width=0)
                dpg.add_button(
                    label="Pause",
                    callback=lambda: print("Pause clicked"),
                    tag="pause_button_main",
                    width=150,
                    height=45
                )
                dpg.add_button(
                    label="Minimize",
                    width=150,
                    height=45,
                    tag="minimize_button_main"
                )
            
            dpg.add_spacer(height=10)
            
            # Sensitivity section
            self.sensitifity_heading = dpg.add_text("Sensitivity", color=(230, 180, 255))
            self.sensitivity_slider = dpg.add_slider_int(
                default_value=7,
                min_value=1,
                max_value=10,
                callback=lambda s, a: self.controller.set_sensitivity(a),
                width=-1,
                show=True
            )
            
            dpg.add_spacer(height=10)

            # Maximum brightness section
            self.max_brightness_heading = dpg.add_text("Maximum Brightness", color=(230, 180, 255))
            self.max_brightness_slider = dpg.add_slider_int(
                default_value=80,
                min_value=0,
                max_value=100,
                callback=lambda s, a: self.controller.set_max_brightness(a),
                width=-1,
                show=True
            )

            # Manual brightness section, initially hidden
            self.manual_brightness_heading = dpg.add_text("Manual Brightness", color=(230, 180, 255), show=False)
            self.manual_brightness_slider = dpg.add_slider_int(
                default_value=80,
                min_value=0,
                max_value=100,
                callback=lambda s, a: self.controller.set_manual_brightness(a),
                width=-1,
                show=False
            )

            dpg.add_spacer(height=20)

            # Status section
            with dpg.collapsing_header(label="Status", default_open=False):
                dpg.add_text("", tag="status_text")
                dpg.add_text("", tag="time_text")
        
        # Create an item handler registry for resizing
        with dpg.item_handler_registry(tag="resize_handler_registry") as registry:
            dpg.add_item_resize_handler(callback=self.center_align)

        # Bind the handler registry to the primary window
        dpg.bind_item_handler_registry("primary_window", "resize_handler_registry")

        # Bind font and set up theme
        dpg.bind_font(default_font)
        self.setup_theme()

        # Set the primary window and show viewport
        dpg.set_primary_window("primary_window", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def toggle_pause(self):
        """Toggle the pause state."""
        paused = self.controller.toggle_pause()
        dpg.set_item_label("pause_button_main", "Resume" if paused else "Pause")

        # Hide/show sliders based on pause state
        if paused:
            # Hide the existing sliders
            dpg.hide_item(self.sensitifity_heading)
            dpg.hide_item(self.sensitivity_slider)
            dpg.hide_item(self.max_brightness_heading)
            dpg.hide_item(self.max_brightness_slider)
            # Show manual brightness slider
            dpg.show_item(self.manual_brightness_heading)
            dpg.show_item(self.manual_brightness_slider)
        else:
            # Show the existing sliders
            dpg.show_item(self.sensitifity_heading)
            dpg.show_item(self.sensitivity_slider)
            dpg.show_item(self.max_brightness_heading)
            dpg.show_item(self.max_brightness_slider)
            # Show manual brightness slider
            dpg.hide_item(self.manual_brightness_heading)
            dpg.hide_item(self.manual_brightness_slider)

    def update_status(self):
        """Update the status display continuously."""
        while self.running:
            avg_brightness, target_brightness = self.controller.adjust_brightness()
            if avg_brightness is not None and target_brightness is not None:
                status_text = (
                    f"Average Screen Brightness: {avg_brightness:.1f}\n"
                    f"Target Brightness: {target_brightness:.1f}%\n"
                )
                dpg.set_value("status_text", status_text)
            time.sleep(1)

    def run(self):
        

        # Start update thread
        update_thread = threading.Thread(target=self.update_status)
        update_thread.daemon = True
        update_thread.start()

        # Create and show main window
        self.create_window()
        
        # Main application loop
        while dpg.is_dearpygui_running() and self.running:
            dpg.render_dearpygui_frame()

        # Cleanup
        self.running = False
        dpg.destroy_context()