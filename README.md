# 台股工具集（Tw Stock Tools）

提供台灣股市相關的資料擷取與分析工具，透過 Launch Pad 介面快速選用各項工具。

## 專案架構

```text
Tw_stock_tools/
├── docker/
│   ├── build.sh                # 建立 Docker image 的執行腳本
│   ├── Dockerfile              # 多階段建置（Node + Python）
│   └── docker-compose.yaml     # Docker Compose 設定
├── frontend/                   # React 前端（Vite）
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── LaunchPad.jsx   # 工具啟動台元件
│   │       └── ToolCard.jsx    # 工具卡片元件
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── logs/                       # 日誌檔案存放目錄
├── src/
│   └── tw_stock_tools/
│       ├── __init__.py
│       ├── config/
│       │   └── tools.json      # 工具設定檔（新增工具在此）
│       ├── logger.py           # 日誌設定模組
│       ├── main.py             # 主程式進入點（FastAPI 伺服器）
│       └── web/
│           ├── app.py          # FastAPI 應用程式
│           └── routers/
│               └── tools.py    # 工具 API 路由
├── tests/
│   ├── __init__.py
│   └── test_main.py            # 單元測試
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

啟動後開啟瀏覽器前往 <http://localhost:8000>。

### 3. 執行單元測試

```bash
docker run --rm \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/tests:/app/tests" \
  tw-stock-tools:latest \
  python -m pytest tests/ -v
```

## 新增工具

編輯 `src/tw_stock_tools/config/tools.json`，加入新的工具物件：

```json
{
  "id": "my-tool",
  "name": "我的工具",
  "description": "工具說明文字。",
  "icon": "📈",
  "route": "/tools/my-tool",
  "enabled": true
}
```

重新建置 Docker image 後即可在 Launch Pad 看到新工具。

## 授權

MIT License
