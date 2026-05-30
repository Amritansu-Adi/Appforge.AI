// server/routes/codegen.js — Phase 1.3 (Amritansu)
// authenticate wired. SSE start endpoint uses query.token (EventSource cannot set headers).
// Business logic: Task 6.3
import express from 'express';
import path from 'path';
import fs from 'fs';
import { authenticate } from '../middleware/authenticate.js';
import { proxyStreamToAI } from '../middleware/aiProxy.js';
import db from '../db/database.js';

const router = express.Router();

// POST /api/codegen/start  (or GET with ?sessionId=&token= for EventSource)
// SSE endpoint — proxies Python codegen stream to browser.
// Client connects via EventSource: codegenStreamUrl uses query.token
router.get('/start', authenticate, async (req, res) => {
  try {
    const sessionId = req.query.sessionId;
    if (!sessionId) return res.status(400).json({ error: 'sessionId query param required' });

    const session = db.prepare(
      `SELECT * FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    // Load full context for codegen
    const questions = db.prepare(
      `SELECT question_id, category, question, type, options FROM questions WHERE session_id = ? ORDER BY display_order ASC`
    ).all(sessionId);
    const answers = db.prepare(
      `SELECT question_id, answer_text FROM answers WHERE session_id = ?`
    ).all(sessionId);
    const diagrams = db.prepare(
      `SELECT diagram_type, mermaid_src FROM diagrams WHERE session_id = ?`
    ).all(sessionId);
    const docs = db.prepare(
      `SELECT doc_type, markdown_text FROM documents WHERE session_id = ?`
    ).all(sessionId);

    const sessionContext = {
      session_id: sessionId,
      user_id: req.user.userId,
      app_name: session.app_name,
      idea_text: session.idea_text,
      overview_json: session.overview_json ? JSON.parse(session.overview_json) : null,
      complexity: session.complexity,
      questions,
      answers,
      diagrams,
      docs,
    };

    await proxyStreamToAI('/internal/codegen/start', { session_context: sessionContext }, res);
  } catch (err) {
    console.error('codegen/start SSE error:', err.message);
    if (!res.headersSent) res.status(502).json({ error: 'Codegen service error.' });
  }
});

// GET /api/codegen/download/:sessionId
// Serves pre-built zip from disk cache — auth via query.token
router.get('/download/:sessionId', authenticate, (req, res) => {
  try {
    const { sessionId } = req.params;

    const session = db.prepare(
      `SELECT id FROM sessions WHERE id = ? AND user_id = ?`
    ).get(sessionId, req.user.userId);
    if (!session) return res.status(404).json({ error: 'Session not found' });

    // Zip files are cached at server/generated_zips/{sessionId}.zip
    // Path resolution: __dirname is not available in ESM — use process.cwd()
    const zipDir = path.join(process.cwd(), 'generated_zips');
    const zipPath = path.join(zipDir, `${sessionId}.zip`);

    if (!fs.existsSync(zipPath)) {
      return res.status(404).json({ error: 'Zip not ready. Run codegen first.' });
    }

    res.setHeader('Content-Type', 'application/zip');
    res.setHeader(
      'Content-Disposition',
      `attachment; filename="${session.app_name || 'app'}-${sessionId.slice(0, 8)}.zip"`
    );
    fs.createReadStream(zipPath).pipe(res);
  } catch (err) {
    console.error('codegen/download error:', err.message);
    return res.status(500).json({ error: 'Failed to serve zip file' });
  }
});

export default router;