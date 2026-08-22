-- Add password reset columns to users table
ALTER TABLE users ADD COLUMN password_reset_token TEXT;
ALTER TABLE users ADD COLUMN password_reset_expires_at TIMESTAMP WITH TIME ZONE;

-- Create index for faster token lookups
CREATE INDEX CONCURRENTLY idx_users_password_reset_token ON users(password_reset_token) WHERE password_reset_token IS NOT NULL;

-- Add check constraint to prevent resetting active passwords without token
ALTER TABLE users ADD CONSTRAINT chk_reset_token_validity 
  CHECK ((password_reset_token IS NULL AND password_reset_expires_at IS NULL) OR (password_reset_token IS NOT NULL AND password_reset_expires_at IS NOT NULL));
