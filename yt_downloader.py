import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QComboBox, QHBoxLayout
)
import yt_dlp

class YTDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube Video Downloader')
        self.setGeometry(100, 100, 700, 200)
        layout = QVBoxLayout()

        self.label = QLabel('YouTube Link:')
        layout.addWidget(self.label)

        self.link_input = QLineEdit()
        layout.addWidget(self.link_input)

        # Format-Auswahl
        format_layout = QHBoxLayout()
        format_label = QLabel("Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp4 mit Ton (Standard)", "nur mp4 (nur Video)", "nur mp3 (nur Audio)"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        layout.addLayout(format_layout)

        self.download_btn = QPushButton('Datei herunterladen')
        self.download_btn.clicked.connect(self.download_video)
        layout.addWidget(self.download_btn)

        # Fortschrittsbalken
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.setLayout(layout)

    def download_video(self):
        url = self.link_input.text().strip()
        if not url:
            QMessageBox.warning(self, 'Fehler', 'Bitte gib einen YouTube-Link ein.')
            return
        save_path, _ = QFileDialog.getSaveFileName(self, 'Datei speichern', 'video.mp4', 'MP4 Files (*.mp4);;MP3 Files (*.mp3)')
        if not save_path:
            return

        # ffmpeg-Pfad wie gehabt bestimmen
        if getattr(sys, 'frozen', False):
            ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
            if not os.path.exists(ffmpeg_path):
                ffmpeg_path = os.path.join(os.path.dirname(sys.executable), 'ffmpeg.exe')
        else:
            ffmpeg_path = os.path.abspath('ffmpeg.exe')

        # Format-Auswahl
        format_choice = self.format_combo.currentIndex()
        if format_choice == 0:  # mp4 mit Ton (Standard)
            format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            merge_output_format = 'mp4'
        elif format_choice == 1:  # nur mp4 (nur Video)
            format_str = 'bestvideo[ext=mp4]'
            merge_output_format = 'mp4'
        else:  # nur mp3 (nur Audio)
            format_str = 'bestaudio[ext=m4a]/bestaudio'
            merge_output_format = 'mp3'

        ydl_opts = {
            'outtmpl': save_path,
            'format': format_str,
            'merge_output_format': merge_output_format,
            'quiet': True,
            'noplaylist': True,
            'progress_hooks': [self.yt_hook],
            'ffmpeg_location': ffmpeg_path,
            'postprocessors': []
        }
        if format_choice == 2:  # mp3
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })

        self.progress.setValue(0)
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            QMessageBox.information(self, 'Erfolg', 'Download abgeschlossen!')
        except Exception as e:
            QMessageBox.critical(self, 'Fehler', f'Fehler beim Download: {e}')

    def yt_hook(self, d):
        if d['status'] == 'downloading':
            if d.get('total_bytes'):
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                self.progress.setValue(int(percent))
            elif d.get('total_bytes_estimate'):
                percent = d['downloaded_bytes'] / d['total_bytes_estimate'] * 100
                self.progress.setValue(int(percent))
        elif d['status'] == 'finished':
            self.progress.setValue(100)
        elif d['status'] == 'error':
            QMessageBox.critical(self, 'Fehler', 'Fehler beim Download.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YTDownloader()
    window.show()
    sys.exit(app.exec_())
