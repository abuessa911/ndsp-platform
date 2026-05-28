const API_BASE = import.meta.env.VITE_NDSP_API_BASE || "http://localhost:8088";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    }
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "request_failed");
  }

  return data;
}

export function apiGet(path, options = {}) {
  return request(path, {
    method: "GET",
    headers: options.headers || {}
  });
}

export function apiPost(path, body, options = {}) {
  return request(path, {
    method: "POST",
    headers: options.headers || {},
    body: JSON.stringify(body)
  });
}

export function apiPatch(path, body, options = {}) {
  return request(path, {
    method: "PATCH",
    headers: options.headers || {},
    body: JSON.stringify(body)
  });
}
