# 台股工具集（Tw Stock Tools）

提供台灣股市相關的資料擷取與分析工具，透過 Launch Pad 介面快速選用各項工具。

## 功能列表

- **股票損益計算器** — 輸入購買均價、持有股數與現價，計算損益金額與百分比（支援一般股票與 ETF 不同稅率）
- **股利計算器** — 輸入持有股數與每股股利，計算股利總金額與扣除匯費後的實收金額

## 專案架構

```text
Tw_stock_tools/
├── docker/
│   ├── build.sh                    # 建立 Docker image 的執行腳本
│   ├── Dockerfile                  # 多階段建置（Node + Python）
│   └── docker-compose.yaml         # Docker Compose 設定
├── frontend/                       # React 前端（Vite）
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx                 # 路由設定
│   │   ├── components/
│   │   │   ├── LaunchPad.jsx       # 工具啟動台元件
│   │   │   └── ToolCard.jsx        # 工具卡片元件
│   │   └── pages/
│   │       ├── StockProfitCalculator.jsx  # 股票損益計算器頁面
│   │       └── DividendCalculator.jsx     # 股利計算器頁面
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── logs/                           # 日誌檔案存放目錄
├── src/
│   └── tw_stock_tools/
│       ├── __init__.py
│       ├── config/
│       │   └── tools.json          # 工具設定檔（新增工具在此）
│       ├── logger.py               # 日誌設定模組
│       ├── main.py                 # 主程式進入點（FastAPI 伺服器）
│       └── web/
│           ├── app.py              # FastAPI 應用程式
│           └── routers/
│               ├── tools.py        # 工具列表 API 路由
│               ├── stock_profit.py # 股票損益計算 API 路由
│               └── dividend.py     # 股利計算 API 路由
├── tests/
│   ├── __init__.py
│   ├── test_main.py                # 日誌模組測試
│   ├── test_api.py                 # 工具 API 測試
│   ├── test_stock_profit.py        # 股票損益計算測試
│   └── test_dividend.py            # 股利計算測試
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml                  # Python 套件設定（PEP 621）
├── requirements.txt                # Docker 環境釘版依賴
└── run.sh                          # 啟動主程式的執行腳本
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
  -v "$(pwd)/tests:/app/tests" \
  -v "$(pwd)/src/tw_stock_tools/config:/app/src/tw_stock_tools/config" \
  nk7260ynpa/tw_stock_tools:latest \
  python -m pytest tests/ -v
```

## 工具說明

### 股票損益計算器

| 輸入欄位 | 說明 |
| --- | --- |
| 商品類型 | 一般股票（證交稅 0.3%）或 ETF（證交稅 0.1%） |
| 購買均價 | 已含買進手續費之成本價 |
| 持有股數 | 持有的股數 |
| 現在價格 | 目前市場價格 |

計算公式：

- 賣出手續費 = floor(市值 × 0.1425%)，最低 20 元
- 證交稅 = floor(市值 × 稅率)
- 淨損益 = 市值 - 成本 - 賣出手續費 - 證交稅

### 股利計算器

| 輸入欄位 | 說明 |
| --- | --- |
| 持有股數 | 持有的股數 |
| 每股股利 | 每股配發的現金股利（支援小數點後 3 位） |
| 匯費 | 券商代收轉帳費，預設 10 元 |

計算公式：

- 股利總金額 = 持有股數 × 每股股利
- 實收金額 = 股利總金額 - 匯費

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
