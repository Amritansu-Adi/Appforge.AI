-- ============================================================
-- AppForge AI — Full Database Schema
-- All CREATE TABLE statements are idempotent (IF NOT EXISTS)
-- Managed by: server/db/migrate.js
-- ============================================================

-- Table 1: users
CREATE TABLE IF NOT EXISTS users (
  id           TEXT     PRIMARY KEY,
  email        TEXT     NOT NULL UNIQUE,
  password_hash TEXT    NOT NULL,
  created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_login   DATETIME
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Table 2: sessions
CREATE TABLE IF NOT EXISTS sessions (
  id           TEXT     PRIMARY KEY,
  user_id      TEXT     NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
  status       TEXT     NOT NULL DEFAULT 'idea'
                        CHECK(status IN ('idea','overview','questions','diagrams','docs','codegen','complete')),
  idea_text    TEXT,
  overview_json TEXT,
  complexity   TEXT     CHECK(complexity IN ('simple','standard','complex')),
  app_name     TEXT
);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);

-- Table 3: questions
CREATE TABLE IF NOT EXISTS questions (
  id          INTEGER  PRIMARY KEY AUTOINCREMENT,
  session_id  TEXT     NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  question_id TEXT     NOT NULL,
  category    TEXT,
  question    TEXT     NOT NULL,
  type        TEXT     NOT NULL CHECK(type IN ('text','choice')),
  options_json TEXT
);

-- Table 4: answers
CREATE TABLE IF NOT EXISTS answers (
  id           INTEGER  PRIMARY KEY AUTOINCREMENT,
  session_id   TEXT     NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  question_id  TEXT     NOT NULL,
  answer_text  TEXT     NOT NULL,
  answered_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_answers_session_q ON answers(session_id, question_id);

-- Table 5: diagrams
CREATE TABLE IF NOT EXISTS diagrams (
  id           INTEGER  PRIMARY KEY AUTOINCREMENT,
  session_id   TEXT     NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  diagram_type TEXT     NOT NULL CHECK(diagram_type IN ('usecase','architecture','er')),
  mermaid_src  TEXT     NOT NULL,
  approved     INTEGER  NOT NULL DEFAULT 0,
  version      INTEGER  NOT NULL DEFAULT 1,
  created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_diagrams_session_type ON diagrams(session_id, diagram_type);

-- Table 6: documents
CREATE TABLE IF NOT EXISTS documents (
  id           INTEGER  PRIMARY KEY AUTOINCREMENT,
  session_id   TEXT     NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  doc_type     TEXT     NOT NULL CHECK(doc_type IN ('srs','sdd','brief')),
  file_path    TEXT,
  markdown_text TEXT,
  created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table 7: generated_files
CREATE TABLE IF NOT EXISTS generated_files (
  id           INTEGER  PRIMARY KEY AUTOINCREMENT,
  session_id   TEXT     NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  file_path    TEXT     NOT NULL,
  content      TEXT     NOT NULL,
  status       TEXT     NOT NULL DEFAULT 'pending'
                        CHECK(status IN ('pending','generating','validated','packaged','failed')),
  source       TEXT     NOT NULL CHECK(source IN ('ai','template')),
  created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table 8: langgraph_checkpoints (managed by SqliteSaver — DO NOT write manually)
CREATE TABLE IF NOT EXISTS langgraph_checkpoints (
  thread_id             TEXT NOT NULL,
  checkpoint_id         TEXT NOT NULL,
  parent_checkpoint_id  TEXT,
  type                  TEXT NOT NULL,
  checkpoint            TEXT NOT NULL,
  metadata              TEXT NOT NULL,
  PRIMARY KEY (thread_id, checkpoint_id)
);

-- Table 9: langgraph_writes (required by SqliteSaver alongside checkpoints)
CREATE TABLE IF NOT EXISTS langgraph_writes (
  thread_id      TEXT NOT NULL,
  checkpoint_id  TEXT NOT NULL,
  task_id        TEXT NOT NULL,
  idx            INTEGER NOT NULL,
  channel        TEXT NOT NULL,
  type           TEXT,
  value          TEXT,
  PRIMARY KEY (thread_id, checkpoint_id, task_id, idx)
);