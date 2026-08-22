export type JsonRecord = Record<string, unknown>;

export type AuthUser = {
  id: string | null;
  email: string | null;
  name: string | null;
  role: string | null;
  isAdmin: boolean;
};

export type AuthSession = {
  authenticated: boolean;
  user: AuthUser | null;
};

export type LoginResult = AuthSession & {
  challengeToken: string | null;
  message: string | null;
  redirect: string | null;
  setupRequired: boolean;
  twoFactorRequired: boolean;
};

export class AuthApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "AuthApiError";
    this.status = status;
  }
}

const ADMIN_ROLES = new Set([
  "admin",
  "administrator",
  "owner",
  "superadmin",
  "super_admin",
  "sovereign_admin",
]);

function asRecord(value: unknown): JsonRecord | null {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as JsonRecord)
    : null;
}

function firstRecord(...values: unknown[]): JsonRecord | null {
  for (const value of values) {
    const record = asRecord(value);
    if (record) return record;
  }
  return null;
}

function firstString(record: JsonRecord | null, ...keys: string[]): string | null {
  if (!record) return null;
  for (const key of keys) {
    const value = record[key];
    if (typeof value === "string" && value.trim()) return value.trim();
    if (typeof value === "number" && Number.isFinite(value)) return String(value);
  }
  return null;
}

function firstBoolean(record: JsonRecord | null, ...keys: string[]): boolean | null {
  if (!record) return null;
  for (const key of keys) {
    const value = record[key];
    if (typeof value === "boolean") return value;
    if (value === 1 || value === "1" || value === "true") return true;
    if (value === 0 || value === "0" || value === "false") return false;
  }
  return null;
}

function responseMessage(payload: JsonRecord, status: number): string {
  if (status >= 500) {
    return "خدمة المصادقة غير متاحة مؤقتًا. حاول مرة أخرى بعد قليل.";
  }

  const nestedError = asRecord(payload.error);
  return (
    firstString(payload, "message", "detail", "error") ??
    firstString(nestedError, "message", "detail") ??
    "تعذر إكمال الطلب. تحقق من البيانات وحاول مرة أخرى."
  );
}

async function requestJson(path: string, init: RequestInit = {}): Promise<JsonRecord> {
  let response: Response;
  try {
    response = await fetch(path, {
      ...init,
      credentials: "include",
      headers: {
        Accept: "application/json",
        ...(init.body ? { "Content-Type": "application/json" } : {}),
        ...init.headers,
      },
    });
  } catch {
    throw new AuthApiError("تعذر الاتصال بخدمة المصادقة.", 0);
  }

  const text = await response.text();
  let payload: JsonRecord = {};
  if (text) {
    try {
      payload = asRecord(JSON.parse(text)) ?? {};
    } catch {
      if (!response.ok) {
        throw new AuthApiError("استجابت خدمة المصادقة بصيغة غير متوقعة.", response.status);
      }
    }
  }

  const explicitFailure =
    firstBoolean(payload, "ok") === false || firstBoolean(payload, "success") === false;
  if (!response.ok || explicitFailure) {
    throw new AuthApiError(responseMessage(payload, response.status), response.status);
  }

  return payload;
}

function extractUser(payload: JsonRecord): AuthUser | null {
  const data = asRecord(payload.data);
  const session = firstRecord(payload.session, data?.session);
  const source = firstRecord(payload.user, session?.user, data?.user, payload.account);
  if (!source) return null;

  const role = firstString(source, "role", "user_role", "account_role");
  const explicitAdmin = firstBoolean(source, "isAdmin", "is_admin", "admin", "is_sovereign");

  return {
    id: firstString(source, "id", "user_id", "uuid"),
    email: firstString(source, "email", "username"),
    name: firstString(source, "name", "full_name", "display_name"),
    role,
    isAdmin: explicitAdmin === true || (role ? ADMIN_ROLES.has(role.toLowerCase()) : false),
  };
}

function sessionFromPayload(payload: JsonRecord): AuthSession {
  const data = asRecord(payload.data);
  const session = firstRecord(payload.session, data?.session);
  const user = extractUser(payload);
  const authenticated =
    firstBoolean(payload, "authenticated", "active") ??
    firstBoolean(session, "authenticated", "active") ??
    Boolean(user);

  return { authenticated, user: authenticated ? user : null };
}

