"""主程式單元測試。"""

import logging
import unittest

from tw_stock_tools.logger import setup_logger
from tw_stock_tools.main import main


class TestSetupLogger(unittest.TestCase):
    """測試 logger 設定。"""

    def test_setup_logger_returns_logger(self):
        """測試 setup_logger 回傳 Logger 實例。"""
        logger = setup_logger(name="test_logger")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "test_logger")

    def test_setup_logger_has_handlers(self):
        """測試 logger 包含 console 與 file handler。"""
        logger = setup_logger(name="test_handler_logger")
        handler_types = [type(h) for h in logger.handlers]
        self.assertIn(logging.StreamHandler, handler_types)
        self.assertIn(logging.FileHandler, handler_types)

    def test_setup_logger_no_duplicate_handlers(self):
        """測試重複呼叫不會新增多餘的 handler。"""
        logger = setup_logger(name="test_dup_logger")
        handler_count = len(logger.handlers)
        setup_logger(name="test_dup_logger")
        self.assertEqual(len(logger.handlers), handler_count)


class TestMain(unittest.TestCase):
    """測試主程式。"""

    def test_main_runs_without_error(self):
        """測試 main() 可正常執行。"""
        try:
            main()
        except Exception as e:
            self.fail(f"main() 拋出例外: {e}")


if __name__ == "__main__":
    unittest.main()
