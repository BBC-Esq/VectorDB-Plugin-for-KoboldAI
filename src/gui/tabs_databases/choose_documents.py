from pathlib import Path

from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QProgressDialog,
    QVBoxLayout,
    QDialog,
    QTextEdit,
    QPushButton,
    QMessageBox,
)

from core.constants import PROJECT_ROOT
from core.staging import DOCS_DIR, collect_files, is_supported, stage_files


class SymlinkWorker(QThread):
    progress = Signal(int)
    finished = Signal(int, list)

    def __init__(self, source, target_dir, parent=None):
        super().__init__(parent)
        self.source = list(source)
        self.target_dir = Path(target_dir)

    def run(self):
        made, errors = stage_files(
            self.source,
            self.target_dir,
            on_progress=self.progress.emit,
            should_stop=self.isInterruptionRequested,
        )
        self.finished.emit(made, errors)


def choose_documents_directory():
    existing_worker = getattr(choose_documents_directory, "_symlink_thread", None)
    if existing_worker is not None and existing_worker.isRunning():
        QMessageBox.information(
            None, "Staging In Progress",
            "Files are still being staged. Wait for the current job to finish or cancel it before starting another."
        )
        return

    current_dir = PROJECT_ROOT
    target_dir = DOCS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    msg_box = QMessageBox()
    msg_box.setWindowTitle("Selection Type")
    msg_box.setText("Would you like to select a directory or individual files?")

    dir_button = msg_box.addButton("Select Directory", QMessageBox.ActionRole)
    msg_box.addButton("Select Files", QMessageBox.ActionRole)
    cancel_button = msg_box.addButton("Cancel", QMessageBox.RejectRole)

    msg_box.exec()
    clicked_button = msg_box.clickedButton()

    if clicked_button == cancel_button:
        return

    file_dialog = QFileDialog()

    def start_worker(source):
        progress = QProgressDialog(
            "Creating symlinks...", "Cancel", 0, 0
        )
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)

        worker = SymlinkWorker(source, target_dir)
        main_window = _get_main_window()

        progress.canceled.connect(worker.requestInterruption)

        def update_progress(pct):
            if progress.maximum() == 0:
                progress.setRange(0, 100)
            progress.setValue(pct)

        worker.progress.connect(update_progress)

        def _done(count, errs):
            if main_window and hasattr(main_window, "databases_tab"):
                db_tab = main_window.databases_tab
                if hasattr(db_tab, "refresh_staged_files"):
                    db_tab.refresh_staged_files()

            progress.reset()
            msg = f"Created {count} symlinks"
            if errs:
                msg += f" – {len(errs)} errors (see console)"
                print(*errs, sep="\n")
            QMessageBox.information(None, "Symlinks", msg)

        worker.finished.connect(_done)
        worker.progress.connect(update_progress)
        worker.start()

        choose_documents_directory._symlink_thread = worker

    if clicked_button == dir_button:
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        selected_dir = file_dialog.getExistingDirectory(
            None, "Choose Directory for Database", str(current_dir)
        )
        if selected_dir:
            selection = collect_files([selected_dir])
            top_level_files = selection.top_level
            subdirectory_files = selection.nested

            include_subdirs = False
            if subdirectory_files:
                reply = QMessageBox.question(
                    None,
                    "Include Subdirectories?",
                    (
                        f"This folder contains {len(top_level_files)} compatible file(s) "
                        f"at the top level and {len(subdirectory_files)} more in "
                        f"subdirectories.\n\nInclude the subdirectory files as well?"
                    ),
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                include_subdirs = (reply == QMessageBox.Yes)

            files_to_symlink = (
                top_level_files + subdirectory_files if include_subdirs else top_level_files
            )

            if files_to_symlink:
                start_worker(files_to_symlink)
            else:
                QMessageBox.information(
                    None, "No Compatible Files",
                    "No compatible files were found in the selected directory."
                )
    else:
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_paths = file_dialog.getOpenFileNames(
            None, "Choose Documents and Images for Database", str(current_dir)
        )[0]
        if file_paths:
            compatible_files = []
            incompatible_files = []
            for file_path in file_paths:
                path = Path(file_path)
                if is_supported(path):
                    compatible_files.append(str(path))
                else:
                    incompatible_files.append(path.name)

            if incompatible_files and not show_incompatible_files_dialog(
                incompatible_files
            ):
                return

            if compatible_files:
                start_worker(compatible_files)


def show_incompatible_files_dialog(incompatible_files):
    dialog_text = (
        "The following files cannot be added here due to their file extension:\n\n"
        + "\n".join(incompatible_files)
        + "\n\nHowever, if any of them are audio files you can still add them directly in the Tools Tab."
        "\n\nClick 'Ok' to add the compatible documents only (remembering to add audio files separately)"
        " or 'Cancel' to back out completely."
    )

    incompatible_dialog = QDialog()
    incompatible_dialog.resize(800, 600)
    incompatible_dialog.setWindowTitle("Incompatible Files Detected")

    layout = QVBoxLayout()
    text_edit = QTextEdit()
    text_edit.setReadOnly(True)
    text_edit.setText(dialog_text)
    layout.addWidget(text_edit)

    button_box = QHBoxLayout()
    ok_button = QPushButton("OK")
    cancel_button = QPushButton("Cancel")
    button_box.addWidget(ok_button)
    button_box.addWidget(cancel_button)

    layout.addLayout(button_box)
    incompatible_dialog.setLayout(layout)

    ok_button.clicked.connect(incompatible_dialog.accept)
    cancel_button.clicked.connect(incompatible_dialog.reject)

    return incompatible_dialog.exec() == QDialog.Accepted


def _get_main_window():
    for widget in QApplication.topLevelWidgets():
        if hasattr(widget, "databases_tab"):
            return widget
    return None
