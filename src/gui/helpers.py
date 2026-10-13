import os
import platform
import subprocess
import tempfile
import threading

from PySide6.QtWidgets import QMessageBox


def open_file(file_path):
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", file_path])
        else:
            subprocess.Popen(["xdg-open", file_path])
    except OSError:
        QMessageBox.warning(None, "Error", "No default viewer detected.")


def show_pdfs_need_ocr_dialog(non_ocr_pdfs):
    message = "The following PDF files appear to have no text content and likelyk need OCR done on them:\n\n"
    for pdf_path in non_ocr_pdfs:
        message += f"  - {pdf_path}\n"
    message += "\nPlease perform OCR on these by going to the Tools Tab first or remove them from the files selected for processing."

    msg_box = QMessageBox()
    msg_box.setWindowTitle("PDFs Need OCR")
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Icon.Warning)

    msg_box.addButton(QMessageBox.StandardButton.Ok)
    view_report_button = msg_box.addButton("View Report", QMessageBox.ButtonRole.ActionRole)

    msg_box.exec()

    if msg_box.clickedButton() == view_report_button:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write("PDFs that need OCR:\n\n")
            for pdf_path in non_ocr_pdfs:
                temp_file.write(f"{pdf_path}\n")
            temp_path = temp_file.name

        os.startfile(temp_path)

        def cleanup_temp_file():
            try:
                os.unlink(temp_path)
            except OSError:
                pass

        threading.Timer(1.0, cleanup_temp_file).start()
