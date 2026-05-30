// server/routes/ai.js — Phase 1.3 (Amritansu)
// authenticate wired on all routes. Business logic: Tasks 2.4, 3.2, 4.3, 5.2
import express from 'express';
import { authenticate } from '../middleware/authenticate.js';
import { proxyToAI, proxyStreamToAI } from '../middleware/aiProxy.js';
import db from '../db/database.js';

const router = express.Router();

// ─── Task 2.4 ─────────────────────────────────────────────────────────────────
// POST /api/ai/overview
// Validates idea word count (min 20), proxies to Python, saves to sessions table
router.post('/overview', authenticate, async (req, res) => {
  try {
    const { idea, sessionId } = req.body;

    if (!idea || !sessionId) {
      return res.status(400).json({ error: 'idea and sessionId are required' });
    }

    const session = db.prepare(
      `SELECT * FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    const wordCount = idea.trim().split(/\s+/).filter(Boolean).length;
    if (wordCount < 20) {
      return res.status(400).json({ error: 'Idea must be at least 20 words' });
    }

    const overview = await proxyToAI('/internal/ai/overview', {
      session_id: sessionId,
      user_id: req.user.userId,
      idea_text: idea,
    });

    db.prepare(
      `UPDATE sessions
       SET overview_json = ?, app_name = ?, complexity = ?, status = 'overview', updated_at = CURRENT_TIMESTAMP
       WHERE id = ?`
    ).run(JSON.stringify(overview), overview.app_name, overview.complexity, sessionId);

    return res.json({ overview });
  } catch (err) {
    console.error('ai/overview error:', err.message);
    return res.status(502).json({ error: 'AI service error. Please try again.' });
  }
});

// ─── Task 3.2 ─────────────────────────────────────────────────────────────────
// POST /api/ai/questions
// Loads overview from DB, proxies to Python, bulk-inserts questions
router.post('/questions', authenticate, async (req, res) => {
  try {
    const { sessionId } = req.body;
    if (!sessionId) return res.status(400).json({ error: 'sessionId is required' });

    const session = db.prepare(
      `SELECT * FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });
    if (!session.overview_json) {
      return res.status(400).json({ error: 'Overview not yet generated for this session' });
    }

    const questions = await proxyToAI('/internal/ai/questions', {
      session_id: sessionId,
      user_id: req.user.userId,
      overview_json: JSON.parse(session.overview_json),
      complexity: session.complexity,
    });

    // Bulk insert — idempotent via DELETE first (regenerate scenario)
    db.prepare(`DELETE FROM questions WHERE session_id = ?`).run(sessionId);

    const insertQ = db.prepare(
      `INSERT INTO questions (session_id, question_id, category, question, type, options, display_order)
       VALUES (?, ?, ?, ?, ?, ?, ?)`
    );
    const insertMany = db.transaction((qs) => {
      qs.forEach((q, idx) => {
        insertQ.run(
          sessionId,
          q.question_id,
          q.category,
          q.question,
          q.type,
          q.options ? JSON.stringify(q.options) : null,
          idx
        );
      });
    });
    insertMany(questions);

    db.prepare(
      `UPDATE sessions SET status = 'questions', updated_at = CURRENT_TIMESTAMP WHERE id = ?`
    ).run(sessionId);

    return res.json({ questions });
  } catch (err) {
    console.error('ai/questions error:', err.message);
    return res.status(502).json({ error: 'AI service error. Please try again.' });
  }
});

