import gc
from pathlib import Path
import yaml
from PySide6.QtCore import QAbstractListModel, QModelIndex, QRegularExpression, QThread, QTimer, Qt, Signal
from PySide6.QtGui import QAction, QRegularExpressionValidator, QIntValidator
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QListView, QMenu, QGroupBox, QLabel, QLineEdit, QGridLayout, QSizePolicy, QComboBox, QProgressDialog, QCheckBox

from gui.tabs_databases.choose_documents import choose_documents_directory, SymlinkWorker
from core.utilities import my_cprint, save_config_atomically
from core.databases import DatabaseBuild, check_preconditions_for_db_creation
from core.settings import build_chunking, chunk_overlap_for, set_chunk_size, set_embedding_model
from core.staging import DOCS_DIR, collect_files, remove_staged_file, staged_files
from core.downloads import is_vector_model_downloaded, model_directory, model_directory_name, vector_models
from gui.download_model import model_downloaded_signal
from gui.helpers import open_file, show_pdfs_need_ocr_dialog
from core.constants import MAX_CHUNK_SIZE, MIN_CHUNK_SIZE, TOOLTIPS, PROJECT_ROOT


class VectorDBWorker(QThread):
    """Runs DB creation in a completely separate Python interpreter via
    subprocess.Popen, with stdout drained inside the thread's run() and progress
    emitted via Qt signals.

    subprocess.Popen (as opposed to multiprocessing.Process) is critical on
    Windows with PySide6: multiprocessing's 'spawn' inherits DLL state from the
    GUI process (TileDB, CUDA, torch) which causes access violations
    (0xC0000005) in the child. See dev/production_integration_log.md (Phase 6).
    """

    progress = Signal(str)
    finished = Signal(bool, int, str)

    def __init__(self, database_name, parent=None):
        super().__init__(parent)
        self.build = DatabaseBuild(database_name)
        self.result = None

    def run(self):
        try:
            self.progress.emit("Initializing database creation...")
            self.result = self.build.run(self._on_line)
            self.finished.emit(self.result.success, self.result.exit_code, self.result.message)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.finished.emit(False, -1, f"Database creation failed: {e}")

    def _on_line(self, line):
        try:
            print(f"  [DB Creation] {line}", flush=True)
        except UnicodeEncodeError:
            print(f"  [DB Creation] {line}".encode("ascii", "replace").decode("ascii"), flush=True)
        self.progress.emit(line)

    def cancel(self):
        self.build.cancel()


