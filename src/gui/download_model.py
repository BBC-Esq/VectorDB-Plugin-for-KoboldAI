import threading

from PySide6.QtCore import QObject, Signal

from core.downloads import ModelDownloader


class ModelDownloadedSignal(QObject):
    downloaded = Signal(str, str)
    failed = Signal(str)

model_downloaded_signal = ModelDownloadedSignal()


def start_download(model_info, model_type):
    def worker():
        try:
            directory_name = ModelDownloader(model_info, model_type).download()
        except Exception as e:
            model_downloaded_signal.failed.emit(str(e))
        else:
            model_downloaded_signal.downloaded.emit(directory_name, model_type)

    threading.Thread(target=worker, daemon=True).start()
