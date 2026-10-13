import html
import time
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QComboBox, QFileDialog, QMessageBox
)
from PySide6.QtCore import QThread, Signal
from core.ocr_tools import OCR_ENGINES, ocr_output_path, run_ocr, summarize_ocr_events

class OcrWorkerThread(QThread):
    finished_signal = Signal(bool, str, float, object)

    def __init__(self, pdf_path, backend, parent=None):
        super().__init__(parent)
        self.pdf_path = pdf_path
        self.backend = backend

    def run(self):
        start_time = time.time()
        success, message, events = run_ocr(self.pdf_path, self.backend)
        elapsed_time = time.time() - start_time
        self.finished_signal.emit(success, message or "", elapsed_time, events)

class OCRToolSettingsTab(QWidget):
    ENGINE_MAPPING = OCR_ENGINES

    def __init__(self):
        super().__init__()
        self.selected_pdf_file = None
        self.last_events = {}
        self.create_layout()
        self.setButtons(True)
        self.worker_thread = None

    def create_layout(self):
        main_layout = QVBoxLayout()

        engine_selection_hbox = QHBoxLayout()

        engine_label = QLabel("OCR Engine")
        engine_selection_hbox.addWidget(engine_label)

        self.engine_combo = QComboBox()
        self.engine_combo.addItems(list(OCR_ENGINES))
        self.engine_combo.setCurrentText("RapidOCR")
        engine_selection_hbox.addWidget(self.engine_combo)

        self.select_pdf_button = QPushButton("Choose PDF")
        self.select_pdf_button.clicked.connect(self.select_pdf_file)
        engine_selection_hbox.addWidget(self.select_pdf_button)

        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.start_ocr_process)
        engine_selection_hbox.addWidget(self.process_button)

        engine_selection_hbox.setStretchFactor(engine_label, 1)
        engine_selection_hbox.setStretchFactor(self.engine_combo, 2)
        engine_selection_hbox.setStretchFactor(self.select_pdf_button, 1)
        engine_selection_hbox.setStretchFactor(self.process_button, 1)

        main_layout.addLayout(engine_selection_hbox)

        self.file_path_label = QLabel("No PDF file selected")
        main_layout.addWidget(self.file_path_label)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: gray;")
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def setButtons(self, enabled):
        self.select_pdf_button.setEnabled(enabled)
        self.process_button.setEnabled(enabled)
        self.engine_combo.setEnabled(enabled)
        if enabled:
            self.status_label.setText("")

    def select_pdf_file(self):
        current_dir = Path.cwd()
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Select PDF File", 
            str(current_dir),
            "PDF Files (*.pdf)"
        )
        if file_name:
            file_path = Path(file_name)
            short_path = f"...{file_path.parent.name}/{file_path.name}"
            self.file_path_label.setText(short_path)
            self.file_path_label.setToolTip(str(file_path.absolute()))
            self.selected_pdf_file = file_name
            self.status_label.setText("")

    def show_error_message(self, message):
        self.status_label.setStyleSheet("color: red;")
        self.status_label.setText("Error: OCR process failed")
        QMessageBox.critical(self, "Error", f"OCR process failed:\n{message}")

    def show_success_message(self):
        warnings, infos = summarize_ocr_events(getattr(self, 'last_events', {}))

        minutes, seconds = divmod(self.elapsed_time, 60)
        time_str = f"{int(minutes)}m {seconds:.1f}s" if minutes > 0 else f"{seconds:.1f}s"
        if warnings:
            self.status_label.setStyleSheet("color: #FF9800;")
            self.status_label.setText(f"Success with {len(warnings)} warning(s) - {time_str}")
        else:
            self.status_label.setStyleSheet("color: #4CAF50;")
            self.status_label.setText(f"Success! Completed in {time_str}")

        if not self.selected_pdf_file:
            return

        processed_file = ocr_output_path(self.selected_pdf_file)

        if processed_file.exists():
            file_link = f'<a href="file:///{processed_file}" style="color: #4CAF50; text-decoration: none;">Open New File</a>'
        else:
            file_link = "The processed file could not be found."

        notes = ""
        if warnings or infos:
            bullets = "".join(f'&bull; <span style="color:#FF9800;">{html.escape(w)}</span><br>' for w in warnings)
            bullets += "".join(f"&bull; {html.escape(i)}<br>" for i in infos)
            notes = f"<br><b>Quality notes:</b><br>{bullets}"

        QMessageBox.information(
            self,
            "Success!",
            f"""Processing completed in {time_str}!<br><br>
            A new <b>.pdf</b> ending in <b>'_OCR'</b> has been saved
            in the same directory as the original file.<br><br>

            {file_link}
            {notes}
            """
        )

    def start_ocr_process(self):
        if not self.selected_pdf_file:
            QMessageBox.warning(self, "Warning", "Please select a PDF file first.")
            return

        selected_engine = self.engine_combo.currentText()
        backend = self.ENGINE_MAPPING[selected_engine]

        self.status_label.setStyleSheet("color: #0074D9;")
        self.status_label.setText(f"Processing with {selected_engine}...")
        print(f"Starting OCR process for {self.selected_pdf_file}")

        self.setButtons(False)

        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.wait()

        self.worker_thread = OcrWorkerThread(self.selected_pdf_file, backend)
        self.worker_thread.finished_signal.connect(self.ocr_finished)
        self.worker_thread.start()

    def ocr_finished(self, success, message, elapsed_time, events):
        self.setButtons(True)

        self.elapsed_time = elapsed_time
        self.last_events = events if isinstance(events, dict) else {}

        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread = None

        from PySide6.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self._show_completion_message(success, message))

    def _show_completion_message(self, success, message):
        if success:
            self.show_success_message()
        else:
            self.show_error_message(message)
