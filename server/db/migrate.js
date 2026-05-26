import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import db from "./database.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SCHEMA_PATH = path.join(__dirname, "schema.sql");

export async function runMigrations() {
  console.log("🗃️  Running database migrations...");

  const sql = fs.readFileSync(SCHEMA_PATH, "utf8");

  // Split on semicolons, filter empty statements, execute each
  const statements = sql
    .split(";")
    .map((s) => s.trim())
    .filter((s) => s.length > 0 && !s.startsWith("--"));

  const migrate = db.transaction(() => {
    for (const stmt of statements) {
      db.prepare(stmt).run();
    }
  });

  try {
    migrate();
    console.log("✅ Migrations complete.");
  } catch (err) {
    console.error("❌ Migration failed:", err.message);
    throw err;
  }
}

// Allow direct execution: node db/migrate.js
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  runMigrations()
    .then(() => process.exit(0))
    .catch(() => process.exit(1));
}