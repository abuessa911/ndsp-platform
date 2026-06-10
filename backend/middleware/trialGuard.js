'use strict';

/**
 * NDSP Trial Guard
 * Purpose:
 * - Build safe UI state for authenticated users.
 * - Treat trial users as Elite Trial users.
 * - Keep payment visibility disabled during active trial.
 *
 * Important:
 * - This middleware is not the only protection.
 * - Payment creation must also be blocked from backend routes.
 */

function safeDate(value) {
  if (!value) return null;
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? null : d;
}

function addDays(date, days) {
  const d = new Date(date);
  d.setDate(d.getDate() + Number(days || 0));
  return d;
}

function normalizePlan(value) {
  return String(value || '').trim().toLowerCase();
}

function isTrialPlan(plan) {
  const p = normalizePlan(plan);
  return p === 'trial' || p === 'elite_trial' || p === 'elite-trial' || p === 'elite trial';
}

function formatDateAR(date) {
  if (!date) return null;
  try {
    return date.toLocaleDateString('ar-SA');
  } catch (_) {
    return date.toISOString().slice(0, 10);
  }
}

async function getColumns(pool, table) {
  const result = await pool.query(
    `SELECT column_name
     FROM information_schema.columns
     WHERE table_schema='public' AND table_name=$1`,
    [table]
  );

  return new Set(result.rows.map(r => r.column_name));
}

async function getUserTrialRecord(pool, user) {
  if (!pool || !user) return null;

  const userId = user.id || user.user_id || user.sub || null;
  const email = user.email || null;

  try {
    const userCols = await getColumns(pool, 'users');

    const fields = ['id', 'email', 'role']
      .concat(['plan', 'plan_code', 'subscription_plan', 'current_plan', 'trial_ends_at', 'trial_end', 'trial_end_date', 'created_at', 'updated_at']
      .filter(c => userCols.has(c)));

    if (fields.length > 0) {
      let where = null;
      let params = [];

      if (userId && userCols.has('id')) {
        where = 'id::text = $1::text';
        params = [String(userId)];
      } else if (email && userCols.has('email')) {
        where = 'lower(email)=lower($1)';
        params = [email];
      }

      if (where) {
        const q = `SELECT ${fields.map(f => `"${f}"`).join(', ')} FROM users WHERE ${where} LIMIT 1`;
        const result = await pool.query(q, params);
        if (result.rows[0]) return result.rows[0];
      }
    }
  } catch (_) {
    return null;
  }

  return null;
}

function buildUIState(user, dbUser) {
  const subscription = user && user.subscription ? user.subscription : {};

  const plan =
    subscription.plan ||
    subscription.plan_code ||
    subscription.code ||
    dbUser?.plan ||
    dbUser?.plan_code ||
    dbUser?.subscription_plan ||
    dbUser?.current_plan ||
    user?.plan ||
    user?.plan_code ||
    'trial';

  const trialDays = 16;

  const createdAt =
    safeDate(subscription.createdAt) ||
    safeDate(subscription.trial_started_at) ||
    safeDate(subscription.activated_at) ||
    safeDate(dbUser?.trial_started_at) ||
    safeDate(dbUser?.activated_at) ||
    safeDate(user?.trial_started_at) ||
    safeDate(user?.activated_at) ||
    safeDate(subscription.created_at) ||
    safeDate(user?.created_at) ||
    safeDate(dbUser?.created_at) ||
    new Date();

  const explicitTrialEnd =
    safeDate(subscription.trialEndDate) ||
    safeDate(subscription.trial_end_date) ||
    safeDate(subscription.trial_ends_at) ||
    safeDate(dbUser?.trial_end_date) ||
    safeDate(dbUser?.trial_ends_at) ||
    safeDate(dbUser?.trial_end);

  const trialEnd = explicitTrialEnd || addDays(createdAt, trialDays);
  const now = new Date();
  const daysLeftRaw = Math.ceil((trialEnd.getTime() - now.getTime()) / 86400000);
  const daysLeft = daysLeftRaw > 0 ? daysLeftRaw : 0;

  const trialUser = isTrialPlan(plan);

  return {
    isTrialUser: trialUser,
    plan: trialUser ? 'elite_trial' : String(plan || ''),
    showPayment: !trialUser,
    showPricing: !trialUser,
    showUpgrade: !trialUser,
    showTrialBadge: trialUser,
    daysLeft,
    trialEnd: formatDateAR(trialEnd),
    showFeedbackPrompt: trialUser && daysLeft <= 2,
    allEliteAccess: trialUser,
    paymentLockedReason: trialUser ? 'trial_active' : null
  };
}

function createTrialGuard(pool) {
  return async function trialGuard(req, res, next) {
    try {
      const user = req.user;

      if (!user) {
        req.uiState = {
          isTrialUser: false,
          showPayment: false,
          showPricing: true,
          showUpgrade: false,
          showTrialBadge: false,
          daysLeft: 0,
          trialEnd: null,
          showFeedbackPrompt: false,
          allEliteAccess: false
        };
        return next();
      }

      const dbUser = await getUserTrialRecord(pool, user);
      req.uiState = buildUIState(user, dbUser);
      return next();
    } catch (err) {
      console.error('[NDSP_TRIAL_GUARD_ERROR]', err && err.message ? err.message : err);

      req.uiState = {
        isTrialUser: true,
        plan: 'elite_trial',
        showPayment: false,
        showPricing: false,
        showUpgrade: false,
        showTrialBadge: true,
        daysLeft: 0,
        trialEnd: null,
        showFeedbackPrompt: false,
        allEliteAccess: true,
        paymentLockedReason: 'trial_guard_fallback'
      };

      return next();
    }
  };
}

module.exports = createTrialGuard;
