import React, { useEffect, useState } from "react";

const SESSION_ENDPOINT = "/api/auth/session";
const LOGIN_PATH = "/login/";

function buildLoginUrl() {
  const next = `${window.location.pathname}${window.location.search}${window.location.hash}`;
  return `${LOGIN_PATH}?next=${encodeURIComponent(next)}`;
}

export function AuthGate({ children }) {
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    const controller = new AbortController();

    async function verifySession() {
      try {
        const response = await fetch(SESSION_ENDPOINT, {
          method: "GET",
          credentials: "include",
          headers: {
            Accept: "application/json",
          },
          cache: "no-store",
          signal: controller.signal,
        });

        if (!response.ok) {
          window.location.replace(buildLoginUrl());
          return;
        }

        const body = await response.json();

        if (body?.ok !== true || !body?.user?.id) {
          window.location.replace(buildLoginUrl());
          return;
        }

        setAuthorized(true);
      } catch (error) {
        if (error?.name === "AbortError") {
          return;
        }

        window.location.replace(buildLoginUrl());
      }
    }

    verifySession();

    return () => {
      controller.abort();
    };
  }, []);

  if (!authorized) {
    return null;
  }

  return children;
}
