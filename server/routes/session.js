// server/routes/session.js — Phase 1.3 (Amritansu)
// authenticate wired. Business logic implemented in Task 2.1.
import express from 'express';
import { v4 as uuidv4 } from 'uuid';
import { authenticate } from '../middleware/authenticate.js';
import db from '../db/database.js';

const router = express.Router();

// POST /api/session/create
// Task 2.1: INSERT session row — status='idea', user_id=req.user.userId
router.post('/create', authenticate, async (req, res) => {
  try {
    const { idea_text = '', app_name = null } = req.body;
    const id = uuidv4();
    const now = new Date().toISOString();

    db.prepare(
      `INSERT INTO sessions (id, user_id, app_name, idea_text, status, created_at, updated_at)
       VALUES (?, ?, ?, ?, 'idea', ?, ?)`
    ).run(id, req.user.userId, app_name, idea_text, now, now);

    return res.status(201).json({ sessionId: id });
  } catch (err) {
    console.error('session/create error:', err.message);
    return res.status(500).json({ error: 'Failed to create session' });
  }
});

// GET /api/session/list
// Returns [{id, app_name, status, created_at}] for current user, newest first
router.get('/list', authenticate, (req, res) => {
  try {
    const rows = db.prepare(
      `SELECT id, app_name, status, created_at
       FROM sessions
       WHERE user_id = ?
       ORDER BY created_at DESC`
    ).all(req.user.userId);

    return res.json(rows);
  } catch (err) {
    console.error('session/list error:', err.message);
    return res.status(500).json({ error: 'Failed to list sessions' });
  }
});

// GET /api/session/:id
// Returns full session row — 404 if session.user_id ≠ req.user.userId
router.get('/:id', authenticate, (req, res) => {
  try {
    const session = db.prepare(
      `SELECT * FROM sessions WHERE id = ? AND user_id = ?`
    ).get(req.params.id, req.user.userId);

    if (!session) return res.status(404).json({ error: 'Session not found' });
    return res.json(session);
  } catch (err) {
    console.error('session/:id GET error:', err.message);
    return res.status(500).json({ error: 'Failed to get session' });
  }
});

// PATCH /api/session/:id/status
// body: { status: string } — validated against 8-value enum
const VALID_STATUSES = ['idea', 'overview', 'questions', 'answers', 'diagrams', 'docs', 'codegen', 'complete'];

router.patch('/:id/status', authenticate, (req, res) => {
  try {
    const { status } = req.body;

    if (!status || !VALID_STATUSES.includes(status)) {
      return res.status(400).json({
        error: `Invalid status. Must be one of: ${VALID_STATUSES.join(', ')}`,
      });
    }

    const session = db.prepare(
      `SELECT id FROM sessions WHERE id = ? AND user_id = ?`
    ).get(req.params.id, req.user.userId);

    if (!session) return res.status(404).json({ error: 'Session not found' });

    db.prepare(
      `UPDATE sessions SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?`
    ).run(status, req.params.id);

    return res.json({ updated: true, status });
  } catch (err) {
    console.error('session/:id/status PATCH error:', err.message);
    return res.status(500).json({ error: 'Failed to update status' });
  }
});

// DELETE /api/session/:id
// CASCADE via FK handles child table cleanup (questions, answers, diagrams, documents, generated_files)
router.delete('/:id', authenticate, (req, res) => {
  try {
    const session = db.prepare(
      `SELECT id FROM sessions WHERE id = ? AND user_id = ?`
    ).get(req.params.id, req.user.userId);

    if (!session) return res.status(404).json({ error: 'Session not found' });

    db.prepare(`DELETE FROM sessions WHERE id = ?`).run(req.params.id);

    return res.json({ deleted: true });
  } catch (err) {
    console.error('session/:id DELETE error:', err.message);
    return res.status(500).json({ error: 'Failed to delete session' });
  }
});

export default router;