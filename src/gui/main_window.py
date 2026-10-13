import os
import sys
import logging
import traceback
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMenuBar
from core.initialize import main as initialize_system
from gui.tabs import create_tabs
from core.staging import clear_staged_files
from gui.themes import list_theme_files, make_theme_changer, load_stylesheet, ensure_theme_config
from gui.credentials import manage_credentials


class DocQA_GUI(QWidget):
    def __init__(self):
        super().__init__()
        try:
            initialize_system()
            self.init_ui()
            self.init_menu()
            logging.info("GUI initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing GUI: {str(e)}")
            logging.debug(traceback.format_exc())
            raise

    def init_ui(self):
        try:
            self.setWindowTitle('KoboldCPP VectorDB Plugin - www.chintellalaw.com')
            self.setGeometry(300, 300, 700, 800)
            self.setMinimumSize(350, 410)

            main_layout = QVBoxLayout(self)
            main_layout.addWidget(create_tabs())
            logging.info("UI initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing UI: {str(e)}")
            logging.debug(traceback.format_exc())
            raise

    def init_menu(self):
        try:
            self.menu_bar = QMenuBar(self)
            self.layout().setMenuBar(self.menu_bar)
            self.file_menu = self.menu_bar.addMenu('File')
            self.theme_menu = self.file_menu.addMenu('Themes')
            for theme in list_theme_files():
                self.theme_menu.addAction(theme).triggered.connect(make_theme_changer(theme))
            self.hf_token_menu = self.file_menu.addAction('Hugging Face Access Token')
            self.hf_token_menu.triggered.connect(lambda: manage_credentials(self, 'hf'))
            logging.info("Menu initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing menu: {str(e)}")
            logging.debug(traceback.format_exc())
            raise

    def closeEvent(self, event):
        try:
            clear_staged_files()
            logging.info("Application closed successfully")
            super().closeEvent(event)
        except Exception as e:
            logging.error(f"Error during application close: {str(e)}")
            logging.debug(traceback.format_exc())


def main():
    try:
        with open('test_write.txt', 'w') as f:
            f.write("Testing write permissions")
        os.remove('test_write.txt')
    except Exception as e:
        print(f"Cannot write to the current directory: {e}")

    try:
        logging.info("Starting application")
        app = QApplication(sys.argv)
        theme = ensure_theme_config()
        app.setStyleSheet(load_stylesheet(theme))
        ex = DocQA_GUI()
        ex.show()
        logging.info("Application main window shown")
        sys.exit(app.exec())
    except Exception as e:
        logging.critical(f"Critical error in main function: {str(e)}")
        logging.debug(traceback.format_exc())
        print("A critical error occurred. Please check the log file 'app.log' for details.")
        sys.exit(1)
