--
-- PostgreSQL database dump
--

\restrict 2OyYMQImzVWiqKEu4BUDIX1FlPbhvMMlVRaCfcd31b9W9rbNdSnZYTOgc6efPlM

-- Dumped from database version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: ndsp_consume_daily_unique_usage(text, text, text, integer, text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_consume_daily_unique_usage(p_subject_key text, p_feature_code text, p_usage_key text, p_limit integer, p_subject_kind text DEFAULT 'user_id'::text) RETURNS TABLE(allowed boolean, used_count integer, remaining integer, already_counted boolean)
    LANGUAGE plpgsql
    AS $_$
DECLARE
  v_exists boolean;
  v_used integer;
BEGIN
  IF p_subject_key IS NULL OR length(p_subject_key) NOT BETWEEN 1 AND 160 THEN
    RAISE EXCEPTION 'INVALID_SUBJECT_KEY';
  END IF;
  IF p_feature_code IS NULL OR p_feature_code !~ '^[a-z0-9][a-z0-9._:-]{1,79}$' THEN
    RAISE EXCEPTION 'INVALID_FEATURE_CODE';
  END IF;
  IF p_usage_key IS NULL OR length(p_usage_key) NOT BETWEEN 1 AND 240 THEN
    RAISE EXCEPTION 'INVALID_USAGE_KEY';
  END IF;
  IF p_limit < 1 THEN
    RAISE EXCEPTION 'INVALID_DAILY_LIMIT';
  END IF;
  IF p_subject_kind NOT IN ('user_id', 'user_hash') THEN
    RAISE EXCEPTION 'INVALID_SUBJECT_KIND';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtext(p_subject_key),
    hashtext(p_feature_code || ':' || CURRENT_DATE::text)
  );

  SELECT EXISTS (
    SELECT 1
      FROM public.ndsp_usage_daily
     WHERE subject_key = p_subject_key
       AND usage_date = CURRENT_DATE
       AND feature_code = p_feature_code
       AND usage_key = p_usage_key
  ) INTO v_exists;

  SELECT count(*)::integer
    INTO v_used
    FROM public.ndsp_usage_daily
   WHERE subject_key = p_subject_key
     AND usage_date = CURRENT_DATE
     AND feature_code = p_feature_code;

  IF NOT v_exists AND v_used >= p_limit THEN
    RETURN QUERY SELECT false, v_used, 0, false;
    RETURN;
  END IF;

  INSERT INTO public.ndsp_usage_daily (
    subject_key, subject_kind, usage_date, feature_code, usage_key
  ) VALUES (
    p_subject_key, p_subject_kind, CURRENT_DATE, p_feature_code, p_usage_key
  )
  ON CONFLICT (subject_key, usage_date, feature_code, usage_key)
  DO UPDATE SET
    last_used_at = now(),
    use_count = public.ndsp_usage_daily.use_count + 1;

  IF NOT v_exists THEN
    v_used := v_used + 1;
  END IF;

  RETURN QUERY SELECT true, v_used, GREATEST(p_limit - v_used, 0), v_exists;
END;
$_$;


--
-- Name: FUNCTION ndsp_consume_daily_unique_usage(p_subject_key text, p_feature_code text, p_usage_key text, p_limit integer, p_subject_kind text); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.ndsp_consume_daily_unique_usage(p_subject_key text, p_feature_code text, p_usage_key text, p_limit integer, p_subject_kind text) IS 'Atomic unique daily usage gate. Application binding must call this before a limited operation.';


