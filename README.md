# YT_Downloader

**YT_Downloader** ist ein einfaches, grafisches Tool zum Herunterladen von YouTube-Videos und -Audios in bester Qualität. Es basiert auf Python, PyQt5 für die Benutzeroberfläche und [yt-dlp](https://github.com/yt-dlp/yt-dlp) für den eigentlichen Download.

---

## Funktionen

- **YouTube-Video-Download** als MP4 (mit oder ohne Ton) oder nur als MP3 (Audio).
- **Automatische Auswahl der besten verfügbaren Qualität**.
- **Fortschrittsbalken** während des Downloads.
- **Einfache Bedienung** über eine übersichtliche grafische Oberfläche.
- **Standalone-EXE** möglich (keine Python-Installation beim Nutzer nötig).

---

## Installation

### Voraussetzungen

- **Python 3.8 oder neuer** (nur für die Python-Version, nicht für die EXE)
- **pip** (Python-Paketmanager)
- **ffmpeg.exe** (für das Zusammenführen von Video und Audio, ist mitgeliefert)

### 1. Repository klonen

```bash
git clone https://github.com/dein-benutzername/YT_Downloader.git
cd YT_Downloader
pip install PyQt5 yt-dlp
```

### 2. Standalone-EXE erstellen

```bash
pip install pyinstaller
pyinstaller --add-binary "ffmpeg.exe;." --onedir --clean --windowed yt_downloader.py
```
