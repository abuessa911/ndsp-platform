import request from "../api/apiClient";

export async function getScenario(symbol) {
  const data = await request(`/api/scenario/levels?symbol=${symbol}`);

  if (data?.ok && data?.levels) {
    return data.levels;
  }

  return null;
}