--
-- Name: ndsp_enforce_activation_trial_policy(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_enforce_activation_trial_policy() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  d integer;
  st text;
BEGIN
  d := COALESCE(NEW.trial_days, 16);
  st := UPPER(COALESCE(NEW.status,''));

  IF UPPER(COALESCE(NEW.role,'')) = 'ADMIN' THEN
    RETURN NEW;
  END IF;

  IF st IN ('PENDING_REVIEW','PENDING_ADMIN_REVIEW') THEN
    NEW.status := 'PENDING_REVIEW';
    NEW.email_verified := false;
    NEW.activated_at := NULL;
    NEW.trial_started_at := NULL;
    NEW.trial_ends_at := NULL;
    NEW.trial_days := d;
    NEW.trial_day := 1;
    RETURN NEW;
  END IF;

  IF TG_OP = 'INSERT' THEN
    IF st IS NULL OR st = '' OR st IN ('PENDING_EMAIL_VERIFICATION','ACTIVE') THEN
      NEW.status := 'ACTIVE';
      NEW.email_verified := true;
      NEW.trial_days := d;
      NEW.activated_at := COALESCE(NEW.activated_at, NOW());
      NEW.trial_started_at := COALESCE(NEW.trial_started_at, NEW.activated_at, NOW());
      NEW.trial_day := 1;
      NEW.trial_ends_at := COALESCE(NEW.trial_ends_at, NEW.trial_started_at + (d || ' days')::interval);
      RETURN NEW;
    END IF;
  END IF;

  IF TG_OP = 'UPDATE' THEN
    IF UPPER(COALESCE(NEW.status,'')) = 'ACTIVE'
       AND UPPER(COALESCE(OLD.status,'')) <> 'ACTIVE' THEN
      NEW.status := 'ACTIVE';
      NEW.email_verified := true;
      NEW.trial_days := d;
      NEW.activated_at := COALESCE(NEW.activated_at, NOW());
      NEW.trial_started_at := COALESCE(NEW.trial_started_at, NEW.activated_at, NOW());
      NEW.trial_day := 1;
      NEW.trial_ends_at := COALESCE(NEW.trial_ends_at, NEW.trial_started_at + (d || ' days')::interval);
      RETURN NEW;
    END IF;
  END IF;

  RETURN NEW;
END;
$$;


--
-- Name: ndsp_guard_trial_registration_before_activation(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_guard_trial_registration_before_activation() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    IF UPPER(COALESCE(NEW.status::text, '')) IN ('ACTIVE','VERIFIED','EMAIL_VERIFIED') THEN
      NEW.status := 'PENDING_EMAIL_VERIFICATION';
    END IF;

    NEW.trial_started_at := NULL;

    IF to_jsonb(NEW) ? 'trial_ends_at' THEN
      NEW.trial_ends_at := NULL;
    END IF;

    IF to_jsonb(NEW) ? 'activated_at' THEN
      NEW.activated_at := NULL;
    END IF;
  END IF;

  RETURN NEW;
END;
$$;


--
-- Name: ndsp_guard_users_trial_activation(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_guard_users_trial_activation() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  seg TEXT;
  inv_active BOOLEAN;
BEGIN
  seg := COALESCE(NEW.approved_segment, NEW.trial_segment, NEW.account_type, NEW.requested_segment);

  IF seg = 'private_invite' THEN
    IF NEW.invite_code_id IS NULL THEN
      IF COALESCE(NEW.status,'') IN ('ACTIVE','active','APPROVED','approved') THEN
        RAISE EXCEPTION 'NDSP_POLICY_BLOCK_PRIVATE_INVITE_WITHOUT_INVITE_CODE';
      END IF;
    ELSE
      SELECT active INTO inv_active
      FROM invite_codes
      WHERE id = NEW.invite_code_id
        AND segment = 'private_invite'
        AND active = TRUE
        AND (expires_at IS NULL OR expires_at > NOW());

      IF COALESCE(inv_active, FALSE) IS NOT TRUE THEN
        IF COALESCE(NEW.status,'') IN ('ACTIVE','active','APPROVED','approved') THEN
          RAISE EXCEPTION 'NDSP_POLICY_BLOCK_PRIVATE_INVITE_INVALID_OR_INACTIVE_CODE';
        END IF;
      END IF;
    END IF;
  END IF;

  IF seg IN ('professional','academic') THEN
    IF COALESCE(NEW.review_status,'') NOT IN ('APPROVED','approved') THEN
      IF COALESCE(NEW.status,'') IN ('ACTIVE','active','APPROVED','approved') THEN
        RAISE EXCEPTION 'NDSP_POLICY_BLOCK_SPECIALIST_AUTO_ACTIVATION_WITHOUT_REVIEW';
      END IF;
    END IF;
  END IF;

  RETURN NEW;
END;
$$;


--
-- Name: ndsp_phone_canonical(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_phone_canonical(p text) RETURNS text
    LANGUAGE plpgsql IMMUTABLE
    AS $$
DECLARE d text;
BEGIN
  d := regexp_replace(COALESCE(p,''), '[^0-9]+', '', 'g');

  IF d IS NULL OR d = '' THEN
    RETURN NULL;
  END IF;

  IF d LIKE '00966%' THEN
    d := substring(d from 3);
  END IF;

  IF d LIKE '966%' THEN
    RETURN d;
  END IF;

  IF d LIKE '05%' AND length(d)=10 THEN
    RETURN '966' || substring(d from 2);
  END IF;

  IF d LIKE '5%' AND length(d)=9 THEN
    RETURN '966' || d;
  END IF;

  RETURN d;
END;
$$;


--
-- Name: ndsp_set_registration_review_status(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_set_registration_review_status() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF NEW.requested_segment = 'private_invite' THEN
    NEW.review_status := 'PENDING_PRIVATE_INVITE_APPROVAL';
  ELSIF NEW.requested_segment IN ('professional','academic') THEN
    NEW.review_status := 'PENDING_SPECIALIST_REVIEW';
  ELSIF NEW.review_status IS NULL THEN
    NEW.review_status := 'PENDING_REVIEW';
  END IF;

  RETURN NEW;
END;
$$;


--
-- Name: ndsp_start_trial_on_first_login(uuid); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_start_trial_on_first_login(p_user_id uuid) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  UPDATE users
  SET
    trial_started_at = now(),
    trial_ends_at = now() + interval '16 days'
  WHERE id = p_user_id
    AND trial_started_at IS NULL
    AND trial_ends_at IS NULL
    AND UPPER(COALESCE(status,'')) = 'ACTIVE';
END;
$$;


--
-- Name: ndsp_sync_access_guard_credentials_from_users(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_sync_access_guard_credentials_from_users() RETURNS trigger
    LANGUAGE plpgsql SECURITY DEFINER
    SET search_path TO 'public'
    AS $$
BEGIN
  IF NEW.email IS NULL OR btrim(NEW.email) = '' THEN
    RETURN NEW;
  END IF;

  IF NEW.password_hash IS NULL OR btrim(NEW.password_hash) = '' THEN
    RETURN NEW;
  END IF;

  INSERT INTO public.access_guard_credentials (
    user_id,
    email,
    password_hash,
    disabled,
    created_at,
    updated_at
  )
  VALUES (
    NEW.id::text,
    lower(NEW.email),
    NEW.password_hash,
    false,
    NOW(),
    NOW()
  )
  ON CONFLICT (user_id)
  DO UPDATE SET
    email = EXCLUDED.email,
    password_hash = EXCLUDED.password_hash,
    disabled = false,
    updated_at = NOW();

  RETURN NEW;
END;
$$;


--
-- Name: ndsp_sync_user_to_trial_registration(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_sync_user_to_trial_registration() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  j jsonb;
  email_text text;
  role_text text;
  raw_category text;
  category_text text;
  phone_text text;
  name_text text;
  plan_text text;
  invite_code_text text;
  status_text text;
  review_status_text text;
BEGIN
  j := to_jsonb(NEW);

  email_text := lower(trim(coalesce(j->>'email', j->>'email_normalized', '')));

  IF email_text = '' OR position('@' in email_text) = 0 THEN
    RETURN NEW;
  END IF;

  role_text := lower(trim(coalesce(j->>'role', '')));

  IF role_text IN ('admin', 'administrator', 'superadmin', 'owner') THEN
    RETURN NEW;
  END IF;

  raw_category := lower(trim(coalesce(
    j->>'category',
    j->>'trial_category',
    j->>'seat_type',
    j->>'cohort',
    j->>'mode',
    j->>'type',
    ''
  )));

  invite_code_text := nullif(trim(coalesce(
    j->>'invite_code',
    j->>'inviteCode',
    j->>'private_invite_code',
    ''
  )), '');

  IF raw_category ~ '(private|invite|premium|خاص|مميز)' OR invite_code_text IS NOT NULL THEN
    category_text := 'private_invite';
  ELSIF raw_category ~ '(professional|academic|analyst|specialist|متخصص|أكاديمي|محلل)' THEN
    category_text := 'professional';
  ELSE
    category_text := 'ordinary';
  END IF;

  phone_text := nullif(trim(coalesce(
    j->>'phone',
    j->>'phone_e164',
    j->>'mobile',
    j->>'mobile_number',
    ''
  )), '');

  name_text := nullif(trim(coalesce(
    j->>'name',
    j->>'full_name',
    j->>'fullName',
    j->>'display_name',
    j->>'username',
    ''
  )), '');

  plan_text := nullif(trim(coalesce(j->>'plan', 'Elite')), '');

  status_text := upper(trim(coalesce(j->>'status', 'ACTIVE')));

  IF status_text IN ('ACTIVE', 'APPROVED', 'ENABLED') THEN
    status_text := 'ACTIVE';
    review_status_text := 'APPROVED';
  ELSIF status_text IN ('PENDING', 'PENDING_REVIEW', 'PENDING_EMAIL_VERIFICATION') THEN
    review_status_text := 'PENDING_REVIEW';
  ELSE
    review_status_text := 'APPROVED';
  END IF;

  IF EXISTS (
    SELECT 1
    FROM public.ndsp_trial_registrations
    WHERE lower(email) = email_text
       OR lower(email_normalized) = email_text
  ) THEN
    UPDATE public.ndsp_trial_registrations
    SET
      category = category_text,
      email = email_text,
      email_normalized = email_text,
      phone = COALESCE(phone_text, phone),
      phone_e164 = COALESCE(phone_text, phone_e164),
      name = COALESCE(name_text, name),
      plan = COALESCE(plan_text, plan),
      status = status_text,
      invite_code = COALESCE(invite_code_text, invite_code),
      review_status = COALESCE(review_status_text, review_status),
      activated_at = CASE
        WHEN status_text = 'ACTIVE' THEN COALESCE(activated_at, now())
        ELSE activated_at
      END,
      updated_at = now()
    WHERE lower(email) = email_text
       OR lower(email_normalized) = email_text;
  ELSE
    INSERT INTO public.ndsp_trial_registrations (
      category,
      email,
      email_normalized,
      phone,
      phone_e164,
      name,
      plan,
      status,
      invite_code,
      activated_at,
      review_status,
      created_at,
      updated_at
    )
    VALUES (
      category_text,
      email_text,
      email_text,
      phone_text,
      phone_text,
      name_text,
      COALESCE(plan_text, 'Elite'),
      status_text,
      invite_code_text,
      CASE WHEN status_text = 'ACTIVE' THEN now() ELSE NULL END,
      COALESCE(review_status_text, 'APPROVED'),
      COALESCE(NEW.created_at, now()),
      now()
    );
  END IF;

  RETURN NEW;
END;
$$;


--
-- Name: ndsp_users_normalize_identity(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_users_normalize_identity() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.email := lower(trim(NEW.email));
  NEW.canonical_email := lower(trim(NEW.email));
  NEW.canonical_phone := NULLIF(regexp_replace(coalesce(NEW.phone,''),'[^0-9+]','','g'), '');
  RETURN NEW;
END;
$$;


--
-- Name: ndsp_users_phone_unique_guard(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_users_phone_unique_guard() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  c text;
  existing_id text;
BEGIN
  c := ndsp_phone_canonical(NEW.phone);

  IF c IS NULL OR c = '' THEN
    RETURN NEW;
  END IF;

  SELECT id::text
  INTO existing_id
  FROM users
  WHERE ndsp_phone_canonical(phone) = c
    AND id::text <> COALESCE(NEW.id::text, '')
  LIMIT 1;

  IF existing_id IS NOT NULL THEN
    RAISE EXCEPTION 'DUPLICATE_PHONE canonical conflict'
      USING ERRCODE='23505',
            CONSTRAINT='ux_users_phone_canonical_guard',
            DETAIL='DUPLICATE_PHONE';
  END IF;

  RETURN NEW;
END;
$$;


--
-- Name: ndsp_users_trial_activation_guard(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.ndsp_users_trial_activation_guard() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  new_j jsonb;
  old_j jsonb;
  new_active boolean;
  old_active boolean;
BEGIN
  new_j := to_jsonb(NEW);
  old_j := CASE WHEN TG_OP = 'UPDATE' THEN to_jsonb(OLD) ELSE '{}'::jsonb END;

  new_active :=
    upper(coalesce(new_j->>'status','')) IN ('ACTIVE','APPROVED','VERIFIED','EMAIL_VERIFIED')
    OR coalesce(new_j->>'email_verified_at','') <> ''
    OR lower(coalesce(new_j->>'email_verified','')) IN ('true','t','1','yes');

  old_active :=
    upper(coalesce(old_j->>'status','')) IN ('ACTIVE','APPROVED','VERIFIED','EMAIL_VERIFIED')
    OR coalesce(old_j->>'email_verified_at','') <> ''
    OR lower(coalesce(old_j->>'email_verified','')) IN ('true','t','1','yes');

  IF new_active AND ((NOT old_active) OR NEW.trial_started_at IS NULL OR NEW.trial_ends_at IS NULL) THEN
    NEW.activated_at := COALESCE(NEW.activated_at, now());
    NEW.trial_started_at := COALESCE(NEW.trial_started_at, NEW.activated_at);
    NEW.trial_days := COALESCE(NULLIF(NEW.trial_days, 0), 16);
    NEW.trial_ends_at := NEW.trial_started_at + make_interval(days => NEW.trial_days);
  END IF;

  RETURN NEW;
END;
$$;


SET default_table_access_method = heap;

--
-- Name: access_guard_credentials; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_guard_credentials (
    id bigint NOT NULL,
    user_id text NOT NULL,
    email text NOT NULL,
    password_hash text NOT NULL,
    disabled boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: access_guard_credentials_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_guard_credentials_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_guard_credentials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_guard_credentials_id_seq OWNED BY public.access_guard_credentials.id;


--
-- Name: access_guard_sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_guard_sessions (
    id bigint NOT NULL,
    user_id text NOT NULL,
    token_hash text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone DEFAULT (now() + '16:00:00'::interval) NOT NULL,
    revoked boolean DEFAULT false NOT NULL
);


--
-- Name: access_guard_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_guard_sessions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_guard_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_guard_sessions_id_seq OWNED BY public.access_guard_sessions.id;


--
-- Name: admin_audit_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin_audit_log (
    id bigint NOT NULL,
    actor_email text,
    action text NOT NULL,
    entity_type text NOT NULL,
    entity_id text,
    details jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: admin_audit_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.admin_audit_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: admin_audit_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.admin_audit_log_id_seq OWNED BY public.admin_audit_log.id;


--
-- Name: admin_user_disable_backups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin_user_disable_backups (
    id uuid,
    name text,
    email text,
    password_hash text,
    plan text,
    role text,
    trial_day integer,
    trial_started_at timestamp with time zone,
    created_at timestamp with time zone,
    status text,
    trial_ends_at timestamp with time zone,
    plan_id integer,
    category text,
    phone text,
    two_factor_enabled boolean,
    two_factor_secret text,
    two_factor_confirmed_at timestamp with time zone,
    two_factor_setup_required boolean,
    two_factor_skipped_at timestamp with time zone,
    two_factor_last_prompt_at timestamp with time zone,
    requested_segment text,
    approved_segment text,
    trial_segment text,
    account_type text,
    email_verified boolean,
    invite_code_id bigint,
    review_status text,
    activated_at timestamp with time zone,
    trial_days integer,
    canonical_email text,
    canonical_phone text,
    password_reset_token text,
    password_reset_expires_at timestamp with time zone,
    backup_created_at timestamp with time zone,
    backup_reason text
);


--
-- Name: dsp_invite_codes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dsp_invite_codes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    code_hash text NOT NULL,
    code_prefix text NOT NULL,
    segment text DEFAULT 'private_premium'::text NOT NULL,
    max_uses integer DEFAULT 1 NOT NULL,
    used_count integer DEFAULT 0 NOT NULL,
    active boolean DEFAULT true NOT NULL,
    expires_at timestamp with time zone,
    note text
);


--
-- Name: dsp_registration_abuse_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dsp_registration_abuse_log (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    email_hash text,
    phone_hash text,
    ip_hash text,
    device_hash text,
    user_agent_hash text,
    risk_reason text,
    risk_score integer DEFAULT 0,
    decision text DEFAULT 'PENDING_REVIEW'::text
);


--
-- Name: dsp_registration_abuse_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dsp_registration_abuse_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dsp_registration_abuse_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dsp_registration_abuse_log_id_seq OWNED BY public.dsp_registration_abuse_log.id;


--
-- Name: dsp_trial_survey_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dsp_trial_survey_events (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    user_email_hash text,
    event_type text NOT NULL,
    shown boolean DEFAULT false,
    completed boolean DEFAULT false,
    source text DEFAULT 'user_portal'::text
);


--
-- Name: dsp_trial_survey_events_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dsp_trial_survey_events_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dsp_trial_survey_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dsp_trial_survey_events_id_seq OWNED BY public.dsp_trial_survey_events.id;


--
-- Name: email_delivery_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_delivery_log (
    id bigint NOT NULL,
    recipient_email text NOT NULL,
    recipient_type text NOT NULL,
    email_purpose text NOT NULL,
    related_request_id bigint,
    status text DEFAULT 'QUEUED'::text NOT NULL,
    attempt_count integer DEFAULT 0 NOT NULL,
    last_error text,
    provider_message_id text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    sent_at timestamp with time zone,
    CONSTRAINT email_delivery_log_recipient_type_check CHECK ((recipient_type = ANY (ARRAY['admin'::text, 'user'::text]))),
    CONSTRAINT email_delivery_log_status_check CHECK ((status = ANY (ARRAY['QUEUED'::text, 'SENT'::text, 'FAILED'::text, 'RETRYING'::text, 'SKIPPED'::text])))
);


--
-- Name: email_delivery_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.email_delivery_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: email_delivery_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.email_delivery_log_id_seq OWNED BY public.email_delivery_log.id;


--
-- Name: feedback_surveys; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.feedback_surveys (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    user_type text,
    value_answer text,
    clarity_answer text,
    improvement_answer text,
    upgrade_answer text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    discount_status text DEFAULT 'pending'::text NOT NULL,
    admin_note text,
    reviewed_at timestamp with time zone
);


--
-- Name: invite_codes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.invite_codes (
    id bigint NOT NULL,
    code text NOT NULL,
    segment text NOT NULL,
    label text,
    max_uses integer DEFAULT 1 NOT NULL,
    used_count integer DEFAULT 0 NOT NULL,
    active boolean DEFAULT true NOT NULL,
    created_by text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone,
    notes text,
    CONSTRAINT invite_codes_max_uses_check CHECK ((max_uses >= 1)),
    CONSTRAINT invite_codes_segment_check CHECK ((segment = ANY (ARRAY['private_invite'::text, 'professional'::text, 'academic'::text, 'ordinary'::text]))),
    CONSTRAINT invite_codes_used_count_check CHECK ((used_count >= 0))
);


--
-- Name: invite_codes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.invite_codes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: invite_codes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.invite_codes_id_seq OWNED BY public.invite_codes.id;


--
-- Name: ndsp_admin_audit_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_admin_audit_log (
    id uuid NOT NULL,
    actor_role text NOT NULL,
    actor_key_hint text,
    action text NOT NULL,
    scope text DEFAULT 'system'::text NOT NULL,
    request_payload jsonb,
    result jsonb,
    ip_address text,
    user_agent text,
    status text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_admin_runtime_flags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_admin_runtime_flags (
    key text NOT NULL,
    value text NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_assets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_assets (
    id bigint NOT NULL,
    code text NOT NULL,
    name text NOT NULL,
    symbol text NOT NULL,
    name_ar text,
    name_en text,
    category text NOT NULL,
    source text NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_assets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_assets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_assets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_assets_id_seq OWNED BY public.ndsp_assets.id;


--
-- Name: ndsp_assets_legacy_before_clean_rebuild; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_assets_legacy_before_clean_rebuild (
    code text NOT NULL,
    name text NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    symbol text,
    name_ar text,
    name_en text,
    category text,
    source text
);


--
-- Name: ndsp_audit_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_audit_log (
    id bigint NOT NULL,
    actor_user_id text,
    actor_email text,
    action text NOT NULL,
    entity text NOT NULL,
    entity_id text,
    before_data jsonb,
    after_data jsonb,
    ip text,
    user_agent text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_audit_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_audit_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_audit_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_audit_log_id_seq OWNED BY public.ndsp_audit_log.id;


--
-- Name: ndsp_auth_activation_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_auth_activation_tokens (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    token_hash text NOT NULL,
    purpose text DEFAULT 'email_activation'::text NOT NULL,
    used_at timestamp with time zone,
    expires_at timestamp with time zone DEFAULT (now() + '48:00:00'::interval) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_auth_activation_tokens_backup_before_test_20260613_215437; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_auth_activation_tokens_backup_before_test_20260613_215437 (
    id uuid,
    user_id uuid,
    token_hash text,
    purpose text,
    used_at timestamp with time zone,
    expires_at timestamp with time zone,
    created_at timestamp with time zone
);


--
-- Name: ndsp_auth_audit; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_auth_audit (
    id bigint NOT NULL,
    user_id bigint,
    event text NOT NULL,
    detail text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_auth_audit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_auth_audit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_auth_audit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_auth_audit_id_seq OWNED BY public.ndsp_auth_audit.id;


--
-- Name: ndsp_auth_sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_auth_sessions (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    session_hash text NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    ip_address text,
    user_agent text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_auth_users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_auth_users (
    id uuid NOT NULL,
    email text NOT NULL,
    phone text,
    name text,
    plan text DEFAULT 'Elite'::text NOT NULL,
    category text DEFAULT 'ordinary'::text NOT NULL,
    status text DEFAULT 'PENDING_EMAIL_VERIFICATION'::text NOT NULL,
    trial_started_at timestamp with time zone,
    trial_ends_at timestamp with time zone,
    activated_at timestamp with time zone,
    last_login_at timestamp with time zone,
    ip_hash text,
    fingerprint_hash text,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_clean_auth_audit_v2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_clean_auth_audit_v2 (
    id bigint NOT NULL,
    event_type text NOT NULL,
    user_id text,
    email_hash character(64),
    success boolean NOT NULL,
    ip_hash character(64),
    user_agent_hash character(64),
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_clean_auth_audit_v2_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_clean_auth_audit_v2_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_clean_auth_audit_v2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_clean_auth_audit_v2_id_seq OWNED BY public.ndsp_clean_auth_audit_v2.id;


--
-- Name: ndsp_clean_auth_sessions_v2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_clean_auth_sessions_v2 (
    token_hash character(64) NOT NULL,
    user_id text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    revoked_at timestamp with time zone,
    ip_hash character(64),
    user_agent_hash character(64)
);


--
-- Name: ndsp_completed_decisions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_completed_decisions (
    id bigint NOT NULL,
    decision_id text NOT NULL,
    symbol text NOT NULL,
    market text,
    decision_state text DEFAULT 'Draft'::text NOT NULL,
    decision_quality numeric,
    scenario_state text,
    direction_context text,
    activation_level text,
    arrival_level text,
    review_zone text,
    invalidation_level text,
    nmp_zone text,
    risk_status text,
    devil_advocate_status text,
    visibility text DEFAULT 'private'::text NOT NULL,
    payload jsonb DEFAULT '{}'::jsonb NOT NULL,
    disclaimer text NOT NULL,
    completed_at timestamp with time zone,
    published_at timestamp with time zone,
    expires_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_completed_decisions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_completed_decisions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_completed_decisions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_completed_decisions_id_seq OWNED BY public.ndsp_completed_decisions.id;


--
-- Name: ndsp_decision_evidence_snapshots; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_decision_evidence_snapshots (
    evidence_id bigint NOT NULL,
    decision_id text NOT NULL,
    asset_symbol text,
    timeframe text,
    snapshot_kind text DEFAULT 'decision_input'::text NOT NULL,
    contract_version text NOT NULL,
    source_observed_at timestamp with time zone,
    captured_at timestamp with time zone DEFAULT now() NOT NULL,
    payload_sha256 character varying(64) NOT NULL,
    source_manifest jsonb DEFAULT '[]'::jsonb NOT NULL,
    governed_snapshot jsonb DEFAULT '{}'::jsonb NOT NULL,
    visibility text DEFAULT 'governed'::text NOT NULL,
    verification_status text DEFAULT 'captured'::text NOT NULL,
    supersedes_evidence_id bigint,
    CONSTRAINT ndsp_decision_evidence_hash_ck CHECK (((payload_sha256)::text ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT ndsp_decision_evidence_snapshot_ck CHECK ((jsonb_typeof(governed_snapshot) = 'object'::text)),
    CONSTRAINT ndsp_decision_evidence_source_manifest_ck CHECK ((jsonb_typeof(source_manifest) = ANY (ARRAY['array'::text, 'object'::text]))),
    CONSTRAINT ndsp_decision_evidence_status_ck CHECK ((verification_status = ANY (ARRAY['captured'::text, 'verified'::text, 'superseded'::text, 'rejected'::text]))),
    CONSTRAINT ndsp_decision_evidence_visibility_ck CHECK ((visibility = ANY (ARRAY['private'::text, 'governed'::text, 'public'::text])))
);


--
-- Name: ndsp_decision_evidence_snapshots_evidence_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.ndsp_decision_evidence_snapshots ALTER COLUMN evidence_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ndsp_decision_evidence_snapshots_evidence_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ndsp_decision_ledger; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_decision_ledger (
    id bigint NOT NULL,
    symbol text NOT NULL,
    scenario_state text,
    directional_context text,
    decision_quality integer,
    price numeric,
    provider text,
    generated_at timestamp with time zone,
    payload jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_decision_ledger_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_decision_ledger_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_decision_ledger_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_decision_ledger_id_seq OWNED BY public.ndsp_decision_ledger.id;


--
-- Name: ndsp_decision_timeline; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_decision_timeline (
    id bigint NOT NULL,
    decision_id text NOT NULL,
    event_type text NOT NULL,
    event_title text NOT NULL,
    event_detail text,
    event_payload jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_decision_timeline_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_decision_timeline_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_decision_timeline_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_decision_timeline_id_seq OWNED BY public.ndsp_decision_timeline.id;


--
-- Name: ndsp_discount_codes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_discount_codes (
    id integer NOT NULL,
    code text NOT NULL,
    percent numeric(6,2) DEFAULT 0 NOT NULL,
    amount numeric(12,2) DEFAULT 0 NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    expires_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_discount_codes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_discount_codes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_discount_codes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_discount_codes_id_seq OWNED BY public.ndsp_discount_codes.id;


--
-- Name: ndsp_duplicate_phone_audit; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_duplicate_phone_audit (
    id bigint NOT NULL,
    canonical_phone text,
    keeper_user_id text,
    duplicate_user_id text,
    duplicate_email text,
    action text,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: ndsp_duplicate_phone_audit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_duplicate_phone_audit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_duplicate_phone_audit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_duplicate_phone_audit_id_seq OWNED BY public.ndsp_duplicate_phone_audit.id;


--
-- Name: ndsp_email_delivery_queue; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.ndsp_email_delivery_queue AS
 SELECT id,
    recipient_email,
    recipient_type,
    email_purpose,
    related_request_id,
    status,
    attempt_count,
    last_error,
    created_at,
    sent_at
   FROM public.email_delivery_log
  WHERE (status = ANY (ARRAY['QUEUED'::text, 'FAILED'::text, 'RETRYING'::text]))
  ORDER BY created_at;


--
-- Name: ndsp_feedback_entries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_feedback_entries (
    id uuid NOT NULL,
    registration_id text,
    email text,
    category text DEFAULT 'ordinary'::text NOT NULL,
    plan text DEFAULT 'Elite'::text NOT NULL,
    rating integer,
    scenario_clarity integer,
    ease_of_use integer,
    output_quality integer,
    professional_reliability integer,
    message text,
    source text DEFAULT 'final_trial_day'::text NOT NULL,
    status text DEFAULT 'new'::text NOT NULL,
    metadata jsonb,
    ip_address text,
    user_agent text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_feedback_notice_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_feedback_notice_log (
    id uuid NOT NULL,
    registration_id text,
    email text,
    category text DEFAULT 'ordinary'::text NOT NULL,
    notice_type text NOT NULL,
    shown_at timestamp with time zone DEFAULT now() NOT NULL,
    metadata jsonb
);


--
-- Name: ndsp_invitation_codes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_invitation_codes (
    id bigint NOT NULL,
    code text NOT NULL,
    cohort_code text NOT NULL,
    used_by_email text,
    used_at timestamp with time zone,
    created_by text,
    expires_at timestamp with time zone DEFAULT (now() + '30 days'::interval),
    notes text,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: ndsp_invitation_codes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_invitation_codes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_invitation_codes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_invitation_codes_id_seq OWNED BY public.ndsp_invitation_codes.id;


--
-- Name: ndsp_launch_cleanup_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_launch_cleanup_log (
    id bigint NOT NULL,
    cleanup_ts timestamp with time zone DEFAULT now() NOT NULL,
    table_name text NOT NULL,
    deleted_count bigint DEFAULT 0 NOT NULL,
    reason text NOT NULL,
    archive_schema text NOT NULL
);


--
-- Name: ndsp_launch_cleanup_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_launch_cleanup_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_launch_cleanup_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_launch_cleanup_log_id_seq OWNED BY public.ndsp_launch_cleanup_log.id;


--
-- Name: ndsp_layers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_layers (
    id integer NOT NULL,
    code text NOT NULL,
    name text NOT NULL,
    description text DEFAULT ''::text NOT NULL,
    is_visible boolean DEFAULT true NOT NULL,
    is_sovereign boolean DEFAULT false NOT NULL,
    sort_order integer DEFAULT 0 NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_layers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_layers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_layers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_layers_id_seq OWNED BY public.ndsp_layers.id;


--
-- Name: ndsp_legal_acceptances; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_legal_acceptances (
    acceptance_id bigint NOT NULL,
    subject_key text,
    email_sha256 character varying(64) NOT NULL,
    request_id text NOT NULL,
    disclaimer_version text NOT NULL,
    terms_version text NOT NULL,
    privacy_version text NOT NULL,
    acceptance_source text NOT NULL,
    upstream_status smallint,
    user_agent_sha256 character varying(64),
    evidence_sha256 character varying(64) NOT NULL,
    accepted_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone DEFAULT now() NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    CONSTRAINT ndsp_legal_acceptances_agent_hash_ck CHECK (((user_agent_sha256 IS NULL) OR ((user_agent_sha256)::text ~ '^[0-9a-f]{64}$'::text))),
    CONSTRAINT ndsp_legal_acceptances_email_hash_ck CHECK (((email_sha256)::text ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT ndsp_legal_acceptances_evidence_hash_ck CHECK (((evidence_sha256)::text ~ '^[0-9a-f]{64}$'::text)),
    CONSTRAINT ndsp_legal_acceptances_status_ck CHECK (((upstream_status IS NULL) OR ((upstream_status >= 100) AND (upstream_status <= 599)))),
    CONSTRAINT ndsp_legal_acceptances_versions_ck CHECK (((length(disclaimer_version) > 0) AND (length(terms_version) > 0) AND (length(privacy_version) > 0)))
);


--
-- Name: ndsp_legal_acceptances_acceptance_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.ndsp_legal_acceptances ALTER COLUMN acceptance_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ndsp_legal_acceptances_acceptance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ndsp_market_assets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_market_assets (
    id bigint NOT NULL,
    symbol text NOT NULL,
    name_ar text,
    name_en text,
    category text,
    source text,
    is_active boolean DEFAULT true,
    sort_order integer DEFAULT 0,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: ndsp_market_assets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_market_assets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_market_assets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_market_assets_id_seq OWNED BY public.ndsp_market_assets.id;


--
-- Name: ndsp_nowpayments_payments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_nowpayments_payments (
    id bigint NOT NULL,
    order_id text DEFAULT ((('ndsp-pay-'::text || ((EXTRACT(epoch FROM now()))::bigint)::text) || '-'::text) || ((floor((random() * (1000000)::double precision)))::integer)::text) NOT NULL,
    user_id text,
    user_email text,
    plan_id integer,
    plan_code text,
    billing_cycle text DEFAULT 'monthly'::text NOT NULL,
    price_amount numeric(12,2) DEFAULT 0 NOT NULL,
    price_currency text DEFAULT 'usd'::text NOT NULL,
    provider_invoice_id text,
    provider_payment_id text,
    invoice_url text,
    payment_status text DEFAULT 'created'::text NOT NULL,
    raw_create_response jsonb,
    raw_ipn jsonb,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    status text DEFAULT 'pending_review'::text NOT NULL,
    amount numeric,
    currency text DEFAULT 'USDT'::text,
    network text,
    payment_id text,
    raw_payload jsonb DEFAULT '{}'::jsonb NOT NULL
);


--
-- Name: ndsp_nowpayments_payments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_nowpayments_payments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_nowpayments_payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_nowpayments_payments_id_seq OWNED BY public.ndsp_nowpayments_payments.id;


--
-- Name: ndsp_operational_compat_audit; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_operational_compat_audit (
    id integer NOT NULL,
    route text NOT NULL,
    email text,
    payload jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_operational_compat_audit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_operational_compat_audit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_operational_compat_audit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_operational_compat_audit_id_seq OWNED BY public.ndsp_operational_compat_audit.id;


--
-- Name: ndsp_payment_audit; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_payment_audit (
    id bigint NOT NULL,
    provider text NOT NULL,
    event_type text NOT NULL,
    order_id text,
    payment_status text,
    payload jsonb,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_payment_audit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_payment_audit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_payment_audit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_payment_audit_id_seq OWNED BY public.ndsp_payment_audit.id;


--
-- Name: ndsp_plan_layers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_plan_layers (
    plan_id integer NOT NULL,
    layer_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_plans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_plans (
    id integer NOT NULL,
    code text NOT NULL,
    name text NOT NULL,
    price numeric(12,2) DEFAULT 0 NOT NULL,
    description text DEFAULT ''::text NOT NULL,
    trial_days integer DEFAULT 16 NOT NULL,
    features jsonb DEFAULT '[]'::jsonb NOT NULL,
    limits jsonb DEFAULT '{}'::jsonb NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_plans_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_plans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_plans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_plans_id_seq OWNED BY public.ndsp_plans.id;


--
-- Name: ndsp_portal_readings_cache; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_portal_readings_cache (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    page_type text NOT NULL,
    symbol text NOT NULL,
    timeframe text NOT NULL,
    source_service text,
    payload jsonb NOT NULL,
    status text DEFAULT 'configured'::text NOT NULL,
    generated_by text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    expires_at timestamp with time zone,
    CONSTRAINT ndsp_portal_readings_cache_page_type_chk CHECK ((page_type = ANY (ARRAY['asset-view'::text, 'daily-brief'::text, 'command-center'::text]))),
    CONSTRAINT ndsp_portal_readings_cache_status_chk CHECK ((status = ANY (ARRAY['configured'::text, 'not_configured'::text, 'stale'::text]))),
    CONSTRAINT ndsp_portal_readings_cache_timeframe_chk CHECK ((timeframe = ANY (ARRAY['daily'::text, 'weekly'::text, 'monthly'::text, 'none'::text])))
);


--
-- Name: ndsp_premium_trial_invites; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_premium_trial_invites (
    id bigint NOT NULL,
    code text NOT NULL,
    email text,
    label text,
    max_uses integer DEFAULT 1 NOT NULL,
    used_count integer DEFAULT 0 NOT NULL,
    status text DEFAULT 'active'::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone,
    created_by text DEFAULT 'admin'::text,
    used_by_email text,
    used_at timestamp with time zone,
    last_used_ip text,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    CONSTRAINT ndsp_premium_trial_invites_max_uses_check CHECK ((max_uses >= 1)),
    CONSTRAINT ndsp_premium_trial_invites_used_count_check CHECK ((used_count >= 0))
);


--
-- Name: ndsp_premium_trial_invites_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_premium_trial_invites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_premium_trial_invites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_premium_trial_invites_id_seq OWNED BY public.ndsp_premium_trial_invites.id;


--
-- Name: ndsp_price_cache; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_price_cache (
    symbol text NOT NULL,
    price numeric(20,8),
    change_24h numeric(14,6),
    change_pct numeric(10,4),
    high_24h numeric(20,8),
    low_24h numeric(20,8),
    volume numeric(30,4),
    source text,
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: ndsp_private_invite_codes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_private_invite_codes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    code text NOT NULL,
    status text DEFAULT 'ACTIVE'::text NOT NULL,
    used_by uuid,
    used_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_product_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_product_events (
    product_event_id bigint NOT NULL,
    subject_key text,
    session_key text,
    event_name text NOT NULL,
    plan_code text,
    occurred_at timestamp with time zone DEFAULT now() NOT NULL,
    properties jsonb DEFAULT '{}'::jsonb NOT NULL,
    CONSTRAINT ndsp_product_events_name_ck CHECK ((event_name ~ '^[a-z0-9][a-z0-9._:-]{1,79}$'::text)),
    CONSTRAINT ndsp_product_events_properties_ck CHECK ((jsonb_typeof(properties) = 'object'::text))
);


--
-- Name: ndsp_product_events_product_event_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.ndsp_product_events ALTER COLUMN product_event_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ndsp_product_events_product_event_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ndsp_provider_health_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_provider_health_history (
    provider_health_id bigint NOT NULL,
    provider_code text NOT NULL,
    market_code text,
    asset_symbol text,
    health_status text NOT NULL,
    latency_ms integer,
    freshness_seconds integer,
    failure_code text,
    contract_version text,
    observed_at timestamp with time zone DEFAULT now() NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    CONSTRAINT ndsp_provider_health_freshness_ck CHECK (((freshness_seconds IS NULL) OR (freshness_seconds >= 0))),
    CONSTRAINT ndsp_provider_health_latency_ck CHECK (((latency_ms IS NULL) OR (latency_ms >= 0))),
    CONSTRAINT ndsp_provider_health_status_ck CHECK ((health_status = ANY (ARRAY['healthy'::text, 'degraded'::text, 'stale'::text, 'unavailable'::text, 'unknown'::text])))
);


--
-- Name: ndsp_provider_health_history_provider_health_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.ndsp_provider_health_history ALTER COLUMN provider_health_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ndsp_provider_health_history_provider_health_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ndsp_registration_email_dispatch; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_registration_email_dispatch (
    user_id uuid NOT NULL,
    user_email text NOT NULL,
    user_sent_at timestamp with time zone,
    owner_sent_at timestamp with time zone,
    attempts integer DEFAULT 0 NOT NULL,
    last_error text,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_registration_guard_audit; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_registration_guard_audit (
    id bigint NOT NULL,
    email text,
    action text NOT NULL,
    reason text,
    ip_masked text,
    source_path text,
    user_agent text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_registration_guard_audit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_registration_guard_audit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_registration_guard_audit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_registration_guard_audit_id_seq OWNED BY public.ndsp_registration_guard_audit.id;


--
-- Name: ndsp_registration_locks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_registration_locks (
    id bigint NOT NULL,
    email text NOT NULL,
    user_id text,
    ip_hash text,
    fingerprint_hash text,
    ip_masked text,
    user_agent text,
    source_path text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_registration_locks_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_registration_locks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_registration_locks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_registration_locks_id_seq OWNED BY public.ndsp_registration_locks.id;


--
-- Name: registration_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registration_requests (
    id bigint NOT NULL,
    email text NOT NULL,
    full_name text,
    phone text,
    requested_segment text DEFAULT 'ordinary'::text NOT NULL,
    approved_segment text,
    review_status text DEFAULT 'PENDING_REVIEW'::text NOT NULL,
    invite_code text,
    invite_code_id bigint,
    professional_context text,
    academic_context text,
    social_or_work_profile text,
    admin_notes text,
    ip_hash text,
    device_hash text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    reviewed_at timestamp with time zone,
    reviewed_by text,
    CONSTRAINT registration_requests_approved_segment_check CHECK ((approved_segment = ANY (ARRAY['ordinary'::text, 'professional'::text, 'academic'::text, 'private_invite'::text]))),
    CONSTRAINT registration_requests_requested_segment_check CHECK ((requested_segment = ANY (ARRAY['ordinary'::text, 'professional'::text, 'academic'::text, 'private_invite'::text]))),
    CONSTRAINT registration_requests_review_status_check CHECK ((review_status = ANY (ARRAY['PENDING_REVIEW'::text, 'PENDING_SPECIALIST_REVIEW'::text, 'PENDING_PRIVATE_INVITE_APPROVAL'::text, 'APPROVED'::text, 'REJECTED'::text, 'EXPIRED'::text])))
);


--
-- Name: ndsp_registration_review_queue; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.ndsp_registration_review_queue AS
 SELECT id,
    email,
    full_name,
    phone,
    requested_segment,
    approved_segment,
    review_status,
    invite_code,
    professional_context,
    academic_context,
    social_or_work_profile,
    created_at,
    reviewed_at,
    reviewed_by
   FROM public.registration_requests
  WHERE (review_status = ANY (ARRAY['PENDING_REVIEW'::text, 'PENDING_SPECIALIST_REVIEW'::text, 'PENDING_PRIVATE_INVITE_APPROVAL'::text]))
  ORDER BY created_at DESC;


--
-- Name: ndsp_schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_schema_migrations (
    migration_key text NOT NULL,
    applied_at timestamp with time zone DEFAULT now() NOT NULL,
    checksum_sha256 character varying(64) NOT NULL,
    release_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    CONSTRAINT ndsp_schema_migrations_checksum_ck CHECK (((checksum_sha256)::text ~ '^[0-9a-f]{64}$'::text))
);


--
-- Name: ndsp_seats_status; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.ndsp_seats_status AS
SELECT
    NULL::text AS code,
    NULL::text AS name_ar,
    NULL::text AS name_en,
    NULL::integer AS total_seats,
    NULL::integer AS used_seats,
    NULL::integer AS available_seats,
    NULL::numeric AS fill_pct;


--
-- Name: ndsp_sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_sessions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    token_hash text NOT NULL,
    status text DEFAULT 'active'::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    last_seen_at timestamp with time zone
);


--
-- Name: ndsp_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_sessions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_sessions_id_seq OWNED BY public.ndsp_sessions.id;


--
-- Name: ndsp_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_settings (
    key text NOT NULL,
    value jsonb NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_subscriptions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_subscriptions (
    id bigint NOT NULL,
    user_id text NOT NULL,
    user_email text,
    plan_id integer,
    plan_code text,
    status text DEFAULT 'active'::text NOT NULL,
    provider text DEFAULT 'nowpayments'::text NOT NULL,
    provider_order_id text,
    provider_payment_id text,
    billing_cycle text DEFAULT 'monthly'::text NOT NULL,
    starts_at timestamp with time zone DEFAULT now() NOT NULL,
    ends_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_subscriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_subscriptions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_subscriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_subscriptions_id_seq OWNED BY public.ndsp_subscriptions.id;


--
-- Name: ndsp_survey_answers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_survey_answers (
    response_key text NOT NULL,
    question_key text NOT NULL,
    answer_value jsonb DEFAULT '{}'::jsonb NOT NULL,
    answer_text character varying(500),
    question_snapshot text NOT NULL,
    answer_language character varying(8) DEFAULT 'ar'::character varying NOT NULL,
    answered_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ndsp_survey_answers_text_ck CHECK (((answer_text IS NULL) OR (char_length((answer_text)::text) <= 500))),
    CONSTRAINT ndsp_survey_answers_value_ck CHECK ((jsonb_typeof(answer_value) = ANY (ARRAY['object'::text, 'array'::text, 'string'::text, 'number'::text, 'boolean'::text])))
);


--
-- Name: ndsp_survey_campaigns; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_survey_campaigns (
    campaign_key text NOT NULL,
    campaign_version text NOT NULL,
    survey_kind text NOT NULL,
    status text DEFAULT 'draft'::text NOT NULL,
    starts_at timestamp with time zone,
    ends_at timestamp with time zone,
    trigger_policy jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ndsp_survey_campaigns_status_ck CHECK ((status = ANY (ARRAY['draft'::text, 'active'::text, 'paused'::text, 'closed'::text]))),
    CONSTRAINT ndsp_survey_campaigns_window_ck CHECK (((ends_at IS NULL) OR (starts_at IS NULL) OR (ends_at > starts_at)))
);


--
-- Name: ndsp_survey_questions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_survey_questions (
    question_key text NOT NULL,
    campaign_key text NOT NULL,
    question_code text NOT NULL,
    question_type text NOT NULL,
    question_text_ar text NOT NULL,
    question_text_en text,
    display_order smallint NOT NULL,
    required boolean DEFAULT false NOT NULL,
    answer_options jsonb DEFAULT '[]'::jsonb NOT NULL,
    display_condition jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ndsp_survey_questions_options_ck CHECK ((jsonb_typeof(answer_options) = 'array'::text)),
    CONSTRAINT ndsp_survey_questions_order_ck CHECK (((display_order >= 1) AND (display_order <= 100))),
    CONSTRAINT ndsp_survey_questions_type_ck CHECK ((question_type = ANY (ARRAY['rating_1_5'::text, 'single_choice'::text, 'short_text'::text])))
);


--
-- Name: ndsp_survey_responses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_survey_responses (
    response_key text NOT NULL,
    campaign_key text NOT NULL,
    subject_key text NOT NULL,
    plan_code text,
    experience_level text,
    use_case text,
    interface_version text,
    trigger_code text NOT NULL,
    status text DEFAULT 'started'::text NOT NULL,
    started_at timestamp with time zone DEFAULT now() NOT NULL,
    completed_at timestamp with time zone,
    skipped_at timestamp with time zone,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    CONSTRAINT ndsp_survey_responses_completion_ck CHECK ((((status = 'completed'::text) AND (completed_at IS NOT NULL)) OR ((status = 'skipped'::text) AND (skipped_at IS NOT NULL)) OR (status = 'started'::text))),
    CONSTRAINT ndsp_survey_responses_experience_ck CHECK (((experience_level IS NULL) OR (experience_level = ANY (ARRAY['beginner'::text, 'intermediate'::text, 'advanced'::text])))),
    CONSTRAINT ndsp_survey_responses_status_ck CHECK ((status = ANY (ARRAY['started'::text, 'completed'::text, 'skipped'::text]))),
    CONSTRAINT ndsp_survey_responses_use_case_ck CHECK (((use_case IS NULL) OR (use_case = ANY (ARRAY['personal'::text, 'learning_research'::text, 'professional'::text, 'team'::text]))))
);


--
-- Name: ndsp_telegram_delivery_routes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_telegram_delivery_routes (
    id integer NOT NULL,
    plan_code text NOT NULL,
    enabled boolean DEFAULT false NOT NULL,
    target_type text DEFAULT 'channel'::text NOT NULL,
    chat_id text,
    daily_limit integer,
    description text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    last_test_ok boolean,
    last_test_at timestamp with time zone,
    last_test_message text
);


--
-- Name: ndsp_telegram_delivery_routes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_telegram_delivery_routes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_telegram_delivery_routes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_telegram_delivery_routes_id_seq OWNED BY public.ndsp_telegram_delivery_routes.id;


--
-- Name: ndsp_trial_activation_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_trial_activation_requests (
    id bigint NOT NULL,
    category text NOT NULL,
    email text,
    name text,
    source_path text,
    invite_code text,
    status text DEFAULT 'pending_admin_review'::text NOT NULL,
    raw_payload jsonb DEFAULT '{}'::jsonb NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    admin_note text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    approved_at timestamp with time zone,
    rejected_at timestamp with time zone,
    approved_by text,
    rejected_by text
);


--
-- Name: ndsp_trial_activation_requests_backup_before_test_20260613_2154; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_trial_activation_requests_backup_before_test_20260613_2154 (
    id bigint,
    category text,
    email text,
    name text,
    source_path text,
    invite_code text,
    status text,
    raw_payload jsonb,
    metadata jsonb,
    admin_note text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    approved_at timestamp with time zone,
    rejected_at timestamp with time zone,
    approved_by text,
    rejected_by text
);


--
-- Name: ndsp_trial_activation_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_trial_activation_requests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_trial_activation_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_trial_activation_requests_id_seq OWNED BY public.ndsp_trial_activation_requests.id;


--
-- Name: ndsp_trial_attempts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_trial_attempts (
    id bigint NOT NULL,
    category text NOT NULL,
    email_normalized text,
    phone_e164 text,
    ip_address text,
    user_agent text,
    result text NOT NULL,
    reason text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_trial_attempts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_trial_attempts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_trial_attempts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_trial_attempts_id_seq OWNED BY public.ndsp_trial_attempts.id;


--
-- Name: ndsp_trial_fingerprint_guard; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_trial_fingerprint_guard (
    id bigint NOT NULL,
    fingerprint_hash text NOT NULL,
    first_email text,
    first_user_id text,
    first_mode text,
    first_ip text,
    status text DEFAULT 'PENDING'::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    accepted_at timestamp with time zone
);


--
-- Name: ndsp_trial_fingerprint_guard_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_trial_fingerprint_guard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_trial_fingerprint_guard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_trial_fingerprint_guard_id_seq OWNED BY public.ndsp_trial_fingerprint_guard.id;


--
-- Name: ndsp_trial_invite_codes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_trial_invite_codes (
    code text NOT NULL,
    category text DEFAULT 'private_invite'::text NOT NULL,
    max_uses integer DEFAULT 1 NOT NULL,
    used_count integer DEFAULT 0 NOT NULL,
    active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_trial_premium_invites; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.ndsp_trial_premium_invites AS
 SELECT id,
    code,
    email,
    label,
    max_uses,
    used_count,
    status,
    created_at,
    expires_at,
    created_by,
    used_by_email,
    used_at,
    last_used_ip,
    metadata
   FROM public.ndsp_premium_trial_invites;


--
-- Name: ndsp_trial_registrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_trial_registrations (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    category text NOT NULL,
    email text NOT NULL,
    email_normalized text NOT NULL,
    phone text NOT NULL,
    phone_e164 text NOT NULL,
    name text DEFAULT ''::text NOT NULL,
    plan text DEFAULT 'Elite'::text NOT NULL,
    status text NOT NULL,
    invite_code text,
    ip_address text DEFAULT ''::text NOT NULL,
    user_agent text DEFAULT ''::text NOT NULL,
    activation_token_hash text,
    token_expires_at timestamp with time zone,
    activated_at timestamp with time zone,
    reservation_expires_at timestamp with time zone,
    review_status text,
    review_note text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ndsp_trial_registrations_category_check CHECK ((category = ANY (ARRAY['ordinary'::text, 'professional'::text, 'private_invite'::text])))
);


--
-- Name: ndsp_trial_seat_assignments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_trial_seat_assignments (
    id bigint NOT NULL,
    user_id text,
    user_email text,
    cohort_code text NOT NULL,
    status text DEFAULT 'reserved'::text NOT NULL,
    assigned_by text,
    assigned_at timestamp with time zone DEFAULT now() NOT NULL,
    notes text
);


--
-- Name: TABLE ndsp_trial_seat_assignments; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.ndsp_trial_seat_assignments IS 'Manual/admin assignment table for trial cohort seats.';


--
-- Name: ndsp_trial_seat_assignments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_trial_seat_assignments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_trial_seat_assignments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_trial_seat_assignments_id_seq OWNED BY public.ndsp_trial_seat_assignments.id;


--
-- Name: ndsp_trial_seat_policy; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_trial_seat_policy (
    id bigint NOT NULL,
    cohort_code text NOT NULL,
    cohort_label_ar text NOT NULL,
    cohort_label_en text NOT NULL,
    max_seats integer NOT NULL,
    sort_order integer DEFAULT 100 NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    notes text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ndsp_trial_seat_policy_max_seats_check CHECK ((max_seats >= 0))
);


--
-- Name: TABLE ndsp_trial_seat_policy; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.ndsp_trial_seat_policy IS 'NDSP trial seat allocation policy. Current launch: 50 seats = 10 academic/specialist, 25 beginner, 15 premium/private.';


--
-- Name: ndsp_trial_seat_policy_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_trial_seat_policy_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_trial_seat_policy_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_trial_seat_policy_id_seq OWNED BY public.ndsp_trial_seat_policy.id;


--
-- Name: ndsp_trial_seat_status; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.ndsp_trial_seat_status AS
 SELECT p.cohort_code,
    p.cohort_label_ar,
    p.cohort_label_en,
    p.max_seats,
    (count(a.id))::integer AS used_seats,
    GREATEST((p.max_seats - (count(a.id))::integer), 0) AS remaining_seats,
    p.sort_order,
    p.is_active
   FROM (public.ndsp_trial_seat_policy p
     LEFT JOIN public.ndsp_trial_seat_assignments a ON (((a.cohort_code = p.cohort_code) AND (a.status = ANY (ARRAY['reserved'::text, 'active'::text, 'approved'::text])))))
  WHERE (p.is_active = true)
  GROUP BY p.cohort_code, p.cohort_label_ar, p.cohort_label_en, p.max_seats, p.sort_order, p.is_active
  ORDER BY p.sort_order;


--
-- Name: VIEW ndsp_trial_seat_status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.ndsp_trial_seat_status IS 'Current trial seat usage and remaining capacity by cohort.';


--
-- Name: ndsp_usage_daily; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_usage_daily (
    subject_key text NOT NULL,
    subject_kind text DEFAULT 'user_id'::text NOT NULL,
    usage_date date DEFAULT CURRENT_DATE NOT NULL,
    feature_code text NOT NULL,
    usage_key text NOT NULL,
    first_used_at timestamp with time zone DEFAULT now() NOT NULL,
    last_used_at timestamp with time zone DEFAULT now() NOT NULL,
    use_count integer DEFAULT 1 NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    CONSTRAINT ndsp_usage_daily_count_ck CHECK ((use_count >= 1)),
    CONSTRAINT ndsp_usage_daily_feature_ck CHECK ((feature_code ~ '^[a-z0-9][a-z0-9._:-]{1,79}$'::text)),
    CONSTRAINT ndsp_usage_daily_key_ck CHECK (((length(usage_key) >= 1) AND (length(usage_key) <= 240))),
    CONSTRAINT ndsp_usage_daily_subject_ck CHECK (((length(subject_key) >= 1) AND (length(subject_key) <= 160))),
    CONSTRAINT ndsp_usage_daily_subject_kind_ck CHECK ((subject_kind = ANY (ARRAY['user_id'::text, 'user_hash'::text])))
);


--
-- Name: ndsp_usage_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_usage_events (
    usage_event_id bigint NOT NULL,
    subject_key text,
    subject_kind text DEFAULT 'user_id'::text NOT NULL,
    event_name text NOT NULL,
    feature_code text,
    usage_key text,
    allowed boolean NOT NULL,
    reason_code text,
    request_id text,
    occurred_at timestamp with time zone DEFAULT now() NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    CONSTRAINT ndsp_usage_events_name_ck CHECK ((event_name ~ '^[a-z0-9][a-z0-9._:-]{1,79}$'::text)),
    CONSTRAINT ndsp_usage_events_subject_ck CHECK (((subject_key IS NULL) OR ((length(subject_key) >= 1) AND (length(subject_key) <= 160)))),
    CONSTRAINT ndsp_usage_events_subject_kind_ck CHECK ((subject_kind = ANY (ARRAY['user_id'::text, 'user_hash'::text, 'anonymous'::text])))
);


--
-- Name: ndsp_usage_events_usage_event_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.ndsp_usage_events ALTER COLUMN usage_event_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ndsp_usage_events_usage_event_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ndsp_user_alert_preferences; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_user_alert_preferences (
    id integer NOT NULL,
    email text,
    user_id text,
    in_app boolean DEFAULT true NOT NULL,
    email_enabled boolean DEFAULT true NOT NULL,
    telegram_enabled boolean DEFAULT false NOT NULL,
    telegram_id text,
    preferences jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_user_alert_preferences_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_user_alert_preferences_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_user_alert_preferences_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_user_alert_preferences_id_seq OWNED BY public.ndsp_user_alert_preferences.id;


--
-- Name: ndsp_user_experience_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_user_experience_events (
    id bigint NOT NULL,
    user_id text NOT NULL,
    event_type text NOT NULL,
    event_version text,
    language text,
    payload jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_user_experience_events_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_user_experience_events_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_user_experience_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_user_experience_events_id_seq OWNED BY public.ndsp_user_experience_events.id;


--
-- Name: ndsp_user_feedback; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_user_feedback (
    id bigint NOT NULL,
    user_id text NOT NULL,
    category text NOT NULL,
    page_href text,
    message text NOT NULL,
    payload jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_user_feedback_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_user_feedback_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_user_feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_user_feedback_id_seq OWNED BY public.ndsp_user_feedback.id;


--
-- Name: ndsp_user_notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_user_notifications (
    id bigint NOT NULL,
    user_id text NOT NULL,
    kind text NOT NULL,
    title text NOT NULL,
    body text NOT NULL,
    action_href text,
    read_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_user_notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_user_notifications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_user_notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_user_notifications_id_seq OWNED BY public.ndsp_user_notifications.id;


--
-- Name: ndsp_user_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_user_profiles (
    subject_key text NOT NULL,
    experience_level text,
    use_case text,
    view_mode text DEFAULT 'simple'::text NOT NULL,
    reading_style text,
    onboarding_completed_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    CONSTRAINT ndsp_user_profiles_experience_ck CHECK (((experience_level IS NULL) OR (experience_level = ANY (ARRAY['beginner'::text, 'intermediate'::text, 'advanced'::text])))),
    CONSTRAINT ndsp_user_profiles_reading_style_ck CHECK (((reading_style IS NULL) OR (reading_style = ANY (ARRAY['investment'::text, 'speculative'::text])))),
    CONSTRAINT ndsp_user_profiles_use_case_ck CHECK (((use_case IS NULL) OR (use_case = ANY (ARRAY['personal'::text, 'learning_research'::text, 'professional'::text, 'team'::text])))),
    CONSTRAINT ndsp_user_profiles_view_mode_ck CHECK ((view_mode = ANY (ARRAY['simple'::text, 'professional'::text])))
);


--
-- Name: ndsp_users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ndsp_users (
    id bigint NOT NULL,
    email text NOT NULL,
    name text NOT NULL,
    role text DEFAULT 'user'::text NOT NULL,
    status text DEFAULT 'active'::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ndsp_users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ndsp_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ndsp_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ndsp_users_id_seq OWNED BY public.ndsp_users.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL,
    email text NOT NULL,
    password_hash text NOT NULL,
    plan text DEFAULT 'insight'::text NOT NULL,
    role text DEFAULT 'user'::text NOT NULL,
    trial_day integer DEFAULT 1 NOT NULL,
    trial_started_at timestamp with time zone DEFAULT now(),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    status text DEFAULT 'active'::text NOT NULL,
    trial_ends_at timestamp with time zone,
    plan_id integer,
    category text,
    phone text,
    two_factor_enabled boolean DEFAULT false,
    two_factor_secret text,
    two_factor_confirmed_at timestamp with time zone,
    two_factor_setup_required boolean DEFAULT true,
    two_factor_skipped_at timestamp with time zone,
    two_factor_last_prompt_at timestamp with time zone,
    requested_segment text,
    approved_segment text,
    trial_segment text,
    account_type text,
    email_verified boolean DEFAULT false NOT NULL,
    invite_code_id bigint,
    review_status text,
    activated_at timestamp with time zone,
    trial_days integer DEFAULT 16 NOT NULL,
    canonical_email text,
    canonical_phone text,
    password_reset_token text,
    password_reset_expires_at timestamp with time zone,
    trial_active boolean,
    plan_changed_at timestamp with time zone,
    legal_policy_version text,
    legal_accepted_at timestamp with time zone,
    legal_language text,
    survey_mid_completed_at timestamp with time zone,
    survey_end_completed_at timestamp with time zone,
    experience_version text,
    CONSTRAINT chk_reset_token_validity CHECK ((((password_reset_token IS NULL) AND (password_reset_expires_at IS NULL)) OR ((password_reset_token IS NOT NULL) AND (password_reset_expires_at IS NOT NULL))))
);


--
-- Name: ndsp_users_trial_view; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.ndsp_users_trial_view AS
 SELECT id,
    name,
    email,
    password_hash,
    plan,
    role,
    trial_day,
    trial_started_at,
    created_at,
    status,
    trial_ends_at,
    plan_id,
    category,
    phone,
    two_factor_enabled,
    two_factor_secret,
    two_factor_confirmed_at,
    two_factor_setup_required,
    two_factor_skipped_at,
    two_factor_last_prompt_at,
    requested_segment,
    approved_segment,
    trial_segment,
    account_type,
    email_verified,
    invite_code_id,
    review_status,
    activated_at,
    trial_days,
        CASE
            WHEN (trial_started_at IS NULL) THEN NULL::integer
            ELSE GREATEST(0, (ceil((EXTRACT(epoch FROM (trial_ends_at - now())) / 86400.0)))::integer)
        END AS trial_days_remaining,
        CASE
            WHEN (trial_started_at IS NULL) THEN 'NOT_STARTED'::text
            WHEN (now() > trial_ends_at) THEN 'EXPIRED'::text
            ELSE 'ACTIVE'::text
        END AS trial_runtime_status
   FROM public.users u;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    title text NOT NULL,
    body text NOT NULL,
    type text DEFAULT 'info'::text NOT NULL,
    is_read boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: plan_features; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plan_features (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    plan_id text,
    feature text NOT NULL,
    is_hidden boolean DEFAULT false NOT NULL,
    sort_order integer DEFAULT 0 NOT NULL
);


--
-- Name: plan_layer_access; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plan_layer_access (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    plan_id text,
    layer_key text NOT NULL,
    visible boolean DEFAULT false NOT NULL
);


--
-- Name: plan_upgrade_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plan_upgrade_requests (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    current_plan text NOT NULL,
    requested_plan text NOT NULL,
    reason text,
    status text DEFAULT 'pending'::text NOT NULL,
    admin_note text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    reviewed_at timestamp with time zone
);


--
-- Name: plans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plans (
    id text NOT NULL,
    name text NOT NULL,
    price text NOT NULL,
    audience text,
    active boolean DEFAULT true NOT NULL,
    trial_days integer DEFAULT 16 NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: premium_invites; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.premium_invites AS
 SELECT id,
    code,
    email,
    label,
    max_uses,
    used_count,
    status,
    created_at,
    expires_at,
    created_by,
    used_by_email,
    used_at,
    last_used_ip,
    metadata
   FROM public.ndsp_premium_trial_invites;


--
-- Name: premium_trial_invites; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.premium_trial_invites AS
 SELECT id,
    code,
    email,
    label,
    max_uses,
    used_count,
    status,
    created_at,
    expires_at,
    created_by,
    used_by_email,
    used_at,
    last_used_ip,
    metadata
   FROM public.ndsp_premium_trial_invites;


--
-- Name: registration_attachments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registration_attachments (
    id bigint NOT NULL,
    registration_request_id bigint NOT NULL,
    attachment_type text NOT NULL,
    original_filename text,
    stored_path text,
    mime_type text,
    file_size_bytes bigint,
    safe_status text DEFAULT 'PENDING_SCAN'::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT registration_attachments_attachment_type_check CHECK ((attachment_type = ANY (ARRAY['academic_analysis_image'::text, 'professional_deep_analysis_image'::text, 'academic_account_image'::text, 'social_account_image'::text, 'work_account_image'::text, 'other'::text]))),
    CONSTRAINT registration_attachments_safe_status_check CHECK ((safe_status = ANY (ARRAY['PENDING_SCAN'::text, 'SAFE'::text, 'REJECTED'::text, 'QUARANTINED'::text])))
);


--
-- Name: registration_attachments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.registration_attachments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: registration_attachments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.registration_attachments_id_seq OWNED BY public.registration_attachments.id;


--
-- Name: registration_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.registration_requests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: registration_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.registration_requests_id_seq OWNED BY public.registration_requests.id;


--
-- Name: requests_backup_before_mobile_test_20260613_215940; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.requests_backup_before_mobile_test_20260613_215940 (
    id bigint,
    category text,
    email text,
    name text,
    source_path text,
    invite_code text,
    status text,
    raw_payload jsonb,
    metadata jsonb,
    admin_note text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    approved_at timestamp with time zone,
    rejected_at timestamp with time zone,
    approved_by text,
    rejected_by text
);


--
-- Name: saas_subscription_invites; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.saas_subscription_invites (
    id bigint NOT NULL,
    subscription_id bigint NOT NULL,
    channel text NOT NULL,
    invite_link text NOT NULL,
    status text DEFAULT 'active'::text NOT NULL,
    created_at text NOT NULL,
    revoked_at text,
    raw text
);


--
-- Name: saas_subscription_invites_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.saas_subscription_invites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: saas_subscription_invites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.saas_subscription_invites_id_seq OWNED BY public.saas_subscription_invites.id;


--
-- Name: saas_subscriptions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.saas_subscriptions (
    id bigint NOT NULL,
    email text,
    telegram_id text,
    plan text DEFAULT 'free'::text NOT NULL,
    status text DEFAULT 'active'::text NOT NULL,
    expires_at text,
    created_at text NOT NULL,
    updated_at text NOT NULL
);


--
-- Name: saas_subscriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.saas_subscriptions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: saas_subscriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.saas_subscriptions_id_seq OWNED BY public.saas_subscriptions.id;


--
-- Name: tokens_backup_before_mobile_test_20260613_215940; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tokens_backup_before_mobile_test_20260613_215940 (
    id uuid,
    user_id uuid,
    token_hash text,
    purpose text,
    used_at timestamp with time zone,
    expires_at timestamp with time zone,
    created_at timestamp with time zone
);


--
-- Name: trial_invite_codes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trial_invite_codes (
    code text NOT NULL,
    status text DEFAULT 'active'::text NOT NULL,
    category text DEFAULT 'premium_invite'::text NOT NULL,
    max_uses integer DEFAULT 1 NOT NULL,
    used_count integer DEFAULT 0 NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone,
    used_at timestamp with time zone,
    used_by_email text,
    note text
);


--
-- Name: trial_invites_premium; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.trial_invites_premium AS
 SELECT id,
    code,
    email,
    label,
    max_uses,
    used_count,
    status,
    created_at,
    expires_at,
    created_by,
    used_by_email,
    used_at,
    last_used_ip,
    metadata
   FROM public.ndsp_premium_trial_invites;


--
-- Name: trial_premium_invites; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.trial_premium_invites AS
 SELECT id,
    code,
    email,
    label,
    max_uses,
    used_count,
    status,
    created_at,
    expires_at,
    created_by,
    used_by_email,
    used_at,
    last_used_ip,
    metadata
   FROM public.ndsp_premium_trial_invites;


--
-- Name: user_2fa_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_2fa_settings (
    user_id uuid NOT NULL,
    enabled boolean DEFAULT false NOT NULL,
    method text DEFAULT 'totp'::text NOT NULL,
    totp_secret text,
    recovery_hashes jsonb DEFAULT '[]'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    last_verified_at timestamp with time zone
);


--
-- Name: user_alert_channels; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_alert_channels (
    id bigint NOT NULL,
    user_id text NOT NULL,
    user_email text,
    email text,
    email_verified boolean DEFAULT false NOT NULL,
    email_verify_code_hash text,
    email_verify_expires_at timestamp with time zone,
    telegram_chat_id text,
    telegram_username text,
    telegram_verified boolean DEFAULT false NOT NULL,
    telegram_link_code_hash text,
    telegram_link_expires_at timestamp with time zone,
    telegram_link_started_at timestamp with time zone,
    last_test_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: user_alert_channels_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_alert_channels_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_alert_channels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_alert_channels_id_seq OWNED BY public.user_alert_channels.id;


--
-- Name: user_two_factor_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_two_factor_settings (
    user_id uuid NOT NULL,
    email text,
    secret text,
    enabled boolean DEFAULT false,
    verified boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: users_backup_before_mobile_test_20260613_215940; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_backup_before_mobile_test_20260613_215940 (
    id uuid,
    name text,
    email text,
    password_hash text,
    plan text,
    role text,
    trial_day integer,
    trial_started_at timestamp with time zone,
    created_at timestamp with time zone,
    status text,
    trial_ends_at timestamp with time zone,
    plan_id integer,
    category text,
    phone text,
    two_factor_enabled boolean,
    two_factor_secret text,
    two_factor_confirmed_at timestamp with time zone,
    two_factor_setup_required boolean,
    two_factor_skipped_at timestamp with time zone,
    two_factor_last_prompt_at timestamp with time zone,
    requested_segment text,
    approved_segment text,
    trial_segment text,
    account_type text,
    email_verified boolean,
    invite_code_id bigint,
    review_status text,
    activated_at timestamp with time zone,
    trial_days integer,
    canonical_email text,
    canonical_phone text,
    password_reset_token text,
    password_reset_expires_at timestamp with time zone
);


--
-- Name: users_backup_before_test_20260613_215437; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_backup_before_test_20260613_215437 (
    id uuid,
    name text,
    email text,
    password_hash text,
    plan text,
    role text,
    trial_day integer,
    trial_started_at timestamp with time zone,
    created_at timestamp with time zone,
    status text,
    trial_ends_at timestamp with time zone,
    plan_id integer,
    category text,
    phone text,
    two_factor_enabled boolean,
    two_factor_secret text,
    two_factor_confirmed_at timestamp with time zone,
    two_factor_setup_required boolean,
    two_factor_skipped_at timestamp with time zone,
    two_factor_last_prompt_at timestamp with time zone,
    requested_segment text,
    approved_segment text,
    trial_segment text,
    account_type text,
    email_verified boolean,
    invite_code_id bigint,
    review_status text,
    activated_at timestamp with time zone,
    trial_days integer,
    canonical_email text,
    canonical_phone text,
    password_reset_token text,
    password_reset_expires_at timestamp with time zone
);


--
-- Name: users_deleted_backup_all; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_deleted_backup_all (
    id uuid,
    name text,
    email text,
    password_hash text,
    plan text,
    role text,
    trial_day integer,
    trial_started_at timestamp with time zone,
    created_at timestamp with time zone,
    status text,
    trial_ends_at timestamp with time zone,
    plan_id integer,
    category text,
    phone text,
    two_factor_enabled boolean,
    two_factor_secret text,
    two_factor_confirmed_at timestamp with time zone,
    two_factor_setup_required boolean,
    two_factor_skipped_at timestamp with time zone,
    two_factor_last_prompt_at timestamp with time zone,
    requested_segment text,
    approved_segment text,
    trial_segment text,
    account_type text,
    email_verified boolean,
    invite_code_id bigint,
    review_status text,
    activated_at timestamp with time zone,
    trial_days integer,
    canonical_email text,
    canonical_phone text,
    password_reset_token text,
    password_reset_expires_at timestamp with time zone,
    deleted_backup_at timestamp with time zone,
    deleted_reason text
);


--
-- Name: users_password_backup; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_password_backup (
    id uuid,
    name text,
    email text,
    password_hash text,
    plan text,
    role text,
    trial_day integer,
    trial_started_at timestamp with time zone,
    created_at timestamp with time zone,
    status text,
    trial_ends_at timestamp with time zone,
    plan_id integer,
    category text,
    phone text,
    two_factor_enabled boolean,
    two_factor_secret text,
    two_factor_confirmed_at timestamp with time zone,
    two_factor_setup_required boolean,
    two_factor_skipped_at timestamp with time zone,
    two_factor_last_prompt_at timestamp with time zone,
    requested_segment text,
    approved_segment text,
    trial_segment text,
    account_type text,
    email_verified boolean,
    invite_code_id bigint,
    review_status text,
    activated_at timestamp with time zone,
    trial_days integer,
    canonical_email text,
    canonical_phone text,
    password_reset_token text,
    password_reset_expires_at timestamp with time zone
);


--
-- Name: access_guard_credentials id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_guard_credentials ALTER COLUMN id SET DEFAULT nextval('public.access_guard_credentials_id_seq'::regclass);


--
-- Name: access_guard_sessions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_guard_sessions ALTER COLUMN id SET DEFAULT nextval('public.access_guard_sessions_id_seq'::regclass);


--
-- Name: admin_audit_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_audit_log ALTER COLUMN id SET DEFAULT nextval('public.admin_audit_log_id_seq'::regclass);


--
-- Name: dsp_registration_abuse_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dsp_registration_abuse_log ALTER COLUMN id SET DEFAULT nextval('public.dsp_registration_abuse_log_id_seq'::regclass);


--
-- Name: dsp_trial_survey_events id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dsp_trial_survey_events ALTER COLUMN id SET DEFAULT nextval('public.dsp_trial_survey_events_id_seq'::regclass);


--
-- Name: email_delivery_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_delivery_log ALTER COLUMN id SET DEFAULT nextval('public.email_delivery_log_id_seq'::regclass);


--
-- Name: invite_codes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.invite_codes ALTER COLUMN id SET DEFAULT nextval('public.invite_codes_id_seq'::regclass);


--
-- Name: ndsp_assets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_assets ALTER COLUMN id SET DEFAULT nextval('public.ndsp_assets_id_seq'::regclass);


--
-- Name: ndsp_audit_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_audit_log ALTER COLUMN id SET DEFAULT nextval('public.ndsp_audit_log_id_seq'::regclass);


--
-- Name: ndsp_auth_audit id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_auth_audit ALTER COLUMN id SET DEFAULT nextval('public.ndsp_auth_audit_id_seq'::regclass);


--
-- Name: ndsp_clean_auth_audit_v2 id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_clean_auth_audit_v2 ALTER COLUMN id SET DEFAULT nextval('public.ndsp_clean_auth_audit_v2_id_seq'::regclass);


--
-- Name: ndsp_completed_decisions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_completed_decisions ALTER COLUMN id SET DEFAULT nextval('public.ndsp_completed_decisions_id_seq'::regclass);


--
-- Name: ndsp_decision_ledger id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_decision_ledger ALTER COLUMN id SET DEFAULT nextval('public.ndsp_decision_ledger_id_seq'::regclass);


--
-- Name: ndsp_decision_timeline id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_decision_timeline ALTER COLUMN id SET DEFAULT nextval('public.ndsp_decision_timeline_id_seq'::regclass);


--
-- Name: ndsp_discount_codes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_discount_codes ALTER COLUMN id SET DEFAULT nextval('public.ndsp_discount_codes_id_seq'::regclass);


--
-- Name: ndsp_duplicate_phone_audit id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_duplicate_phone_audit ALTER COLUMN id SET DEFAULT nextval('public.ndsp_duplicate_phone_audit_id_seq'::regclass);


--
-- Name: ndsp_invitation_codes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_invitation_codes ALTER COLUMN id SET DEFAULT nextval('public.ndsp_invitation_codes_id_seq'::regclass);


--
-- Name: ndsp_launch_cleanup_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_launch_cleanup_log ALTER COLUMN id SET DEFAULT nextval('public.ndsp_launch_cleanup_log_id_seq'::regclass);


--
-- Name: ndsp_layers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_layers ALTER COLUMN id SET DEFAULT nextval('public.ndsp_layers_id_seq'::regclass);


--
-- Name: ndsp_market_assets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_market_assets ALTER COLUMN id SET DEFAULT nextval('public.ndsp_market_assets_id_seq'::regclass);


--
-- Name: ndsp_nowpayments_payments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_nowpayments_payments ALTER COLUMN id SET DEFAULT nextval('public.ndsp_nowpayments_payments_id_seq'::regclass);


--
-- Name: ndsp_operational_compat_audit id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_operational_compat_audit ALTER COLUMN id SET DEFAULT nextval('public.ndsp_operational_compat_audit_id_seq'::regclass);


--
-- Name: ndsp_payment_audit id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_payment_audit ALTER COLUMN id SET DEFAULT nextval('public.ndsp_payment_audit_id_seq'::regclass);


--
-- Name: ndsp_plans id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_plans ALTER COLUMN id SET DEFAULT nextval('public.ndsp_plans_id_seq'::regclass);


--
-- Name: ndsp_premium_trial_invites id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_premium_trial_invites ALTER COLUMN id SET DEFAULT nextval('public.ndsp_premium_trial_invites_id_seq'::regclass);


--
-- Name: ndsp_registration_guard_audit id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_registration_guard_audit ALTER COLUMN id SET DEFAULT nextval('public.ndsp_registration_guard_audit_id_seq'::regclass);


--
-- Name: ndsp_registration_locks id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_registration_locks ALTER COLUMN id SET DEFAULT nextval('public.ndsp_registration_locks_id_seq'::regclass);


--
-- Name: ndsp_sessions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_sessions ALTER COLUMN id SET DEFAULT nextval('public.ndsp_sessions_id_seq'::regclass);


--
-- Name: ndsp_subscriptions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_subscriptions ALTER COLUMN id SET DEFAULT nextval('public.ndsp_subscriptions_id_seq'::regclass);


--
-- Name: ndsp_telegram_delivery_routes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_telegram_delivery_routes ALTER COLUMN id SET DEFAULT nextval('public.ndsp_telegram_delivery_routes_id_seq'::regclass);


--
-- Name: ndsp_trial_activation_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_activation_requests ALTER COLUMN id SET DEFAULT nextval('public.ndsp_trial_activation_requests_id_seq'::regclass);


--
-- Name: ndsp_trial_attempts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_attempts ALTER COLUMN id SET DEFAULT nextval('public.ndsp_trial_attempts_id_seq'::regclass);


--
-- Name: ndsp_trial_fingerprint_guard id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_fingerprint_guard ALTER COLUMN id SET DEFAULT nextval('public.ndsp_trial_fingerprint_guard_id_seq'::regclass);


--
-- Name: ndsp_trial_seat_assignments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_seat_assignments ALTER COLUMN id SET DEFAULT nextval('public.ndsp_trial_seat_assignments_id_seq'::regclass);


--
-- Name: ndsp_trial_seat_policy id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_seat_policy ALTER COLUMN id SET DEFAULT nextval('public.ndsp_trial_seat_policy_id_seq'::regclass);


--
-- Name: ndsp_user_alert_preferences id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_user_alert_preferences ALTER COLUMN id SET DEFAULT nextval('public.ndsp_user_alert_preferences_id_seq'::regclass);


--
-- Name: ndsp_user_experience_events id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_user_experience_events ALTER COLUMN id SET DEFAULT nextval('public.ndsp_user_experience_events_id_seq'::regclass);


--
-- Name: ndsp_user_feedback id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_user_feedback ALTER COLUMN id SET DEFAULT nextval('public.ndsp_user_feedback_id_seq'::regclass);


--
-- Name: ndsp_user_notifications id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_user_notifications ALTER COLUMN id SET DEFAULT nextval('public.ndsp_user_notifications_id_seq'::regclass);


--
-- Name: ndsp_users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_users ALTER COLUMN id SET DEFAULT nextval('public.ndsp_users_id_seq'::regclass);


--
-- Name: registration_attachments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_attachments ALTER COLUMN id SET DEFAULT nextval('public.registration_attachments_id_seq'::regclass);


--
-- Name: registration_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_requests ALTER COLUMN id SET DEFAULT nextval('public.registration_requests_id_seq'::regclass);


--
-- Name: saas_subscription_invites id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saas_subscription_invites ALTER COLUMN id SET DEFAULT nextval('public.saas_subscription_invites_id_seq'::regclass);


--
-- Name: saas_subscriptions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saas_subscriptions ALTER COLUMN id SET DEFAULT nextval('public.saas_subscriptions_id_seq'::regclass);


--
-- Name: user_alert_channels id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_alert_channels ALTER COLUMN id SET DEFAULT nextval('public.user_alert_channels_id_seq'::regclass);


--
-- Name: access_guard_credentials access_guard_credentials_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_guard_credentials
    ADD CONSTRAINT access_guard_credentials_email_key UNIQUE (email);


--
-- Name: access_guard_credentials access_guard_credentials_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_guard_credentials
    ADD CONSTRAINT access_guard_credentials_pkey PRIMARY KEY (id);


--
-- Name: access_guard_credentials access_guard_credentials_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_guard_credentials
    ADD CONSTRAINT access_guard_credentials_user_id_key UNIQUE (user_id);


--
-- Name: access_guard_sessions access_guard_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_guard_sessions
    ADD CONSTRAINT access_guard_sessions_pkey PRIMARY KEY (id);


--
-- Name: access_guard_sessions access_guard_sessions_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_guard_sessions
    ADD CONSTRAINT access_guard_sessions_token_hash_key UNIQUE (token_hash);


--
-- Name: admin_audit_log admin_audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_audit_log
    ADD CONSTRAINT admin_audit_log_pkey PRIMARY KEY (id);


--
-- Name: dsp_invite_codes dsp_invite_codes_code_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dsp_invite_codes
    ADD CONSTRAINT dsp_invite_codes_code_hash_key UNIQUE (code_hash);


--
-- Name: dsp_invite_codes dsp_invite_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dsp_invite_codes
    ADD CONSTRAINT dsp_invite_codes_pkey PRIMARY KEY (id);


--
-- Name: dsp_registration_abuse_log dsp_registration_abuse_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dsp_registration_abuse_log
    ADD CONSTRAINT dsp_registration_abuse_log_pkey PRIMARY KEY (id);


--
-- Name: dsp_trial_survey_events dsp_trial_survey_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dsp_trial_survey_events
    ADD CONSTRAINT dsp_trial_survey_events_pkey PRIMARY KEY (id);


--
-- Name: email_delivery_log email_delivery_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_delivery_log
    ADD CONSTRAINT email_delivery_log_pkey PRIMARY KEY (id);


--
-- Name: feedback_surveys feedback_surveys_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.feedback_surveys
    ADD CONSTRAINT feedback_surveys_pkey PRIMARY KEY (id);


--
-- Name: invite_codes invite_codes_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.invite_codes
    ADD CONSTRAINT invite_codes_code_key UNIQUE (code);


--
-- Name: invite_codes invite_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.invite_codes
    ADD CONSTRAINT invite_codes_pkey PRIMARY KEY (id);


--
-- Name: ndsp_admin_audit_log ndsp_admin_audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_admin_audit_log
    ADD CONSTRAINT ndsp_admin_audit_log_pkey PRIMARY KEY (id);


--
-- Name: ndsp_admin_runtime_flags ndsp_admin_runtime_flags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_admin_runtime_flags
    ADD CONSTRAINT ndsp_admin_runtime_flags_pkey PRIMARY KEY (key);


--
-- Name: ndsp_assets ndsp_assets_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_assets
    ADD CONSTRAINT ndsp_assets_code_key UNIQUE (code);


--
-- Name: ndsp_assets_legacy_before_clean_rebuild ndsp_assets_code_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_assets_legacy_before_clean_rebuild
    ADD CONSTRAINT ndsp_assets_code_unique UNIQUE (code);


--
-- Name: ndsp_assets_legacy_before_clean_rebuild ndsp_assets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_assets_legacy_before_clean_rebuild
    ADD CONSTRAINT ndsp_assets_pkey PRIMARY KEY (code);


--
-- Name: ndsp_assets ndsp_assets_pkey1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_assets
    ADD CONSTRAINT ndsp_assets_pkey1 PRIMARY KEY (id);


--
-- Name: ndsp_assets ndsp_assets_symbol_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_assets
    ADD CONSTRAINT ndsp_assets_symbol_key UNIQUE (symbol);


--
-- Name: ndsp_assets_legacy_before_clean_rebuild ndsp_assets_symbol_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_assets_legacy_before_clean_rebuild
    ADD CONSTRAINT ndsp_assets_symbol_unique UNIQUE (symbol);


--
-- Name: ndsp_audit_log ndsp_audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_audit_log
    ADD CONSTRAINT ndsp_audit_log_pkey PRIMARY KEY (id);


--
-- Name: ndsp_auth_activation_tokens ndsp_auth_activation_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_auth_activation_tokens
    ADD CONSTRAINT ndsp_auth_activation_tokens_pkey PRIMARY KEY (id);


--
-- Name: ndsp_auth_activation_tokens ndsp_auth_activation_tokens_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_auth_activation_tokens
    ADD CONSTRAINT ndsp_auth_activation_tokens_token_hash_key UNIQUE (token_hash);


--
-- Name: ndsp_auth_audit ndsp_auth_audit_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_auth_audit
    ADD CONSTRAINT ndsp_auth_audit_pkey PRIMARY KEY (id);


--
-- Name: ndsp_auth_sessions ndsp_auth_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_auth_sessions
    ADD CONSTRAINT ndsp_auth_sessions_pkey PRIMARY KEY (id);


--
-- Name: ndsp_auth_sessions ndsp_auth_sessions_session_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_auth_sessions
    ADD CONSTRAINT ndsp_auth_sessions_session_hash_key UNIQUE (session_hash);


--
-- Name: ndsp_auth_users ndsp_auth_users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_auth_users
    ADD CONSTRAINT ndsp_auth_users_email_key UNIQUE (email);


--
-- Name: ndsp_auth_users ndsp_auth_users_phone_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_auth_users
    ADD CONSTRAINT ndsp_auth_users_phone_key UNIQUE (phone);


--
-- Name: ndsp_auth_users ndsp_auth_users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_auth_users
    ADD CONSTRAINT ndsp_auth_users_pkey PRIMARY KEY (id);


--
-- Name: ndsp_clean_auth_audit_v2 ndsp_clean_auth_audit_v2_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_clean_auth_audit_v2
    ADD CONSTRAINT ndsp_clean_auth_audit_v2_pkey PRIMARY KEY (id);


--
-- Name: ndsp_clean_auth_sessions_v2 ndsp_clean_auth_sessions_v2_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_clean_auth_sessions_v2
    ADD CONSTRAINT ndsp_clean_auth_sessions_v2_pkey PRIMARY KEY (token_hash);


--
-- Name: ndsp_completed_decisions ndsp_completed_decisions_decision_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_completed_decisions
    ADD CONSTRAINT ndsp_completed_decisions_decision_id_key UNIQUE (decision_id);


--
-- Name: ndsp_completed_decisions ndsp_completed_decisions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_completed_decisions
    ADD CONSTRAINT ndsp_completed_decisions_pkey PRIMARY KEY (id);


--
-- Name: ndsp_decision_evidence_snapshots ndsp_decision_evidence_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_decision_evidence_snapshots
    ADD CONSTRAINT ndsp_decision_evidence_snapshots_pkey PRIMARY KEY (evidence_id);


--
-- Name: ndsp_decision_evidence_snapshots ndsp_decision_evidence_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_decision_evidence_snapshots
    ADD CONSTRAINT ndsp_decision_evidence_uq UNIQUE (decision_id, contract_version, payload_sha256);


--
-- Name: ndsp_decision_ledger ndsp_decision_ledger_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_decision_ledger
    ADD CONSTRAINT ndsp_decision_ledger_pkey PRIMARY KEY (id);


--
-- Name: ndsp_decision_timeline ndsp_decision_timeline_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_decision_timeline
    ADD CONSTRAINT ndsp_decision_timeline_pkey PRIMARY KEY (id);


--
-- Name: ndsp_discount_codes ndsp_discount_codes_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_discount_codes
    ADD CONSTRAINT ndsp_discount_codes_code_key UNIQUE (code);


--
-- Name: ndsp_discount_codes ndsp_discount_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_discount_codes
    ADD CONSTRAINT ndsp_discount_codes_pkey PRIMARY KEY (id);


--
-- Name: ndsp_duplicate_phone_audit ndsp_duplicate_phone_audit_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_duplicate_phone_audit
    ADD CONSTRAINT ndsp_duplicate_phone_audit_pkey PRIMARY KEY (id);


--
-- Name: ndsp_feedback_entries ndsp_feedback_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_feedback_entries
    ADD CONSTRAINT ndsp_feedback_entries_pkey PRIMARY KEY (id);


--
-- Name: ndsp_feedback_notice_log ndsp_feedback_notice_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_feedback_notice_log
    ADD CONSTRAINT ndsp_feedback_notice_log_pkey PRIMARY KEY (id);


--
-- Name: ndsp_invitation_codes ndsp_invitation_codes_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_invitation_codes
    ADD CONSTRAINT ndsp_invitation_codes_code_key UNIQUE (code);


--
-- Name: ndsp_invitation_codes ndsp_invitation_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_invitation_codes
    ADD CONSTRAINT ndsp_invitation_codes_pkey PRIMARY KEY (id);


--
-- Name: ndsp_launch_cleanup_log ndsp_launch_cleanup_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_launch_cleanup_log
    ADD CONSTRAINT ndsp_launch_cleanup_log_pkey PRIMARY KEY (id);


--
-- Name: ndsp_layers ndsp_layers_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_layers
    ADD CONSTRAINT ndsp_layers_code_key UNIQUE (code);


--
-- Name: ndsp_layers ndsp_layers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_layers
    ADD CONSTRAINT ndsp_layers_pkey PRIMARY KEY (id);


--
-- Name: ndsp_legal_acceptances ndsp_legal_acceptances_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_legal_acceptances
    ADD CONSTRAINT ndsp_legal_acceptances_pkey PRIMARY KEY (acceptance_id);


--
-- Name: ndsp_legal_acceptances ndsp_legal_acceptances_request_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_legal_acceptances
    ADD CONSTRAINT ndsp_legal_acceptances_request_uq UNIQUE (request_id);


--
-- Name: ndsp_market_assets ndsp_market_assets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_market_assets
    ADD CONSTRAINT ndsp_market_assets_pkey PRIMARY KEY (id);


--
-- Name: ndsp_market_assets ndsp_market_assets_symbol_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_market_assets
    ADD CONSTRAINT ndsp_market_assets_symbol_key UNIQUE (symbol);


--
-- Name: ndsp_nowpayments_payments ndsp_nowpayments_payments_order_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_nowpayments_payments
    ADD CONSTRAINT ndsp_nowpayments_payments_order_id_key UNIQUE (order_id);


--
-- Name: ndsp_nowpayments_payments ndsp_nowpayments_payments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_nowpayments_payments
    ADD CONSTRAINT ndsp_nowpayments_payments_pkey PRIMARY KEY (id);


--
-- Name: ndsp_operational_compat_audit ndsp_operational_compat_audit_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_operational_compat_audit
    ADD CONSTRAINT ndsp_operational_compat_audit_pkey PRIMARY KEY (id);


--
-- Name: ndsp_payment_audit ndsp_payment_audit_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_payment_audit
    ADD CONSTRAINT ndsp_payment_audit_pkey PRIMARY KEY (id);


--
-- Name: ndsp_plan_layers ndsp_plan_layers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_plan_layers
    ADD CONSTRAINT ndsp_plan_layers_pkey PRIMARY KEY (plan_id, layer_id);


--
-- Name: ndsp_plans ndsp_plans_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_plans
    ADD CONSTRAINT ndsp_plans_code_key UNIQUE (code);


--
-- Name: ndsp_plans ndsp_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_plans
    ADD CONSTRAINT ndsp_plans_pkey PRIMARY KEY (id);


--
-- Name: ndsp_portal_readings_cache ndsp_portal_readings_cache_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_portal_readings_cache
    ADD CONSTRAINT ndsp_portal_readings_cache_pkey PRIMARY KEY (id);


--
-- Name: ndsp_premium_trial_invites ndsp_premium_trial_invites_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_premium_trial_invites
    ADD CONSTRAINT ndsp_premium_trial_invites_code_key UNIQUE (code);


--
-- Name: ndsp_premium_trial_invites ndsp_premium_trial_invites_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_premium_trial_invites
    ADD CONSTRAINT ndsp_premium_trial_invites_pkey PRIMARY KEY (id);


--
-- Name: ndsp_price_cache ndsp_price_cache_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_price_cache
    ADD CONSTRAINT ndsp_price_cache_pkey PRIMARY KEY (symbol);


--
-- Name: ndsp_private_invite_codes ndsp_private_invite_codes_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_private_invite_codes
    ADD CONSTRAINT ndsp_private_invite_codes_code_key UNIQUE (code);


--
-- Name: ndsp_private_invite_codes ndsp_private_invite_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_private_invite_codes
    ADD CONSTRAINT ndsp_private_invite_codes_pkey PRIMARY KEY (id);


--
-- Name: ndsp_product_events ndsp_product_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_product_events
    ADD CONSTRAINT ndsp_product_events_pkey PRIMARY KEY (product_event_id);


--
-- Name: ndsp_provider_health_history ndsp_provider_health_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_provider_health_history
    ADD CONSTRAINT ndsp_provider_health_history_pkey PRIMARY KEY (provider_health_id);


--
-- Name: ndsp_registration_email_dispatch ndsp_registration_email_dispatch_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_registration_email_dispatch
    ADD CONSTRAINT ndsp_registration_email_dispatch_pkey PRIMARY KEY (user_id);


--
-- Name: ndsp_registration_guard_audit ndsp_registration_guard_audit_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_registration_guard_audit
    ADD CONSTRAINT ndsp_registration_guard_audit_pkey PRIMARY KEY (id);


--
-- Name: ndsp_registration_locks ndsp_registration_locks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_registration_locks
    ADD CONSTRAINT ndsp_registration_locks_pkey PRIMARY KEY (id);


--
-- Name: ndsp_schema_migrations ndsp_schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_schema_migrations
    ADD CONSTRAINT ndsp_schema_migrations_pkey PRIMARY KEY (migration_key);


--
-- Name: ndsp_sessions ndsp_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_sessions
    ADD CONSTRAINT ndsp_sessions_pkey PRIMARY KEY (id);


--
-- Name: ndsp_sessions ndsp_sessions_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_sessions
    ADD CONSTRAINT ndsp_sessions_token_hash_key UNIQUE (token_hash);


--
-- Name: ndsp_settings ndsp_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_settings
    ADD CONSTRAINT ndsp_settings_pkey PRIMARY KEY (key);


--
-- Name: ndsp_subscriptions ndsp_subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_subscriptions
    ADD CONSTRAINT ndsp_subscriptions_pkey PRIMARY KEY (id);


--
-- Name: ndsp_survey_answers ndsp_survey_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_survey_answers
    ADD CONSTRAINT ndsp_survey_answers_pkey PRIMARY KEY (response_key, question_key);


--
-- Name: ndsp_survey_campaigns ndsp_survey_campaigns_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_survey_campaigns
    ADD CONSTRAINT ndsp_survey_campaigns_pkey PRIMARY KEY (campaign_key);


--
-- Name: ndsp_survey_questions ndsp_survey_questions_campaign_code_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_survey_questions
    ADD CONSTRAINT ndsp_survey_questions_campaign_code_uq UNIQUE (campaign_key, question_code);


--
-- Name: ndsp_survey_questions ndsp_survey_questions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_survey_questions
    ADD CONSTRAINT ndsp_survey_questions_pkey PRIMARY KEY (question_key);


--
-- Name: ndsp_survey_responses ndsp_survey_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_survey_responses
    ADD CONSTRAINT ndsp_survey_responses_pkey PRIMARY KEY (response_key);


--
-- Name: ndsp_survey_responses ndsp_survey_responses_subject_campaign_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_survey_responses
    ADD CONSTRAINT ndsp_survey_responses_subject_campaign_uq UNIQUE (subject_key, campaign_key);


--
-- Name: ndsp_telegram_delivery_routes ndsp_telegram_delivery_routes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_telegram_delivery_routes
    ADD CONSTRAINT ndsp_telegram_delivery_routes_pkey PRIMARY KEY (id);


--
-- Name: ndsp_telegram_delivery_routes ndsp_telegram_delivery_routes_plan_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_telegram_delivery_routes
    ADD CONSTRAINT ndsp_telegram_delivery_routes_plan_code_key UNIQUE (plan_code);


--
-- Name: ndsp_trial_activation_requests ndsp_trial_activation_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_activation_requests
    ADD CONSTRAINT ndsp_trial_activation_requests_pkey PRIMARY KEY (id);


--
-- Name: ndsp_trial_attempts ndsp_trial_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_attempts
    ADD CONSTRAINT ndsp_trial_attempts_pkey PRIMARY KEY (id);


--
-- Name: ndsp_trial_fingerprint_guard ndsp_trial_fingerprint_guard_fingerprint_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_fingerprint_guard
    ADD CONSTRAINT ndsp_trial_fingerprint_guard_fingerprint_hash_key UNIQUE (fingerprint_hash);


--
-- Name: ndsp_trial_fingerprint_guard ndsp_trial_fingerprint_guard_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_fingerprint_guard
    ADD CONSTRAINT ndsp_trial_fingerprint_guard_pkey PRIMARY KEY (id);


--
-- Name: ndsp_trial_invite_codes ndsp_trial_invite_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_invite_codes
    ADD CONSTRAINT ndsp_trial_invite_codes_pkey PRIMARY KEY (code);


--
-- Name: ndsp_trial_registrations ndsp_trial_registrations_activation_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_registrations
    ADD CONSTRAINT ndsp_trial_registrations_activation_token_hash_key UNIQUE (activation_token_hash);


--
-- Name: ndsp_trial_registrations ndsp_trial_registrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_registrations
    ADD CONSTRAINT ndsp_trial_registrations_pkey PRIMARY KEY (id);


--
-- Name: ndsp_trial_seat_assignments ndsp_trial_seat_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_seat_assignments
    ADD CONSTRAINT ndsp_trial_seat_assignments_pkey PRIMARY KEY (id);


--
-- Name: ndsp_trial_seat_policy ndsp_trial_seat_policy_cohort_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_seat_policy
    ADD CONSTRAINT ndsp_trial_seat_policy_cohort_code_key UNIQUE (cohort_code);


--
-- Name: ndsp_trial_seat_policy ndsp_trial_seat_policy_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_seat_policy
    ADD CONSTRAINT ndsp_trial_seat_policy_pkey PRIMARY KEY (id);


--
-- Name: ndsp_usage_daily ndsp_usage_daily_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_usage_daily
    ADD CONSTRAINT ndsp_usage_daily_pkey PRIMARY KEY (subject_key, usage_date, feature_code, usage_key);


--
-- Name: ndsp_usage_events ndsp_usage_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_usage_events
    ADD CONSTRAINT ndsp_usage_events_pkey PRIMARY KEY (usage_event_id);


--
-- Name: ndsp_user_alert_preferences ndsp_user_alert_preferences_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_user_alert_preferences
    ADD CONSTRAINT ndsp_user_alert_preferences_email_key UNIQUE (email);


--
-- Name: ndsp_user_alert_preferences ndsp_user_alert_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_user_alert_preferences
    ADD CONSTRAINT ndsp_user_alert_preferences_pkey PRIMARY KEY (id);


--
-- Name: ndsp_user_experience_events ndsp_user_experience_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_user_experience_events
    ADD CONSTRAINT ndsp_user_experience_events_pkey PRIMARY KEY (id);


--
-- Name: ndsp_user_feedback ndsp_user_feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_user_feedback
    ADD CONSTRAINT ndsp_user_feedback_pkey PRIMARY KEY (id);


--
-- Name: ndsp_user_notifications ndsp_user_notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_user_notifications
    ADD CONSTRAINT ndsp_user_notifications_pkey PRIMARY KEY (id);


--
-- Name: ndsp_user_profiles ndsp_user_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_user_profiles
    ADD CONSTRAINT ndsp_user_profiles_pkey PRIMARY KEY (subject_key);


--
-- Name: ndsp_users ndsp_users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_users
    ADD CONSTRAINT ndsp_users_email_key UNIQUE (email);


--
-- Name: ndsp_users ndsp_users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_users
    ADD CONSTRAINT ndsp_users_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: plan_features plan_features_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plan_features
    ADD CONSTRAINT plan_features_pkey PRIMARY KEY (id);


--
-- Name: plan_layer_access plan_layer_access_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plan_layer_access
    ADD CONSTRAINT plan_layer_access_pkey PRIMARY KEY (id);


--
-- Name: plan_layer_access plan_layer_access_plan_id_layer_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plan_layer_access
    ADD CONSTRAINT plan_layer_access_plan_id_layer_key_key UNIQUE (plan_id, layer_key);


--
-- Name: plan_upgrade_requests plan_upgrade_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plan_upgrade_requests
    ADD CONSTRAINT plan_upgrade_requests_pkey PRIMARY KEY (id);


--
-- Name: plans plans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_pkey PRIMARY KEY (id);


--
-- Name: registration_attachments registration_attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_attachments
    ADD CONSTRAINT registration_attachments_pkey PRIMARY KEY (id);


--
-- Name: registration_requests registration_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_requests
    ADD CONSTRAINT registration_requests_pkey PRIMARY KEY (id);


--
-- Name: saas_subscription_invites saas_subscription_invites_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saas_subscription_invites
    ADD CONSTRAINT saas_subscription_invites_pkey PRIMARY KEY (id);


--
-- Name: saas_subscriptions saas_subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saas_subscriptions
    ADD CONSTRAINT saas_subscriptions_pkey PRIMARY KEY (id);


--
-- Name: trial_invite_codes trial_invite_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trial_invite_codes
    ADD CONSTRAINT trial_invite_codes_pkey PRIMARY KEY (code);


--
-- Name: user_2fa_settings user_2fa_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_2fa_settings
    ADD CONSTRAINT user_2fa_settings_pkey PRIMARY KEY (user_id);


--
-- Name: user_alert_channels user_alert_channels_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_alert_channels
    ADD CONSTRAINT user_alert_channels_pkey PRIMARY KEY (id);


--
-- Name: user_alert_channels user_alert_channels_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_alert_channels
    ADD CONSTRAINT user_alert_channels_user_id_key UNIQUE (user_id);


--
-- Name: user_two_factor_settings user_two_factor_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_two_factor_settings
    ADD CONSTRAINT user_two_factor_settings_pkey PRIMARY KEY (user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: feedback_discount_status_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX feedback_discount_status_idx ON public.feedback_surveys USING btree (discount_status);


--
-- Name: idx_dsp_abuse_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_dsp_abuse_created ON public.dsp_registration_abuse_log USING btree (created_at);


--
-- Name: idx_dsp_invite_active; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_dsp_invite_active ON public.dsp_invite_codes USING btree (active, segment);


--
-- Name: idx_dsp_survey_event; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_dsp_survey_event ON public.dsp_trial_survey_events USING btree (event_type, created_at);


--
-- Name: idx_email_delivery_log_recipient; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_email_delivery_log_recipient ON public.email_delivery_log USING btree (lower(recipient_email));


--
-- Name: idx_email_delivery_log_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_email_delivery_log_status ON public.email_delivery_log USING btree (status);


--
-- Name: idx_ndsp_decision_ledger_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_decision_ledger_created_at ON public.ndsp_decision_ledger USING btree (created_at DESC);


--
-- Name: idx_ndsp_decision_ledger_symbol_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_decision_ledger_symbol_created_at ON public.ndsp_decision_ledger USING btree (symbol, created_at DESC);


--
-- Name: idx_ndsp_portal_readings_cache_lookup; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_portal_readings_cache_lookup ON public.ndsp_portal_readings_cache USING btree (page_type, symbol, timeframe, status, expires_at);


--
-- Name: idx_ndsp_premium_trial_invites_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_premium_trial_invites_code ON public.ndsp_premium_trial_invites USING btree (code);


--
-- Name: idx_ndsp_premium_trial_invites_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_premium_trial_invites_email ON public.ndsp_premium_trial_invites USING btree (email);


--
-- Name: idx_ndsp_premium_trial_invites_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_premium_trial_invites_status ON public.ndsp_premium_trial_invites USING btree (status);


--
-- Name: idx_ndsp_sessions_hash; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_sessions_hash ON public.ndsp_sessions USING btree (token_hash);


--
-- Name: idx_ndsp_subscriptions_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_subscriptions_user ON public.ndsp_subscriptions USING btree (user_id);


--
-- Name: idx_ndsp_trial_activation_requests_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_trial_activation_requests_category ON public.ndsp_trial_activation_requests USING btree (category);


--
-- Name: idx_ndsp_trial_activation_requests_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_trial_activation_requests_created_at ON public.ndsp_trial_activation_requests USING btree (created_at DESC);


--
-- Name: idx_ndsp_trial_activation_requests_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_trial_activation_requests_email ON public.ndsp_trial_activation_requests USING btree (lower(email));


--
-- Name: idx_ndsp_trial_activation_requests_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_trial_activation_requests_status ON public.ndsp_trial_activation_requests USING btree (status);


--
-- Name: idx_ndsp_trial_seat_assignments_cohort; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_trial_seat_assignments_cohort ON public.ndsp_trial_seat_assignments USING btree (cohort_code);


--
-- Name: idx_ndsp_trial_seat_assignments_user_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX idx_ndsp_trial_seat_assignments_user_email ON public.ndsp_trial_seat_assignments USING btree (lower(user_email)) WHERE (user_email IS NOT NULL);


--
-- Name: idx_ndsp_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_users_email ON public.ndsp_users USING btree (email);


--
-- Name: idx_registration_requests_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_registration_requests_email ON public.registration_requests USING btree (lower(email));


--
-- Name: idx_registration_requests_requested_segment; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_registration_requests_requested_segment ON public.registration_requests USING btree (requested_segment);


--
-- Name: idx_registration_requests_review_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_registration_requests_review_status ON public.registration_requests USING btree (review_status);


--
-- Name: idx_saas_invites_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_saas_invites_link ON public.saas_subscription_invites USING btree (invite_link);


--
-- Name: idx_saas_invites_sub_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_saas_invites_sub_id ON public.saas_subscription_invites USING btree (subscription_id);


--
-- Name: idx_saas_sub_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_saas_sub_email ON public.saas_subscriptions USING btree (email);


--
-- Name: idx_saas_sub_telegram_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_saas_sub_telegram_id ON public.saas_subscriptions USING btree (telegram_id);


--
-- Name: idx_trial_invite_codes_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trial_invite_codes_created_at ON public.trial_invite_codes USING btree (created_at);


--
-- Name: idx_trial_invite_codes_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trial_invite_codes_status ON public.trial_invite_codes USING btree (status);


--
-- Name: idx_user_2fa_enabled; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_user_2fa_enabled ON public.user_2fa_settings USING btree (enabled);


--
-- Name: idx_users_password_reset_token; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_users_password_reset_token ON public.users USING btree (password_reset_token) WHERE (password_reset_token IS NOT NULL);


--
-- Name: ix_ndsp_admin_audit_action_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_admin_audit_action_created ON public.ndsp_admin_audit_log USING btree (action, created_at DESC);


--
-- Name: ix_ndsp_auth_activation_tokens_hash; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_auth_activation_tokens_hash ON public.ndsp_auth_activation_tokens USING btree (token_hash);


--
-- Name: ix_ndsp_auth_activation_tokens_token_hash; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_auth_activation_tokens_token_hash ON public.ndsp_auth_activation_tokens USING btree (token_hash);


--
-- Name: ix_ndsp_auth_activation_tokens_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_auth_activation_tokens_user_id ON public.ndsp_auth_activation_tokens USING btree (user_id);


--
-- Name: ix_ndsp_auth_sessions_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_auth_sessions_user ON public.ndsp_auth_sessions USING btree (user_id);


--
-- Name: ix_ndsp_auth_tokens_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_auth_tokens_user ON public.ndsp_auth_activation_tokens USING btree (user_id);


--
-- Name: ix_ndsp_auth_users_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_auth_users_category ON public.ndsp_auth_users USING btree (category);


--
-- Name: ix_ndsp_auth_users_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_auth_users_status ON public.ndsp_auth_users USING btree (status);


--
-- Name: ix_ndsp_feedback_category_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_feedback_category_status ON public.ndsp_feedback_entries USING btree (category, status, created_at DESC);


--
-- Name: ix_ndsp_feedback_email_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_feedback_email_created ON public.ndsp_feedback_entries USING btree (email, created_at DESC);


--
-- Name: ix_ndsp_private_invite_codes_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_private_invite_codes_code ON public.ndsp_private_invite_codes USING btree (code);


--
-- Name: ix_ndsp_trial_attempts_ip_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ndsp_trial_attempts_ip_created ON public.ndsp_trial_attempts USING btree (ip_address, created_at);


--
-- Name: ix_user_alert_channels_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_alert_channels_email ON public.user_alert_channels USING btree (lower(email));


--
-- Name: ix_user_alert_channels_telegram_hash; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_alert_channels_telegram_hash ON public.user_alert_channels USING btree (telegram_link_code_hash);


--
-- Name: ix_user_alert_channels_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_alert_channels_user_id ON public.user_alert_channels USING btree (user_id);


--
-- Name: ndsp_auth_audit_created_at_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_auth_audit_created_at_idx ON public.ndsp_auth_audit USING btree (created_at DESC);


--
-- Name: ndsp_auth_sessions_expires_at_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_auth_sessions_expires_at_idx ON public.ndsp_auth_sessions USING btree (expires_at);


--
-- Name: ndsp_auth_sessions_user_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_auth_sessions_user_id_idx ON public.ndsp_auth_sessions USING btree (user_id);


--
-- Name: ndsp_clean_auth_audit_v2_created_at_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_clean_auth_audit_v2_created_at_idx ON public.ndsp_clean_auth_audit_v2 USING btree (created_at DESC);


--
-- Name: ndsp_clean_auth_sessions_v2_expires_at_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_clean_auth_sessions_v2_expires_at_idx ON public.ndsp_clean_auth_sessions_v2 USING btree (expires_at);


--
-- Name: ndsp_clean_auth_sessions_v2_user_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_clean_auth_sessions_v2_user_id_idx ON public.ndsp_clean_auth_sessions_v2 USING btree (user_id);


--
-- Name: ndsp_completed_decisions_created_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_completed_decisions_created_idx ON public.ndsp_completed_decisions USING btree (created_at DESC);


--
-- Name: ndsp_completed_decisions_state_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_completed_decisions_state_idx ON public.ndsp_completed_decisions USING btree (decision_state);


--
-- Name: ndsp_completed_decisions_symbol_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_completed_decisions_symbol_idx ON public.ndsp_completed_decisions USING btree (symbol);


--
-- Name: ndsp_decision_evidence_asset_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_decision_evidence_asset_time_idx ON public.ndsp_decision_evidence_snapshots USING btree (asset_symbol, timeframe, captured_at DESC);


--
-- Name: ndsp_decision_evidence_decision_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_decision_evidence_decision_time_idx ON public.ndsp_decision_evidence_snapshots USING btree (decision_id, captured_at DESC);


--
-- Name: ndsp_decision_timeline_decision_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_decision_timeline_decision_idx ON public.ndsp_decision_timeline USING btree (decision_id, created_at);


--
-- Name: ndsp_legal_acceptances_email_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_legal_acceptances_email_time_idx ON public.ndsp_legal_acceptances USING btree (email_sha256, accepted_at DESC);


--
-- Name: ndsp_legal_acceptances_subject_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_legal_acceptances_subject_time_idx ON public.ndsp_legal_acceptances USING btree (subject_key, accepted_at DESC) WHERE (subject_key IS NOT NULL);


--
-- Name: ndsp_nowpayments_status_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_nowpayments_status_idx ON public.ndsp_nowpayments_payments USING btree (payment_status);


--
-- Name: ndsp_nowpayments_user_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_nowpayments_user_idx ON public.ndsp_nowpayments_payments USING btree (user_id);


--
-- Name: ndsp_product_events_name_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_product_events_name_time_idx ON public.ndsp_product_events USING btree (event_name, occurred_at DESC);


--
-- Name: ndsp_product_events_subject_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_product_events_subject_time_idx ON public.ndsp_product_events USING btree (subject_key, occurred_at DESC) WHERE (subject_key IS NOT NULL);


--
-- Name: ndsp_provider_health_asset_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_provider_health_asset_time_idx ON public.ndsp_provider_health_history USING btree (asset_symbol, observed_at DESC) WHERE (asset_symbol IS NOT NULL);


--
-- Name: ndsp_provider_health_provider_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_provider_health_provider_time_idx ON public.ndsp_provider_health_history USING btree (provider_code, observed_at DESC);


--
-- Name: ndsp_registration_locks_email_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_registration_locks_email_idx ON public.ndsp_registration_locks USING btree (lower(email));


--
-- Name: ndsp_registration_locks_fingerprint_hash_unique; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ndsp_registration_locks_fingerprint_hash_unique ON public.ndsp_registration_locks USING btree (fingerprint_hash) WHERE ((fingerprint_hash IS NOT NULL) AND (is_active = true));


--
-- Name: ndsp_registration_locks_ip_hash_unique; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ndsp_registration_locks_ip_hash_unique ON public.ndsp_registration_locks USING btree (ip_hash) WHERE ((ip_hash IS NOT NULL) AND (is_active = true));


--
-- Name: ndsp_subscriptions_user_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_subscriptions_user_idx ON public.ndsp_subscriptions USING btree (user_id);


--
-- Name: ndsp_survey_questions_campaign_order_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_survey_questions_campaign_order_idx ON public.ndsp_survey_questions USING btree (campaign_key, display_order);


--
-- Name: ndsp_survey_responses_campaign_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_survey_responses_campaign_time_idx ON public.ndsp_survey_responses USING btree (campaign_key, started_at DESC);


--
-- Name: ndsp_usage_daily_feature_date_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_usage_daily_feature_date_idx ON public.ndsp_usage_daily USING btree (feature_code, usage_date DESC);


--
-- Name: ndsp_usage_daily_subject_date_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_usage_daily_subject_date_idx ON public.ndsp_usage_daily USING btree (subject_key, usage_date DESC);


--
-- Name: ndsp_usage_events_name_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_usage_events_name_time_idx ON public.ndsp_usage_events USING btree (event_name, occurred_at DESC);


--
-- Name: ndsp_usage_events_subject_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_usage_events_subject_time_idx ON public.ndsp_usage_events USING btree (subject_key, occurred_at DESC);


--
-- Name: ndsp_user_experience_events_user_created_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_user_experience_events_user_created_idx ON public.ndsp_user_experience_events USING btree (user_id, created_at DESC);


--
-- Name: ndsp_user_notifications_user_created_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_user_notifications_user_created_idx ON public.ndsp_user_notifications USING btree (user_id, created_at DESC);


--
-- Name: notifications_user_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX notifications_user_idx ON public.notifications USING btree (user_id, created_at DESC);


--
-- Name: users_canonical_email_unique_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX users_canonical_email_unique_idx ON public.users USING btree (canonical_email) WHERE ((canonical_email IS NOT NULL) AND (canonical_email <> ''::text));


--
-- Name: users_canonical_phone_unique_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX users_canonical_phone_unique_idx ON public.users USING btree (canonical_phone) WHERE ((canonical_phone IS NOT NULL) AND (canonical_phone <> ''::text));


--
-- Name: users_email_lower_unique_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX users_email_lower_unique_idx ON public.users USING btree (lower(email));


--
-- Name: users_email_unique_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX users_email_unique_idx ON public.users USING btree (lower(email));


--
-- Name: users_phone_last9_unique_v45; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX users_phone_last9_unique_v45 ON public.users USING btree ("right"(regexp_replace(COALESCE(phone, ''::text), '[^0-9]+'::text, ''::text, 'g'::text), 9)) WHERE ((phone IS NOT NULL) AND (btrim(phone) <> ''::text) AND (length("right"(regexp_replace(COALESCE(phone, ''::text), '[^0-9]+'::text, ''::text, 'g'::text), 9)) = 9));


--
-- Name: users_phone_unique_nonempty; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX users_phone_unique_nonempty ON public.users USING btree (phone) WHERE ((phone IS NOT NULL) AND (btrim(phone) <> ''::text));


--
-- Name: ux_ndsp_trial_email_normalized; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ux_ndsp_trial_email_normalized ON public.ndsp_trial_registrations USING btree (email_normalized);


--
-- Name: ux_ndsp_trial_fingerprint_guard_hash; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ux_ndsp_trial_fingerprint_guard_hash ON public.ndsp_trial_fingerprint_guard USING btree (fingerprint_hash);


--
-- Name: ux_ndsp_trial_phone_e164; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ux_ndsp_trial_phone_e164 ON public.ndsp_trial_registrations USING btree (phone_e164);


--
-- Name: ux_users_email_lower; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ux_users_email_lower ON public.users USING btree (lower(email)) WHERE ((email IS NOT NULL) AND (email <> ''::text));


--
-- Name: ux_users_phone_digits; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ux_users_phone_digits ON public.users USING btree (regexp_replace(COALESCE(phone, ''::text), '[^0-9]+'::text, ''::text, 'g'::text)) WHERE ((phone IS NOT NULL) AND (regexp_replace(COALESCE(phone, ''::text), '[^0-9]+'::text, ''::text, 'g'::text) <> ''::text));


--
-- Name: ndsp_seats_status _RETURN; Type: RULE; Schema: public; Owner: -
--

CREATE OR REPLACE VIEW public.ndsp_seats_status AS
 SELECT p.cohort_code AS code,
    p.cohort_label_ar AS name_ar,
    p.cohort_label_en AS name_en,
    p.max_seats AS total_seats,
    (count(a.id) FILTER (WHERE (a.status = 'reserved'::text)))::integer AS used_seats,
    ((p.max_seats - count(a.id) FILTER (WHERE (a.status = 'reserved'::text))))::integer AS available_seats,
    round(((100.0 * (count(a.id) FILTER (WHERE (a.status = 'reserved'::text)))::numeric) / (NULLIF(p.max_seats, 0))::numeric), 1) AS fill_pct
   FROM (public.ndsp_trial_seat_policy p
     LEFT JOIN public.ndsp_trial_seat_assignments a ON ((a.cohort_code = p.cohort_code)))
  WHERE p.is_active
  GROUP BY p.id, p.cohort_code, p.cohort_label_ar, p.cohort_label_en, p.max_seats
  ORDER BY p.sort_order;


--
-- Name: ndsp_auth_users ndsp_prevent_duplicate_identity_ndsp_auth_users_; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER ndsp_prevent_duplicate_identity_ndsp_auth_users_ BEFORE INSERT OR UPDATE ON public.ndsp_auth_users FOR EACH ROW EXECUTE FUNCTION ndsp_guard.prevent_duplicate_identity_safe('email', 'phone');


--
-- Name: ndsp_trial_activation_requests ndsp_prevent_duplicate_identity_ndsp_trial_activation_r; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER ndsp_prevent_duplicate_identity_ndsp_trial_activation_r BEFORE INSERT OR UPDATE ON public.ndsp_trial_activation_requests FOR EACH ROW EXECUTE FUNCTION ndsp_guard.prevent_duplicate_identity_safe('email', '');


--
-- Name: ndsp_trial_registrations ndsp_prevent_duplicate_identity_ndsp_trial_registration; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER ndsp_prevent_duplicate_identity_ndsp_trial_registration BEFORE INSERT OR UPDATE ON public.ndsp_trial_registrations FOR EACH ROW EXECUTE FUNCTION ndsp_guard.prevent_duplicate_identity_safe('email', 'phone');


--
-- Name: ndsp_users ndsp_prevent_duplicate_identity_ndsp_users_; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER ndsp_prevent_duplicate_identity_ndsp_users_ BEFORE INSERT OR UPDATE ON public.ndsp_users FOR EACH ROW EXECUTE FUNCTION ndsp_guard.prevent_duplicate_identity_safe('email', '');


--
-- Name: registration_requests ndsp_prevent_duplicate_identity_registration_requests_; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER ndsp_prevent_duplicate_identity_registration_requests_ BEFORE INSERT OR UPDATE ON public.registration_requests FOR EACH ROW EXECUTE FUNCTION ndsp_guard.prevent_duplicate_identity_safe('email', 'phone');


--
-- Name: users ndsp_prevent_duplicate_identity_users_; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER ndsp_prevent_duplicate_identity_users_ BEFORE INSERT OR UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION ndsp_guard.prevent_duplicate_identity_safe('email', 'phone');


--
-- Name: users ndsp_trial_guard_before_insert; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER ndsp_trial_guard_before_insert BEFORE INSERT ON public.users FOR EACH ROW EXECUTE FUNCTION public.ndsp_guard_trial_registration_before_activation();


--
-- Name: users trg_ndsp_enforce_activation_trial_policy; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_ndsp_enforce_activation_trial_policy BEFORE INSERT OR UPDATE OF status ON public.users FOR EACH ROW EXECUTE FUNCTION public.ndsp_enforce_activation_trial_policy();


--
-- Name: registration_requests trg_ndsp_set_registration_review_status; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_ndsp_set_registration_review_status BEFORE INSERT ON public.registration_requests FOR EACH ROW EXECUTE FUNCTION public.ndsp_set_registration_review_status();


--
-- Name: users trg_ndsp_sync_access_guard_credentials_from_users; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_ndsp_sync_access_guard_credentials_from_users AFTER INSERT OR UPDATE OF email, password_hash ON public.users FOR EACH ROW EXECUTE FUNCTION public.ndsp_sync_access_guard_credentials_from_users();


--
-- Name: users trg_ndsp_users_normalize_identity; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_ndsp_users_normalize_identity BEFORE INSERT OR UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.ndsp_users_normalize_identity();


--
-- Name: users trg_users_phone_unique_guard; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_users_phone_unique_guard BEFORE INSERT OR UPDATE OF phone ON public.users FOR EACH ROW EXECUTE FUNCTION public.ndsp_users_phone_unique_guard();


--
-- Name: email_delivery_log email_delivery_log_related_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_delivery_log
    ADD CONSTRAINT email_delivery_log_related_request_id_fkey FOREIGN KEY (related_request_id) REFERENCES public.registration_requests(id) ON DELETE SET NULL;


--
-- Name: feedback_surveys feedback_surveys_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.feedback_surveys
    ADD CONSTRAINT feedback_surveys_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: ndsp_auth_sessions ndsp_auth_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_auth_sessions
    ADD CONSTRAINT ndsp_auth_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ndsp_auth_users(id) ON DELETE CASCADE;


--
-- Name: ndsp_decision_evidence_snapshots ndsp_decision_evidence_snapshots_supersedes_evidence_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_decision_evidence_snapshots
    ADD CONSTRAINT ndsp_decision_evidence_snapshots_supersedes_evidence_id_fkey FOREIGN KEY (supersedes_evidence_id) REFERENCES public.ndsp_decision_evidence_snapshots(evidence_id);


--
-- Name: ndsp_invitation_codes ndsp_invitation_codes_cohort_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_invitation_codes
    ADD CONSTRAINT ndsp_invitation_codes_cohort_code_fkey FOREIGN KEY (cohort_code) REFERENCES public.ndsp_trial_seat_policy(cohort_code) ON UPDATE CASCADE;


--
-- Name: ndsp_nowpayments_payments ndsp_nowpayments_payments_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_nowpayments_payments
    ADD CONSTRAINT ndsp_nowpayments_payments_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.ndsp_plans(id) ON DELETE SET NULL;


--
-- Name: ndsp_plan_layers ndsp_plan_layers_layer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_plan_layers
    ADD CONSTRAINT ndsp_plan_layers_layer_id_fkey FOREIGN KEY (layer_id) REFERENCES public.ndsp_layers(id) ON DELETE CASCADE;


--
-- Name: ndsp_plan_layers ndsp_plan_layers_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_plan_layers
    ADD CONSTRAINT ndsp_plan_layers_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.ndsp_plans(id) ON DELETE CASCADE;


--
-- Name: ndsp_sessions ndsp_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_sessions
    ADD CONSTRAINT ndsp_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ndsp_users(id) ON DELETE CASCADE;


--
-- Name: ndsp_subscriptions ndsp_subscriptions_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_subscriptions
    ADD CONSTRAINT ndsp_subscriptions_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.ndsp_plans(id) ON DELETE SET NULL;


--
-- Name: ndsp_survey_answers ndsp_survey_answers_question_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_survey_answers
    ADD CONSTRAINT ndsp_survey_answers_question_key_fkey FOREIGN KEY (question_key) REFERENCES public.ndsp_survey_questions(question_key);


--
-- Name: ndsp_survey_answers ndsp_survey_answers_response_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_survey_answers
    ADD CONSTRAINT ndsp_survey_answers_response_key_fkey FOREIGN KEY (response_key) REFERENCES public.ndsp_survey_responses(response_key) ON DELETE CASCADE;


--
-- Name: ndsp_survey_questions ndsp_survey_questions_campaign_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_survey_questions
    ADD CONSTRAINT ndsp_survey_questions_campaign_key_fkey FOREIGN KEY (campaign_key) REFERENCES public.ndsp_survey_campaigns(campaign_key) ON DELETE CASCADE;


--
-- Name: ndsp_survey_responses ndsp_survey_responses_campaign_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_survey_responses
    ADD CONSTRAINT ndsp_survey_responses_campaign_key_fkey FOREIGN KEY (campaign_key) REFERENCES public.ndsp_survey_campaigns(campaign_key);


--
-- Name: ndsp_trial_seat_assignments ndsp_trial_seat_assignments_cohort_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_trial_seat_assignments
    ADD CONSTRAINT ndsp_trial_seat_assignments_cohort_code_fkey FOREIGN KEY (cohort_code) REFERENCES public.ndsp_trial_seat_policy(cohort_code) ON UPDATE CASCADE;


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: plan_features plan_features_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plan_features
    ADD CONSTRAINT plan_features_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.plans(id) ON DELETE CASCADE;


--
-- Name: plan_layer_access plan_layer_access_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plan_layer_access
    ADD CONSTRAINT plan_layer_access_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.plans(id) ON DELETE CASCADE;


--
-- Name: plan_upgrade_requests plan_upgrade_requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plan_upgrade_requests
    ADD CONSTRAINT plan_upgrade_requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: registration_attachments registration_attachments_registration_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_attachments
    ADD CONSTRAINT registration_attachments_registration_request_id_fkey FOREIGN KEY (registration_request_id) REFERENCES public.registration_requests(id) ON DELETE CASCADE;


--
-- Name: registration_requests registration_requests_invite_code_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_requests
    ADD CONSTRAINT registration_requests_invite_code_id_fkey FOREIGN KEY (invite_code_id) REFERENCES public.invite_codes(id) ON DELETE SET NULL;


--
-- Name: user_2fa_settings user_2fa_settings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_2fa_settings
    ADD CONSTRAINT user_2fa_settings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: users users_invite_code_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_invite_code_id_fkey FOREIGN KEY (invite_code_id) REFERENCES public.invite_codes(id) ON DELETE SET NULL;


--
-- Name: users users_plan_id_ndsp_plans_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_plan_id_ndsp_plans_fk FOREIGN KEY (plan_id) REFERENCES public.ndsp_plans(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

\unrestrict 2OyYMQImzVWiqKEu4BUDIX1FlPbhvMMlVRaCfcd31b9W9rbNdSnZYTOgc6efPlM

