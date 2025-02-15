from yt_dlp import YoutubeDL

def download_pinterest_video(url):
    # Настройки для yt-dlp
    ydl_opts = {
        'format': 'best',  # Скачивает лучшее доступное качество
        'outtmpl': '%(title)s.%(ext)s',  # Имя файла будет взято из заголовка видео
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
        print("Скачивание завершено!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")