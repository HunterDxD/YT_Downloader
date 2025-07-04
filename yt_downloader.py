import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
import yt_dlp

class YTDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube Video Downloader')
        self.setGeometry(100, 100, 400, 150)
        layout = QVBoxLayout()

        self.label = QLabel('YouTube Link:')
        layout.addWidget(self.label)

        self.link_input = QLineEdit()
        layout.addWidget(self.link_input)

        self.download_btn = QPushButton('Video herunterladen')
        self.download_btn.clicked.connect(self.download_video)
        layout.addWidget(self.download_btn)

        self.setLayout(layout)

    def download_video(self):
        url = self.link_input.text().strip()
        if not url:
            QMessageBox.warning(self, 'Fehler', 'Bitte gib einen YouTube-Link ein.')
            return
        try:
            save_path, _ = QFileDialog.getSaveFileName(self, 'Video speichern', 'video.mp4', 'MP4 Files (*.mp4)')
            if not save_path:
                return

            # Pfad zur ffmpeg.exe bestimmen (funktioniert auch als EXE)
            if getattr(sys, 'frozen', False):
                # Wenn als EXE gebündelt
                ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
                if not os.path.exists(ffmpeg_path):
                    # Falls ffmpeg.exe im selben Ordner wie die EXE liegt
                    ffmpeg_path = os.path.join(os.path.dirname(sys.executable), 'ffmpeg.exe')
            else:
                # Im Entwicklermodus (Python-Skript)
                ffmpeg_path = os.path.abspath('ffmpeg.exe')

            ydl_opts = {
                'outtmpl': save_path,
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'quiet': True,
                'noplaylist': True,
                'progress_hooks': [self.yt_hook],
                'ffmpeg_location': ffmpeg_path
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            QMessageBox.information(self, 'Erfolg', 'Download abgeschlossen!')
        except Exception as e:
            QMessageBox.critical(self, 'Fehler', f'Fehler beim Download: {e}')

    def yt_hook(self, d):
        if d['status'] == 'error':
            QMessageBox.critical(self, 'Fehler', 'Fehler beim Download.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YTDownloader()
    window.show()
    sys.exit(app.exec_())