function loginResultFromPayload(payload: JsonRecord): LoginResult {
  const data = asRecord(payload.data);
  const session = sessionFromPayload(payload);
  const stage = firstString(payload, "stage", "context")?.toLowerCase() ?? "";
  const twoFactorRequired =
    firstBoolean(
      payload,
      "two_factor_required",
      "twoFactorRequired",
      "requires_2fa",
      "requires2fa",
      "challenge_required",
    ) === true || (!session.authenticated && stage.includes("2fa"));

  return {
    ...session,
    challengeToken:
      firstString(payload, "challengeToken", "challenge_token", "token") ??
      firstString(data, "challengeToken", "challenge_token"),
    message: firstString(payload, "message", "detail", "hint"),
    redirect: firstString(payload, "redirect"),
    setupRequired:
      firstBoolean(payload, "setup_required", "setupRequired", "two_factor_setup_required") === true,
    twoFactorRequired,
  };
}

export async function getSession(): Promise<AuthSession> {
  try {
    return sessionFromPayload(await requestJson("/api/auth/session"));
  } catch (error) {
    if (error instanceof AuthApiError && (error.status === 401 || error.status === 403)) {
      return { authenticated: false, user: null };
    }
    throw error;
  }
}

export async function login(email: string, password: string): Promise<LoginResult> {
  const payload = await requestJson("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  return loginResultFromPayload(payload);
}

export async function verifyTwoFactor(input: {
  email: string;
  code: string;
  challengeToken: string | null;
}): Promise<LoginResult> {
  const payload = await requestJson("/api/auth/2fa/login/verify", {
    method: "POST",
    body: JSON.stringify({
      email: input.email,
      code: input.code,
      ...(input.challengeToken
        ? {
            challengeToken: input.challengeToken,
            challenge_token: input.challengeToken,
          }
        : {}),
    }),
  });
  return loginResultFromPayload(payload);
}

export async function logout(): Promise<void> {
  await requestJson("/api/auth/logout", {
    method: "POST",
    body: JSON.stringify({}),
  });
}

export async function requestPasswordReset(email: string): Promise<void> {
  await requestJson("/api/auth/forgot-password", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

export async function resetPassword(input: {
  email: string | null;
  newPassword: string;
  token: string;
}): Promise<void> {
  await requestJson("/api/auth/reset-password", {
    method: "POST",
    body: JSON.stringify({
      token: input.token,
      newPassword: input.newPassword,
      ...(input.email ? { email: input.email } : {}),
    }),
  });
}


export type TrialRegistrationInput = {
  name: string;
  email: string;
  password: string;
  phone?: string;
  consent: boolean;
};

export type TrialRegistrationResult = {
  ok: boolean;
  message: string | null;
  redirect: string | null;
  status: string | null;
};

export async function registerTrial(
  input: TrialRegistrationInput,
): Promise<TrialRegistrationResult> {
  const name = input.name.trim();
  const email = input.email.trim();
  const phone = input.phone?.trim() ?? "";

  const payload = await requestJson("/api/trial/register", {
    method: "POST",
    body: JSON.stringify({
      name,
      full_name: name,
      email,
      password: input.password,
      ...(phone ? { phone } : {}),
      consent: input.consent,
      source: "sovereign-ui",
    }),
  });

  return {
    ok: firstBoolean(payload, "ok", "success", "created") ?? true,
    message: firstString(payload, "message", "detail", "hint"),
    redirect: firstString(payload, "redirect", "login_url", "loginUrl"),
    status: firstString(payload, "status", "account_status", "accountStatus"),
  };
}

export function internalClientPath(value: string | null | undefined): string | null {
  if (!value) return null;
  try {
    const url = new URL(value, window.location.origin);
    if (url.origin !== window.location.origin) return null;
    const path = `${url.pathname}${url.search}${url.hash}`;
    if (!path.startsWith("/") || path.startsWith("//")) return null;
    return path;
  } catch {
    return null;
  }
}

export function authErrorMessage(error: unknown): string {
  return error instanceof AuthApiError
    ? error.message
    : "حدث خطأ غير متوقع أثناء التحقق من الحساب.";
}
