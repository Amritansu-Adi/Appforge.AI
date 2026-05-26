/**
 * server/middleware/aiProxy.js
 * Owner: Amritansu
 *
 * Thin proxy utilities for forwarding requests from Node.js to the
 * Python AI service (FastAPI :8000). Auth is verified by Node.js BEFORE
 * calling these helpers — the Python service only checks X-Internal-Secret.
 *
 * Usage (non-streaming):
 *   const data = await proxyToAI("/internal/ai/overview", { session_id, idea_text });
 *
 * Usage (SSE streaming):
 *   await proxyStreamToAI("/internal/codegen/start", body, res);
 */

import fetch from "node-fetch";

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || "http://localhost:8000";
const AI_SERVICE_SECRET = process.env.AI_SERVICE_SECRET;

if (!AI_SERVICE_SECRET) {
  console.warn("⚠️  AI_SERVICE_SECRET not set. Python AI service calls will be rejected.");
}

/**
 * Standard JSON request/response proxy.
 * @param {string} path  - Internal Python endpoint path e.g. "/internal/ai/overview"
 * @param {object} body  - JSON payload to forward
 * @returns {Promise<object>} Parsed JSON response from Python service
 */
export async function proxyToAI(path, body) {
  const response = await fetch(`${AI_SERVICE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Internal-Secret": AI_SERVICE_SECRET,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    let err;
    try { err = await response.json(); } catch { err = { detail: "AI service error" }; }
    const error = new Error(err.detail || "AI service returned an error");
    error.status = response.status;
    throw error;
  }

  return response.json();
}

/**
 * SSE streaming proxy — pipes Python's text/event-stream directly to the
 * Express response so the browser receives token-by-token updates.
 *
 * @param {string} path          - Internal Python SSE endpoint
 * @param {object} body          - JSON payload
 * @param {import("express").Response} expressRes  - Express response object
 */
export async function proxyStreamToAI(path, body, expressRes) {
  const response = await fetch(`${AI_SERVICE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Internal-Secret": AI_SERVICE_SECRET,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    let err;
    try { err = await response.json(); } catch { err = { detail: "AI service error" }; }
    expressRes.status(response.status).json({ error: err.detail || "AI service error" });
    return;
  }

  expressRes.setHeader("Content-Type", "text/event-stream");
  expressRes.setHeader("Cache-Control", "no-cache");
  expressRes.setHeader("Connection", "keep-alive");
  expressRes.setHeader("X-Accel-Buffering", "no"); // Disable nginx buffering if behind proxy
  response.body.pipe(expressRes);
}
