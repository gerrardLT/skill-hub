-- The application uses SQLAlchemy metadata for portable initialization.
-- This file documents PostgreSQL production prerequisites and hardening.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Recommended role split. Replace passwords and ownership in deployment automation.
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'agentic_sdlc_app') THEN
    CREATE ROLE agentic_sdlc_app LOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'agentic_sdlc_readonly') THEN
    CREATE ROLE agentic_sdlc_readonly LOGIN;
  END IF;
END $$;

ALTER DATABASE agentic_sdlc SET timezone TO 'UTC';
ALTER DATABASE agentic_sdlc SET statement_timeout TO '30s';
ALTER DATABASE agentic_sdlc SET idle_in_transaction_session_timeout TO '60s';
