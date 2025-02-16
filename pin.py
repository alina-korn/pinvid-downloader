from yt_dlp import YoutubeDL
import os

def get_unique_filename(filename):
    """Если файл уже существует, добавляет номер в конец имени файла."""
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    return filename

def download_pinterest_video(url, download_folder="download"):
    """Скачивает видео с Pinterest по переданному URL."""
    # Создаем папку, если она не существует
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Настройки для yt-dlp
    ydl_opts = {
        'format': 'mp4',  # Скачивает видео в MP4
        'outtmpl': f'{download_folder}/%(title)s.%(ext)s',  # Шаблон имени файла
        'quiet': True,  # Отключает лишние сообщения в консоли
    }

    # Скачивание видео
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)  # Получаем информацию о видео и скачиваем
            video_title = info_dict.get('title', 'video')  # Название видео
            filename = f"{download_folder}/{video_title}.mp4"
            unique_filename = get_unique_filename(filename)  # Проверяем уникальность имени файла

            # Если имя изменилось, переименовываем файл
            if filename != unique_filename and os.path.exists(filename):
                os.rename(filename, unique_filename)

            print(f"✅ Скачано: {video_title}")
        except Exception as e:
            print(f"❌ Ошибка при скачивании {url}: {e}")

if __name__ == "__main__":
    # Ввод URL (можно несколько через запятую)
    urls_input = input("Введите URL видео с Pinterest (через запятую для нескольких): ")
    urls = [url.strip() for url in urls_input.split(',')]

    print("📥 Начало скачивания...")
    
    for url in urls:
        download_pinterest_video(url)

    print("✅ Все видео загружены! Смотрите в папке 'download'.")





