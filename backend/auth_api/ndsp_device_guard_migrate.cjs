require('dotenv').config();
const { Pool } = require('pg');

const pool = new Pool({
  connectionString:
    process.env.DATABASE_URL ||
    process.env.POSTGRES_URL ||
    process.env.POSTGRES_URI ||
    process.env.PG_CONNECTION_STRING ||
    'postgresql://postgres:postgres@127.0.0.1:5432/postgres'
});

async function main() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS public.ndsp_registration_locks (
      id BIGSERIAL PRIMARY KEY,
      email TEXT NOT NULL,
      user_id TEXT NULL,
      ip_hash TEXT NULL,
      fingerprint_hash TEXT NULL,
      ip_masked TEXT NULL,
      user_agent TEXT NULL,
      source_path TEXT NULL,
      is_active BOOLEAN NOT NULL DEFAULT TRUE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS ndsp_registration_locks_email_idx
      ON public.ndsp_registration_locks (lower(email));

    CREATE UNIQUE INDEX IF NOT EXISTS ndsp_registration_locks_ip_hash_unique
      ON public.ndsp_registration_locks (ip_hash)
      WHERE ip_hash IS NOT NULL AND is_active = TRUE;

    CREATE UNIQUE INDEX IF NOT EXISTS ndsp_registration_locks_fingerprint_hash_unique
      ON public.ndsp_registration_locks (fingerprint_hash)
      WHERE fingerprint_hash IS NOT NULL AND is_active = TRUE;

    CREATE TABLE IF NOT EXISTS public.ndsp_registration_guard_audit (
      id BIGSERIAL PRIMARY KEY,
      email TEXT NULL,
      action TEXT NOT NULL,
      reason TEXT NULL,
      ip_masked TEXT NULL,
      source_path TEXT NULL,
      user_agent TEXT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
  `);

  console.log('✅ Device registration guard tables ready');
}

main()
  .catch(err => {
    console.error('❌ Migration failed:', err);
    process.exit(1);
  })
  .finally(() => pool.end());
