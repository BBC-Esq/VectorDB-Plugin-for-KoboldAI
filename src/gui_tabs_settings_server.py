import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QGridLayout, QGroupBox, QCheckBox, 
                               QLineEdit, QComboBox, QPushButton, QRadioButton, QHBoxLayout, QToolTip)
from PySide6.QtGui import QIntValidator, QDoubleValidator, QPalette, QColor
from PySide6.QtCore import Qt, QTimer

class ServerSettingsTab(QWidget):
    def __init__(self):
        super(ServerSettingsTab, self).__init__()
        self.setWindowTitle("Kobold AI Settings")
        
        self.grid_layout = QGridLayout()
        
        # First row
        self.grid_layout.addWidget(QLabel("GPU Type:"), 0, 0)
        self.gpu_type_combo = QComboBox()
        self.gpu_type_combo.addItems(['usecublas', 'usevulkan', 'useclblast'])
        self.grid_layout.addWidget(self.gpu_type_combo, 0, 1)
        
        self.grid_layout.addWidget(QLabel("VRAM:"), 0, 2)
        self.vram_combo = QComboBox()
        self.vram_combo.addItems(['Normal VRAM', 'Low VRAM'])
        self.grid_layout.addWidget(self.vram_combo, 0, 3)
        
        self.grid_layout.addWidget(QLabel("Quant KV:"), 0, 4)
        self.quant_kv_combo = QComboBox()
        self.quant_kv_combo.addItems(['none', '0=f16', '1=q8', '2=q4'])
        self.grid_layout.addWidget(self.quant_kv_combo, 0, 5)
        
        self.mmq_checkbox = QCheckBox("MMQ")
        self.grid_layout.addWidget(self.mmq_checkbox, 0, 6)
        
        # Second row
        self.grid_layout.addWidget(QLabel("Blas Batch Size:"), 1, 0)
        self.blas_batch_size_combo = QComboBox()
        self.blas_batch_size_combo.addItems(['Not Specified', '-1', '32', '64', '128', '256', '512', '1024', '2048'])
        self.grid_layout.addWidget(self.blas_batch_size_combo, 1, 1)
        
        self.grid_layout.addWidget(QLabel("Blas Threads:"), 1, 2)
        self.blas_threads_combo = QComboBox()
        self.blas_threads_combo.addItems([str(i) for i in range(1, 25)])
        self.blas_threads_combo.setCurrentIndex(7)
        self.grid_layout.addWidget(self.blas_threads_combo, 1, 3)
        
        self.grid_layout.addWidget(QLabel("CPU Threads:"), 1, 4)
        self.threads_combo = QComboBox()
        self.threads_combo.addItems([str(i) for i in range(1, 25)])
        self.threads_combo.setCurrentIndex(7)
        self.grid_layout.addWidget(self.threads_combo, 1, 5)
        
        self.nommap_checkbox = QCheckBox("nommap")
        self.grid_layout.addWidget(self.nommap_checkbox, 1, 6)
        
        # Third row
        self.grid_layout.addWidget(QLabel("Context Size:"), 2, 0)
        self.context_size_combo = QComboBox()
        self.context_size_combo.addItems(['256', '512', '1024', '2048', '3072', '4096', '6144', '8192', 
                                     '12288', '16384', '24576', '32768', '49152', '65536', '98304', '131072'])
        self.grid_layout.addWidget(self.context_size_combo, 2, 1)
        
        hbox = QHBoxLayout()
        self.flash_attention_checkbox = QCheckBox("Flash Attention")
        self.select_model_button = QPushButton("Select Model")
        self.start_server_button = QPushButton("Start Server")
        hbox.addWidget(self.flash_attention_checkbox)
        hbox.addWidget(self.select_model_button)
        hbox.addWidget(self.start_server_button)
        
        self.grid_layout.addLayout(hbox, 2, 2, 1, 5)
        
        self.setLayout(self.grid_layout)
        
        # Call the function to disable widgets when the script loads
        QTimer.singleShot(0, self.disable_widgets)

    def disable_widgets(self):
        tooltip_message = "This widget is temporarily disabled."
        
        for i in range(self.grid_layout.rowCount()):
            for j in range(self.grid_layout.columnCount()):
                item = self.grid_layout.itemAtPosition(i, j)
                if item:
                    widget = item.widget()
                    if widget:
                        widget.setEnabled(False)
                        widget.setToolTip(tooltip_message)
                        
                        # Change appearance to look more noticeably disabled
                        if isinstance(widget, QLabel):
                            widget.setStyleSheet("color: #606060;")  # Darker gray for labels
                        elif isinstance(widget, (QComboBox, QLineEdit)):
                            widget.setStyleSheet("""
                                background-color: #404040;
                                color: #808080;
                                border: 1px solid #505050;
                            """)
                        elif isinstance(widget, QPushButton):
                            widget.setStyleSheet("""
                                background-color: #404040;
                                color: #808080;
                                border: 1px solid #505050;
                            """)
                        elif isinstance(widget, QCheckBox):
                            widget.setStyleSheet("""
                                color: #808080;
                            """)

def main():
    app = QApplication(sys.argv)
    window = ServerSettingsTab()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()