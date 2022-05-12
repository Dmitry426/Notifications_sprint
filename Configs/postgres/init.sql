CREATE SCHEMA IF NOT EXISTS events;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS events.notifications(
    id uuid PRIMARY KEY  DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    body TEXT NOT NULL,
    is_read boolean DEFAULT FALSE,
    created_at timestamptz DEFAULT NOW(),
    updated_at timestamptz DEFAULT NOW()
);
