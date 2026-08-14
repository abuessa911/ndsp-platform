import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { ReactNode } from "react";
import { getSession, logout } from "../api/auth";
import type { AuthSession, AuthUser } from "../api/auth";

export type AuthStatus = "loading" | "anonymous" | "authenticated" | "unavailable";

type AuthContextValue = {
  error: string | null;
  isAdmin: boolean;
  refresh: () => Promise<AuthSession>;
  signOut: () => Promise<void>;
  status: AuthStatus;
  user: AuthUser | null;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<AuthStatus>("loading");
  const [user, setUser] = useState<AuthUser | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setStatus("loading");
    setError(null);
    try {
      const session = await getSession();
      setUser(session.user);
      setStatus(session.authenticated ? "authenticated" : "anonymous");
      return session;
    } catch (requestError) {
      setUser(null);
      setStatus("unavailable");
      setError("تعذر التحقق من الجلسة الآمنة.");
      throw requestError;
    }
  }, []);

  useEffect(() => {
    void refresh().catch(() => undefined);
  }, [refresh]);

  const signOut = useCallback(async () => {
    await logout();
    setUser(null);
    setError(null);
    setStatus("anonymous");
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      error,
      isAdmin: user?.isAdmin === true,
      refresh,
      signOut,
      status,
      user,
    }),
    [error, refresh, signOut, status, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}
