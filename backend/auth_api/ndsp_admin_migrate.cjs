require('dotenv').config();
const { Pool } = require('pg');

const connectionString =
  process.env.DATABASE_URL ||
  process.env.POSTGRES_URL ||
  process.env.POSTGRES_URI ||
  process.env.PG_CONNECTION_STRING ||
  'postgresql://postgres:postgres@127.0.0.1:5432/postgres';

const pool = new Pool({ connectionString });

async function main() {
  await pool.query('BEGIN');

  await pool.query(`
    CREATE TABLE IF NOT EXISTS public.ndsp_plans (
      id SERIAL PRIMARY KEY,
      code TEXT UNIQUE NOT NULL,
      name TEXT NOT NULL,
      price NUMERIC(12,2) NOT NULL DEFAULT 0,
      description TEXT NOT NULL DEFAULT '',
      trial_days INTEGER NOT NULL DEFAULT 16,
      features JSONB NOT NULL DEFAULT '[]'::jsonb,
      limits JSONB NOT NULL DEFAULT '{}'::jsonb,
      is_active BOOLEAN NOT NULL DEFAULT TRUE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );

    CREATE TABLE IF NOT EXISTS public.ndsp_layers (
      id SERIAL PRIMARY KEY,
      code TEXT UNIQUE NOT NULL,
      name TEXT NOT NULL,
      description TEXT NOT NULL DEFAULT '',
      is_visible BOOLEAN NOT NULL DEFAULT TRUE,
      is_sovereign BOOLEAN NOT NULL DEFAULT FALSE,
      sort_order INTEGER NOT NULL DEFAULT 0,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );

    CREATE TABLE IF NOT EXISTS public.ndsp_plan_layers (
      plan_id INTEGER NOT NULL REFERENCES public.ndsp_plans(id) ON DELETE CASCADE,
      layer_id INTEGER NOT NULL REFERENCES public.ndsp_layers(id) ON DELETE CASCADE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      PRIMARY KEY (plan_id, layer_id)
    );

    CREATE TABLE IF NOT EXISTS public.ndsp_assets (
      code TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      is_active BOOLEAN NOT NULL DEFAULT TRUE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );

    CREATE TABLE IF NOT EXISTS public.ndsp_settings (
      key TEXT PRIMARY KEY,
      value JSONB NOT NULL,
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );

    CREATE TABLE IF NOT EXISTS public.ndsp_discount_codes (
      id SERIAL PRIMARY KEY,
      code TEXT UNIQUE NOT NULL,
      percent NUMERIC(6,2) NOT NULL DEFAULT 0,
      amount NUMERIC(12,2) NOT NULL DEFAULT 0,
      is_active BOOLEAN NOT NULL DEFAULT TRUE,
      expires_at TIMESTAMPTZ NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );

    CREATE TABLE IF NOT EXISTS public.ndsp_audit_log (
      id BIGSERIAL PRIMARY KEY,
      actor_user_id TEXT NULL,
      actor_email TEXT NULL,
      action TEXT NOT NULL,
      entity TEXT NOT NULL,
      entity_id TEXT NULL,
      before_data JSONB NULL,
      after_data JSONB NULL,
      ip TEXT NULL,
      user_agent TEXT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
  `);

  await pool.query(`
    INSERT INTO public.ndsp_plans
      (code, name, price, description, trial_days, features, limits, is_active)
    VALUES
      ('trial', 'التجربة', 0, 'تجربة مجانية لمدة 16 يوم', 16, '["دخول أساسي", "استبيان نهاية التجربة"]', '{"assets":3,"layers":"basic"}', TRUE),
      ('basic', 'Basic', 19, 'باقة أساسية للمستخدمين الجدد', 16, '["BTC", "ETH", "GOLD", "طبقات أساسية"]', '{"assets":3,"layers":"basic"}', TRUE),
      ('pro', 'Pro', 49, 'باقة احترافية تشمل معظم الطبقات والأصول', 16, '["BTC", "ETH", "XRP", "SOL", "GOLD", "NASDAQ", "طبقات متقدمة"]', '{"assets":6,"layers":"advanced"}', TRUE),
      ('sovereign', 'Sovereign', 149, 'باقة سيادية للطبقات الحساسة', 16, '["كل الأصول", "كل الطبقات", "صلاحيات سيادية"]', '{"assets":"all","layers":"all"}', TRUE)
    ON CONFLICT (code) DO UPDATE SET
      name = EXCLUDED.name,
      description = EXCLUDED.description,
      updated_at = now();

    INSERT INTO public.ndsp_layers
      (code, name, description, is_visible, is_sovereign, sort_order)
    VALUES
      ('market_pulse', 'Market Pulse', 'طبقة قراءة نبض السوق', TRUE, FALSE, 10),
      ('liquidity', 'Liquidity', 'طبقة السيولة ومناطق التجميع', TRUE, FALSE, 20),
      ('risk', 'Risk Engine', 'طبقة إدارة المخاطر', TRUE, FALSE, 30),
      ('macro', 'Macro View', 'طبقة الرؤية الاقتصادية الكلية', TRUE, FALSE, 40),
      ('sovereign_core', 'Sovereign Core', 'طبقة سيادية محمية', FALSE, TRUE, 100),
      ('admin_intel', 'Admin Intelligence', 'طبقة إدارية داخلية', FALSE, TRUE, 110)
    ON CONFLICT (code) DO UPDATE SET
      name = EXCLUDED.name,
      description = EXCLUDED.description,
      updated_at = now();

    INSERT INTO public.ndsp_assets
      (code, name, is_active)
    VALUES
      ('BTC', 'Bitcoin', TRUE),
      ('ETH', 'Ethereum', TRUE),
      ('XRP', 'Ripple XRP', TRUE),
      ('SOL', 'Solana', TRUE),
      ('GOLD', 'Gold', TRUE),
      ('NASDAQ', 'Nasdaq', TRUE)
    ON CONFLICT (code) DO UPDATE SET
      name = EXCLUDED.name,
      updated_at = now();
  `);

  await pool.query(`
    INSERT INTO public.ndsp_plan_layers (plan_id, layer_id)
    SELECT p.id, l.id
    FROM public.ndsp_plans p
    JOIN public.ndsp_layers l ON (
      (p.code IN ('trial','basic') AND l.code IN ('market_pulse','risk')) OR
      (p.code = 'pro' AND l.code IN ('market_pulse','liquidity','risk','macro')) OR
      (p.code = 'sovereign')
    )
    ON CONFLICT DO NOTHING;
  `);

  await pool.query(`
    INSERT INTO public.ndsp_settings (key, value)
    VALUES
      ('official_email', to_jsonb('support@ndsp.app'::text)),
      ('trial_days', to_jsonb(16::int)),
      ('registration_enabled', to_jsonb(true)),
      ('payment_enabled', to_jsonb(false)),
      ('welcome_subject', to_jsonb('مرحباً بك في NDSP'::text)),
      ('welcome_message', to_jsonb('أهلاً بك في منصة NDSP. تم تفعيل تجربتك لمدة 16 يوم.'::text))
    ON CONFLICT (key) DO NOTHING;
  `);

  await pool.query(`
    DO $$
    DECLARE
      plan_col_exists BOOLEAN;
      plan_col_type TEXT;
    BEGIN
      IF to_regclass('public.users') IS NOT NULL THEN
        ALTER TABLE public.users ADD COLUMN IF NOT EXISTS role TEXT NOT NULL DEFAULT 'user';
        ALTER TABLE public.users ADD COLUMN IF NOT EXISTS status TEXT NOT NULL DEFAULT 'active';
        ALTER TABLE public.users ADD COLUMN IF NOT EXISTS trial_ends_at TIMESTAMPTZ NULL;

        SELECT EXISTS (
          SELECT 1 FROM information_schema.columns
          WHERE table_schema='public' AND table_name='users' AND column_name='plan_id'
        ) INTO plan_col_exists;

        IF plan_col_exists THEN
          SELECT udt_name INTO plan_col_type
          FROM information_schema.columns
          WHERE table_schema='public' AND table_name='users' AND column_name='plan_id';

          IF plan_col_type NOT IN ('int4','int8') THEN
            ALTER TABLE public.users ADD COLUMN IF NOT EXISTS ndsp_plan_id INTEGER NULL;
          END IF;
        ELSE
          ALTER TABLE public.users ADD COLUMN IF NOT EXISTS plan_id INTEGER NULL;
        END IF;

        IF EXISTS (
          SELECT 1 FROM information_schema.columns
          WHERE table_schema='public' AND table_name='users' AND column_name='plan_id' AND udt_name IN ('int4','int8')
        ) THEN
          IF NOT EXISTS (
            SELECT 1 FROM pg_constraint WHERE conname='users_plan_id_ndsp_plans_fk'
          ) THEN
            BEGIN
              ALTER TABLE public.users
              ADD CONSTRAINT users_plan_id_ndsp_plans_fk
              FOREIGN KEY (plan_id) REFERENCES public.ndsp_plans(id) ON DELETE SET NULL;
            EXCEPTION WHEN others THEN
              NULL;
            END;
          END IF;

          UPDATE public.users
          SET plan_id = (SELECT id FROM public.ndsp_plans WHERE code='trial' LIMIT 1)
          WHERE plan_id IS NULL;
        END IF;

        IF EXISTS (
          SELECT 1 FROM information_schema.columns
          WHERE table_schema='public' AND table_name='users' AND column_name='ndsp_plan_id'
        ) THEN
          UPDATE public.users
          SET ndsp_plan_id = (SELECT id FROM public.ndsp_plans WHERE code='trial' LIMIT 1)
          WHERE ndsp_plan_id IS NULL;
        END IF;

        IF NOT EXISTS (SELECT 1 FROM public.users WHERE role='admin') THEN
          EXECUTE 'UPDATE public.users SET role=''admin'' WHERE ctid = (SELECT ctid FROM public.users ORDER BY ctid LIMIT 1)';
        END IF;
      END IF;
    END $$;
  `);

  await pool.query('COMMIT');
  console.log('✅ PostgreSQL migration completed');
}

main()
  .catch(async (err) => {
    try { await pool.query('ROLLBACK'); } catch (_) {}
    console.error('❌ Migration failed:', err);
    process.exit(1);
  })
  .finally(() => pool.end());
