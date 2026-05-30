// server/routes/diagram.js — Phase 1.3 (Amritansu)
// authenticate wired. Business logic: Task 4.3
import express from 'express';
import { authenticate } from '../middleware/authenticate.js';
import { proxyToAI } from '../middleware/aiProxy.js';
import db from '../db/database.js';

const router = express.Router();

// GET /api/diagram/:sessionId
// Returns all 3 diagrams for a session with approval state
router.get('/:sessionId', authenticate, (req, res) => {
  try {
    const { sessionId } = req.params;

    const session = db.prepare(
      `SELECT id FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    const diagrams = db.prepare(
      `SELECT id, diagram_type, mermaid_src, approved, version, created_at
       FROM diagrams WHERE session_id = ?`
    ).all(sessionId);

    return res.json({ diagrams });
  } catch (err) {
    console.error('diagram/:sessionId GET error:', err.message);
    return res.status(500).json({ error: 'Failed to get diagrams' });
  }
});

// POST /api/diagram/approve/:id
// Sets approved=1 for a specific diagram row
router.post('/approve/:id', authenticate, (req, res) => {
  try {
    const diagram = db.prepare(
      `SELECT d.id, d.session_id FROM diagrams d
       JOIN sessions s ON s.id = d.session_id
       WHERE d.id = ? AND s.user_id = ?`
    ).get(req.params.id, req.user.userId);

    if (!diagram) return res.status(404).json({ error: 'Diagram not found' });

    db.prepare(`UPDATE diagrams SET approved = 1 WHERE id = ?`).run(req.params.id);

    return res.json({ approved: true, id: req.params.id });
  } catch (err) {
    console.error('diagram/approve/:id error:', err.message);
    return res.status(500).json({ error: 'Failed to approve diagram' });
  }
});

// POST /api/diagram/regenerate/:id
// Increments version, resets approved=0, calls Python to regenerate this one diagram type
router.post('/regenerate/:id', authenticate, async (req, res) => {
  try {
    const { sessionId } = req.body;
    if (!sessionId) return res.status(400).json({ error: 'sessionId is required' });

    const diagram = db.prepare(
      `SELECT d.id, d.diagram_type, d.session_id FROM diagrams d
       JOIN sessions s ON s.id = d.session_id
       WHERE d.id = ? AND s.user_id = ? AND d.session_id = ?`
    ).get(req.params.id, req.user.userId, sessionId);

    if (!diagram) return res.status(404).json({ error: 'Diagram not found' });

    const session = db.prepare(`SELECT * FROM sessions WHERE id = ?`).get(sessionId);
    const answers = db.prepare(
      `SELECT question_id, answer_text FROM answers WHERE session_id = ?`
    ).all(sessionId);

    // Re-invoke full diagram generation (Python returns all 3; we only update the one requested)
    const diagramSet = await proxyToAI('/internal/ai/diagrams', {
      session_id: sessionId,
      user_id: req.user.userId,
      overview_json: JSON.parse(session.overview_json || '{}'),
      answers,
    });

    // Map diagram_type → diagramSet key
    const typeKeyMap = {
      usecase:      'use_case_diagram',
      architecture: 'architecture_diagram',
      er:           'er_diagram',
    };
    const newSrc = diagramSet[typeKeyMap[diagram.diagram_type]];

    db.prepare(
      `UPDATE diagrams
       SET mermaid_src = ?, approved = 0, version = version + 1
       WHERE id = ?`
    ).run(newSrc, req.params.id);

    const updated = db.prepare(
      `SELECT id, diagram_type, mermaid_src, approved, version FROM diagrams WHERE id = ?`
    ).get(req.params.id);

    return res.json({ diagram: updated });
  } catch (err) {
    console.error('diagram/regenerate/:id error:', err.message);
    return res.status(502).json({ error: 'Failed to regenerate diagram' });
  }
});

export default router;