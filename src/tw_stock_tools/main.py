"""主程式進入點。

台股工具集的主要執行邏輯。
"""

import uvicorn

from tw_stock_tools.logger import setup_logger

logger = setup_logger()


def main() -> None:
    """啟動 FastAPI Web 伺服器。"""
    logger.info("台股工具集啟動")
    uvicorn.run(
        "tw_stock_tools.web.app:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )


if __name__ == "__main__":
    main()
