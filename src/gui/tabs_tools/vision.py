from pathlib import Path
import logging
import yaml
import os
import traceback
from PySide6.QtCore import QThread, Signal as pyqtSignal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox,
    QFileDialog, QDialog, QCheckBox,
    QListWidget, QListWidgetItem, QLabel
)

from modules.process_images import choose_image_loader
from core.constants import VISION_MODELS
from core.vision_benchmark import (
    compare_models_on_image, summarize_documents, write_comparison_report, write_folder_report,
)

CONFIG_FILE = 'config.yaml'


def _load_cfg() -> dict:
    p = Path(CONFIG_FILE)
    if not p.exists():
        return {}
    try:
        with p.open('r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


class ModelComparisonProgressDialog(QDialog):
    PENDING = "⏸"     # ⏸
    RUNNING = "⏳"     # ⏳
    SUCCESS = "✅"     # ✅
    FAILED = "❌"      # ❌

    def __init__(self, model_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vision Model Comparison")
        self.setModal(True)
        self.setMinimumWidth(420)
        self._was_cancelled = False
        self._finished = False

        layout = QVBoxLayout(self)

        self.header_label = QLabel(
            f"Processing image with {len(model_names)} selected model(s)..."
        )
        layout.addWidget(self.header_label)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.NoSelection)
        self.list_widget.setFocusPolicy(Qt.NoFocus)
        for name in model_names:
            item = QListWidgetItem(f"{self.PENDING}  {name}")
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)

        button_row = QHBoxLayout()
        button_row.addStretch(1)
        self.action_button = QPushButton("Cancel")
        self.action_button.clicked.connect(self._on_action_clicked)
        button_row.addWidget(self.action_button)
        layout.addLayout(button_row)

        self._model_names = list(model_names)

    def _set_row(self, index, icon, suffix=""):
        if 0 <= index < len(self._model_names):
            text = f"{icon}  {self._model_names[index]}"
            if suffix:
                text += f"   {suffix}"
            self.list_widget.item(index).setText(text)

    def on_model_started(self, index, name):
        self._set_row(index, self.RUNNING, "processing…")

    def on_model_completed(self, index, name, elapsed):
        self._set_row(index, self.SUCCESS, f"({elapsed:.1f} s)")

    def on_model_failed(self, index, name):
        self._set_row(index, self.FAILED)

    def mark_finished(self):
        self._finished = True
        self.action_button.setText("Close")
        self.header_label.setText("Done. See the comparison output file for details.")

    def was_cancelled(self):
        return self._was_cancelled

    def _on_action_clicked(self):
        if not self._finished:
            self._was_cancelled = True
        self.close()

    def closeEvent(self, event):
        if not self._finished:
            self._was_cancelled = True
        super().closeEvent(event)


class ModelSelectionDialog(QDialog):
    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Vision Models")
        layout = QVBoxLayout()

        self.checkboxes = {}
        for model_name, info in models.items():
            vram_text = info.get('vram', '—')
            checkbox = QCheckBox(f"{model_name} (VRAM: {vram_text})")
            checkbox.setChecked(True)
            self.checkboxes[model_name] = checkbox
            layout.addWidget(checkbox)

        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def get_selected_models(self):
        return [model for model, checkbox in self.checkboxes.items() if checkbox.isChecked()]


class ImageProcessorThread(QThread):
    finished = pyqtSignal(list, float, str)
    error = pyqtSignal(str)

    def run(self):
        try:
            cfg = _load_cfg()
            chosen_model = ((cfg.get('vision') or {}).get('chosen_model')
                            or next(iter(VISION_MODELS.keys())))
            print(f"[Tools] Using chosen_model from config: {chosen_model}")

            documents, processing_time = choose_image_loader(
                {"vision": {"chosen_model": chosen_model}}, return_timing=True
            )

            self.finished.emit(documents, processing_time, chosen_model)
        except Exception as e:
            error_msg = f"Error in image processing: {str(e)}\n{traceback.format_exc()}"
            self.error.emit(error_msg)


