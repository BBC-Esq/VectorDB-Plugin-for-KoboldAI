import os
import shutil
import subprocess
import threading
from pathlib import Path

from PySide6.QtCore import Qt, QObject, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QLabel, QGridLayout, QVBoxLayout, QGroupBox, QPushButton, QMessageBox
)

from constants import VECTOR_MODELS
import webbrowser

class VectorModelsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.group_boxes = {}
        self.stretch_factors = {
            'BAAI': 4,
            'hkunlp': 4,
            'sentence-transformers': 3,
            'thenlper': 4,
        }

        models_dir = Path('Models')
        if not models_dir.exists():
            models_dir.mkdir(parents=True)

        self.vector_models_dir = models_dir / "vector"
        if not self.vector_models_dir.exists():
            self.vector_models_dir.mkdir(parents=True)

        self.existing_vector_directories = {d.name for d in self.vector_models_dir.iterdir() if d.is_dir()}

        headers = ["Model Name", "Dimensions", "Max Sequence", "Size (MB)", "Link"]
        column_stretch_factors = [3, 2, 2, 2, 3]

        def add_centered_widget(grid, widget, row, col):
            grid.addWidget(widget, row, col, alignment=Qt.AlignCenter)

        vector_models_group_box = QGroupBox("Vector Models")
        vector_models_layout = QVBoxLayout()
        vector_models_group_box.setLayout(vector_models_layout)

        for vendor, models in VECTOR_MODELS.items():
            group_box = QGroupBox(vendor)
            group_layout = QGridLayout()
            group_layout.setVerticalSpacing(0)
            group_layout.setHorizontalSpacing(0)
            group_box.setLayout(group_layout)
            self.group_boxes[vendor] = group_box

            for col, header in enumerate(headers):
                header_label = QLabel(header)
                header_label.setAlignment(Qt.AlignCenter)
                header_label.setStyleSheet("text-decoration: underline;")
                group_layout.addWidget(header_label, 0, col)

            for col, stretch_factor in enumerate(column_stretch_factors):
                group_layout.setColumnStretch(col, stretch_factor)

            for model in models:
                model_name = f"{vendor}/{model['name']}"
                grid = group_box.layout()
                row = grid.rowCount()

                add_centered_widget(grid, QLabel(model['name']), row, 0)
                add_centered_widget(grid, QLabel(str(model['dimensions'])), row, 1)
                add_centered_widget(grid, QLabel(str(model['max_sequence'])), row, 2)
                add_centered_widget(grid, QLabel(str(model['size_mb'])), row, 3)

                link = QLabel()
                link.setTextFormat(Qt.RichText)
                link.setText(f'<a href="https://huggingface.co/{model["repo_id"]}">Link</a>')
                link.setOpenExternalLinks(False)
                link.linkActivated.connect(self.open_link)
                add_centered_widget(grid, link, row, 4)

            vector_models_layout.addWidget(group_box, self.stretch_factors.get(vendor, 1))

        self.main_layout.addWidget(vector_models_group_box)

    def get_model_directory_name_vector(self, model_name):
        return model_name.replace('/', '--')

    def open_link(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    window = VectorModelsTab()
    window.show()
    app.exec()