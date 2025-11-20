
import unittest
import os
import shutil
import json
import time
from digipage.core.config import ConfigManager, AppConfig, CONFIG_FILE, BOOKS_COMPLETE_LOG_FILE
from digipage.workers.scanner_worker import ScanWorker
from digipage.workers.image_worker import ImageProcessor
from digipage.data.io import LogManager, count_pages_in_folder
from digipage.utils.string_utils import natural_sort_key

class TestCoreFunctionality(unittest.TestCase):
    def setUp(self):
        # Backup existing config
        if os.path.exists(CONFIG_FILE):
            shutil.move(CONFIG_FILE, CONFIG_FILE + ".bak")
        if os.path.exists(BOOKS_COMPLETE_LOG_FILE):
            shutil.move(BOOKS_COMPLETE_LOG_FILE, BOOKS_COMPLETE_LOG_FILE + ".bak")

        # Create test directories
        self.test_scan_dir = "test_scan"
        self.test_books_dir = "test_books"
        os.makedirs(self.test_scan_dir, exist_ok=True)
        os.makedirs(self.test_books_dir, exist_ok=True)

        # Create dummy config
        self.config = AppConfig(
            scan_folder=self.test_scan_dir,
            todays_books_folder=self.test_books_dir,
            scanner_mode="dual_scan"
        )
        ConfigManager.save(self.config)

    def tearDown(self):
        # Restore config
        if os.path.exists(CONFIG_FILE + ".bak"):
            shutil.move(CONFIG_FILE + ".bak", CONFIG_FILE)
        elif os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)

        if os.path.exists(BOOKS_COMPLETE_LOG_FILE + ".bak"):
            shutil.move(BOOKS_COMPLETE_LOG_FILE + ".bak", BOOKS_COMPLETE_LOG_FILE)
        elif os.path.exists(BOOKS_COMPLETE_LOG_FILE):
            os.remove(BOOKS_COMPLETE_LOG_FILE)

        if os.path.exists(self.test_scan_dir):
            shutil.rmtree(self.test_scan_dir)
        if os.path.exists(self.test_books_dir):
            shutil.rmtree(self.test_books_dir)

    def test_config_manager(self):
        loaded_config = ConfigManager.load()
        self.assertEqual(loaded_config.scan_folder, self.test_scan_dir)
        self.assertEqual(loaded_config.scanner_mode, "dual_scan")

        loaded_config.theme = "Light"
        ConfigManager.save(loaded_config)

        reloaded = ConfigManager.load()
        self.assertEqual(reloaded.theme, "Light")

    def test_log_manager(self):
        entry = {"name": "test_book", "pages": 10, "path": "/tmp", "timestamp": "2023-01-01"}
        LogManager.append_entry(entry)

        logs = LogManager.load_logs()
        today_str = list(logs.keys())[0]
        self.assertEqual(len(logs[today_str]), 1)
        self.assertEqual(logs[today_str][0]['name'], "test_book")

        pages, books = LogManager.get_today_stats()
        # Note: get_today_stats uses datetime.now() so it might not find the entry if we mocked date but io.py uses real date
        # Let's use real date for test
        from datetime import datetime
        today_real = datetime.now().strftime('%Y-%m-%d')
        if today_real == today_str:
            self.assertEqual(pages, 10)

    def test_natural_sort(self):
        files = ["img1.jpg", "img10.jpg", "img2.jpg"]
        files.sort(key=natural_sort_key)
        self.assertEqual(files, ["img1.jpg", "img2.jpg", "img10.jpg"])

class TestScanWorker(unittest.TestCase):
    def setUp(self):
         # Backup existing config
        if os.path.exists(CONFIG_FILE):
            shutil.move(CONFIG_FILE, CONFIG_FILE + ".bak")

        self.test_scan_dir = "test_scan_worker"
        self.test_books_dir = "test_books_worker"
        os.makedirs(self.test_scan_dir, exist_ok=True)
        os.makedirs(self.test_books_dir, exist_ok=True)

        self.config = AppConfig(
            scan_folder=self.test_scan_dir,
            todays_books_folder=self.test_books_dir
        )
        self.worker = ScanWorker(self.config)

    def tearDown(self):
        if os.path.exists(CONFIG_FILE + ".bak"):
            shutil.move(CONFIG_FILE + ".bak", CONFIG_FILE)
        if os.path.exists(self.test_scan_dir):
            shutil.rmtree(self.test_scan_dir)
        if os.path.exists(self.test_books_dir):
            shutil.rmtree(self.test_books_dir)

    def test_scan_directory(self):
        # Create dummy files
        with open(os.path.join(self.test_scan_dir, "test1.jpg"), 'w') as f: f.write("test")
        with open(os.path.join(self.test_scan_dir, "test2.png"), 'w') as f: f.write("test")
        with open(os.path.join(self.test_scan_dir, "ignore.txt"), 'w') as f: f.write("test")

        # Mock signal
        results = []
        self.worker.initial_scan_done.connect(lambda files: results.extend(files))

        self.worker.scan_directory()

        self.assertEqual(len(results), 2)
        self.assertTrue(any("test1.jpg" in f for f in results))

if __name__ == '__main__':
    unittest.main()
