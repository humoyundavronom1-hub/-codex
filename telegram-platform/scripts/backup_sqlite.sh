#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB_FILE="${ROOT_DIR}/db/app.db"
BACKUP_DIR="${SQLITE_BACKUP_DIR:-${ROOT_DIR}/db/backups}"
mkdir -p "$BACKUP_DIR"

TS="$(date +%Y%m%d-%H%M%S)"
cp "$DB_FILE" "${BACKUP_DIR}/app-${TS}.db"
find "$BACKUP_DIR" -type f -name 'app-*.db' -mtime +14 -delete
