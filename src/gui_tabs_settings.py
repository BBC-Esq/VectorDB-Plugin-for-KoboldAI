from PySide6.QtWidgets import QVBoxLayout, QGroupBox, QPushButton, QHBoxLayout, QWidget, QMessageBox
from gui_tabs_settings_server import ServerSettingsTab
from gui_tabs_settings_database_create import ChunkSettingsTab
from gui_tabs_settings_database_query import DatabaseSettingsTab
from gui_tabs_settings_vision import VisionSettingsTab

def update_all_configs(configs):
    updated = False
    for title, config in configs.items():
        if title != "Kobold AI":  # Skip Kobold AI tab
            updated = config.update_config() or updated
    if updated:
        print("config.yaml file updated")
    
    message = 'Settings Updated' if updated else 'No Updates'
    details = 'One or more settings have been updated.' if updated else 'No new settings were entered.'
    
    QMessageBox.information(None, message, details)

def adjust_stretch(groups, layout):
    for group, factor in groups.items():
        layout.setStretchFactor(group, factor if group.isChecked() else 0)

class GuiSettingsTab(QWidget):
    def __init__(self):
        super(GuiSettingsTab, self).__init__()
        self.layout = QVBoxLayout()
        classes = {
            "Kobold AI": (ServerSettingsTab, 3),
            "Database Query": (DatabaseSettingsTab, 2),
            "Database Creation": (ChunkSettingsTab, 1),
        }
        self.groups = {}
        self.configs = {}
        for title, (TabClass, stretch) in classes.items():
            settings = TabClass()
            group = QGroupBox(title)
            layout = QVBoxLayout()
            layout.addWidget(settings)
            group.setLayout(layout)
            group.setCheckable(True)
            group.setChecked(True)
            self.groups[group] = stretch
            self.configs[title] = settings
            self.layout.addWidget(group, stretch)
            group.toggled.connect(lambda checked, group=group: (
                self.configs[group.title()].setVisible(checked) if group.title() in self.configs else None,
                adjust_stretch(self.groups, self.layout)
            ))

        # VisionSettingsTab - handled separately
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

        self.update_all_button = QPushButton("Update Settings")
        self.update_all_button.setStyleSheet("min-width: 200px;")
        self.update_all_button.clicked.connect(lambda: update_all_configs(self.configs))

        center_button_layout = QHBoxLayout()
        center_button_layout.addStretch(1)
        center_button_layout.addWidget(self.update_all_button)
        center_button_layout.addStretch(1)
        self.layout.addLayout(center_button_layout)

        self.setLayout(self.layout)
        adjust_stretch(self.groups, self.layout)