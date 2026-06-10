const express = require('express');
const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
  connectionString:
    process.env.DATABASE_URL ||
    process.env.POSTGRES_URL ||
    process.env.POSTGRES_URI ||
    process.env.PG_CONNECTION_STRING ||
    'postgresql://postgres:postgres@127.0.0.1:5432/postgres'
});

async function getSetting(key, fallback) {
  try {
    const r = await pool.query(
      `SELECT value FROM public.ndsp_settings WHERE key=$1 LIMIT 1`,
      [key]
    );
    return r.rows[0] ? r.rows[0].value : fallback;
  } catch (_) {
    return fallback;
  }
}

async function compatiblePlanColumn() {
  const r = await pool.query(`
    SELECT column_name, udt_name
    FROM information_schema.columns
    WHERE table_schema='public' AND table_name='users'
  `);

  const cols = new Map(r.rows.map(x => [x.column_name, x.udt_name]));

  if (cols.has('ndsp_plan_id')) return 'ndsp_plan_id';
  if (cols.has('plan_id') && ['int4', 'int8'].includes(cols.get('plan_id'))) return 'plan_id';
  return null;
}

function installTrialInfo(app) {
  const router = express.Router();

  router.get('/trial/info', async (_req, res) => {
    try {
      const enabled = await getSetting('trial_welcome_enabled', true);
      const trialDays = Number(await getSetting('trial_days', 16));
      const planCode = String(await getSetting('trial_plan_code', 'trial'));
      const seatsLimit = Number(await getSetting('trial_seats_limit', 300));

      const planRes = await pool.query(`
        SELECT id, code, name, price, description, trial_days, features, limits, is_active
        FROM public.ndsp_plans
        WHERE lower(code)=lower($1)
        LIMIT 1
      `, [planCode]);

      const plan = planRes.rows[0] || {
        id: null,
        code: 'trial',
        name: 'التجربة',
        price: '0.00',
        description: 'تجربة مجانية لمدة 16 يوم',
        trial_days: trialDays,
        features: ['دخول أساسي', 'استبيان نهاية التجربة'],
        limits: { assets: 3, layers: 'basic' },
        is_active: true
      };

      let usedSeats = 0;

      try {
        const planCol = await compatiblePlanColumn();

        if (planCol && plan.id) {
          const r = await pool.query(`
            SELECT COUNT(*)::int AS count
            FROM public.users
            WHERE ${planCol}=$1
          `, [plan.id]);
          usedSeats = r.rows[0]?.count || 0;
        } else {
          const r = await pool.query(`
            SELECT COUNT(*)::int AS count
            FROM public.users
          `);
          usedSeats = r.rows[0]?.count || 0;
        }
      } catch (_) {}

      const remainingSeats = Math.max(seatsLimit - usedSeats, 0);

      res.json({
        enabled,
        trial_days: trialDays,
        plan,
        goal_title: await getSetting('trial_goal_title', 'الهدف من تجربة NDSP'),
        goal_message: await getSetting(
          'trial_goal_message',
          'تجربة NDSP لمدة 16 يوم تهدف إلى قياس جودة المنصة قبل الإطلاق المدفوع.'
        ),
        survey_required: true,
        survey_message: await getSetting(
          'trial_survey_message',
          'عند نهاية فترة التجربة سيظهر لك استبيان قصير لتقييم التجربة.'
        ),
        seats: {
          limited: true,
          limit: seatsLimit,
          used: usedSeats,
          remaining: remainingSeats,
          message: await getSetting(
            'trial_limited_seats_message',
            'المقاعد التجريبية محدودة لضمان جودة المتابعة.'
          )
        }
      });
    } catch (err) {
      console.error('trial info error:', err);
      res.status(500).json({
        error: 'TRIAL_INFO_ERROR',
        message: err.message
      });
    }
  });

  app.use('/api', router);

  console.log('✅ NDSP trial info route mounted: /api/trial/info');
}

module.exports = { installTrialInfo };
