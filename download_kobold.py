import sys
import requests
import threading
import cpuinfo
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QComboBox, QPushButton, QProgressBar, QGridLayout, 
                               QCheckBox, QMessageBox, QGroupBox)
from PySide6.QtCore import Qt, QThread, Signal

def check_instruction_set():
    """
    Check if the CPU supports AVX2 instruction set.
    """
    info = cpuinfo.get_cpu_info()
    flags = info['flags']
    return 'avx2' in flags

def check_nvidia_gpu():
    """
    Check if the system has an Nvidia GPU with nvidia-smi installed.
    """
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

class DownloadThread(QThread):
    progress_update = Signal(int)
    download_complete = Signal(str)
    download_error = Signal(str)

    def __init__(self, url, filename):
        super().__init__()
        self.url = url
        self.filename = filename

    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            with open(self.filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        progress = int((downloaded_size / total_size) * 100)
                        self.progress_update.emit(progress)

            self.download_complete.emit(self.filename)
        except requests.exceptions.RequestException as e:
            self.download_error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Downloader")
        self.setGeometry(100, 100, 300, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.setup_ui()

    def setup_ui(self):
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        # First group box
        info_group = QGroupBox()
        info_layout = QVBoxLayout(info_group)

        self.avx2_label = QLabel()
        info_layout.addWidget(self.avx2_label)

        self.gpu_label = QLabel()
        info_layout.addWidget(self.gpu_label)

        self.update_system_info()

        grid_layout = self.create_table_like_layout()
        info_layout.addLayout(grid_layout)

        self.layout.addWidget(info_group)

        # Second group box
        download_group = QGroupBox()
        download_layout = QVBoxLayout(download_group)

        self.label = QLabel("Select a file to download:")
        download_layout.addWidget(self.label)

        self.file_combobox = QComboBox()
        self.file_combobox.addItems(download_links.keys())
        self.file_combobox.setCurrentText("koboldcpp_nocuda.exe")
        download_layout.addWidget(self.file_combobox)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        download_layout.addWidget(self.download_button)

        self.layout.addWidget(download_group)

    def update_system_info(self):
        avx2_supported = check_instruction_set()
        nvidia_gpu_detected = check_nvidia_gpu()

        if avx2_supported:
            self.avx2_label.setText("AVX2 instruction set detected.")
        else:
            self.avx2_label.setText("The AVX2 instruction set is not detected. You must use 'koboldcpp_oldcpu.exe'.")

        if nvidia_gpu_detected:
            self.gpu_label.setText("Nvidia GPU detected.")
        else:
            self.gpu_label.setText("No Nvidia GPU detected. You cannot use 'koboldcpp.exe' nor 'koboldcpp_cu12.exe'.")

    def create_table_like_layout(self):
        grid_layout = QGridLayout()

        # Headers
        headers = ["Binary", "Requires AVX2", "CUDA Support"]
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet("font-weight: bold;")
            grid_layout.addWidget(label, 0, col, Qt.AlignCenter)

        # Content
        for row, binary in enumerate(download_links.keys(), start=1):
            grid_layout.addWidget(QLabel(binary), row, 0)
            
            avx2_checkbox = QCheckBox()
            avx2_checkbox.setChecked(binary != "koboldcpp_oldcpu.exe")
            avx2_checkbox.setAttribute(Qt.WA_TransparentForMouseEvents)
            avx2_checkbox.setFocusPolicy(Qt.NoFocus)
            grid_layout.addWidget(avx2_checkbox, row, 1, Qt.AlignCenter)
            
            cuda_checkbox = QCheckBox()
            cuda_checkbox.setChecked(binary != "koboldcpp_nocuda.exe")
            cuda_checkbox.setAttribute(Qt.WA_TransparentForMouseEvents)
            cuda_checkbox.setFocusPolicy(Qt.NoFocus)
            grid_layout.addWidget(cuda_checkbox, row, 2, Qt.AlignCenter)

        return grid_layout

    def start_download(self):
        selected_file = self.file_combobox.currentText()
        if selected_file in download_links:
            download_url = download_links[selected_file]
            self.download_thread = DownloadThread(download_url, selected_file)
            self.download_thread.progress_update.connect(self.update_progress)
            self.download_thread.download_complete.connect(self.download_finished)
            self.download_thread.download_error.connect(self.download_error)
            self.download_thread.start()
        else:
            QMessageBox.critical(self, "Error", f"{selected_file} not found in the download links.")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def download_finished(self, filename):
        self.progress_bar.setValue(0)
        QMessageBox.information(self, "Success", f"File downloaded successfully and saved as {filename}")

    def download_error(self, error_message):
        self.progress_bar.setValue(0)
        QMessageBox.critical(self, "Error", f"An error occurred while downloading the file: {error_message}")

download_links = {
    "koboldcpp.exe": "https://github.com/LostRuins/koboldcpp/releases/download/v1.70.1/koboldcpp.exe",
    "koboldcpp_cu12.exe": "https://github.com/LostRuins/koboldcpp/releases/download/v1.70.1/koboldcpp_cu12.exe",
    "koboldcpp_oldcpu.exe": "https://github.com/LostRuins/koboldcpp/releases/download/v1.70.1/koboldcpp_oldcpu.exe",
    "koboldcpp_nocuda.exe": "https://github.com/LostRuins/koboldcpp/releases/download/v1.70.1/koboldcpp_nocuda.exe"
}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())