import logging
from pathlib import Path

import yaml
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QPushButton, QCheckBox, QHBoxLayout, QMessageBox,
                               QApplication, QComboBox)

from utilities import check_preconditions_for_submit_question

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='app.log')

current_dir = Path(__file__).resolve().parent

class RefreshingComboBox(QComboBox):
    def __init__(self, parent=None):
        super(RefreshingComboBox, self).__init__(parent)

    def showPopup(self):
        self.clear()
        self.addItems(self.parent().load_created_databases())
        super(RefreshingComboBox, self).showPopup()

class GuiSignals(QObject):
    response_signal = Signal(str)
    citations_signal = Signal(str)
    error_signal = Signal(str)
    finished_signal = Signal()

class DatabaseQueryTab(QWidget):
    def __init__(self):
        super(DatabaseQueryTab, self).__init__()
        self.config_path = Path(__file__).resolve().parent / 'config.yaml'
        self.gui_signals = GuiSignals()
        self.initWidgets()
        self.setup_signals()

    def initWidgets(self):
        layout = QVBoxLayout(self)

        self.read_only_text = QTextEdit()
        self.read_only_text.setReadOnly(True)
        layout.addWidget(self.read_only_text, 5)

        hbox1_layout = QHBoxLayout()

        self.database_pulldown = RefreshingComboBox(self)
        self.database_pulldown.addItems(self.load_created_databases())
        hbox1_layout.addWidget(self.database_pulldown)

        self.model_combo_box = QComboBox()
        hbox1_layout.addWidget(self.model_combo_box)

        self.eject_button = QPushButton("Eject Local Model")
        self.eject_button.setEnabled(False)
        hbox1_layout.addWidget(self.eject_button)

        layout.addLayout(hbox1_layout)

        self.text_input = QTextEdit()
        layout.addWidget(self.text_input, 1)

        hbox2_layout = QHBoxLayout()

        self.copy_response_button = QPushButton("Copy Response")
        self.copy_response_button.clicked.connect(self.on_copy_response_clicked)
        hbox2_layout.addWidget(self.copy_response_button)

        self.chunks_only_checkbox = QCheckBox("Chunks Only")
        hbox2_layout.addWidget(self.chunks_only_checkbox)

        self.submit_button = QPushButton("Submit Question")
        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        hbox2_layout.addWidget(self.submit_button)

        layout.addLayout(hbox2_layout)

    def setup_signals(self):
        pass

    def load_created_databases(self):
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                return list(config.get('created_databases', {}).keys())
        return []

    def on_submit_button_clicked(self):
        script_dir = Path(__file__).resolve().parent
        is_valid, error_message = check_preconditions_for_submit_question(script_dir)
        if not is_valid:
            QMessageBox.warning(self, "Error", error_message)
            return

        # Placeholder for future functionality
        pass

    def on_copy_response_clicked(self):
        clipboard = QApplication.clipboard()
        response_text = self.read_only_text.toPlainText()
        if response_text:
            clipboard.setText(response_text)
            QMessageBox.information(self, "Information", "Response copied to clipboard.")
        else:
            QMessageBox.warning(self, "Warning", "No response to copy.")