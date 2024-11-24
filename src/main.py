import sys
import traceback
import logging
from PyQt5.QtWidgets import QApplication
from ui import UI

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='glimmer_app.log')

def main():
    try:
        app = QApplication(sys.argv)
        
        # Additional safety checks
        if not app:
            logging.critical("Failed to create QApplication")
            return
        
        window = UI()
        
        # Verify window creation
        if not window:
            logging.critical("Failed to create main window")
            return
        
        window.show()
        
        # Log successful initialization
        logging.info("Application initialized successfully")
        
        sys.exit(app.exec_())
    
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        logging.error(traceback.format_exc())
        print(f"Critical error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
