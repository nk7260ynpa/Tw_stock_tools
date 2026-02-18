"""股票損益計算 API 路由。

提供台灣股票損益計算的 RESTful API。
"""

import math
from enum import Enum

from pydantic import BaseModel, Field

from fastapi import APIRouter

router = APIRouter(prefix="/api/tools/stock-profit", tags=["stock-profit"])

# 台股標準費率
COMMISSION_RATE = 0.001425  # 手續費率 0.1425%
MIN_COMMISSION = 20  # 最低手續費（元）

# 證交稅率（依商品類型）
TAX_RATES = {
    "stock": 0.003,  # 一般股票 0.3%
    "etf": 0.001,    # ETF 0.1%
}


class StockType(str, Enum):
    """商品類型。"""

    STOCK = "stock"
    ETF = "etf"


class StockProfitRequest(BaseModel):
    """損益計算請求。"""

    avg_price: float = Field(..., gt=0, description="購買均價（已含買進手續費之成本價）")
    shares: int = Field(..., gt=0, description="持有股數")
    current_price: float = Field(..., gt=0, description="現在價格")
    stock_type: StockType = Field(StockType.STOCK, description="商品類型")


class StockProfitResponse(BaseModel):
    """損益計算結果。"""

    stock_type: str = Field(..., description="商品類型")
    transaction_tax_rate: float = Field(..., description="證交稅率")
    cost: float = Field(..., description="總買入成本")
    market_value: float = Field(..., description="目前市值")
    sell_commission: int = Field(..., description="賣出手續費")
    transaction_tax: int = Field(..., description="證交稅")
    total_fees: int = Field(..., description="總交易成本")
    profit_loss: float = Field(..., description="淨損益金額")
    profit_loss_pct: float = Field(..., description="損益百分比")


def _calc_commission(amount: float) -> int:
    """計算手續費（無條件捨去，最低 20 元）。

    Args:
        amount: 成交金額。

    Returns:
        手續費（整數）。
    """
    fee = math.floor(amount * COMMISSION_RATE)
    return max(fee, MIN_COMMISSION)


@router.post("/calculate", response_model=StockProfitResponse)
def calculate_profit(req: StockProfitRequest) -> StockProfitResponse:
    """計算股票損益（含賣出手續費與證交稅）。

    購買均價視為已含買進手續費之成本價，僅扣除賣出時的手續費與證交稅。

    Args:
        req: 包含購買均價、持有股數、現在價格的請求。

    Returns:
        損益計算結果。
    """
    tax_rate = TAX_RATES[req.stock_type.value]

    cost = req.avg_price * req.shares
    market_value = req.current_price * req.shares

    sell_commission = _calc_commission(market_value)
    transaction_tax = math.floor(market_value * tax_rate)

    total_fees = sell_commission + transaction_tax
    profit_loss = market_value - cost - total_fees
    profit_loss_pct = profit_loss / cost * 100

    return StockProfitResponse(
        stock_type=req.stock_type.value,
        transaction_tax_rate=tax_rate,
        cost=round(cost, 2),
        market_value=round(market_value, 2),
        sell_commission=sell_commission,
        transaction_tax=transaction_tax,
        total_fees=total_fees,
        profit_loss=round(profit_loss, 2),
        profit_loss_pct=round(profit_loss_pct, 2),
    )
