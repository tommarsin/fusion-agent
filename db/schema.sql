-- ============================================================
-- Fusion Agent — Game Content Compliance AI System
-- Schema v1.0 — VNG Cloud vDB (PostgreSQL)
-- Áp theo concept.md §3 (quyết định #005–#010)
-- ============================================================

-- ── Enum types ────────────────────────────────────────────────────────────────

DO $$ BEGIN
  CREATE TYPE content_layer_enum AS ENUM (
    'legal_source', 'operating_rule', 'daily_tool', 'platform_policy', 'case_study'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE rule_scope_enum AS ENUM ('core', 'tenant', 'campaign');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE rule_status_enum AS ENUM ('pending', 'approved', 'rejected');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE platform_enum AS ENUM (
    'meta', 'tiktok', 'google', 'store', 'website', 'group', 'all'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE audit_action_enum AS ENUM ('ask', 'scan', 'ingest', 'approve');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE role_enum AS ENUM ('Admin', 'Mod', 'User');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE submission_status_enum AS ENUM ('pending', 'approved', 'rejected');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE campaign_status_enum AS ENUM ('active', 'paused', 'ended');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- ── Tables ────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS tenants (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    slug        TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS campaigns (
    id          SERIAL PRIMARY KEY,
    tenant_id   INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    platforms   platform_enum[] NOT NULL DEFAULT '{}',
    period      TEXT,                    -- vd "2026-Q3", free-form cho POC
    status      campaign_status_enum NOT NULL DEFAULT 'active',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rules (
    id                  SERIAL PRIMARY KEY,
    doc_id              TEXT NOT NULL UNIQUE,   -- vd "LEGAL-001", "OP-013"
    content_layer       content_layer_enum NOT NULL,
    scope               rule_scope_enum NOT NULL DEFAULT 'core',
    tenant_id           INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    campaign_id         INTEGER REFERENCES campaigns(id) ON DELETE SET NULL,
    platforms           platform_enum[] NOT NULL DEFAULT '{all}',
    status              rule_status_enum NOT NULL DEFAULT 'approved',
    title               TEXT NOT NULL,
    body_md             TEXT NOT NULL,
    metadata_json       JSONB NOT NULL DEFAULT '{}',
    source_url          TEXT,
    related_core_doc_id TEXT REFERENCES rules(doc_id) ON DELETE SET NULL,
    version             INTEGER NOT NULL DEFAULT 1,
    created_by_role     role_enum NOT NULL DEFAULT 'Admin',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- siết-only constraint: tenant/campaign rules phải có tenant_id
    CONSTRAINT tenant_rule_needs_tenant CHECK (
        scope = 'core' OR tenant_id IS NOT NULL
    )
);

CREATE TABLE IF NOT EXISTS rule_versions (
    id              SERIAL PRIMARY KEY,
    rule_id         INTEGER NOT NULL REFERENCES rules(id) ON DELETE CASCADE,
    version         INTEGER NOT NULL,
    raw_text        TEXT NOT NULL,
    structured_md   TEXT,
    source_url      TEXT,
    fetched_at      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (rule_id, version)
);

CREATE TABLE IF NOT EXISTS rule_submissions (
    id                  SERIAL PRIMARY KEY,
    link                TEXT NOT NULL,
    note                TEXT,
    submitted_by_role   role_enum NOT NULL DEFAULT 'Mod',
    tenant_id           INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    status              submission_status_enum NOT NULL DEFAULT 'pending',
    reviewed_at         TIMESTAMPTZ,
    result_rule_id      INTEGER REFERENCES rules(id) ON DELETE SET NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_log (
    id          SERIAL PRIMARY KEY,
    actor_role  role_enum NOT NULL,
    tenant_id   INTEGER REFERENCES tenants(id) ON DELETE SET NULL,
    action      audit_action_enum NOT NULL,
    input_hash  TEXT,       -- SHA-256 của input content (privacy)
    verdict     TEXT,       -- SAFE | WARNING | BLOCKED | n/a
    summary     TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ai_config (
    id                  INTEGER PRIMARY KEY DEFAULT 1,
    detect_mode         TEXT NOT NULL DEFAULT 'strict',
    on_violation        TEXT NOT NULL DEFAULT 'warn_explain_suggest',
    explanation_style   TEXT NOT NULL DEFAULT 'detailed',
    CONSTRAINT single_row CHECK (id = 1)   -- read-only seed, không có UI chỉnh (#009)
);

-- ── Indexes ───────────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_rules_scope_status
    ON rules(scope, status);

CREATE INDEX IF NOT EXISTS idx_rules_tenant
    ON rules(tenant_id) WHERE tenant_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_rules_content_layer
    ON rules(content_layer);

CREATE INDEX IF NOT EXISTS idx_audit_log_created
    ON audit_log(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_audit_log_tenant
    ON audit_log(tenant_id) WHERE tenant_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_rule_submissions_status
    ON rule_submissions(status);

-- ── Seed data ─────────────────────────────────────────────────────────────────
-- (khớp với dữ liệu thực tế đã seed vào vDB 2026-06-12; idempotent)

-- ai_config: read-only seed (quyết định #009) — strict detect, warn+explain+suggest
INSERT INTO ai_config (id, detect_mode, on_violation, explanation_style)
VALUES (1, 'strict', 'warn_explain_suggest', 'detailed')
ON CONFLICT (id) DO NOTHING;

-- Tenants: 2 game demo hư cấu
INSERT INTO tenants (name, slug) VALUES
    ('Nova Studios', 'nova-studios'),
    ('Pixel Realm',  'pixel-realm')
ON CONFLICT (slug) DO NOTHING;

-- Campaign mẫu
INSERT INTO campaigns (tenant_id, name, platforms, period, status)
SELECT t.id, 'Summer Launch 2026', ARRAY['meta','tiktok']::platform_enum[], 'Q3 2026', 'active'
FROM tenants t WHERE t.slug = 'nova-studios'
ON CONFLICT DO NOTHING;

-- Core rules: legal + platform policy mẫu
INSERT INTO rules (doc_id, content_layer, scope, platforms, status, title, body_md,
                   metadata_json, source_url, version, created_by_role)
VALUES
  (
    'CORE-LEGAL-001',
    'legal_source',
    'core',
    ARRAY['all']::platform_enum[],
    'approved',
    'Luat Quang cao - Cam tu tuyet doi khong chung minh',
    $body$## Luat Quang cao 2012 - Dieu 8
Cam quang cao su dung cac tu tuyet doi ("nhat", "so mot", "duy nhat")
ma khong co tai lieu chung minh. Ap dung cho moi kenh quang cao game.$body$,
    '{"law_id": "36/2012/QH13", "effective": "2013-01-01", "priority": "critical"}',
    'https://thuvienphapluat.vn/van-ban/Thuong-mai/Luat-Quang-cao-2012-142928.aspx',
    1,
    'Admin'
  ),
  (
    'CORE-LEGAL-002',
    'legal_source',
    'core',
    ARRAY['all']::platform_enum[],
    'approved',
    'ND13/2023 - Thu thap du lieu ca nhan trong su kien game',
    $body$## Nghi dinh 13/2023/ND-CP
Yeu cau dong y ro rang truoc khi thu thap du lieu ca nhan.
CCCD/CMND = du lieu nhay cam — BLOCKED trong marketing game.$body$,
    '{"law_id": "13/2023/ND-CP", "effective": "2023-07-01", "priority": "critical"}',
    'https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/Nghi-dinh-13-2023-ND-CP-bao-ve-du-lieu-ca-nhan-562178.aspx',
    1,
    'Admin'
  ),
  (
    'CORE-PLATFORM-001',
    'platform_policy',
    'core',
    ARRAY['meta']::platform_enum[],
    'approved',
    'Meta Ads - Noi dung cam trong quang cao game',
    $body$## Meta Advertising Policies
Cam: noi dung cam ky, bao luc qua muc, quang cao co bac.
Han che: game co yeu to thuong mai ao, tu khoa nhay cam.$body$,
    '{"platform": "meta", "priority": "high"}',
    'https://www.facebook.com/policies/ads/',
    1,
    'Admin'
  )
ON CONFLICT (doc_id) DO NOTHING;
