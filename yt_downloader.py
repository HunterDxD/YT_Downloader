import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from pytube import YouTube

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
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if not stream:
                QMessageBox.warning(self, 'Fehler', 'Kein passender Stream gefunden.')
                return
            save_path, _ = QFileDialog.getSaveFileName(self, 'Video speichern', f"{yt.title}.mp4", 'MP4 Files (*.mp4)')
            if save_path:
                stream.download(output_path=None, filename=save_path)
                QMessageBox.information(self, 'Erfolg', 'Download abgeschlossen!')
        except Exception as e:
            QMessageBox.critical(self, 'Fehler', f'Fehler beim Download: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YTDownloader()
    window.show()
    sys.exit(app.exec_())
