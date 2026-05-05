/**
 * API 路徑工具。
 *
 * 將絕對路徑轉換為包含 Vite base 前綴的路徑，
 * 以支援透過反向代理（例如 Dashboard 的 /app/tools/）存取後端 API。
 */

/**
 * 組合 API URL，將傳入的路徑補上 Vite base 前綴。
 *
 * @param {string} path - 以 `/` 開頭的 API 路徑，例如 `/api/tools`。
 * @returns {string} 已加上 base 前綴的完整路徑。
 */
export const apiUrl = (path) => {
  const base = import.meta.env.BASE_URL || "/";
  const normalizedBase = base.endsWith("/") ? base : `${base}/`;
  const normalizedPath = path.startsWith("/") ? path.slice(1) : path;
  return `${normalizedBase}${normalizedPath}`;
};
