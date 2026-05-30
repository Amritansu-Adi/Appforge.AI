// server/routes/answers.js — Phase 1.3 (Amritansu)
// authenticate wired. Business logic: Task 3.2
import express from 'express';
import { authenticate } from '../middleware/authenticate.js';
import db from '../db/database.js';

// const router = express.Router();

// POST /api/answers/save
// Upsert answer — INSERT OR REPLACE on UNIQUE(session_id, question_id)
// Allows user to go back and revise answers.
router.post('/save', authenticate, async (req, res) => {
  try {
    const { sessionId, questionId, answerText } = req.body;

    if (!sessionId || !questionId || !answerText) {
      return res.status(400).json({ error: 'sessionId, questionId, and answerText are required' });
    }

    if (answerText.trim().length < 1) {
      return res.status(400).json({ error: 'Answer cannot be empty' });
    }

    // Verify session ownership before writing answer
    const session = db.prepare(
      `SELECT id FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    // UNIQUE INDEX on (session_id, question_id) — ON CONFLICT REPLACE upserts cleanly
    db.prepare(
      `INSERT INTO answers (session_id, question_id, answer_text, answered_at)
       VALUES (?, ?, ?, CURRENT_TIMESTAMP)
       ON CONFLICT(session_id, question_id)
       DO UPDATE SET answer_text = excluded.answer_text, answered_at = CURRENT_TIMESTAMP`
    ).run(sessionId, questionId, answerText.trim());

    return res.json({ saved: true, questionId });
  } catch (err) {
    console.error('answers/save error:', err.message);
    return res.status(500).json({ error: 'Failed to save answer' });
  }
});

// GET /api/answers/:sessionId
// Returns all answers for a session — used for session restore on refresh
router.get('/:sessionId', authenticate, (req, res) => {
  try {
    const { sessionId } = req.params;

    // Ownership check
    const session = db.prepare(
      `SELECT id FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    const answers = db.prepare(
      `SELECT question_id, answer_text, answered_at FROM answers WHERE session_id = ?`
    ).all(sessionId);

    return res.json({ answers });
  } catch (err) {
    console.error('answers/:sessionId GET error:', err.message);
    return res.status(500).json({ error: 'Failed to get answers' });
  }
});

export default router;