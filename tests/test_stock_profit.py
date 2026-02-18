"""股票損益計算 API 單元測試。"""

import unittest

from fastapi.testclient import TestClient

from tw_stock_tools.web.app import app


class TestStockProfitAPI(unittest.TestCase):
    """測試股票損益計算 API。"""

    def setUp(self):
        """建立測試用 HTTP client。"""
        self.client = TestClient(app)

    def test_calculate_profit_with_fees(self):
        """測試獲利情境（含賣出手續費與證交稅）。"""
        response = self.client.post(
            "/api/tools/stock-profit/calculate",
            json={"avg_price": 38.10, "shares": 21685, "current_price": 40.05},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["cost"], 826198.5)
        self.assertEqual(data["market_value"], 868484.25)
        # 賣出手續費: floor(868484.25 * 0.001425) = 1237
        self.assertEqual(data["sell_commission"], 1237)
        # 證交稅: floor(868484.25 * 0.003) = 2605
        self.assertEqual(data["transaction_tax"], 2605)
        self.assertEqual(data["total_fees"], 3842)
        # 淨損益: 868484.25 - 826198.5 - 3842 = 38443.75
        self.assertEqual(data["profit_loss"], 38443.75)

    def test_calculate_loss_with_fees(self):
        """測試虧損情境。"""
        response = self.client.post(
            "/api/tools/stock-profit/calculate",
            json={"avg_price": 100.0, "shares": 500, "current_price": 80.0},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["sell_commission"], 57)
        self.assertEqual(data["transaction_tax"], 120)
        self.assertEqual(data["profit_loss"], -10177.0)

    def test_min_commission(self):
        """測試最低手續費 20 元。"""
        response = self.client.post(
            "/api/tools/stock-profit/calculate",
            json={"avg_price": 10.0, "shares": 1, "current_price": 10.0},
        )
        data = response.json()
        self.assertEqual(data["sell_commission"], 20)

    def test_invalid_input_returns_422(self):
        """測試無效輸入回傳 422。"""
        response = self.client.post(
            "/api/tools/stock-profit/calculate",
            json={"avg_price": -10, "shares": 1000, "current_price": 50},
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