class MultiModelProcessorThread(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    model_started = pyqtSignal(int, str)
    model_completed = pyqtSignal(int, str, float)
    model_failed = pyqtSignal(int, str)

    def __init__(self, image_path, selected_models):
        super().__init__()
        self.image_path = image_path
        self.selected_models = selected_models
        self.is_cancelled = False

    def cancel(self):
        self.is_cancelled = True

    def run(self):
        try:
            results = compare_models_on_image(
                self.image_path,
                self.selected_models,
                on_started=self.model_started.emit,
                on_completed=self.model_completed.emit,
                on_failed=self.model_failed.emit,
                should_stop=lambda: self.is_cancelled,
            )
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))


class VisionToolSettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        mainVLayout = QVBoxLayout()
        self.setLayout(mainVLayout)

        hBoxLayout = QHBoxLayout()
        mainVLayout.addLayout(hBoxLayout)

        processButton = QPushButton("Multiple Files + One Vision Model")
        hBoxLayout.addWidget(processButton)
        processButton.clicked.connect(self.startProcessing)

        newButton = QPushButton("Single Image + All Vision Models")
        hBoxLayout.addWidget(newButton)
        newButton.clicked.connect(self.selectSingleImage)

        self.thread = None
        self.progress = None

    def startProcessing(self):
        if self.thread is None:
            self.thread = ImageProcessorThread()
            self.thread.finished.connect(self.onProcessingFinished)
            self.thread.error.connect(self.onProcessingError)
            self.thread.start()

    def onProcessingFinished(self, documents, processing_time, chosen_model):
        self.thread = None
        print(f"Processed {len(documents)} documents")
        summary = summarize_documents(documents)
        self.open_file(write_folder_report(summary, processing_time, chosen_model))

    def onProcessingError(self, error_msg):
        self.thread = None
        logging.error(f"Processing error: {error_msg}")
        QMessageBox.critical(self, "Processing Error", f"An error occurred during image processing:\n\n{error_msg}")

    def selectSingleImage(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image File",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.tif *.tiff)"
        )
        if file_path:
            dialog = ModelSelectionDialog(VISION_MODELS, self)
            if dialog.exec():
                selected_models = dialog.get_selected_models()
                if not selected_models:
                    QMessageBox.warning(self, "Warning", "Please select at least one model.")
                    return

                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText(
                    "Process this image with the selected vision models?\n\n"
                    "This will test each model sequentially and may take several minutes.\n"
                    "Models will be loaded and unloaded to manage memory usage.\n\n"
                    "Do you want to proceed?"
                )
                msgBox.setWindowTitle("Confirm Processing")
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                returnValue = msgBox.exec()

                if returnValue == QMessageBox.Ok:
                    self.progress = ModelComparisonProgressDialog(selected_models, self)
                    self.progress.rejected.connect(self.cancelProcessing)

                    self.thread = MultiModelProcessorThread(file_path, selected_models)
                    self.thread.finished.connect(self.onMultiModelProcessingFinished)
                    self.thread.error.connect(self.onMultiModelProcessingError)
                    self.thread.model_started.connect(self.progress.on_model_started)
                    self.thread.model_completed.connect(self.progress.on_model_completed)
                    self.thread.model_failed.connect(self.progress.on_model_failed)
                    self.thread.start()

                    self.progress.show()

    def cancelProcessing(self):
        if self.thread is not None and hasattr(self.thread, "cancel"):
            self.thread.cancel()

    def onMultiModelProcessingFinished(self, results):
        if self.progress:
            self.progress.mark_finished()
        try:
            output_file = write_comparison_report(self.thread.image_path, results)
            self.open_file(output_file)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving results:\n\n{str(e)}")
        self.thread = None

    def onMultiModelProcessingError(self, error_msg):
        if self.progress:
            self.progress.mark_finished()
            self.progress.close()
        QMessageBox.critical(self, "Error", f"An error occurred during processing:\n\n{error_msg}")
        self.thread = None

    def open_file(self, file_path):
        try:
            os.startfile(file_path)
        except Exception as e:
            error_msg = f"Error opening file: {e}"
            logging.error(error_msg)
            QMessageBox.warning(self, "Error", error_msg)
