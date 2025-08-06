import sys
import os
import yt_dlp
from PyQt5.QtCore import QObject, pyqtSignal

class Downloader(QObject):
    progress = pyqtSignal(int)
    progress_stats = pyqtSignal(int, str, str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, save_path, format_choice, ffmpeg_path):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.format_choice = format_choice
        self.ffmpeg_path = ffmpeg_path

    def yt_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total_bytes:
                downloaded_bytes = d.get('downloaded_bytes')
                speed = d.get('speed', 0)
                if downloaded_bytes is not None:
                    percent = downloaded_bytes / total_bytes * 100
                    speed_str = f"{speed / 1024 / 1024:.2f} MB/s" if speed else "N/A"
                    total_str = f"{total_bytes / 1024 / 1024:.2f} MB"
                    self.progress_stats.emit(int(percent), speed_str, total_str)
        elif d['status'] == 'finished':
            self.progress.emit(100)
        elif d['status'] == 'error':
            self.error.emit("Fehler beim Download.")

    def run(self):
        try:
            if self.format_choice == 0:
                format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                merge_output_format = 'mp4'
            elif self.format_choice == 1:
                format_str = 'bestvideo[ext=mp4]'
                merge_output_format = 'mp4'
            else:
                format_str = 'bestaudio[ext=m4a]/bestaudio'
                merge_output_format = 'mp3'

            ydl_opts = {
                'outtmpl': self.save_path,
                'format': format_str,
                'merge_output_format': merge_output_format,
                'quiet': True,
                'noplaylist': True,
                'progress_hooks': [self.yt_hook],
                'ffmpeg_location': self.ffmpeg_path,
                'postprocessors': []
            }
            if self.format_choice == 2:
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.finished.emit("Download abgeschlossen!")
        except Exception as e:
            self.error.emit(f'Fehler beim Download: {e}')
