from yt_dlp import YoutubeDL
import os

def download_pinterest_video(url):
    # Путь к папке "download"
    download_folder = "download"

    # Создаем папку, если она не существует
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Настройки для yt-dlp
    ydl_opts = {
        'format': 'best',  # Скачивает лучшее доступное качество
        'outtmpl': f'{download_folder}/%(title)s.%(ext)s',  # Сохраняет в папку "download"
        'quiet': True,  # Отключает лишние сообщения в консоли
    }

    # Скачивание видео
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    # Введите URL видео с Pinterest
    url = input("Введите URL видео с Pinterest: ")

    # Скачивание видео
    try:
        print("Скачивание началось...")
        download_pinterest_video(url)
        print("Скачивание завершено! Видео сохранено в папку 'download'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")