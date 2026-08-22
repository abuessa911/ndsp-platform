import request from "../api/apiClient";

export async function getPrice(symbol) {
  const data = await request(`/api/market/prices?symbol=${symbol}`);

  const rows = data?.prices || [];

  return rows.find(
    (r) => String(r.symbol || "").toUpperCase() === symbol
  ) || null;
}
