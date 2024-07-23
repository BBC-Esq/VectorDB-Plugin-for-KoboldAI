import os
import shutil
import subprocess
import threading
from pathlib import Path

from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtWidgets import (
    QWidget, QLabel, QGridLayout, QVBoxLayout, QGroupBox
)

from constants import VECTOR_MODELS, VISION_MODELS
import webbrowser

class VectorModelsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.group_boxes = {}
        self.downloaded_labels = {}
        self.stretch_factors = {
            'BAAI': 3,
            'hkunlp': 3,
            'sentence-transformers': 2,
            'thenlper': 3,
            # 'Alibaba-NLP': 2
        }

        models_dir = Path('Models')
        if not models_dir.exists():
            models_dir.mkdir(parents=True)

        vector_models_dir = models_dir / "Vector"
        vision_models_dir = models_dir / "Vision"

        existing_vector_directories = {d.name for d in vector_models_dir.iterdir() if d.is_dir()}
        existing_vision_directories = {d.name for d in vision_models_dir.iterdir() if d.is_dir()}

        headers = ["Model Name", "Dimensions", "Max Sequence", "Size (MB)", "Downloaded", "Link"]
        column_stretch_factors = [3, 2, 2, 2, 2, 3]

        def add_centered_widget(grid, widget, row, col):
            grid.addWidget(widget, row, col, alignment=Qt.AlignCenter)

        # Create Vector Models main group box
        vector_models_group_box = QGroupBox("Vector Models")
        vector_models_layout = QVBoxLayout()
        vector_models_group_box.setLayout(vector_models_layout)

        # Create vector model sub-group boxes
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

                expected_dir_name = self.get_model_directory_name(model_name, "vector")
                is_downloaded = expected_dir_name in existing_vector_directories
                downloaded_label = QLabel('Yes' if is_downloaded else 'No')
                add_centered_widget(grid, downloaded_label, row, 4)

                self.downloaded_labels[model_name] = (downloaded_label, "vector")

                link = QLabel()
                link.setTextFormat(Qt.RichText)
                link.setText(f'<a href="https://huggingface.co/{model["repo_id"]}">Link</a>')
                link.setOpenExternalLinks(False)
                link.linkActivated.connect(self.open_link)
                add_centered_widget(grid, link, row, 5)

            vector_models_layout.addWidget(group_box, self.stretch_factors.get(vendor, 1))

        self.main_layout.addWidget(vector_models_group_box, 15)

        # Create vision model group box
        vision_group_box = QGroupBox("Vision Models")
        vision_layout = QGridLayout()
        vision_layout.setVerticalSpacing(0)
        vision_layout.setHorizontalSpacing(0)
        vision_group_box.setLayout(vision_layout)

        vision_headers = ["Model Name", "Tokens per Second", "Max Sequence", "Size", "Downloaded", "Link"]
        for col, header in enumerate(vision_headers):
            header_label = QLabel(header)
            header_label.setAlignment(Qt.AlignCenter)
            header_label.setStyleSheet("text-decoration: underline;")
            vision_layout.addWidget(header_label, 0, col)

        for col, stretch_factor in enumerate(column_stretch_factors):
            vision_layout.setColumnStretch(col, stretch_factor)

        for row, (model_name, model_info) in enumerate(VISION_MODELS.items(), start=1):
            add_centered_widget(vision_layout, QLabel(model_name), row, 0)
            add_centered_widget(vision_layout, QLabel("Placeholder"), row, 1)
            add_centered_widget(vision_layout, QLabel("Placeholder"), row, 2)
            add_centered_widget(vision_layout, QLabel(model_info['size']), row, 3)

            expected_dir_name = self.get_model_directory_name(model_name, "vision")
            is_downloaded = expected_dir_name in existing_vision_directories
            downloaded_label = QLabel('Yes' if is_downloaded else 'No')
            add_centered_widget(vision_layout, downloaded_label, row, 4)

            self.downloaded_labels[model_name] = (downloaded_label, "vision")

            link_label = QLabel("Link")
            add_centered_widget(vision_layout, link_label, row, 5)

        self.main_layout.addWidget(vision_group_box, 3)

    def get_model_directory_name(self, model_name, model_type):
        return model_name.replace('/', '_')

    def open_link(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    window = VectorModelsTab()
    window.show()
    app.exec()