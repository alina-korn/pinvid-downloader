import unittest
import os
import re
from unittest.mock import patch, MagicMock
import logging
from main import get_unique_filename, is_valid_pinterest_url, download_pinterest_video

class TestPinterestDownloader(unittest.TestCase):
    def setUp(self):
        """Подготовка перед каждым тестом."""
        # Настройка временной папки для тестов
        if not os.path.exists("download"):
            os.makedirs("download")
        # Настройка логирования для тестов
        logging.basicConfig(filename='test.log', level=logging.INFO)

    def tearDown(self):
        """Очистка после каждого теста."""
        # Удаление тестовых файлов и папки
        for file in os.listdir("download"):
            os.remove(os.path.join("download", file))
        os.rmdir("download")

    def test_get_unique_filename_existing_file(self):
        """Тест генерации уникального имени файла, если файл уже существует."""
        with open("download/test.mp4", "w") as f:
            f.write("test content")
        
        result = get_unique_filename("download/test.mp4")
        self.assertEqual(result, "download/test_1.mp4")
        os.remove("download/test.mp4")  # Удаляем тестовый файл

    def test_get_unique_filename_non_existing_file(self):
        """Тест генерации имени файла, если файла нет."""
        result = get_unique_filename("download/nonexistent.mp4")
        self.assertEqual(result, "download/nonexistent.mp4")

    def test_is_valid_pinterest_url_valid(self):
        """Тест валидации корректного Pinterest URL."""
        valid_urls = [
            "https://www.pinterest.com/pin/12345/",
            "http://pinterest.com/pin/test-video/",
            "https://www.pinterest.co.uk/pin/67890"
        ]
        for url in valid_urls:
            self.assertTrue(is_valid_pinterest_url(url))

    def test_is_valid_pinterest_url_invalid(self):
        """Тест валидации некорректного Pinterest URL."""
        invalid_urls = [
            "https://www.youtube.com/watch?v=123",
            "http://google.com",
            "not_a_url",
            ""
        ]
        for url in invalid_urls:
            self.assertFalse(is_valid_pinterest_url(url))

    @patch('main.YoutubeDL')  # Мокаем YoutubeDL, чтобы не делать реальные запросы
    def test_download_pinterest_video_success(self, mock_ydl):
        """Тест успешного скачивания видео (мок)."""
        # Настройка мока
        mock_instance = MagicMock()
        mock_instance.extract_info.return_value = {'title': 'test_video'}
        mock_ydl.return_value.__enter__.return_value = mock_instance

        # Вызов функции
        download_pinterest_video("https://www.pinterest.com/pin/12345/")
        
        # Проверка, что файл создан (в мок-режиме проверяем только вызовы)
        mock_instance.extract_info.assert_called_once_with("https://www.pinterest.com/pin/12345/", download=True)
        self.assertTrue(os.path.exists("download/test_video.mp4"))

    @patch('main.YoutubeDL')
    def test_download_pinterest_video_error(self, mock_ydl):
        """Тест обработки ошибки при скачивании (мок)."""
        # Настройка мока для выброса исключения
        mock_instance = MagicMock()
        mock_instance.extract_info.side_effect = Exception("Download failed")
        mock_ydl.return_value.__enter__.return_value = mock_instance

        # Вызов функции и проверка результата
        download_pinterest_video("https://www.pinterest.com/pin/12345/")
        # Здесь мы не можем проверить result_label напрямую, так как это GUI-элемент,
        # но можем проверить логи
        with open('test.log', 'r') as log_file:
            logs = log_file.read()
            self.assertIn("Ошибка при скачивании", logs)

if __name__ == '__main__':
    unittest.main()