class StagedFilesListView(QListView):
    files_dropped = Signal(list, list, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListView.DropOnly)

    @staticmethod
    def _collect(urls):
        selection = collect_files([url.toLocalFile() for url in urls if url.isLocalFile()])
        return selection.top_level, selection.nested, len(selection.unsupported)

    def _has_usable_payload(self, event):
        mime = event.mimeData()
        return bool(mime.hasUrls() and any(u.isLocalFile() for u in mime.urls()))

    def dragEnterEvent(self, event):
        if self._has_usable_payload(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self._has_usable_payload(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not self._has_usable_payload(event):
            event.ignore()
            return
        event.acceptProposedAction()
        top_level, subdirectory, skipped = self._collect(event.mimeData().urls())
        self.files_dropped.emit(top_level, subdirectory, skipped)


class StagedFilesModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._names = []

    def set_files(self, names):
        self.beginResetModel()
        self._names = names
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._names)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return self._names[index.row()]
        return None


class DatabasesTab(QWidget):
    CREATE_DB_BUTTON_LABEL = "Create Database"
    CREATE_DB_BUTTON_BUSY_LABEL = "Creating..."

    def __init__(self):
        super().__init__()
        self._staging_worker = None
        model_downloaded_signal.downloaded.connect(self.update_model_combobox)
        self.layout = QVBoxLayout(self)
        self.documents_group_box = self.create_group_box("Files To Add to Database", "Docs_for_DB")
        self.groups = {self.documents_group_box: 1}

        self.layout.addLayout(self._build_settings_row())

        grid_layout_top_buttons = QGridLayout()
        self.choose_docs_button = QPushButton("Choose Files")
        self.choose_docs_button.setToolTip(TOOLTIPS["CHOOSE_FILES"])
        self.choose_docs_button.clicked.connect(choose_documents_directory)
        self.model_combobox = QComboBox()
        self.model_combobox.setToolTip(TOOLTIPS["SELECT_VECTOR_MODEL"])
        self.populate_model_combobox()
        self.model_combobox.currentIndexChanged.connect(self.on_model_selected)
        self.model_combobox.activated.connect(self.refresh_model_combobox)
        self.create_db_button = QPushButton(self.CREATE_DB_BUTTON_LABEL)
        self.create_db_button.setToolTip(TOOLTIPS["CREATE_VECTOR_DB"])
        self.create_db_button.clicked.connect(self.on_create_db_clicked)
        self.create_db_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cancel_db_button = QPushButton("Cancel")
        self.cancel_db_button.setToolTip("Cancel an in-progress database creation and remove any partial files.")
        self.cancel_db_button.clicked.connect(self.on_cancel_db_clicked)
        self.cancel_db_button.setEnabled(False)
        create_cancel_box = QHBoxLayout()
        create_cancel_box.addWidget(self.create_db_button)
        create_cancel_box.addWidget(self.cancel_db_button)
        grid_layout_top_buttons.addWidget(self.choose_docs_button, 0, 0)
        grid_layout_top_buttons.addWidget(self.model_combobox, 0, 1)
        grid_layout_top_buttons.addLayout(create_cancel_box, 0, 2)
        number_of_columns = 3
        for column_index in range(number_of_columns):
            grid_layout_top_buttons.setColumnStretch(column_index, 1)
        hbox2 = QHBoxLayout()
        self.database_name_input = QLineEdit()
        self.database_name_input.setToolTip(TOOLTIPS["DATABASE_NAME_INPUT"])
        self.database_name_input.setPlaceholderText("Enter database name")
        self.database_name_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        regex = QRegularExpression("^[a-z0-9_-]*$")
        validator = QRegularExpressionValidator(regex, self.database_name_input)
        self.database_name_input.setValidator(validator)
        hbox2.addWidget(self.database_name_input)
        self.layout.addLayout(grid_layout_top_buttons)
        self.layout.addLayout(hbox2)
        self.sync_combobox_with_config()
        
        self.db_worker = None
        self.current_model_name = None
        self.current_database_name = None

        self._docs_count_mtime = None
        self._docs_count_cache = 0
        self._config_mtime = None
        self._config_cache = {}
        self._refresh_info_label()
        self._update_precision_label()
        self.info_refresh_timer = QTimer(self)
        self.info_refresh_timer.setInterval(1000)
        self.info_refresh_timer.timeout.connect(self._refresh_info_label)
        self.info_refresh_timer.start()

    def _build_settings_row(self):
        db_cfg = self._read_config().get("database") or {}
        compute = self._read_config().get("Compute_Device") or {}

        row = QHBoxLayout()

        row.addWidget(QLabel("Device:"))
        self.device_combo = QComboBox()
        available = compute.get("available") or ["cpu"]
        self.device_combo.addItems(available)
        current_device = compute.get("database_creation", "cpu")
        if current_device in available:
            self.device_combo.setCurrentIndex(available.index(current_device))
        self.device_combo.setToolTip(TOOLTIPS.get("CREATE_DEVICE_DB", "Device used to create the database."))
        self.device_combo.currentIndexChanged.connect(self._on_device_changed)
        row.addWidget(self.device_combo)
        row.addSpacing(12)

        chunk_size, chunk_overlap = build_chunking()
        row.addWidget(QLabel("Chunk Size:"))
        self.chunk_size_edit = QLineEdit(str(chunk_size))
        self.chunk_size_edit.setValidator(QIntValidator(MIN_CHUNK_SIZE, MAX_CHUNK_SIZE, self))
        self.chunk_size_edit.setToolTip(TOOLTIPS["CHUNK_SIZE"])
        self.chunk_size_edit.setMaximumWidth(90)
        self.chunk_size_edit.textEdited.connect(self._on_chunk_text_edited)
        row.addWidget(self.chunk_size_edit)
        row.addSpacing(12)

        row.addWidget(QLabel("Overlap:"))
        self.chunk_overlap_edit = QLineEdit(str(chunk_overlap))
        self.chunk_overlap_edit.setReadOnly(True)
        self.chunk_overlap_edit.setToolTip("Always half the chunk size, rounded up.")
        self.chunk_overlap_edit.setMaximumWidth(90)
        row.addWidget(self.chunk_overlap_edit)
        row.addSpacing(12)

        self.half_checkbox = QCheckBox("Half-Precision")
        self.half_checkbox.setChecked(bool(db_cfg.get("half", False)))
        self.half_checkbox.setToolTip(TOOLTIPS["HALF_PRECISION"])
        self.half_checkbox.toggled.connect(self._on_half_toggled)
        row.addWidget(self.half_checkbox)

        self.precision_label = QLabel()
        self.precision_label.setTextFormat(Qt.RichText)
        row.addWidget(self.precision_label)

        row.addStretch(1)

        self._chunk_debounce = QTimer(self)
        self._chunk_debounce.setSingleShot(True)
        self._chunk_debounce.setInterval(800)
        self._chunk_debounce.timeout.connect(self._commit_chunk_settings)

        self._half_cooldown = QTimer(self)
        self._half_cooldown.setSingleShot(True)
        self._half_cooldown.setInterval(600)
        self._half_cooldown.timeout.connect(lambda: self.half_checkbox.setEnabled(True))

        return row

    @staticmethod
    def _read_config():
        config_path = PROJECT_ROOT / "config.yaml"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}

    def _write_config(self, mutate):
        config = self._read_config()
        mutate(config)
        save_config_atomically(config, PROJECT_ROOT / "config.yaml")
        self._config_mtime = None

    def _on_device_changed(self):
        device = self.device_combo.currentText()

        def mutate(config):
            config.setdefault("Compute_Device", {})["database_creation"] = device

        self._write_config(mutate)
        self._update_precision_label()

    def _on_chunk_text_edited(self):
        self._chunk_debounce.start()

    def _mark_invalid(self, widget, invalid):
        widget.setStyleSheet("border: 1px solid #c0392b;" if invalid else "")

    def _commit_chunk_settings(self):
        size_text = self.chunk_size_edit.text().strip()
        if not size_text:
            return

        size = int(size_text)
        invalid = not MIN_CHUNK_SIZE <= size <= MAX_CHUNK_SIZE
        self._mark_invalid(self.chunk_size_edit, invalid)
        if invalid:
            return

        overlap = chunk_overlap_for(size)
        self.chunk_overlap_edit.setText(str(overlap))
        current = self._read_config().get("database") or {}
        if current.get("chunk_size") == size and current.get("chunk_overlap") == overlap:
            return

        set_chunk_size(size)
        self._config_mtime = None

    def _on_half_toggled(self, checked):
        self.half_checkbox.setEnabled(False)

        def mutate(config):
            config.setdefault("database", {})["half"] = bool(checked)

        self._write_config(mutate)
        self._update_precision_label()
        self._half_cooldown.start()

    def _update_precision_label(self):
        config = self._read_config()
        precision = self._compute_precision_str(config, self.half_checkbox.isChecked())
        self.precision_label.setText(f"<b>Precision:</b> {precision}")

    def _validation_failed(self, message: str):
        QMessageBox.warning(self, "Validation Failed", message)
        self.reenable_create_db_button()

    def refresh_model_combobox(self, index):
        current_text = self.model_combobox.currentText()
        self.populate_model_combobox()
        idx = self.model_combobox.findText(current_text)
        if idx >= 0:
            self.model_combobox.setCurrentIndex(idx)

    def update_model_combobox(self, model_name, model_type):
        if model_type == "vector":
            self.populate_model_combobox()
            self.sync_combobox_with_config()

    def populate_model_combobox(self):
        self.model_combobox.blockSignals(True)
        try:
            self.model_combobox.clear()
            self.model_combobox.addItem("Select a model", None)
            for model in vector_models():
                if is_vector_model_downloaded(model):
                    self.model_combobox.addItem(model_directory_name(model), str(model_directory(model)))
        finally:
            self.model_combobox.blockSignals(False)

    def sync_combobox_with_config(self):
        config_path = PROJECT_ROOT / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file) or {}
            current_model = config_data.get("EMBEDDING_MODEL_NAME")
            if current_model:
                model_index = self.model_combobox.findData(current_model)
                if model_index != -1:
                    self.model_combobox.setCurrentIndex(model_index)
                else:
                    self.model_combobox.setCurrentIndex(0)
            else:
                self.model_combobox.setCurrentIndex(0)
        else:
            self.model_combobox.setCurrentIndex(0)

    def on_model_selected(self, index):
        set_embedding_model(self.model_combobox.itemData(index))

    def create_group_box(self, title, directory_name):
        group_box = QGroupBox(title)
        layout = QVBoxLayout()
        tree_view = self.setup_directory_view(directory_name)
        layout.addWidget(tree_view)
        group_box.setLayout(layout)
        self.layout.addWidget(group_box)
        group_box.toggled.connect(lambda checked, gb=group_box: self.toggle_group_box(gb, checked))
        return group_box

    @staticmethod
    def _scan_docs(docs_dir):
        return staged_files(docs_dir)

    def _refresh_info_label(self):
        script_dir = PROJECT_ROOT
        docs_dir = script_dir / "Docs_for_DB"

        try:
            docs_mtime = docs_dir.stat().st_mtime if docs_dir.exists() else None
        except OSError:
            docs_mtime = None
        if docs_mtime != self._docs_count_mtime:
            self._docs_count_mtime = docs_mtime
            names = self._scan_docs(docs_dir) if docs_mtime is not None else []
            self._docs_count_cache = len(names)
            if getattr(self, "docs_list_model", None) is not None:
                self.docs_list_model.set_files(names)
        file_count = self._docs_count_cache

        config_path = script_dir / "config.yaml"
        try:
            config_mtime = config_path.stat().st_mtime if config_path.exists() else None
        except OSError:
            config_mtime = None
        if config_mtime != self._config_mtime:
            self._config_mtime = config_mtime
            config = {}
            if config_mtime is not None:
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        config = yaml.safe_load(f) or {}
                except Exception:
                    config = {}
            self._config_cache = config
        config = self._config_cache

        if getattr(self, "documents_group_box", None) is not None:
            suffix = "1 file" if file_count == 1 else f"{file_count} files"
            self.documents_group_box.setTitle(f"Files To Add to Database  —  {suffix}")

    def refresh_staged_files(self):
        self._docs_count_mtime = object()
        self._refresh_info_label()

    def _compute_precision_str(self, config, use_half):
        from core.constants import VECTOR_MODELS

        model_path = config.get("EMBEDDING_MODEL_NAME")
        if not model_path:
            return "—"

        cache_dir_name = Path(model_path).name
        native_precision = None
        for vendor_models in VECTOR_MODELS.values():
            for model_info in vendor_models:
                if model_info.get("cache_dir") == cache_dir_name:
                    native_precision = model_info.get("precision", "float32")
                    break
            if native_precision:
                break

        if not native_precision:
            return "unknown"

        try:
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
        except Exception:
            device = "cpu"

        try:
            from core.utilities import get_appropriate_dtype
            dtype = get_appropriate_dtype(device, use_half, native_precision)
            return str(dtype).split(".")[-1]
        except Exception:
            return native_precision

    def setup_directory_view(self, directory_name):
        list_view = StagedFilesListView()
        model = StagedFilesModel(self)
        list_view.setModel(model)
        list_view.setSelectionMode(QListView.ExtendedSelection)
        list_view.setUniformItemSizes(True)
        list_view.setEditTriggers(QListView.NoEditTriggers)
        list_view.doubleClicked.connect(self.on_double_click)
        list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        list_view.customContextMenuRequested.connect(self.on_context_menu)
        if directory_name == "Docs_for_DB":
            self.docs_list_model = model
            self.docs_list_view = list_view
            list_view.setToolTip("Drag and drop files or folders here to add them to the database.")
            list_view.files_dropped.connect(self.on_files_dropped)
        return list_view

    def on_files_dropped(self, top_level, subdirectory, skipped):
        if self._staging_worker is not None and self._staging_worker.isRunning():
            QMessageBox.information(
                self, "Staging In Progress",
                "Files are still being staged. Wait for the current job to finish before adding more."
            )
            return

        files = list(top_level)
        if subdirectory:
            reply = QMessageBox.question(
                self, "Include Subdirectories?",
                f"{len(top_level)} compatible file(s) were found at the top level and "
                f"{len(subdirectory)} more in subdirectories.\n\nInclude the subdirectory files as well?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                files.extend(subdirectory)

        if not files:
            QMessageBox.information(
                self, "Nothing Added",
                "None of the dropped items are supported file types."
                + (f"\n\n{skipped} file(s) were skipped." if skipped else "")
            )
            return

        target_dir = DOCS_DIR
        target_dir.mkdir(parents=True, exist_ok=True)

        progress = QProgressDialog("Adding files...", "Cancel", 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)

        worker = SymlinkWorker(files, target_dir)
        self._staging_worker = worker
        progress.canceled.connect(worker.requestInterruption)

        def update_progress(pct):
            if progress.maximum() == 0:
                progress.setRange(0, 100)
            progress.setValue(pct)

        def done(count, errors):
            progress.reset()
            self.refresh_staged_files()
            self._staging_worker = None
            msg = f"Added {count} file(s)."
            if skipped:
                msg += f"\n{skipped} unsupported file(s) were skipped."
            if errors:
                msg += f"\n{len(errors)} error(s) - see console."
                print(*errors, sep="\n")
            QMessageBox.information(self, "Files Added", msg)

        worker.progress.connect(update_progress)
        worker.finished.connect(done)
        worker.start()

    def on_double_click(self, index):
        name = index.data(Qt.DisplayRole)
        if name:
            open_file(str(DOCS_DIR / name))

    def on_context_menu(self, point):
        list_view = self.sender()
        context_menu = QMenu(self)
        delete_action = QAction("Delete File", self)
        context_menu.addAction(delete_action)
        delete_action.triggered.connect(lambda: self.on_delete_file(list_view))
        context_menu.exec_(list_view.viewport().mapToGlobal(point))

    def on_delete_file(self, list_view):
        names = [idx.data(Qt.DisplayRole) for idx in list_view.selectedIndexes()]
        failed = [name for name in names if name and not remove_staged_file(name)]
        self.refresh_staged_files()
        if failed:
            QMessageBox.warning(self, "Delete File", "Unable to delete file(s), please delete manually.")

    def on_create_db_clicked(self):
        if self.model_combobox.currentIndex() == 0:
            QMessageBox.warning(self, "No Model Selected", "Please select a model before creating a database.")
            return

        database_name = self.database_name_input.text().strip()
        if not database_name:
            QMessageBox.warning(self, "Database Name Required", "Please enter a database name before creating a database.")
            return

        docs_dir = PROJECT_ROOT / "Docs_for_DB"
        if not docs_dir.exists() or not any(p for p in docs_dir.iterdir() if p.is_file()):
            QMessageBox.warning(
                self,
                "No Files To Add",
                "The Docs_for_DB folder is empty. Add at least one file before creating a database."
            )
            return

        self.create_db_button.setDisabled(True)
        self.create_db_button.setText(self.CREATE_DB_BUTTON_BUSY_LABEL)
        self.choose_docs_button.setDisabled(True)
        self.model_combobox.setDisabled(True)
        self.database_name_input.setDisabled(True)
        self.cancel_db_button.setEnabled(True)

        model_name = self.model_combobox.currentText()

        self.current_database_name = database_name
        self.current_model_name = model_name

        docs_dir = PROJECT_ROOT / "Docs_for_DB"
        has_pdfs = any(p.suffix.lower() == ".pdf" for p in docs_dir.iterdir() if p.is_file())
        skip_ocr = False
        if has_pdfs:
            reply = QMessageBox.question(self, "OCR Check",
                                         "PDF files detected. Do you want to check if any of the PDFs need OCR? "
                                         "If there are a lot of PDFs, it is time-consuming but strongly recommended.",
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)
            skip_ocr = (reply == QMessageBox.No)

        self.start_database_creation(database_name, model_name, skip_ocr)

    def start_database_creation(self, database_name, model_name, skip_ocr):
        try:
            script_dir = PROJECT_ROOT
            ok, msg, non_ocr_pdfs = check_preconditions_for_db_creation(script_dir, database_name, skip_ocr=skip_ocr)
            if not ok:
                if non_ocr_pdfs:
                    show_pdfs_need_ocr_dialog(non_ocr_pdfs)
                self._validation_failed(msg)
                return

            self.db_worker = VectorDBWorker(database_name, parent=self)
            self.db_worker.finished.connect(self.on_worker_finished)
            self.db_worker.start()

            my_cprint(f"Started database creation for: {database_name}", "green")

        except Exception as e:
            self._validation_failed(f"Failed to start database creation: {str(e)}")

    def on_cancel_db_clicked(self):
        if self.db_worker is None or not self.db_worker.isRunning():
            return
        self.cancel_db_button.setEnabled(False)
        self.cancel_db_button.setText("Cancelling...")
        self.db_worker.cancel()

    def on_worker_finished(self, success: bool, exit_code: int, message: str):
        result = self.db_worker.result if self.db_worker is not None else None
        try:
            if success:
                my_cprint(f"{self.current_model_name} removed from memory.", "red")
                if result is not None and result.not_added:
                    shown = "\n".join(result.not_added[:20])
                    more = len(result.not_added) - 20
                    message += (f"\n\n{len(result.not_added)} file(s) were not fully added:\n{shown}"
                                + (f"\n...and {more} more" if more > 0 else ""))
                QMessageBox.information(self, "Success", message)
            elif result is not None and result.cancelled:
                QMessageBox.information(self, "Cancelled", message)
            else:
                QMessageBox.critical(self, "Error", message)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error handling completion: {e}")
        finally:
            if self.db_worker is not None:
                self.db_worker.deleteLater()
                self.db_worker = None
            self.reenable_create_db_button()

    def reenable_create_db_button(self):
        self.create_db_button.setDisabled(False)
        self.create_db_button.setText(self.CREATE_DB_BUTTON_LABEL)
        self.choose_docs_button.setDisabled(False)
        self.model_combobox.setDisabled(False)
        self.database_name_input.setDisabled(False)
        self.cancel_db_button.setEnabled(False)
        self.cancel_db_button.setText("Cancel")
        
        self.current_database_name = None
        self.current_model_name = None
        
        gc.collect()

    def cleanup(self):
        if self.db_worker is not None and self.db_worker.isRunning():
            self.db_worker.cancel()
            self.db_worker.wait(5000)

    def toggle_group_box(self, group_box, checked):
        self.groups[group_box] = 1 if checked else 0
        self.adjust_stretch()

    def adjust_stretch(self):
        for group, stretch in self.groups.items():
            self.layout.setStretchFactor(group, stretch if group.isChecked() else 0)
