import sys
import os
import yt_dlp
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QComboBox, QGridLayout,
    QMainWindow, QStatusBar
)
from PyQt5.QtCore import QThread, pyqtSlot, Qt
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from downloader import Downloader


class YTDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube Video Downloader')
        self.setWindowIcon(self.create_icon("📥"))
        self.setGeometry(100, 100, 700, 250)

        self.set_stylesheet()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)

        self.label = QLabel('YouTube Link:')
        self.grid_layout.addWidget(self.label, 0, 0)

        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Geben Sie hier den YouTube-Link ein...")
        self.grid_layout.addWidget(self.link_input, 0, 1, 1, 2)

        self.format_label = QLabel("Format:")
        self.grid_layout.addWidget(self.format_label, 1, 0)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP4 + Audio", "MP4 (nur Video)", "MP3 (nur Audio)"])
        self.grid_layout.addWidget(self.format_combo, 1, 1)

        self.download_btn = QPushButton(' 📥 Herunterladen')
        self.download_btn.clicked.connect(self.start_download)
        self.grid_layout.addWidget(self.download_btn, 1, 2)

        self.progress = QProgressBar()
        self.grid_layout.addWidget(self.progress, 2, 0, 1, 3)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Bereit")

    def start_download(self):
        url = self.link_input.text().strip()
        if not url:
            QMessageBox.warning(self, 'Fehler', 'Bitte gib einen YouTube-Link ein.')
            return

        format_choice = self.format_combo.currentIndex()
        file_filter = 'MP4 Files (*.mp4)' if format_choice != 2 else 'MP3 Files (*.mp3)'
        default_filename = 'video.mp4' if format_choice != 2 else 'audio.mp3'

        save_path, _ = QFileDialog.getSaveFileName(self, 'Datei speichern', default_filename, file_filter)
        if not save_path:
            return

        if getattr(sys, 'frozen', False):
            ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
            if not os.path.exists(ffmpeg_path):
                ffmpeg_path = os.path.join(os.path.dirname(sys.executable), 'ffmpeg.exe')
        else:
            ffmpeg_path = os.path.abspath('ffmpeg.exe')

        self.download_btn.setEnabled(False)
        self.progress.setValue(0)
        self.status_bar.showMessage("Download wird gestartet...")

        self.thread = QThread()
        self.downloader = Downloader(url, save_path, format_choice, ffmpeg_path)
        self.downloader.moveToThread(self.thread)

        self.thread.started.connect(self.downloader.run)
        self.downloader.progress.connect(self.set_progress)
        self.downloader.progress_stats.connect(self.update_progress_stats)
        self.downloader.finished.connect(self.download_finished)
        self.downloader.error.connect(self.download_error)

        self.thread.start()

    @pyqtSlot(int)
    def set_progress(self, value):
        self.progress.setValue(value)

    @pyqtSlot(int, str, str)
    def update_progress_stats(self, percent, speed, total_size):
        self.progress.setValue(percent)
        self.status_bar.showMessage(f"Download läuft... {percent}% von {total_size} @ {speed}")

    @pyqtSlot(str)
    def download_finished(self, message):
        self.status_bar.showMessage(message)
        QMessageBox.information(self, 'Erfolg', message)
        self.cleanup_thread()

    @pyqtSlot(str)
    def download_error(self, message):
        self.status_bar.showMessage("Fehler")
        QMessageBox.critical(self, 'Fehler', message)
        self.cleanup_thread()

    def cleanup_thread(self):
        self.thread.quit()
        self.thread.wait()
        self.download_btn.setEnabled(True)
        self.progress.setValue(0)

    def create_icon(self, char):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        p = QPainter(pixmap)
        p.setPen(QColor(255, 255, 255))
        p.setFont(QFont("Arial", 24))
        p.drawText(pixmap.rect(), Qt.AlignCenter, char)
        p.end()
        return QIcon(pixmap)

    def set_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 14px;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #4f4f4f;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #4f4f4f;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #ffffff;
                selection-background-color: #5f5f5f;
            }
            QPushButton {
                background-color: #5f5f5f;
                color: #ffffff;
                border: 1px solid #4f4f4f;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #6f6f6f;
            }
            QPushButton:pressed {
                background-color: #4f4f4f;
            }
            QProgressBar {
                border: 1px solid #4f4f4f;
                border-radius: 5px;
                text-align: center;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 10px;
                margin: 0.5px;
            }
            QStatusBar {
                background-color: #2b2b2b;
                color: #ffffff;
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YTDownloader()
    window.show()
    sys.exit(app.exec_())
