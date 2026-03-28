"""台股行事曆 API 路由。

提供台股開休市日期查詢的 RESTful API，資料來源為 MySQL INFO.TradingCalendar 資料表。
"""

import logging
import os
from typing import Optional

from fastapi import APIRouter, Query
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

router = APIRouter(prefix="/api/tools/calendar", tags=["calendar"])

logger = logging.getLogger("tw_stock_tools")

_engine: Optional[Engine] = None


def _get_engine() -> Engine:
    """取得 SQLAlchemy 資料庫引擎（單例模式）。

    透過環境變數取得資料庫連線資訊，預設連線至 Docker 網路內的
    tw_stock_database 主機。

    Returns:
        SQLAlchemy Engine 實例。
    """
    global _engine
    if _engine is None:
        host = os.environ.get("DB_HOST", "tw_stock_database")
        user = os.environ.get("DB_USER", "root")
        password = os.environ.get("DB_PASSWORD", "stock")
        url = f"mysql+pymysql://{user}:{password}@{host}/INFO"
        _engine = create_engine(url, pool_pre_ping=True)
        logger.info("已建立行事曆資料庫連線：%s@%s/INFO", user, host)
    return _engine


@router.get("")
def get_calendar(
    year: int = Query(..., description="查詢年份", ge=2000, le=2100),
    month: int = Query(..., description="查詢月份", ge=1, le=12),
) -> list[dict]:
    """取得指定年月的行事曆資料。

    回傳該月所有日期的開休市狀態與休市原因。
    若資料庫連線失敗，回傳空陣列而非拋出錯誤。

    Args:
        year: 查詢年份（2000-2100）。
        month: 查詢月份（1-12）。

    Returns:
        該月所有日期的開休市狀態清單，每筆包含 date、is_open、description 欄位。
    """
    try:
        engine = _get_engine()
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT Date, IsOpen, Description "
                    "FROM TradingCalendar "
                    "WHERE YEAR(Date) = :year AND MONTH(Date) = :month "
                    "ORDER BY Date"
                ),
                {"year": year, "month": month},
            )
            rows = result.mappings().all()
            return [
                {
                    "date": row["Date"].isoformat(),
                    "is_open": bool(row["IsOpen"]),
                    "description": row["Description"],
                }
                for row in rows
            ]
    except Exception:
        logger.exception("查詢行事曆資料失敗（%d-%02d）", year, month)
        return []


@router.get("/holidays")
def get_holidays(
    year: int = Query(..., description="查詢年份", ge=2000, le=2100),
) -> list[dict]:
    """取得指定年份的所有國定假日休市日（不含週末）。

    篩選條件：IsOpen = 0 且 Description != '週末'。
    若資料庫連線失敗，回傳空陣列而非拋出錯誤。

    Args:
        year: 查詢年份（2000-2100）。

    Returns:
        國定假日休市列表，每筆包含 date、description 欄位。
    """
    try:
        engine = _get_engine()
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT Date, Description "
                    "FROM TradingCalendar "
                    "WHERE YEAR(Date) = :year "
                    "AND IsOpen = 0 "
                    "AND (Description IS NULL OR Description != '週末') "
                    "ORDER BY Date"
                ),
                {"year": year},
            )
            rows = result.mappings().all()
            return [
                {
                    "date": row["Date"].isoformat(),
                    "description": row["Description"],
                }
                for row in rows
            ]
    except Exception:
        logger.exception("查詢休市日資料失敗（%d）", year)
        return []
