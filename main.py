import os
import subprocess
from downloader_logic import process_downloads

# --- НАСТРОЙКИ ПРОГРАММЫ ---
# USE_FILE_BY_DEFAULT:
#   True  - берет ссылки из файла links.txt
#   False - запрашивает ссылку в окне терминала
USE_FILE_BY_DEFAULT = False

# DOWNLOAD_DIR: куда сохранять музыку.
# По умолчанию: папка "Загрузки", подпапка "YouTubeMusic"
DOWNLOAD_DIR = os.path.expanduser("~/Downloads/YouTubeMusic")

# LINKS_FILENAME: имя файла со ссылками.
# Файл должен лежать в той же папке, что и этот скрипт.
LINKS_FILENAME = "links.txt"


# ---------------------------

def start():
    print("=== 🎵 YouTube Music Downloader Started ===")

    # Запускаем загрузку с нашими настройками
    process_downloads(
        use_file=USE_FILE_BY_DEFAULT,
        file_path=LINKS_FILENAME,
        base_path=DOWNLOAD_DIR
    )

    print(f"\n✨ Всё готово! Музыка сохранена в: {DOWNLOAD_DIR}")

    # Открываем папку с результатом в Finder (только для Mac)
    if os.path.exists(DOWNLOAD_DIR):
        subprocess.call(['open', DOWNLOAD_DIR])


if __name__ == "__main__":
    start()