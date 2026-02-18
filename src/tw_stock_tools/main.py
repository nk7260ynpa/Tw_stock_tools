"""主程式進入點。

台股工具集的主要執行邏輯。
"""

from tw_stock_tools.logger import setup_logger

logger = setup_logger()


def main() -> None:
    """主程式進入點。"""
    logger.info("台股工具集啟動")
    logger.info("台股工具集結束")


if __name__ == "__main__":
    main()
