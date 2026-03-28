"""台股行事曆 API 單元測試。"""

import datetime
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from tw_stock_tools.web.app import app


class TestCalendarAPI(unittest.TestCase):
    """測試行事曆 API。"""

    def setUp(self):
        """建立測試用 HTTP client。"""
        self.client = TestClient(app)

    def test_get_calendar_missing_params_returns_422(self):
        """測試 GET /api/tools/calendar 缺少必要參數時回傳 422。"""
        response = self.client.get("/api/tools/calendar")
        self.assertEqual(response.status_code, 422)

    def test_get_calendar_invalid_month_returns_422(self):
        """測試 GET /api/tools/calendar month=13 回傳 422。"""
        response = self.client.get(
            "/api/tools/calendar", params={"year": 2026, "month": 13}
        )
        self.assertEqual(response.status_code, 422)

    @patch("tw_stock_tools.web.routers.calendar._get_engine")
    def test_get_calendar_returns_200(self, mock_get_engine):
        """測試 GET /api/tools/calendar 回傳 200 與正確資料。"""
        mock_rows = [
            {
                "Date": datetime.date(2026, 3, 2),
                "IsOpen": 1,
                "Description": None,
            },
            {
                "Date": datetime.date(2026, 3, 3),
                "IsOpen": 1,
                "Description": None,
            },
            {
                "Date": datetime.date(2026, 3, 7),
                "IsOpen": 0,
                "Description": "週末",
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
            "/api/tools/calendar", params={"year": 2026, "month": 3}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["date"], "2026-03-02")
        self.assertTrue(data[0]["is_open"])
        self.assertFalse(data[2]["is_open"])
        self.assertEqual(data[2]["description"], "週末")

    @patch("tw_stock_tools.web.routers.calendar._get_engine")
    def test_get_calendar_db_error_returns_empty(self, mock_get_engine):
        """測試行事曆 API 資料庫連線失敗時回傳空陣列。"""
        mock_get_engine.side_effect = Exception("Connection refused")

        response = self.client.get(
            "/api/tools/calendar", params={"year": 2026, "month": 3}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [])

    @patch("tw_stock_tools.web.routers.calendar._get_engine")
    def test_get_holidays_returns_200(self, mock_get_engine):
        """測試 GET /api/tools/calendar/holidays 回傳 200 與正確資料。"""
        mock_rows = [
            {
                "Date": datetime.date(2026, 1, 1),
                "Description": "元旦",
            },
            {
                "Date": datetime.date(2026, 2, 17),
                "Description": "農曆春節",
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
            "/api/tools/calendar/holidays", params={"year": 2026}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["date"], "2026-01-01")
        self.assertEqual(data[0]["description"], "元旦")
        self.assertEqual(data[1]["description"], "農曆春節")

    @patch("tw_stock_tools.web.routers.calendar._get_engine")
    def test_get_holidays_db_error_returns_empty(self, mock_get_engine):
        """測試休市日 API 資料庫連線失敗時回傳空陣列。"""
        mock_get_engine.side_effect = Exception("Connection refused")

        response = self.client.get(
            "/api/tools/calendar/holidays", params={"year": 2026}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [])

    def test_get_holidays_missing_year_returns_422(self):
        """測試 GET /api/tools/calendar/holidays 缺少 year 參數時回傳 422。"""
        response = self.client.get("/api/tools/calendar/holidays")
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