// ─── Task 4.3 ─────────────────────────────────────────────────────────────────
// POST /api/ai/diagrams
// Loads answers from DB, proxies to Python, upserts all 3 diagrams
router.post('/diagrams', authenticate, async (req, res) => {
  try {
    const { sessionId } = req.body;
    if (!sessionId) return res.status(400).json({ error: 'sessionId is required' });

    const session = db.prepare(
      `SELECT * FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    const answers = db.prepare(
      `SELECT question_id, answer_text FROM answers WHERE session_id = ?`
    ).all(sessionId);

    const diagramSet = await proxyToAI('/internal/ai/diagrams', {
      session_id: sessionId,
      user_id: req.user.userId,
      overview_json: JSON.parse(session.overview_json || '{}'),
      answers,
    });

    // Upsert all 3 diagrams (INSERT OR REPLACE uses unique index on session_id+diagram_type)
    const upsertDiagram = db.prepare(
      `INSERT INTO diagrams (session_id, diagram_type, mermaid_src, approved, version, created_at)
       VALUES (?, ?, ?, 0, 1, CURRENT_TIMESTAMP)
       ON CONFLICT(session_id, diagram_type)
       DO UPDATE SET mermaid_src = excluded.mermaid_src, approved = 0,
                     version = version + 1`
    );
    const upsertAll = db.transaction((ds) => {
      upsertDiagram.run(sessionId, 'usecase',      ds.use_case_diagram);
      upsertDiagram.run(sessionId, 'architecture', ds.architecture_diagram);
      upsertDiagram.run(sessionId, 'er',           ds.er_diagram);
    });
    upsertAll(diagramSet);

    db.prepare(
      `UPDATE sessions SET status = 'diagrams', updated_at = CURRENT_TIMESTAMP WHERE id = ?`
    ).run(sessionId);

    const rows = db.prepare(
      `SELECT id, diagram_type, mermaid_src, approved, version FROM diagrams WHERE session_id = ?`
    ).all(sessionId);

    return res.json({ diagrams: rows });
  } catch (err) {
    console.error('ai/diagrams error:', err.message);
    return res.status(502).json({ error: 'AI service error. Please try again.' });
  }
});

// ─── Task 5.2 — SSE routes (token via query param — EventSource cannot set headers) ────
// POST /api/ai/srs — SSE stream
router.post('/srs', authenticate, async (req, res) => {
  try {
    const { sessionId } = req.body;
    if (!sessionId) return res.status(400).json({ error: 'sessionId is required' });

    const session = db.prepare(
      `SELECT * FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    const sessionContext = _buildSessionContext(session, sessionId);

    await proxyStreamToAI('/internal/docs/stream/srs', { session_context: sessionContext }, res);
  } catch (err) {
    console.error('ai/srs SSE error:', err.message);
    if (!res.headersSent) res.status(502).json({ error: 'AI service error.' });
  }
});

// POST /api/ai/sdd — SSE stream
router.post('/sdd', authenticate, async (req, res) => {
  try {
    const { sessionId } = req.body;
    if (!sessionId) return res.status(400).json({ error: 'sessionId is required' });

    const session = db.prepare(
      `SELECT * FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    const sessionContext = _buildSessionContext(session, sessionId);

    await proxyStreamToAI('/internal/docs/stream/sdd', { session_context: sessionContext }, res);
  } catch (err) {
    console.error('ai/sdd SSE error:', err.message);
    if (!res.headersSent) res.status(502).json({ error: 'AI service error.' });
  }
});

// POST /api/ai/brief — SSE stream
router.post('/brief', authenticate, async (req, res) => {
  try {
    const { sessionId } = req.body;
    if (!sessionId) return res.status(400).json({ error: 'sessionId is required' });

    const session = db.prepare(
      `SELECT * FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    const sessionContext = _buildSessionContext(session, sessionId);

    await proxyStreamToAI('/internal/docs/stream/brief', { session_context: sessionContext }, res);
  } catch (err) {
    console.error('ai/brief SSE error:', err.message);
    if (!res.headersSent) res.status(502).json({ error: 'AI service error.' });
  }
});

// ─── Internal helper ────────────────────────────────────────────────────────
function _buildSessionContext(session, sessionId) {
  const questions = db.prepare(
    `SELECT question_id, category, question, type, options, display_order
     FROM questions WHERE session_id = ? ORDER BY display_order ASC`
  ).all(sessionId);

  const answers = db.prepare(
    `SELECT question_id, answer_text FROM answers WHERE session_id = ?`
  ).all(sessionId);

  const diagrams = db.prepare(
    `SELECT diagram_type, mermaid_src FROM diagrams WHERE session_id = ?`
  ).all(sessionId);

  return {
    session_id: sessionId,
    app_name: session.app_name,
    idea_text: session.idea_text,
    overview_json: session.overview_json ? JSON.parse(session.overview_json) : null,
    complexity: session.complexity,
    questions,
    answers,
    diagrams,
  };
}

export default router;