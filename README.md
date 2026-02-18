# 台股工具集（Tw Stock Tools）

提供台灣股市相關的資料擷取與分析工具。

## 專案架構

```text
Tw_stock_tools/
├── docker/
│   ├── build.sh                # 建立 Docker image 的執行腳本
│   ├── Dockerfile              # Docker image 定義
│   └── docker-compose.yaml     # Docker Compose 設定
├── logs/                       # 日誌檔案存放目錄
├── src/
│   └── tw_stock_tools/
│       ├── __init__.py         # 套件初始化
│       ├── logger.py           # 日誌設定模組
│       └── main.py             # 主程式進入點
├── tests/
│   ├── __init__.py
│   └── test_main.py            # 主程式單元測試
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt            # Python 依賴套件
└── run.sh                      # 啟動主程式的執行腳本
```

## 環境需求

- Docker

## 快速開始

### 1. 建立 Docker image

```bash
bash docker/build.sh
```

### 2. 執行主程式

```bash
bash run.sh
```

### 3. 執行單元測試

```bash
docker run --rm \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/tests:/app/tests" \
  tw-stock-tools:latest \
  python -m pytest tests/ -v
```

## 授權

MIT License
