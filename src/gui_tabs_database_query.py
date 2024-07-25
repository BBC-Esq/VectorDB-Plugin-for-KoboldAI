import logging
from pathlib import Path

import yaml
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QPushButton, QCheckBox, QHBoxLayout, QMessageBox,
                               QApplication, QComboBox)

from utilities import check_preconditions_for_submit_question
from chat_kobold import KoboldChat

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
        self.kobold_chat = None

    def initWidgets(self):
        layout = QVBoxLayout(self)

        self.read_only_text = QTextEdit()
        self.read_only_text.setReadOnly(True)
        layout.addWidget(self.read_only_text, 5)

        hbox1_layout = QHBoxLayout()

        self.database_pulldown = RefreshingComboBox(self)
        self.database_pulldown.addItems(self.load_created_databases())
        hbox1_layout.addWidget(self.database_pulldown)

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
        self.gui_signals.response_signal.connect(self.update_response)
        self.gui_signals.citations_signal.connect(self.display_citations)
        self.gui_signals.error_signal.connect(self.show_error_message)
        self.gui_signals.finished_signal.connect(self.on_submission_finished)

    def load_created_databases(self):
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                return list(config.get('created_databases', {}).keys())
        return []

    def on_submit_button_clicked(self):
        if self.kobold_chat is not None:
            return

        script_dir = Path(__file__).resolve().parent
        is_valid, error_message = check_preconditions_for_submit_question(script_dir)
        if not is_valid:
            QMessageBox.warning(self, "Error", error_message)
            return

        self.submit_button.setDisabled(True)
        user_question = self.text_input.toPlainText()
        chunks_only = self.chunks_only_checkbox.isChecked()
        selected_database = self.database_pulldown.currentText()

        self.kobold_chat = KoboldChat()
        
        self.connect_kobold_chat_signals()

        self.kobold_chat.ask_kobold(user_question, chunks_only, selected_database)

        self.read_only_text.clear()

    def connect_kobold_chat_signals(self):
        self.kobold_chat.signals.response_signal.connect(self.update_response)
        self.kobold_chat.signals.error_signal.connect(self.show_error_message)
        self.kobold_chat.signals.finished_signal.connect(self.on_submission_finished)
        self.kobold_chat.signals.citation_signal.connect(self.display_citations)

    def disconnect_kobold_chat_signals(self):
        if self.kobold_chat:
            self.kobold_chat.signals.response_signal.disconnect(self.update_response)
            self.kobold_chat.signals.error_signal.disconnect(self.show_error_message)
            self.kobold_chat.signals.finished_signal.disconnect(self.on_submission_finished)
            self.kobold_chat.signals.citation_signal.disconnect(self.display_citations)

    def update_response(self, response_chunk):
        response_chunk = response_chunk.lstrip('\n')
        self.read_only_text.insertPlainText(response_chunk)
        self.read_only_text.ensureCursorVisible()
        QApplication.processEvents()

    def display_citations(self, citations):
        self.read_only_text.append("\n\nCitations:\n" + citations)

    def show_error_message(self, error_message):
        QMessageBox.warning(self, "Error", error_message)
        self.submit_button.setDisabled(False)

    def on_submission_finished(self):
        self.submit_button.setDisabled(False)
        if self.kobold_chat:
            self.disconnect_kobold_chat_signals()
            self.kobold_chat = None
        logging.debug("Cleaned up after submission")

    def on_copy_response_clicked(self):
        clipboard = QApplication.clipboard()
        response_text = self.read_only_text.toPlainText()
        if response_text:
            clipboard.setText(response_text)
            QMessageBox.information(self, "Information", "Response copied to clipboard.")
        else:
            QMessageBox.warning(self, "Warning", "No response to copy.")