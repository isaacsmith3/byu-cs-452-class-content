-- Sample data for cleaned custom schema
-- Inserting realistic test data for all custom tables

-- Insert roles first (referenced by users)
INSERT INTO roles (id, role, created_at) VALUES
(1, 'admin', '2024-01-01 00:00:00'),
(2, 'user', '2024-01-01 00:00:00'),
(3, 'moderator', '2024-01-01 00:00:00');

-- Insert companies (referenced by users_companies and cim_form_submissions)
INSERT INTO companies (id, name, year_founded, created_at) VALUES
(1, 'TechCorp Solutions', 2015, '2024-01-01 00:00:00'),
(2, 'DataFlow Inc', 2018, '2024-01-01 00:00:00'),
(3, 'CloudSystems Ltd', 2020, '2024-01-01 00:00:00'),
(4, 'AI Innovations', 2019, '2024-01-01 00:00:00'),
(5, 'StartupXYZ', 2022, '2024-01-01 00:00:00');

-- Insert users (with role references)
INSERT INTO users (id, email, first_name, last_name, credits, role_id, created_at) VALUES
('user-001', 'john.doe@techcorp.com', 'John', 'Doe', 100, 1, '2024-01-15 10:00:00'),
('user-002', 'jane.smith@dataflow.com', 'Jane', 'Smith', 50, 2, '2024-01-16 11:00:00'),
('user-003', 'bob.wilson@cloudsystems.com', 'Bob', 'Wilson', 75, 2, '2024-01-17 12:00:00'),
('user-004', 'alice.brown@aiinnovations.com', 'Alice', 'Brown', 200, 1, '2024-01-18 13:00:00'),
('user-005', 'charlie.davis@startupxyz.com', 'Charlie', 'Davis', 25, 3, '2024-01-19 14:00:00'),
('user-006', 'diana.garcia@techcorp.com', 'Diana', 'Garcia', 150, 2, '2024-01-20 15:00:00');

-- Insert user-company relationships
INSERT INTO users_companies (user_id, company_id, created_at) VALUES
('user-001', 1, '2024-01-15 10:00:00'),
('user-002', 2, '2024-01-16 11:00:00'),
('user-003', 3, '2024-01-17 12:00:00'),
('user-004', 4, '2024-01-18 13:00:00'),
('user-005', 5, '2024-01-19 14:00:00'),
('user-006', 1, '2024-01-20 15:00:00');

-- Insert waitlist emails
INSERT INTO waitlist_emails (id, email, source, metadata, status, approved, subscribed_at, created_at) VALUES
('waitlist-001', 'early.adopter@email.com', 'landing_page', '{"interest": "ai", "source": "google"}', 'active', 1, '2024-01-01 09:00:00', '2024-01-01 09:00:00'),
('waitlist-002', 'beta.tester@email.com', 'social_media', '{"interest": "analytics", "source": "twitter"}', 'pending', 0, '2024-01-02 10:00:00', '2024-01-02 10:00:00'),
('waitlist-003', 'potential.customer@email.com', 'landing_page', '{"interest": "automation", "source": "linkedin"}', 'converted', 1, '2024-01-03 11:00:00', '2024-01-03 11:00:00'),
('waitlist-004', 'curious.user@email.com', 'referral', '{"interest": "ml", "source": "friend"}', 'unsubscribed', 0, '2024-01-04 12:00:00', '2024-01-04 12:00:00'),
('waitlist-005', 'enterprise.lead@email.com', 'landing_page', '{"interest": "enterprise", "source": "google"}', 'active', 1, '2024-01-05 13:00:00', '2024-01-05 13:00:00');

-- Insert CIM form submissions
INSERT INTO cim_form_submissions (id, company_name, form_data, status, submitter_email, company_id, submitted_at, created_at) VALUES
('form-001', 'TechCorp Solutions', '{"company_size": "50-100", "industry": "technology", "budget": "high"}', 'completed', 'john.doe@techcorp.com', 1, '2024-01-10 10:00:00', '2024-01-10 10:00:00'),
('form-002', 'DataFlow Inc', '{"company_size": "10-50", "industry": "data", "budget": "medium"}', 'processing', 'jane.smith@dataflow.com', 2, '2024-01-11 11:00:00', '2024-01-11 11:00:00'),
('form-003', 'CloudSystems Ltd', '{"company_size": "100+", "industry": "cloud", "budget": "high"}', 'submitted', 'bob.wilson@cloudsystems.com', 3, '2024-01-12 12:00:00', '2024-01-12 12:00:00'),
('form-004', 'AI Innovations', '{"company_size": "5-10", "industry": "ai", "budget": "low"}', 'failed', 'alice.brown@aiinnovations.com', 4, '2024-01-13 13:00:00', '2024-01-13 13:00:00'),
('form-005', 'StartupXYZ', '{"company_size": "1-5", "industry": "startup", "budget": "very_low"}', 'completed', 'charlie.davis@startupxyz.com', 5, '2024-01-14 14:00:00', '2024-01-14 14:00:00'),
('form-006', 'TechCorp Solutions', '{"company_size": "50-100", "industry": "technology", "budget": "high"}', 'processing', 'diana.garcia@techcorp.com', 1, '2024-01-15 15:00:00', '2024-01-15 15:00:00');
