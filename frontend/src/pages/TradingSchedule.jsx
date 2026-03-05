import { useState } from "react";
import { Link } from "react-router-dom";
import "./TradingSchedule.css";

const SCHEDULE_DATA = [
  {
    category: "一般股票交易（TWSE / TPEX）",
    items: [
      { time: "08:30", event: "開始接受委託", note: "券商開始接受投資人下單" },
      { time: "08:30 - 09:00", event: "試撮期間", note: "揭示模擬成交價，不實際成交" },
      { time: "09:00", event: "開盤（集合競價）", note: "以集合競價決定開盤價" },
      { time: "09:00 - 13:25", event: "盤中交易（逐筆交易）", note: "逐筆撮合，即時成交" },
      { time: "13:25 - 13:30", event: "收盤試撮", note: "最後 5 分鐘不逐筆撮合，改集合競價" },
      { time: "13:30", event: "收盤（集合競價）", note: "以集合競價決定收盤價" },
    ],
  },
  {
    category: "零股交易",
    items: [
      { time: "09:10 - 13:30", event: "盤中零股交易", note: "每 1 分鐘集合競價撮合一次" },
      { time: "13:40 - 14:30", event: "盤後零股交易", note: "集合競價一次撮合（14:30 撮合）" },
    ],
  },
  {
    category: "盤後定價交易",
    items: [
      { time: "13:40 - 14:30", event: "盤後定價交易", note: "以收盤價進行撮合" },
      { time: "14:30", event: "撮合成交", note: "依收盤價一次撮合" },
    ],
  },
  {
    category: "期貨交易（TAIFEX）",
    items: [
      { time: "08:45", event: "日盤開盤", note: "集合競價決定開盤價" },
      { time: "08:45 - 13:45", event: "日盤交易時間", note: "逐筆撮合" },
      { time: "13:45", event: "日盤收盤", note: "" },
      { time: "15:00", event: "夜盤開盤", note: "盤後交易時段開始" },
      { time: "15:00 - 隔日 05:00", event: "夜盤交易時間", note: "隔日凌晨 5:00 收盤" },
    ],
  },
  {
    category: "選擇權交易（TAIFEX）",
    items: [
      { time: "08:45", event: "日盤開盤", note: "集合競價決定開盤價" },
      { time: "08:45 - 13:45", event: "日盤交易時間", note: "逐筆撮合" },
      { time: "13:45", event: "日盤收盤", note: "" },
      { time: "15:00", event: "夜盤開盤", note: "盤後交易時段開始" },
      { time: "15:00 - 隔日 05:00", event: "夜盤交易時間", note: "隔日凌晨 5:00 收盤" },
    ],
  },
  {
    category: "權證交易",
    items: [
      { time: "09:00 - 13:25", event: "盤中交易", note: "與一般股票相同，逐筆交易" },
      { time: "13:25 - 13:30", event: "收盤試撮", note: "集合競價" },
      { time: "13:30", event: "收盤", note: "" },
    ],
  },
  {
    category: "興櫃股票",
    items: [
      { time: "09:00 - 15:00", event: "交易時間", note: "議價交易，非集中撮合" },
      { time: "15:00", event: "收盤", note: "" },
    ],
  },
  {
    category: "特殊日期提醒",
    items: [
      { time: "每月第 3 個週三", event: "期貨結算日", note: "股票期貨與指數期貨到期結算" },
      { time: "除權息交易日", event: "除權息", note: "股價依配股配息調整參考價" },
      { time: "T+2", event: "交割日", note: "成交後第 2 個營業日須完成款券交割" },
      { time: "每年 12 月", event: "年底集中結算", note: "信用交易到期需完成還券或延展" },
    ],
  },
];

function TradingSchedule() {
  const [openSections, setOpenSections] = useState(() => new Set());

  const toggleSection = (index) => {
    setOpenSections((prev) => {
      const next = new Set(prev);
      if (next.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  };

  const expandAll = () => {
    setOpenSections(new Set(SCHEDULE_DATA.map((_, i) => i)));
  };

  const collapseAll = () => {
    setOpenSections(new Set());
  };

  return (
    <div className="schedule-page">
      <Link to="/" className="back-link">&larr; 返回 Launch Pad</Link>
      <h2 className="schedule-title">台股特殊時刻表</h2>
      <p className="schedule-subtitle">各市場交易時間總覽</p>

      <div className="schedule-actions">
        <button type="button" className="schedule-action-btn" onClick={expandAll}>全部展開</button>
        <button type="button" className="schedule-action-btn" onClick={collapseAll}>全部收合</button>
      </div>

      <div className="schedule-accordion">
        {SCHEDULE_DATA.map((section, index) => {
          const isOpen = openSections.has(index);
          return (
            <div className="schedule-section" key={index}>
              <button
                type="button"
                className={`schedule-section-header ${isOpen ? "open" : ""}`}
                onClick={() => toggleSection(index)}
              >
                <span className="schedule-section-title">{section.category}</span>
                <span className="schedule-section-arrow">{isOpen ? "\u25B2" : "\u25BC"}</span>
              </button>
              {isOpen && (
                <div className="schedule-section-body">
                  <table className="schedule-table">
                    <thead>
                      <tr>
                        <th className="schedule-th schedule-th-time">時間</th>
                        <th className="schedule-th schedule-th-event">事件</th>
                        <th className="schedule-th schedule-th-note">說明</th>
                      </tr>
                    </thead>
                    <tbody>
                      {section.items.map((item, i) => (
                        <tr key={i} className="schedule-tr">
                          <td className="schedule-td schedule-td-time">{item.time}</td>
                          <td className="schedule-td schedule-td-event">{item.event}</td>
                          <td className="schedule-td schedule-td-note">{item.note}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default TradingSchedule;
