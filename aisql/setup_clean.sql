-- SQLite version of cleaned PostgreSQL schema
-- Custom tables for testing with db_bot

-- Custom function simulation (SQLite doesn't have custom functions like PostgreSQL)
-- We'll handle updated_at in application code or use triggers

-- Custom table: companies
CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    name TEXT,
    year_founded INTEGER
);

-- Custom table: roles  
CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    role TEXT
);

-- Custom table: users
CREATE TABLE users (
    id TEXT PRIMARY KEY, -- UUID as TEXT in SQLite
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    email TEXT DEFAULT '' NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    credits INTEGER DEFAULT 0,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Custom table: users_companies
CREATE TABLE users_companies (
    user_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    company_id INTEGER,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Custom table: waitlist_emails
CREATE TABLE waitlist_emails (
    id TEXT PRIMARY KEY, -- UUID as TEXT in SQLite
    email TEXT NOT NULL UNIQUE,
    source TEXT DEFAULT 'landing_page',
    metadata TEXT DEFAULT '{}', -- JSON as TEXT in SQLite
    subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    approved BOOLEAN DEFAULT 0,
    approved_at DATETIME,
    approved_by TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CHECK (status IN ('pending', 'active', 'unsubscribed', 'converted'))
);

-- Custom table: cim_form_submissions
CREATE TABLE cim_form_submissions (
    id TEXT PRIMARY KEY, -- UUID as TEXT in SQLite
    company_name TEXT NOT NULL,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    form_data TEXT NOT NULL, -- JSON as TEXT in SQLite
    status TEXT DEFAULT 'submitted',
    generated_cim TEXT,
    generated_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    submitter_email TEXT,
    company_id INTEGER,
    CHECK (status IN ('submitted', 'processing', 'completed', 'failed')),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Indexes for performance
CREATE INDEX idx_form_submissions_company_name ON cim_form_submissions(company_name);
CREATE INDEX idx_form_submissions_status ON cim_form_submissions(status);
CREATE INDEX idx_form_submissions_submitted_at ON cim_form_submissions(submitted_at);

-- Trigger to update updated_at (SQLite trigger syntax)
CREATE TRIGGER update_form_submissions_updated_at 
    BEFORE UPDATE ON cim_form_submissions
    FOR EACH ROW
    BEGIN
        UPDATE cim_form_submissions SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER update_waitlist_emails_updated_at 
    BEFORE UPDATE ON waitlist_emails
    FOR EACH ROW
    BEGIN
        UPDATE waitlist_emails SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
