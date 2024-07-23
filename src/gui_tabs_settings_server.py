import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QGridLayout, QGroupBox, QCheckBox, 
                               QLineEdit, QComboBox, QPushButton, QRadioButton, QHBoxLayout)
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtCore import Qt

class ServerSettingsTab(QWidget):
    def __init__(self):
        super(ServerSettingsTab, self).__init__()
        self.setWindowTitle("Kobold AI Settings")
        
        grid_layout = QGridLayout()
        
        # First row
        grid_layout.addWidget(QLabel("GPU Type:"), 0, 0)
        gpu_type_combo = QComboBox()
        gpu_type_combo.addItems(['usecublas', 'usevulkan', 'useclblast'])
        grid_layout.addWidget(gpu_type_combo, 0, 1)
        
        grid_layout.addWidget(QLabel("VRAM:"), 0, 2)
        vram_combo = QComboBox()
        vram_combo.addItems(['Normal VRAM', 'Low VRAM'])
        grid_layout.addWidget(vram_combo, 0, 3)
        
        grid_layout.addWidget(QLabel("Quant KV:"), 0, 4)
        quant_kv_combo = QComboBox()
        quant_kv_combo.addItems(['none', '0=f16', '1=q8', '2=q4'])
        grid_layout.addWidget(quant_kv_combo, 0, 5)
        
        grid_layout.addWidget(QCheckBox("MMQ"), 0, 6)
        
        # Second row
        grid_layout.addWidget(QLabel("Blas Batch Size:"), 1, 0)
        blas_batch_size_combo = QComboBox()
        blas_batch_size_combo.addItems(['Not Specified', '-1', '32', '64', '128', '256', '512', '1024', '2048'])
        grid_layout.addWidget(blas_batch_size_combo, 1, 1)
        
        grid_layout.addWidget(QLabel("Blas Threads:"), 1, 2)
        blas_threads_combo = QComboBox()
        blas_threads_combo.addItems([str(i) for i in range(1, 25)])
        blas_threads_combo.setCurrentIndex(7)
        grid_layout.addWidget(blas_threads_combo, 1, 3)
        
        grid_layout.addWidget(QLabel("CPU Threads:"), 1, 4)
        threads_combo = QComboBox()
        threads_combo.addItems([str(i) for i in range(1, 25)])
        threads_combo.setCurrentIndex(7)
        grid_layout.addWidget(threads_combo, 1, 5)
        
        grid_layout.addWidget(QCheckBox("nommap"), 1, 6)
        
        # Third row
        grid_layout.addWidget(QLabel("Context Size:"), 2, 0)
        context_size_combo = QComboBox()
        context_size_combo.addItems(['256', '512', '1024', '2048', '3072', '4096', '6144', '8192', 
                                     '12288', '16384', '24576', '32768', '49152', '65536', '98304', '131072'])
        grid_layout.addWidget(context_size_combo, 2, 1)
        
        hbox = QHBoxLayout()
        hbox.addWidget(QCheckBox("Flash Attention"))
        hbox.addWidget(QPushButton("Select Model"))
        hbox.addWidget(QPushButton("Start Server"))
        
        grid_layout.addLayout(hbox, 2, 2, 1, 5)
        
        self.setLayout(grid_layout)

def main():
    app = QApplication(sys.argv)
    window = ServerSettingsTab()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()