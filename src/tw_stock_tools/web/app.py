"""FastAPI 應用程式。

提供 API 端點與前端靜態檔案服務。
"""

import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from tw_stock_tools.web.routers.dividend import router as dividend_router
from tw_stock_tools.web.routers.stock_profit import router as stock_profit_router
from tw_stock_tools.web.routers.tools import router as tools_router

logger = logging.getLogger("tw_stock_tools")

app = FastAPI(title="台股工具集", version="0.1.0")

# 註冊 API 路由
app.include_router(tools_router)
app.include_router(stock_profit_router)
app.include_router(dividend_router)


def _resolve_static_dir() -> Path | None:
    """解析前端靜態檔案目錄。

    依序嘗試以下候選路徑：
    1. STATIC_DIR 環境變數（最高優先）
    2. /app/frontend/dist（Docker 容器內標準路徑）
    3. __file__ 相對路徑（本地開發用）

    Returns:
        找到的靜態檔案目錄 Path，若全部不存在則回傳 None。
    """
    candidates: list[Path] = []

    # 1. 環境變數
    env_dir = os.environ.get("STATIC_DIR")
    if env_dir:
        candidates.append(Path(env_dir))

    # 2. Docker 容器內標準路徑
    candidates.append(Path("/app/frontend/dist"))

    # 3. __file__ 相對路徑（本地開發）
    candidates.append(
        Path(__file__).resolve().parent.parent.parent.parent / "frontend" / "dist"
    )

    for candidate in candidates:
        if candidate.exists():
            logger.info("前端靜態檔案目錄：%s", candidate)
            return candidate

    logger.warning("找不到前端靜態檔案目錄，已嘗試：%s", candidates)
    return None


# 前端靜態檔案（React 建置產出）
STATIC_DIR = _resolve_static_dir()
if STATIC_DIR is not None:
    # 掛載靜態資源（CSS、JS 等）
    app.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str) -> FileResponse:
        """處理所有非 API 路徑，回傳 index.html 供 React Router 處理。"""
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(STATIC_DIR / "index.html")
