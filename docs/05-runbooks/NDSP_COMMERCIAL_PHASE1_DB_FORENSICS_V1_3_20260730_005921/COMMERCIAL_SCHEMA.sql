
-- ============================================================
-- TABLE: public.ndsp_legal_acceptances
-- ============================================================
--
-- PostgreSQL database dump
--

\restrict oXTj2SNF9jsUbeISsusgopn2UH6DlhyTpGWNLCJ91JnaephMMHL223dCChJd1ej

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

SET default_tablespace = '';

SET default_table_access_method = heap;

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
-- Name: ndsp_legal_acceptances_email_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_legal_acceptances_email_time_idx ON public.ndsp_legal_acceptances USING btree (email_sha256, accepted_at DESC);


--
-- Name: ndsp_legal_acceptances_subject_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_legal_acceptances_subject_time_idx ON public.ndsp_legal_acceptances USING btree (subject_key, accepted_at DESC) WHERE (subject_key IS NOT NULL);


--
-- PostgreSQL database dump complete
--

\unrestrict oXTj2SNF9jsUbeISsusgopn2UH6DlhyTpGWNLCJ91JnaephMMHL223dCChJd1ej


-- ============================================================
-- TABLE: public.ndsp_subscriptions
-- ============================================================
--
-- PostgreSQL database dump
--

\restrict KgP0I8JsCSiYPkZyFGd0CIaeqsWUnvWrtf0Qjgh16Za4qZqxYoCqdaaaS83UtbG

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

SET default_tablespace = '';

SET default_table_access_method = heap;

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
-- Name: ndsp_subscriptions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_subscriptions ALTER COLUMN id SET DEFAULT nextval('public.ndsp_subscriptions_id_seq'::regclass);


--
-- Name: ndsp_subscriptions ndsp_subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_subscriptions
    ADD CONSTRAINT ndsp_subscriptions_pkey PRIMARY KEY (id);


--
-- Name: idx_ndsp_subscriptions_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ndsp_subscriptions_user ON public.ndsp_subscriptions USING btree (user_id);


--
-- Name: ndsp_subscriptions_user_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ndsp_subscriptions_user_idx ON public.ndsp_subscriptions USING btree (user_id);


--
-- Name: ndsp_subscriptions ndsp_subscriptions_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ndsp_subscriptions
    ADD CONSTRAINT ndsp_subscriptions_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.ndsp_plans(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

\unrestrict KgP0I8JsCSiYPkZyFGd0CIaeqsWUnvWrtf0Qjgh16Za4qZqxYoCqdaaaS83UtbG

