from PySide6.QtWidgets import QVBoxLayout, QGroupBox, QWidget, QPushButton, QMessageBox, QHBoxLayout
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QColor
from gui.tabs_tools.transcribe import TranscriberToolSettingsTab
from gui.tabs_tools.vision import VisionToolSettingsTab
from gui.tabs_tools.vision_settings import VisionSettingsTab
from gui.tabs_tools.ocr import OCRToolSettingsTab

class GuiSettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.groups = {}
        self._subtabs = []
        classes = {
            "TRANSCRIBE FILE": (TranscriberToolSettingsTab, 3),
            "SELECT VISION MODEL": (VisionSettingsTab, 2),
            "TEST VISION MODELS": (VisionToolSettingsTab, 2),
            "OPTICAL CHARACTER RECOGNITION": (OCRToolSettingsTab, 2),
        }
        for title, (TabClass, stretch) in classes.items():
            settings = TabClass()
            self._subtabs.append(settings)
            group = QGroupBox(title, checkable=True, checked=True)
            group.setLayout(QVBoxLayout())
            group.layout().addWidget(settings)

            self.groups[group] = stretch
            self.layout.addWidget(group, stretch)
            
            group.toggled.connect(lambda checked, g=group, s=settings: 
                                  (s.setVisible(checked), self.adjust_stretch()))

        self.adjust_stretch()

    def adjust_stretch(self):
        for group, factor in self.groups.items():
            self.layout.setStretchFactor(group, factor if group.isChecked() else 0)

    def cleanup(self):
        for sub in self._subtabs:
            if hasattr(sub, 'cleanup') and callable(sub.cleanup):
                sub.cleanup()