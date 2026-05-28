import pg from "pg";

const { Pool } = pg;

if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL is required");
}

export const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 8000
});

export async function query(text, params = []) {
  const startedAt = Date.now();
  try {
    const result = await pool.query(text, params);
    return result;
  } catch (error) {
    error.queryText = text;
    error.queryParams = params;
    throw error;
  } finally {
    const duration = Date.now() - startedAt;
    if (duration > 1500) {
      console.warn("SLOW_QUERY_MS=", duration);
    }
  }
}
