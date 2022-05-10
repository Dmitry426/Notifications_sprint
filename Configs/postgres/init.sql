CREATE SCHEMA IF NOT EXISTS events;

CREATE TABLE IF NOT EXISTS events.recipient(
    id uuid PRIMARY KEY  DEFAULT gen_random_uuid(),
    login TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    status boolean DEFAULT FALSE,
    redirect_url TEXT NOT NULL,
    created_at timestamptz DEFAULT NOW(),
    updated_at timestamptz DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS events.scheduler(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    template TEXT NOT NULL,
    recipient TEXT NOT NULL,
    "when" TEXT NOT NULL,
    priority TEXT NOT NULL,
    created_at timestamptz DEFAULT NOW(),
    updated_at timestamptz DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS events.scheduler_id_recipient(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    scheduler uuid,
    recipient uuid
);
