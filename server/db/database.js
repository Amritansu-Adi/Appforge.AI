import Database from "better-sqlite3";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const DB_PATH = process.env.DB_PATH || path.join(__dirname, "../../data/appforge.db");

// Ensure the data directory exists
const dataDir = path.dirname(DB_PATH);
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

// Singleton — one connection shared across the entire server process
const db = new Database(DB_PATH);

// Performance pragmas for SQLite
db.pragma("journal_mode = WAL");   // Write-Ahead Logging — faster concurrent reads
db.pragma("foreign_keys = ON");    // Enforce FK constraints
db.pragma("synchronous = NORMAL"); // Good balance of safety and speed

export default db;