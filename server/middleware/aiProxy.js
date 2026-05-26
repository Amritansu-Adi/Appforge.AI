/**
 * server/middleware/aiProxy.js
 * Owner: Amritansu
 *
 * Thin proxy utilities for forwarding requests from Node.js to the
 * Python AI service (FastAPI :8000). Auth is verified by Node.js BEFORE
 * calling these helpers — the Python service only checks X-Internal-Secret.
 *
 * v4.0 FIX: Replaced node-fetch with axios.
 *   - node-fetch v3 returns a Web Streams ReadableStream which lacks .pipe().
 *   - axios with responseType:'stream' returns a Node.js IncomingMessage
 *     which has .pipe() and works correctly with Express response.
 *   - This fixes revision log issue #5: "node-fetch .pipe() bug fixed".
 *
 * Usage (non-streaming):
 *   const data = await proxyToAI("/internal/ai/overview", { session_id, idea_text });
 *
 * Usage (SSE streaming):
 *   await proxyStreamToAI("/internal/codegen/start", body, res);
 */

import axios from "axios";

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || "http://localhost:8000";
const AI_SERVICE_SECRET = process.env.AI_SERVICE_SECRET;

if (!AI_SERVICE_SECRET) {
  console.warn("⚠️  AI_SERVICE_SECRET not set. Python AI service calls will be rejected.");
}

const _headers = () => ({
  "Content-Type": "application/json",
  "X-Internal-Secret": AI_SERVICE_SECRET,
});

/**
 * Standard JSON request/response proxy.
 * @param {string} path  - Internal Python endpoint path e.g. "/internal/ai/overview"
 * @param {object} body  - JSON payload to forward
 * @returns {Promise<object>} Parsed JSON response from Python service
 */
export async function proxyToAI(path, body) {
  try {
    const response = await axios.post(`${AI_SERVICE_URL}${path}`, body, {
      headers: _headers(),
    });
    return response.data;
  } catch (err) {
    const status = err.response?.status || 502;
    const detail = err.response?.data?.detail || "AI service returned an error";
    const error = new Error(detail);
    error.status = status;
    throw error;
  }
}

/**
 * SSE streaming proxy — pipes Python's text/event-stream directly to the
 * Express response so the browser receives token-by-token updates.
 *
 * v4.0: Uses axios { responseType: 'stream' } which returns a Node.js
 * IncomingMessage — .pipe() works correctly with Express res.
 *
 * @param {string} path          - Internal Python SSE endpoint
 * @param {object} body          - JSON payload
 * @param {import("express").Response} expressRes  - Express response object
 */
export async function proxyStreamToAI(path, body, expressRes) {
  try {
    const response = await axios.post(`${AI_SERVICE_URL}${path}`, body, {
      headers: _headers(),
      responseType: "stream",
    });

    expressRes.setHeader("Content-Type", "text/event-stream");
    expressRes.setHeader("Cache-Control", "no-cache");
    expressRes.setHeader("Connection", "keep-alive");
    expressRes.setHeader("X-Accel-Buffering", "no"); // Disable nginx buffering if behind proxy

    response.data.pipe(expressRes);

    response.data.on("error", (err) => {
      console.error("AI stream error:", err.message);
      if (!expressRes.headersSent) {
        expressRes.status(502).json({ error: "AI stream error" });
      }
    });
  } catch (err) {
    const status = err.response?.status || 502;
    const detail = err.response?.data?.detail || "AI service error";
    if (!expressRes.headersSent) {
      expressRes.status(status).json({ error: detail });
    }
  }
}
