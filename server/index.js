import "dotenv/config";
import express from "express";
import cors from "cors";
import { rateLimit } from "express-rate-limit";
import { runMigrations } from "./db/migrate.js";

// ─── Bootstrap DB ────────────────────────────────────────────
await runMigrations();

const app = express();
const PORT = process.env.PORT || 3001;

// ─── Global Middleware ────────────────────────────────────────
app.use(
  cors({
    origin: process.env.NODE_ENV === "production"
      ? "https://your-render-url.onrender.com"
      : "http://localhost:5173",
    credentials: true,
  })
);
app.use(express.json({ limit: "2mb" }));

// Global rate limit — 200 req / 15 min per IP
app.use(
  rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 200,
    standardHeaders: true,
    legacyHeaders: false,
    message: { error: "Too many requests, please slow down." },
  })
);

// ─── Routes (stubs — filled per phase) ────────────────────────
// Phase 1: Auth
// import authRoutes from "./routes/auth.js";
// app.use("/api/auth", authRoutes);

// Phase 2+: Protected routes
// import { authenticate } from "./middleware/authenticate.js";
// app.use("/api/session", authenticate, sessionRoutes);
// app.use("/api/ai",      authenticate, aiRoutes);       // aiRoutes → proxyToAI()
// app.use("/api/answers", authenticate, answersRoutes);
// app.use("/api/diagram", authenticate, diagramRoutes);
// app.use("/api/docs",    authenticate, docsRoutes);
// app.use("/api/codegen", authenticate, codegenRoutes);

// ─── Health check ─────────────────────────────────────────────
app.get("/api/health", (_req, res) => {
  res.json({
    status: "ok",
    version: "3.0.0",
    env: process.env.NODE_ENV,
    ai_service: process.env.AI_SERVICE_URL || "http://localhost:8000",
  });
});

// ─── 404 handler ─────────────────────────────────────────────
app.use((_req, res) => {
  res.status(404).json({ error: "Route not found" });
});

// ─── Global error handler ─────────────────────────────────────
app.use((err, _req, res, _next) => {
  console.error("[ERROR]", err.message, err.stack);
  res.status(err.status || 500).json({
    error: process.env.NODE_ENV === "production"
      ? "Internal server error"
      : err.message,
  });
});

app.listen(PORT, () => {
  console.log(`✅ AppForge Node.js server running on http://localhost:${PORT}`);
  console.log(`   Environment : ${process.env.NODE_ENV || "development"}`);
  console.log(`   DB Path     : ${process.env.DB_PATH || "./data/appforge.db"}`);
  console.log(`   AI Service  : ${process.env.AI_SERVICE_URL || "http://localhost:8000"}`);
});
