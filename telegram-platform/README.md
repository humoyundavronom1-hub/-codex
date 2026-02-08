# Telegram Moderation + Analytics Platform (NO DOCKER)

Ushbu loyiha lokal server yoki VPS uchun production-ready multi-service stack:
- **Telegram Bot**: Python 3.11 + pyTelegramBotAPI
- **Backend API**: FastAPI + SQLAlchemy + Alembic + JWT
- **Web Admin Panel**: Node.js 20 + Express + EJS + Tailwind + Chart.js
- **Database**: SQLite (`db/app.db`)

## Arxitektura

### Bot xizmati
- `new_chat_members` eventida yangi foydalanuvchini avtomatik mute qiladi.
- Taklif progressi xabarlari yuboradi:
  - `Welcome 👋 To chat you must invite N users. Progress: 0 / N`
  - `✅ One user added / Remaining: X`
  - `🎉 You can now chat freely!`
- Buyruqlar: `/my_status`, `/my_invites`, `/rules`, `/my_stats`.

### Backend API
- JWT asosida admin-only autentifikatsiya.
- Group rules boshqaruvi (`invite_required`, `reset_on_leave`, `ignore_bots`, `admins_bypass`, `auto_kick_timeout`, `risk_threshold`).
- User progress, manual unlock/reset.
- Analytics + leaderboard endpointlar.
- Audit log yozuvlari.

### Web Admin
- Blue/white gov style, fixed left sidebar, top header.
- KPI cards, chartlar, groups/users/analytics ko‘rinishlari.
- Rate limiting va cookie orqali session token.

## Loyiha strukturasi

```text
telegram-platform/
├── bot/
├── backend/
├── web/
├── db/
│   └── backups/
├── deploy/
│   ├── systemd/
│   ├── pm2/
│   ├── nginx/
│   └── cron.example
├── scripts/
│   └── backup_sqlite.sh
├── .env.example
└── README.md
```

## DB jadvallar
- admins
- groups
- users
- user_progress
- invite_logs
- messages_log
- user_daily_stats
- group_daily_stats
- risk_scores
- audit_logs

SQL schema: `backend/db/schema.sql`  
Alembic migration: `backend/alembic/versions/0001_initial.py`

## REST endpointlar
- `POST /api/auth/login`
- `GET /api/dashboard/kpi`
- `GET /api/groups`
- `PUT /api/groups/{group_id}/rules`
- `GET /api/users`
- `POST /api/users/manual-unlock`
- `POST /api/users/reset`
- `GET /api/leaderboards`
- `GET /api/analytics/unlock-funnel`
- `GET /api/logs`
- `GET /api/settings`

## Local ishga tushirish

### 1) Konfiguratsiya
```bash
cp .env.example .env
mkdir -p db/backups
```

### 2) Python virtualenv
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
pip install -r bot/requirements.txt
```

### 3) Backend
```bash
source .venv/bin/activate
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 4) Bot
```bash
source .venv/bin/activate
python bot/main.py
```

### 5) Web
```bash
cd web
npm install
npm start
```

## VPS deploy (NO DOCKER)

### systemd xizmatlari
`deploy/systemd/telegram-backend.service` va `deploy/systemd/telegram-bot.service` ni `/etc/systemd/system/` ga ko‘chiring:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now telegram-backend
sudo systemctl enable --now telegram-bot
```

### PM2 bilan web app
```bash
cd /opt/telegram-platform/web
npm install --omit=dev
pm2 start ../deploy/pm2/ecosystem.config.cjs
pm2 save
pm2 startup
```

### Nginx reverse proxy
`deploy/nginx/telegram-platform.conf` ni `/etc/nginx/sites-available/` ga joylang:
```bash
sudo ln -s /etc/nginx/sites-available/telegram-platform.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### SQLite backup (cron)
`deploy/cron.example` dagi qatorni `crontab -e` ga qo‘shing.

## Security
- Admin-only web access
- JWT tokenlar
- Rate limiting
- Flood/abuse monitoring
- Audit logging
- Pydantic input validation

