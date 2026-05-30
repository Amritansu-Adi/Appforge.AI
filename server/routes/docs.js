// server/routes/docs.js — Phase 1.3 (Amritansu)
// authenticate wired on ALL routes (Bearer header for POST, query.token for GET downloads)
// GET download routes: EventSource/window.open cannot set headers → token in query param
// Business logic: Task 5.2
import express from 'express';
import { authenticate } from '../middleware/authenticate.js';
import db from '../db/database.js';

const router = express.Router();

// GET /api/docs/:sessionId/srs
// Decodes docx_base64 from DB → binary .docx file download
// Auth: query.token (window.open in browser cannot set Authorization header)
router.get('/:sessionId/srs', authenticate, (req, res) => {
  try {
    const { sessionId } = req.params;

    const session = db.prepare(
      `SELECT id FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    const doc = db.prepare(
      `SELECT docx_base64 FROM documents WHERE session_id = ? AND doc_type = 'srs'`
    ).get(sessionId);

    if (!doc || !doc.docx_base64) {
      return res.status(404).json({ error: 'SRS document not yet generated' });
    }

    const buffer = Buffer.from(doc.docx_base64, 'base64');
    res.setHeader(
      'Content-Type',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    );
    res.setHeader(
      'Content-Disposition',
      `attachment; filename="SRS-${sessionId.slice(0, 8)}.docx"`
    );
    return res.send(buffer);
  } catch (err) {
    console.error('docs/:sessionId/srs error:', err.message);
    return res.status(500).json({ error: 'Failed to serve SRS document' });
  }
});

// GET /api/docs/:sessionId/sdd
router.get('/:sessionId/sdd', authenticate, (req, res) => {
  try {
    const { sessionId } = req.params;

    const session = db.prepare(
      `SELECT id FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    const doc = db.prepare(
      `SELECT docx_base64 FROM documents WHERE session_id = ? AND doc_type = 'sdd'`
    ).get(sessionId);

    if (!doc || !doc.docx_base64) {
      return res.status(404).json({ error: 'SDD document not yet generated' });
    }

    const buffer = Buffer.from(doc.docx_base64, 'base64');
    res.setHeader(
      'Content-Type',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    );
    res.setHeader(
      'Content-Disposition',
      `attachment; filename="SDD-${sessionId.slice(0, 8)}.docx"`
    );
    return res.send(buffer);
  } catch (err) {
    console.error('docs/:sessionId/sdd error:', err.message);
    return res.status(500).json({ error: 'Failed to serve SDD document' });
  }
});

// GET /api/docs/:sessionId/brief
// brief doc: markdown_text only — no .docx (docx_base64 is NULL for brief type per schema)
router.get('/:sessionId/brief', authenticate, (req, res) => {
  try {
    const { sessionId } = req.params;

    const session = db.prepare(
      `SELECT id FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    const doc = db.prepare(
      `SELECT markdown_text FROM documents WHERE session_id = ? AND doc_type = 'brief'`
    ).get(sessionId);

    if (!doc || !doc.markdown_text) {
      return res.status(404).json({ error: 'Brief not yet generated' });
    }

    return res.json({ markdown: doc.markdown_text });
  } catch (err) {
    console.error('docs/:sessionId/brief error:', err.message);
    return res.status(500).json({ error: 'Failed to get brief' });
  }
});

export default router;