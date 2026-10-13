import yaml
from PySide6.QtWidgets import QApplication

def list_theme_files():
    from core.constants import THEMES
    return sorted(THEMES.keys())

def load_stylesheet(name):
    from string import Template
    from core.constants import PROJECT_ROOT, THEMES
    if name not in THEMES:
        name = 'default'
    template_path = PROJECT_ROOT / 'CSS' / 'template.css'
    with template_path.open('r') as f:
        template = Template(f.read())
    return template.substitute(THEMES[name])

def ensure_theme_config():
    from core.constants import THEMES
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        if config is None:
            config = {}

        if 'appearance' not in config:
            config['appearance'] = {}

        theme = config['appearance'].get('theme')
        if not theme or theme not in THEMES:
            config['appearance']['theme'] = 'default'

        with open('config.yaml', 'w') as f:
            yaml.safe_dump(config, f)

        return config['appearance']['theme']
    except Exception:
        return 'default'

def update_theme_in_config(new_theme):
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        if config is None:
            config = {}

        if 'appearance' not in config:
            config['appearance'] = {}

        config['appearance']['theme'] = new_theme

        with open('config.yaml', 'w') as f:
            yaml.safe_dump(config, f)
    except Exception:
        pass

def make_theme_changer(theme_name):
    def change_theme():
        QApplication.instance().setStyleSheet(load_stylesheet(theme_name))
        update_theme_in_config(theme_name)
    return change_theme
