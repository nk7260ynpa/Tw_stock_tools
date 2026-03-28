import { useState, useEffect, useMemo, useCallback } from "react";
import { Link } from "react-router-dom";
import "./TradingCalendar.css";

const WEEKDAY_LABELS = ["日", "一", "二", "三", "四", "五", "六"];

function TradingCalendar() {
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1);
  const [calendarData, setCalendarData] = useState([]);
  const [holidays, setHolidays] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tooltip, setTooltip] = useState(null);

  // 取得行事曆資料
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [calRes, holRes] = await Promise.all([
          fetch(`/api/tools/calendar?year=${year}&month=${month}`),
          fetch(`/api/tools/calendar/holidays?year=${year}`),
        ]);
        const calData = await calRes.json();
        const holData = await holRes.json();
        setCalendarData(calData);
        setHolidays(holData);
      } catch (err) {
        console.error("載入行事曆失敗:", err);
        setError("無法載入行事曆資料，請稍後再試。");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [year, month]);

  // 建立日期查詢表
  const dateMap = useMemo(() => {
    const map = {};
    calendarData.forEach((item) => {
      map[item.date] = item;
    });
    return map;
  }, [calendarData]);

  // 統計
  const stats = useMemo(() => {
    const openDays = calendarData.filter((d) => d.is_open).length;
    const closedDays = calendarData.filter((d) => !d.is_open).length;
    return { openDays, closedDays };
  }, [calendarData]);

  // 產生月曆格子
  const calendarGrid = useMemo(() => {
    const firstDay = new Date(year, month - 1, 1);
    const lastDay = new Date(year, month, 0);
    const daysInMonth = lastDay.getDate();
    const startWeekday = firstDay.getDay();

    const grid = [];
    // 前面的空白
    for (let i = 0; i < startWeekday; i++) {
      grid.push(null);
    }
    // 每一天
    for (let day = 1; day <= daysInMonth; day++) {
      const dateStr = `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
      const info = dateMap[dateStr];
      grid.push({
        day,
        date: dateStr,
        isOpen: info ? info.is_open : null,
        description: info ? info.description : null,
      });
    }
    return grid;
  }, [year, month, dateMap]);

  const goToPrevMonth = useCallback(() => {
    if (month === 1) {
      setYear((y) => y - 1);
      setMonth(12);
    } else {
      setMonth((m) => m - 1);
    }
  }, [month]);

  const goToNextMonth = useCallback(() => {
    if (month === 12) {
      setYear((y) => y + 1);
      setMonth(1);
    } else {
      setMonth((m) => m + 1);
    }
  }, [month]);

  const goToToday = useCallback(() => {
    setYear(today.getFullYear());
    setMonth(today.getMonth() + 1);
  }, []);

  const handleDayHover = (e, cell) => {
    if (!cell || cell.isOpen === null) return;
    const rect = e.currentTarget.getBoundingClientRect();
    setTooltip({
      x: rect.left + rect.width / 2,
      y: rect.top,
      text: cell.isOpen
        ? "開市"
        : cell.description
          ? `休市：${cell.description}`
          : "休市",
    });
  };

  const handleDayLeave = () => {
    setTooltip(null);
  };

  const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

  return (
    <div className="calendar-page">
      <Link to="/" className="back-link">&larr; 返回 Launch Pad</Link>
      <h2 className="calendar-title">台股行事曆</h2>
      <p className="calendar-subtitle">台股開休市日期查詢</p>

      {error && <p className="calendar-error">{error}</p>}

      {/* 月份導覽 */}
      <div className="calendar-nav">
        <button type="button" className="calendar-nav-btn" onClick={goToPrevMonth}>
          &lsaquo;
        </button>
        <span className="calendar-nav-label">
          {year} 年 {month} 月
        </span>
        <button type="button" className="calendar-nav-btn" onClick={goToNextMonth}>
          &rsaquo;
        </button>
        <button type="button" className="calendar-today-btn" onClick={goToToday}>
          今天
        </button>
      </div>

      {/* 統計 */}
      {!loading && calendarData.length > 0 && (
        <div className="calendar-stats">
          <span className="calendar-stat">
            <span className="calendar-stat-dot open"></span>
            開市 {stats.openDays} 天
          </span>
          <span className="calendar-stat">
            <span className="calendar-stat-dot closed"></span>
            休市 {stats.closedDays} 天
          </span>
        </div>
      )}

      {/* 月曆 */}
      {loading ? (
        <p className="calendar-loading">資料載入中...</p>
      ) : (
        <div className="calendar-grid-wrapper">
          <div className="calendar-grid">
            {WEEKDAY_LABELS.map((label) => (
              <div key={label} className="calendar-weekday">{label}</div>
            ))}
            {calendarGrid.map((cell, index) => {
              if (!cell) {
                return <div key={`empty-${index}`} className="calendar-cell empty"></div>;
              }

              const isToday = cell.date === todayStr;
              let statusClass = "";
              if (cell.isOpen === true) statusClass = "open";
              else if (cell.isOpen === false) statusClass = "closed";

              return (
                <div
                  key={cell.date}
                  className={`calendar-cell ${statusClass} ${isToday ? "today" : ""}`}
                  onMouseEnter={(e) => handleDayHover(e, cell)}
                  onMouseLeave={handleDayLeave}
                >
                  <span className="calendar-day-num">{cell.day}</span>
                  {cell.isOpen !== null && (
                    <span className={`calendar-dot ${statusClass}`}></span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* 圖例 */}
      <div className="calendar-legend">
        <span className="calendar-legend-item">
          <span className="calendar-legend-dot open"></span>開市
        </span>
        <span className="calendar-legend-item">
          <span className="calendar-legend-dot closed"></span>休市
        </span>
        <span className="calendar-legend-item">
          <span className="calendar-legend-today"></span>今天
        </span>
      </div>

      {/* 國定假日清單 */}
      {holidays.length > 0 && (
        <div className="calendar-holidays">
          <h3 className="calendar-holidays-title">{year} 年國定假日休市日</h3>
          <div className="calendar-holidays-list">
            {holidays.map((h) => (
              <div key={h.date} className="calendar-holiday-item">
                <span className="calendar-holiday-date">{h.date}</span>
                <span className="calendar-holiday-desc">{h.description || "國定假日"}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tooltip */}
      {tooltip && (
        <div
          className="calendar-tooltip"
          style={{
            left: tooltip.x,
            top: tooltip.y,
          }}
        >
          {tooltip.text}
        </div>
      )}
    </div>
  );
}

export default TradingCalendar;
