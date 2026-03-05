"""API 單元測試。"""

import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from tw_stock_tools.web.app import app


class TestToolsAPI(unittest.TestCase):
    """測試工具 API。"""

    def setUp(self):
        """建立測試用 HTTP client。"""
        self.client = TestClient(app)

    def test_get_tools_returns_200(self):
        """測試 GET /api/tools 回傳 200。"""
        response = self.client.get("/api/tools")
        self.assertEqual(response.status_code, 200)

    def test_get_tools_returns_list(self):
        """測試 GET /api/tools 回傳清單。"""
        response = self.client.get("/api/tools")
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_tools_contains_expected_fields(self):
        """測試每個工具包含必要欄位。"""
        response = self.client.get("/api/tools")
        data = response.json()
        if len(data) > 0:
            tool = data[0]
            for field in ("id", "name", "description", "icon", "route"):
                self.assertIn(field, tool)

    def test_tools_count(self):
        """測試工具清單包含 4 個工具。"""
        response = self.client.get("/api/tools")
        data = response.json()
        self.assertEqual(len(data), 4)

    def test_trading_schedule_in_tools(self):
        """測試 trading-schedule 工具存在於清單中。"""
        response = self.client.get("/api/tools")
        data = response.json()
        tool_ids = [t["id"] for t in data]
        self.assertIn("trading-schedule", tool_ids)

    def test_knowledge_in_tools(self):
        """測試 knowledge 工具存在於清單中。"""
        response = self.client.get("/api/tools")
        data = response.json()
        tool_ids = [t["id"] for t in data]
        self.assertIn("knowledge", tool_ids)


class TestKnowledgeAPI(unittest.TestCase):
    """測試知識庫 API。"""

    def setUp(self):
        """建立測試用 HTTP client。"""
        self.client = TestClient(app)

    @patch("tw_stock_tools.web.routers.knowledge._get_engine")
    def test_get_knowledge_returns_200(self, mock_get_engine):
        """測試 GET /api/tools/knowledge 回傳 200 與正確資料。"""
        mock_rows = [
            {
                "id": 1,
                "category": "交易基礎",
                "term": "集合競價",
                "description": "測試說明文字",
            },
            {
                "id": 2,
                "category": "費用與稅務",
                "term": "手續費",
                "description": "另一段說明",
            },
        ]

        mock_conn = MagicMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = mock_rows
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value = mock_result

        mock_engine = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_get_engine.return_value = mock_engine

        response = self.client.get("/api/tools/knowledge")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["term"], "集合競價")
        self.assertEqual(data[1]["category"], "費用與稅務")

    @patch("tw_stock_tools.web.routers.knowledge._get_engine")
    def test_get_knowledge_with_category_filter(self, mock_get_engine):
        """測試 GET /api/tools/knowledge?category=交易基礎 回傳篩選結果。"""
        mock_rows = [
            {
                "id": 1,
                "category": "交易基礎",
                "term": "集合競價",
                "description": "測試說明",
            },
        ]

        mock_conn = MagicMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = mock_rows
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value = mock_result

        mock_engine = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_get_engine.return_value = mock_engine

        response = self.client.get(
            "/api/tools/knowledge", params={"category": "交易基礎"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["category"], "交易基礎")

    @patch("tw_stock_tools.web.routers.knowledge._get_engine")
    def test_get_knowledge_categories_returns_200(self, mock_get_engine):
        """測試 GET /api/tools/knowledge/categories 回傳 200 與分類清單。"""
        mock_conn = MagicMock()
        mock_result = MagicMock()
        mock_result.__iter__ = MagicMock(
            return_value=iter([("交易基礎",), ("費用與稅務",), ("股利與除權息",)])
        )
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value = mock_result

        mock_engine = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_get_engine.return_value = mock_engine

        response = self.client.get("/api/tools/knowledge/categories")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)
        self.assertIn("交易基礎", data)
        self.assertIn("費用與稅務", data)

    @patch("tw_stock_tools.web.routers.knowledge._get_engine")
    def test_get_knowledge_db_error_returns_empty(self, mock_get_engine):
        """測試資料庫連線失敗時回傳空陣列。"""
        mock_get_engine.side_effect = Exception("Connection refused")

        response = self.client.get("/api/tools/knowledge")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [])

    @patch("tw_stock_tools.web.routers.knowledge._get_engine")
    def test_get_knowledge_categories_db_error_returns_empty(
        self, mock_get_engine
    ):
        """測試分類 API 資料庫連線失敗時回傳空陣列。"""
        mock_get_engine.side_effect = Exception("Connection refused")

        response = self.client.get("/api/tools/knowledge/categories")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [])


if __name__ == "__main__":
    unittest.main()
