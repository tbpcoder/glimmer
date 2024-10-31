import pystray
from PIL import Image
import threading

class SystemTray:
    def __init__(self, show_window_callback):
        self.show_window_callback = show_window_callback
        self.icon = None

    def create_icon(self, icon_path):
        image = Image.open(icon_path)
        self.icon = pystray.Icon(
            "ScreenDimmer",
            image,
            "Screen Dimmer",
            menu=pystray.Menu(
                pystray.MenuItem("Show", self.show_window),
                pystray.MenuItem("Exit", self.exit_app)
            )
        )

    def show_window(self):
        if self.show_window_callback:
            self.show_window_callback()

    def exit_app(self):
        if self.icon:
            self.icon.stop()

    def run(self):
        self.icon.run()

    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()