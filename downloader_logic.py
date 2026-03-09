import yt_dlp
import os
import glob
import shutil


def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%', '').strip()
        try:
            percent = float(p)
        except:
            percent = 0
        bar = '█' * int(30 * percent / 100) + '░' * (30 - int(30 * percent / 100))
        print(f"\r📥 Загрузка: |{bar}| {percent:.1f}%", end='')
    elif d['status'] == 'finished':
        print(f"\n✅ Файл скачан. Финализация...")


def process_downloads(use_file, file_path, base_path):
    base_path = os.path.abspath(base_path)
    all_songs_path = os.path.join(base_path, "All songs")
    covers_path = os.path.join(base_path, "Covers")

    for p in [all_songs_path, covers_path]:
        if not os.path.exists(p): os.makedirs(p)

    links = []
    if use_file:
        if not os.path.exists(file_path): return
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                url = line.strip()
                if url.lower().startswith("http"):
                    links.append(url)
    else:
        links = [input("Введите ссылку: ").strip()]

    print(f"✅ В очереди: {len(links)} задач.")

    for i, link in enumerate(links, 1):
        print(f"\n🚀 Задача {i} из {len(links)}")

        try:
            # Сначала получаем инфо
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                info = ydl.extract_info(link, download=False)

            is_album = 'entries' in info
            # Берем название и СРАЗУ убираем "Album - " если оно есть
            raw_title = info.get('title') or info.get('playlist_title') or f"Unknown_{i}"
            clean_title = raw_title.replace("Album - ", "").strip()
            # Оставляем только допустимые символы
            folder_name = "".join([c for c in clean_title if c.isalnum() or c in (' ', '-', '_')]).strip()

            if is_album:
                target_dir = os.path.join(base_path, folder_name)
                print(f"📂 Папка: {folder_name}")
            else:
                target_dir = all_songs_path
                print(f"🎵 Сингл в: All songs")

            if not os.path.exists(target_dir): os.makedirs(target_dir)

            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,  # Убирает большинство варнингов
                'noprogress': True,
                'progress_hooks': [progress_hook],
                'writethumbnail': True,
                'outtmpl': os.path.join(target_dir, '%(title)s.%(ext)s'),
                'postprocessors': [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                    {'key': 'FFmpegMetadata', 'add_metadata': True},
                    {'key': 'EmbedThumbnail'},
                ],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            # Перенос обложек в Covers
            for f in os.listdir(target_dir):
                if f.endswith(('.jpg', '.png', '.webp', '.jpeg')):
                    full_f = os.path.join(target_dir, f)
                    try:
                        shutil.move(full_f, os.path.join(covers_path, f))
                    except:
                        if os.path.exists(full_f): os.remove(full_f)

        except Exception as e:
            print(f"❌ Ошибка: {e}")

    print(f"\n✨ Всё готово!")