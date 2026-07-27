import logging
from pathlib import Path
import yaml
from PySide6.QtCore import Signal, QObject, QThread, QTimer
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QMessageBox, QApplication, QComboBox, QCheckBox, QLabel, QLineEdit
import multiprocessing
from db.database_interactions import process_chunks_only_query
from core.utilities import check_preconditions_for_submit_question, save_config_atomically
from core.constants import PROJECT_ROOT, TOOLTIPS
from chat.kobold import KoboldChat, KoboldThread

FILE_TYPE_MAP = {
    "All Files": "",
    "Images Only": "image",
    "Documents Only": "document",
    "Audio Only": "audio",
}

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="app.log"
)

class RefreshingComboBox(QComboBox):
    def __init__(self, parent=None):
        super(RefreshingComboBox, self).__init__(parent)

    def showPopup(self):
        self.clear()
        self.addItems(self.parent().load_created_databases())
        super(RefreshingComboBox, self).showPopup()

class ChunksOnlyThread(QThread):
    chunks_ready = Signal(str)

    def __init__(self, query, database_name):
        super().__init__()
        self.query = query
        self.database_name = database_name
        self.process = None

    def run(self):
        try:
            result_queue = multiprocessing.Queue()
            self.process = multiprocessing.Process(
                target=process_chunks_only_query,
                args=(self.database_name, self.query, result_queue)
            )
            self.process.start()
            result = result_queue.get()
            self.chunks_ready.emit(result)
            self.process.join()
        except Exception as e:
            logging.exception(f"ChunksOnlyThread error: {e}")
            self.chunks_ready.emit(f"Error querying database: {e}")

class GuiSignals(QObject):
    response_signal = Signal(str)
    citations_signal = Signal(str)
    error_signal = Signal(str)
    finished_signal = Signal()

