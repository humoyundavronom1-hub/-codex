CREATE TABLE IF NOT EXISTS admins (
  id INTEGER PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  full_name TEXT NOT NULL,
  is_active BOOLEAN DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS groups (
  id INTEGER PRIMARY KEY,
  telegram_group_id TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  is_enabled BOOLEAN DEFAULT 1,
  invite_required INTEGER DEFAULT 3,
  reset_on_leave BOOLEAN DEFAULT 0,
  ignore_bots BOOLEAN DEFAULT 1,
  admins_bypass BOOLEAN DEFAULT 1,
  auto_kick_timeout INTEGER DEFAULT 3600,
  risk_threshold REAL DEFAULT 0.65,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  telegram_user_id TEXT UNIQUE NOT NULL,
  username TEXT,
  full_name TEXT NOT NULL,
  is_bot BOOLEAN DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS user_progress (
  id INTEGER PRIMARY KEY,
  group_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  invites_count INTEGER DEFAULT 0,
  required_invites INTEGER DEFAULT 3,
  unlocked BOOLEAN DEFAULT 0,
  muted BOOLEAN DEFAULT 1,
  UNIQUE(group_id, user_id)
);
CREATE TABLE IF NOT EXISTS invite_logs (
  id INTEGER PRIMARY KEY,
  group_id INTEGER NOT NULL,
  inviter_user_id INTEGER NOT NULL,
  invited_user_id INTEGER NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS messages_log (
  id INTEGER PRIMARY KEY,
  group_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  message_type TEXT DEFAULT 'text',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS user_daily_stats (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  group_id INTEGER NOT NULL,
  day TEXT NOT NULL,
  invites INTEGER DEFAULT 0,
  messages INTEGER DEFAULT 0,
  UNIQUE(user_id, group_id, day)
);
CREATE TABLE IF NOT EXISTS group_daily_stats (
  id INTEGER PRIMARY KEY,
  group_id INTEGER NOT NULL,
  day TEXT NOT NULL,
  joins INTEGER DEFAULT 0,
  leaves INTEGER DEFAULT 0,
  unlocks INTEGER DEFAULT 0,
  messages INTEGER DEFAULT 0,
  UNIQUE(group_id, day)
);
CREATE TABLE IF NOT EXISTS risk_scores (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  group_id INTEGER NOT NULL,
  score REAL DEFAULT 0,
  reasons TEXT DEFAULT '',
  UNIQUE(user_id, group_id)
);
CREATE TABLE IF NOT EXISTS audit_logs (
  id INTEGER PRIMARY KEY,
  actor_admin_id INTEGER,
  action TEXT NOT NULL,
  details TEXT DEFAULT '',
  severity TEXT DEFAULT 'info',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_invite_logs_group_inviter ON invite_logs(group_id, inviter_user_id);
CREATE INDEX IF NOT EXISTS idx_messages_log_group_user ON messages_log(group_id, user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_group_unlocked ON user_progress(group_id, unlocked);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created ON audit_logs(created_at);
