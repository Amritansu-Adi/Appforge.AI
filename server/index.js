// server/index.js — v4.0.0 (Amritansu)
// Phase 1.3: All 6 route stubs now active — authenticate wired inside each route file.
import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import rateLimit from 'express-rate-limit';

// Route imports
import authRouter    from './routes/auth.js';
import sessionRouter from './routes/session.js';
import aiRouter      from './routes/ai.js';
import answersRouter from './routes/answers.js';
import diagramRouter from './routes/diagram.js';
import docsRouter    from './routes/docs.js';
import codegenRouter from './routes/codegen.js';

// DB migration — runs idempotently on every startup
import './db/migrate.js';

const app = express();
const PORT = process.env.PORT || 3001;

// ─── Global Middleware ────────────────────────────────────────────────────────
app.use(cors({
  origin: process.env.NODE_ENV === 'production'
    ? process.env.CLIENT_ORIGIN
    : 'http://localhost:5173',
  credentials: true,
}));
app.use(express.json());

// ─── Rate Limiters ───────────────────────────────────────────────────────────
// Session creation: 10 per minute per user (Phase 7.2 test: 11th → 429)
const sessionCreateLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 10,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many sessions created. Please wait a minute.' },
});

// General API limiter: 200 requests/15min per IP
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 200,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests. Please slow down.' },
});

app.use('/api/', apiLimiter);

// Apply session-create specific limiter
app.use('/api/session/create', sessionCreateLimiter);

// ─── Routes ──────────────────────────────────────────────────────────────────
app.use('/api/auth',    authRouter);
app.use('/api/session', sessionRouter);
app.use('/api/ai',      aiRouter);
app.use('/api/answers', answersRouter);
app.use('/api/diagram', diagramRouter);
app.use('/api/docs',    docsRouter);
app.use('/api/codegen', codegenRouter);

// ─── Health ───────────────────────────────────────────────────────────────────
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', service: 'appforge-server', version: '4.0.0' });
});

// ─── Global Error Handler ────────────────────────────────────────────────────
app.use((err, req, res, _next) => {
  console.error('Unhandled error:', err.message);
  res.status(500).json({ error: 'Internal server error' });
});

// ─── Start ───────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`AppForge server v4.0.0 running on port ${PORT}`);
});

export default app;