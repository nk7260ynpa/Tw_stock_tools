"""台股知識庫 API 路由。

提供台股知識條目與分類的 RESTful API，資料來源為 MySQL INFO.Knowledge 資料表。
"""

import logging
import os
from typing import Optional

from fastapi import APIRouter, Query
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

router = APIRouter(prefix="/api/tools/knowledge", tags=["knowledge"])

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
        logger.info("已建立知識庫資料庫連線：%s@%s/INFO", user, host)
    return _engine


@router.get("")
def get_knowledge(
    category: Optional[str] = Query(None, description="依分類名稱篩選"),
) -> list[dict]:
    """取得知識庫條目。

    可選擇以 category query parameter 篩選特定分類的條目。
    若資料庫連線失敗，回傳空陣列而非拋出錯誤。

    Args:
        category: 分類名稱（可選）。

    Returns:
        知識條目清單。
    """
    try:
        engine = _get_engine()
        with engine.connect() as conn:
            if category:
                result = conn.execute(
                    text(
                        "SELECT id, category, term, description "
                        "FROM Knowledge WHERE category = :category "
                        "ORDER BY id"
                    ),
                    {"category": category},
                )
            else:
                result = conn.execute(
                    text(
                        "SELECT id, category, term, description "
                        "FROM Knowledge ORDER BY id"
                    )
                )
            rows = result.mappings().all()
            return [dict(row) for row in rows]
    except Exception:
        logger.exception("查詢知識庫條目失敗")
        return []


@router.get("/categories")
def get_knowledge_categories() -> list[str]:
    """取得所有知識庫分類名稱。

    若資料庫連線失敗，回傳空陣列而非拋出錯誤。

    Returns:
        分類名稱清單。
    """
    try:
        engine = _get_engine()
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT category FROM Knowledge "
                    "GROUP BY category ORDER BY MIN(id)"
                ),
            )
            return [row[0] for row in result]
    except Exception:
        logger.exception("查詢知識庫分類失敗")
        return []
