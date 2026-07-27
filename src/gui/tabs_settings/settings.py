from PySide6.QtWidgets import QVBoxLayout, QGroupBox, QWidget
from gui.tabs_settings.vision import VisionSettingsTab


def adjust_stretch(groups, layout):
    for group, factor in groups.items():
        layout.setStretchFactor(group, factor if group.isChecked() else 0)


class GuiSettingsTab(QWidget):
    def __init__(self):
        super(GuiSettingsTab, self).__init__()
        self.layout = QVBoxLayout()
        self.groups = {}

        visionSettings = VisionSettingsTab()
        visionGroup = QGroupBox("Vision Models")
        visionLayout = QVBoxLayout()
        visionLayout.addWidget(visionSettings)
        visionGroup.setLayout(visionLayout)
        visionGroup.setCheckable(True)
        visionGroup.setChecked(True)
        self.layout.addWidget(visionGroup, 1)
        self.groups[visionGroup] = 1
        visionGroup.toggled.connect(lambda checked: (
            visionSettings.setVisible(checked),
            adjust_stretch(self.groups, self.layout)
        ))

        self.layout.addStretch(1)
        self.setLayout(self.layout)
        adjust_stretch(self.groups, self.layout)
