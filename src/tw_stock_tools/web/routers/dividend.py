"""股利計算 API 路由。

提供台灣股票股利總金額計算的 RESTful API。
"""

from pydantic import BaseModel, Field

from fastapi import APIRouter

router = APIRouter(prefix="/api/tools/dividend", tags=["dividend"])


class DividendRequest(BaseModel):
    """股利計算請求。"""

    shares: int = Field(..., gt=0, description="持有股數")
    dividend: float = Field(..., gt=0, description="每股股利（元）")
    transfer_fee: int = Field(10, ge=0, description="匯費（元），預設 10 元")


class DividendResponse(BaseModel):
    """股利計算結果。"""

    shares: int = Field(..., description="持有股數")
    dividend: float = Field(..., description="每股股利")
    total: float = Field(..., description="股利總金額")
    transfer_fee: int = Field(..., description="匯費")
    net: float = Field(..., description="實收金額")


@router.post("/calculate", response_model=DividendResponse)
def calculate_dividend(req: DividendRequest) -> DividendResponse:
    """計算股利總金額。

    Args:
        req: 包含持有股數、每股股利與匯費的請求。

    Returns:
        股利計算結果。
    """
    total = req.shares * req.dividend
    net = total - req.transfer_fee

    return DividendResponse(
        shares=req.shares,
        dividend=req.dividend,
        total=round(total, 3),
        transfer_fee=req.transfer_fee,
        net=round(net, 3),
    )
