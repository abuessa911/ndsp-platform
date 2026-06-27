import { CONFIG } from "../../config/env";

async function request(path) {
  const url = `${CONFIG.BASE_URL}${path}`;

  const res = await fetch(url, {
    method: "GET",
    cache: "no-store",
    headers: {
      Accept: "application/json"
    }
  });

  if (!res.ok) {
    throw new Error(`API_ERROR: ${res.status}`);
  }

  return res.json();
}

export default request;
