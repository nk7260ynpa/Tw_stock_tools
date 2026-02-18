"""FastAPI 應用程式。

提供 API 端點與前端靜態檔案服務。
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from tw_stock_tools.web.routers.tools import router as tools_router

app = FastAPI(title="台股工具集", version="0.1.0")

# 註冊 API 路由
app.include_router(tools_router)

# 前端靜態檔案（React 建置產出）
STATIC_DIR = Path(__file__).resolve().parent.parent.parent.parent / "frontend" / "dist"
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="frontend")
