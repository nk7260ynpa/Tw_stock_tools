"""API 單元測試。"""

import unittest

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


if __name__ == "__main__":
    unittest.main()
