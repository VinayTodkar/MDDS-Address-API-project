-- =========================================================
-- MDDS Address API - PostgreSQL Database Schema
-- Phase 1
-- =========================================================

-- ---------------------------------------------------------
-- EXTENSIONS
-- ---------------------------------------------------------

CREATE EXTENSION IF NOT EXISTS pg_trgm;


-- =========================================================
-- COUNTRY
-- =========================================================

CREATE TABLE IF NOT EXISTS countries (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT countries_name_unique UNIQUE (name)
);


-- =========================================================
-- STATE
-- =========================================================

CREATE TABLE IF NOT EXISTS states (
    id BIGSERIAL PRIMARY KEY,

    code VARCHAR(10) NOT NULL,
    name VARCHAR(150) NOT NULL,

    country_id BIGINT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_states_country
        FOREIGN KEY (country_id)
        REFERENCES countries(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT states_country_code_unique
        UNIQUE (country_id, code)
);


-- =========================================================
-- DISTRICT
-- =========================================================

CREATE TABLE IF NOT EXISTS districts (
    id BIGSERIAL PRIMARY KEY,

    code VARCHAR(20) NOT NULL,
    name VARCHAR(150) NOT NULL,

    state_id BIGINT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_districts_state
        FOREIGN KEY (state_id)
        REFERENCES states(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT districts_state_code_unique
        UNIQUE (state_id, code)
);


-- =========================================================
-- SUB-DISTRICT
-- =========================================================

CREATE TABLE IF NOT EXISTS sub_districts (
    id BIGSERIAL PRIMARY KEY,

    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,

    district_id BIGINT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_sub_districts_district
        FOREIGN KEY (district_id)
        REFERENCES districts(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT sub_districts_district_code_unique
        UNIQUE (district_id, code)
);


-- =========================================================
-- VILLAGE / AREA
-- =========================================================

CREATE TABLE IF NOT EXISTS villages (
    id BIGSERIAL PRIMARY KEY,

    code VARCHAR(30) NOT NULL,
    name VARCHAR(250) NOT NULL,

    sub_district_id BIGINT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_villages_sub_district
        FOREIGN KEY (sub_district_id)
        REFERENCES sub_districts(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT villages_sub_district_code_unique
        UNIQUE (sub_district_id, code)
);


-- =========================================================
-- USER
-- =========================================================

CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,

    email VARCHAR(255) NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,

    plan_type VARCHAR(50) NOT NULL DEFAULT 'FREE',

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT users_plan_type_check
        CHECK (plan_type IN ('FREE', 'BASIC', 'PRO', 'ENTERPRISE', 'ADMIN'))
);


-- =========================================================
-- API KEY
-- =========================================================

CREATE TABLE IF NOT EXISTS api_keys (
    id BIGSERIAL PRIMARY KEY,

    key VARCHAR(100) NOT NULL UNIQUE,

    secret_hash TEXT NOT NULL,

    user_id BIGINT NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ,

    CONSTRAINT fk_api_keys_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- =========================================================
-- USER STATE ACCESS
-- =========================================================

CREATE TABLE IF NOT EXISTS user_state_access (
    user_id BIGINT NOT NULL,
    state_id BIGINT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id, state_id),

    CONSTRAINT fk_user_state_access_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_user_state_access_state
        FOREIGN KEY (state_id)
        REFERENCES states(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- =========================================================
-- API LOG
-- =========================================================

CREATE TABLE IF NOT EXISTS api_logs (
    id BIGSERIAL PRIMARY KEY,

    endpoint VARCHAR(500) NOT NULL,

    method VARCHAR(10),

    response_time_ms INTEGER,

    status_code INTEGER,

    api_key_id BIGINT,

    user_id BIGINT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_api_logs_api_key
        FOREIGN KEY (api_key_id)
        REFERENCES api_keys(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_api_logs_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


-- =========================================================
-- INDEXES
-- =========================================================

-- State
CREATE INDEX IF NOT EXISTS idx_states_country_id
ON states(country_id);

CREATE INDEX IF NOT EXISTS idx_states_name
ON states(name);


-- District
CREATE INDEX IF NOT EXISTS idx_districts_state_id
ON districts(state_id);

CREATE INDEX IF NOT EXISTS idx_districts_name
ON districts(name);


-- Sub-District
CREATE INDEX IF NOT EXISTS idx_sub_districts_district_id
ON sub_districts(district_id);

CREATE INDEX IF NOT EXISTS idx_sub_districts_name
ON sub_districts(name);


-- Village
CREATE INDEX IF NOT EXISTS idx_villages_sub_district_id
ON villages(sub_district_id);

CREATE INDEX IF NOT EXISTS idx_villages_name
ON villages(name);


-- Trigram indexes for faster name searching
CREATE INDEX IF NOT EXISTS idx_villages_name_trgm
ON villages
USING GIN (name gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_sub_districts_name_trgm
ON sub_districts
USING GIN (name gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_districts_name_trgm
ON districts
USING GIN (name gin_trgm_ops);


-- User/API indexes
CREATE INDEX IF NOT EXISTS idx_api_keys_user_id
ON api_keys(user_id);

CREATE INDEX IF NOT EXISTS idx_api_logs_created_at
ON api_logs(created_at);

CREATE INDEX IF NOT EXISTS idx_api_logs_user_id
ON api_logs(user_id);

CREATE INDEX IF NOT EXISTS idx_api_logs_api_key_id
ON api_logs(api_key_id);


-- =========================================================
-- INITIAL COUNTRY
-- =========================================================

INSERT INTO countries (name, code)
VALUES ('India', 'IN')
ON CONFLICT (code) DO NOTHING;


-- =========================================================
-- VERIFICATION
-- =========================================================

SELECT
    table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;