class DatabaseQueryTab(QWidget):
    def __init__(self):
        super(DatabaseQueryTab, self).__init__()
        self.config_path = PROJECT_ROOT / "config.yaml"
        self.gui_signals = GuiSignals()
        self.initWidgets()
        self.setup_signals()
        self.kobold_thread = None
        self.chunks_only_thread = None

    def initWidgets(self):
        layout = QVBoxLayout(self)
        self.read_only_text = QTextEdit()
        self.read_only_text.setReadOnly(True)
        layout.addWidget(self.read_only_text, 5)
        for row in self._build_settings_rows():
            layout.addLayout(row)
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
        self.submit_button = QPushButton("Submit Question")
        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        hbox2_layout.addWidget(self.submit_button)
        self.chunks_only_checkbox = QCheckBox("Chunks Only")
        hbox2_layout.addWidget(self.chunks_only_checkbox)
        layout.addLayout(hbox2_layout)

    def _read_config(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}

    def _write_config(self, mutate):
        config = self._read_config()
        mutate(config)
        save_config_atomically(config, self.config_path)

    def _build_settings_rows(self):
        config = self._read_config()
        db_cfg = config.get("database") or {}
        compute = config.get("Compute_Device") or {}

        row1 = QHBoxLayout()

        row1.addWidget(QLabel("Device:"))
        self.query_device_combo = QComboBox()
        available = compute.get("available") or ["cpu"]
        self.query_device_combo.addItems(available)
        current = compute.get("database_query", "cpu")
        if current in available:
            self.query_device_combo.setCurrentIndex(available.index(current))
        self.query_device_combo.setToolTip(TOOLTIPS["CREATE_DEVICE_QUERY"])
        self.query_device_combo.currentIndexChanged.connect(self._on_query_device_changed)
        row1.addWidget(self.query_device_combo)
        row1.addSpacing(12)

        row1.addWidget(QLabel("Similarity:"))
        self.similarity_edit = QLineEdit(str(db_cfg.get("similarity", 0.7)))
        validator = QDoubleValidator(0.0, 1.0, 3, self)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.similarity_edit.setValidator(validator)
        self.similarity_edit.setToolTip(TOOLTIPS["SIMILARITY"])
        self.similarity_edit.setMaximumWidth(80)
        self.similarity_edit.textEdited.connect(lambda: self._query_debounce.start())
        row1.addWidget(self.similarity_edit)
        row1.addSpacing(12)

        row1.addWidget(QLabel("Contexts:"))
        self.contexts_edit = QLineEdit(str(db_cfg.get("contexts", 5)))
        self.contexts_edit.setValidator(QIntValidator(1, 1000, self))
        self.contexts_edit.setToolTip(TOOLTIPS["CONTEXTS"])
        self.contexts_edit.setMaximumWidth(80)
        self.contexts_edit.textEdited.connect(lambda: self._query_debounce.start())
        row1.addWidget(self.contexts_edit)
        row1.addSpacing(12)

        row1.addWidget(QLabel("File Type:"))
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(list(FILE_TYPE_MAP.keys()))
        stored = db_cfg.get("document_types", "")
        for label, value in FILE_TYPE_MAP.items():
            if value == stored:
                self.file_type_combo.setCurrentIndex(list(FILE_TYPE_MAP.keys()).index(label))
                break
        self.file_type_combo.setToolTip(TOOLTIPS["FILE_TYPE_FILTER"])
        self.file_type_combo.currentIndexChanged.connect(self._on_file_type_changed)
        row1.addWidget(self.file_type_combo)
        row1.addStretch(1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Search Filter:"))
        self.search_term_edit = QLineEdit(db_cfg.get("search_term", "") or "")
        self.search_term_edit.setPlaceholderText("Optional keyword that results must contain")
        self.search_term_edit.setToolTip(TOOLTIPS["SEARCH_TERM_FILTER"])
        self.search_term_edit.textEdited.connect(lambda: self._query_debounce.start())
        row2.addWidget(self.search_term_edit, 1)
        self.clear_filter_button = QPushButton("Clear Filter")
        self.clear_filter_button.clicked.connect(self._on_clear_filter)
        row2.addWidget(self.clear_filter_button)

        self._query_debounce = QTimer(self)
        self._query_debounce.setSingleShot(True)
        self._query_debounce.setInterval(800)
        self._query_debounce.timeout.connect(self._commit_query_settings)

        return [row1, row2]

    def _mark_invalid(self, widget, invalid):
        widget.setStyleSheet("border: 1px solid #c0392b;" if invalid else "")

    def _commit_query_settings(self):
        similarity_text = self.similarity_edit.text().strip()
        contexts_text = self.contexts_edit.text().strip()
        search_term = self.search_term_edit.text().strip()

        similarity = None
        if similarity_text:
            try:
                similarity = float(similarity_text)
            except ValueError:
                similarity = None
        bad_similarity = similarity is None or not (0.0 <= similarity <= 1.0)
        self._mark_invalid(self.similarity_edit, bad_similarity)

        contexts = None
        if contexts_text:
            try:
                contexts = int(contexts_text)
            except ValueError:
                contexts = None
        bad_contexts = contexts is None or not (1 <= contexts <= 1000)
        self._mark_invalid(self.contexts_edit, bad_contexts)

        if bad_similarity or bad_contexts:
            return

        current = self._read_config().get("database") or {}
        if (current.get("similarity") == similarity
                and current.get("contexts") == contexts
                and (current.get("search_term") or "") == search_term):
            return

        def mutate(config):
            db = config.setdefault("database", {})
            db["similarity"] = similarity
            db["contexts"] = contexts
            db["search_term"] = search_term

        self._write_config(mutate)

    def _on_query_device_changed(self):
        device = self.query_device_combo.currentText()

        def mutate(config):
            config.setdefault("Compute_Device", {})["database_query"] = device

        self._write_config(mutate)

    def _on_file_type_changed(self):
        value = FILE_TYPE_MAP.get(self.file_type_combo.currentText(), "")

        def mutate(config):
            config.setdefault("database", {})["document_types"] = value

        self._write_config(mutate)

    def _on_clear_filter(self):
        self.search_term_edit.clear()
        self._mark_invalid(self.search_term_edit, False)

        def mutate(config):
            config.setdefault("database", {})["search_term"] = ""

        self._write_config(mutate)

    def setup_signals(self):
        self.gui_signals.response_signal.connect(self.update_response)
        self.gui_signals.citations_signal.connect(self.display_citations)
        self.gui_signals.error_signal.connect(self.show_error_message)
        self.gui_signals.finished_signal.connect(self.on_submission_finished)

    def load_created_databases(self):
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
                return list(config.get("created_databases", {}).keys())
        return []

    def on_submit_button_clicked(self):
        if self.kobold_thread is not None and self.kobold_thread.isRunning():
            return
        script_dir = PROJECT_ROOT
        is_valid, error_message = check_preconditions_for_submit_question(script_dir)
        if not is_valid:
            QMessageBox.warning(self, "Error", error_message)
            return
        self.submit_button.setDisabled(True)
        user_question = self.text_input.toPlainText()
        selected_database = self.database_pulldown.currentText()
        chunks_only = self.chunks_only_checkbox.isChecked()
        self.read_only_text.clear()
        if chunks_only:
            self.chunks_only_thread = ChunksOnlyThread(user_question, selected_database)
            self.chunks_only_thread.chunks_ready.connect(self.display_chunks)
            self.chunks_only_thread.finished.connect(self.on_submission_finished)
            self.chunks_only_thread.start()
            return
        self.kobold_thread = KoboldThread(user_question, selected_database)
        self.kobold_thread.kobold_chat.signals.response_signal.connect(self.update_response)
        self.kobold_thread.kobold_chat.signals.error_signal.connect(self.show_error_message)
        self.kobold_thread.kobold_chat.signals.finished_signal.connect(self.on_submission_finished)
        self.kobold_thread.kobold_chat.signals.citation_signal.connect(self.display_citations)
        self.kobold_thread.start()

    def display_chunks(self, chunks):
        self.read_only_text.setPlainText(chunks)
        self.submit_button.setDisabled(False)

    def disconnect_kobold_thread_signals(self):
        if self.kobold_thread:
            try:
                self.kobold_thread.kobold_chat.signals.response_signal.disconnect(self.update_response)
                self.kobold_thread.kobold_chat.signals.error_signal.disconnect(self.show_error_message)
                self.kobold_thread.kobold_chat.signals.finished_signal.disconnect(self.on_submission_finished)
                self.kobold_thread.kobold_chat.signals.citation_signal.disconnect(self.display_citations)
            except Exception as e:
                logging.debug("Error disconnecting thread signals: " + str(e))

    def update_response(self, response_chunk):
        response_chunk = response_chunk.lstrip("\n")
        if response_chunk:
            self.read_only_text.insertPlainText(response_chunk)
            self.read_only_text.ensureCursorVisible()
            self.read_only_text.repaint()
            QApplication.processEvents()

    def display_citations(self, citations):
        self.read_only_text.append("\n\nCitations:\n" + citations)
        self.read_only_text.repaint()
        QApplication.processEvents()

    def show_error_message(self, error_message):
        QMessageBox.warning(self, "Error", error_message)
        self.submit_button.setDisabled(False)

    def on_submission_finished(self):
        self.submit_button.setDisabled(False)
        if self.kobold_thread:
            self.disconnect_kobold_thread_signals()
            self.kobold_thread = None
        logging.debug("Cleaned up after submission")

    def on_copy_response_clicked(self):
        clipboard = QApplication.clipboard()
        response_text = self.read_only_text.toPlainText()
        if response_text:
            clipboard.setText(response_text)
            QMessageBox.information(self, "Information", "Response copied to clipboard.")
        else:
            QMessageBox.warning(self, "Warning", "No response to copy.")
