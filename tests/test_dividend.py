"""股利計算 API 單元測試。"""

import unittest

from fastapi.testclient import TestClient

from tw_stock_tools.web.app import app


class TestDividendAPI(unittest.TestCase):
    """測試股利計算 API。"""

    def setUp(self):
        """建立測試用 HTTP client。"""
        self.client = TestClient(app)

    def test_calculate_dividend(self):
        """測試基本股利計算。"""
        response = self.client.post(
            "/api/tools/dividend/calculate",
            json={"shares": 1000, "dividend": 2.5},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["shares"], 1000)
        self.assertEqual(data["dividend"], 2.5)
        self.assertEqual(data["total"], 2500.0)
        self.assertEqual(data["transfer_fee"], 10)
        self.assertEqual(data["net"], 2490.0)

    def test_calculate_dividend_with_custom_fee(self):
        """測試自訂匯費。"""
        response = self.client.post(
            "/api/tools/dividend/calculate",
            json={"shares": 2400, "dividend": 0.305, "transfer_fee": 11},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total"], 732.0)
        self.assertEqual(data["transfer_fee"], 11)
        self.assertEqual(data["net"], 721.0)

    def test_default_transfer_fee(self):
        """測試預設匯費為 10 元。"""
        response = self.client.post(
            "/api/tools/dividend/calculate",
            json={"shares": 2400, "dividend": 0.305},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["transfer_fee"], 10)
        self.assertEqual(data["net"], 722.0)

    def test_zero_transfer_fee(self):
        """測試匯費為 0。"""
        response = self.client.post(
            "/api/tools/dividend/calculate",
            json={"shares": 1000, "dividend": 1.0, "transfer_fee": 0},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total"], 1000.0)
        self.assertEqual(data["net"], 1000.0)

    def test_invalid_input_returns_422(self):
        """測試無效輸入回傳 422。"""
        response = self.client.post(
            "/api/tools/dividend/calculate",
            json={"shares": -1, "dividend": 2.5},
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
