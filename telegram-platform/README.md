# Telegram Moderation + Analytics Platform (React + Shared DB)

Ushbu loyiha endi **React frontend + web/backend backend** arxitekturasida ishlaydi.
Asosiy g‘oya:
- Frontend va backend **alohida ishga tushadi**.
- Ikkalasi ham **bitta umumiy SQLite baza** (`db/app.db`) bilan ishlaydi.
- Backend kodi web ilova ichida: `web/backend/`.

## Yangi arxitektura

```text
telegram-platform/
├── bot/                     # Telegram bot (Python)
├── backend/                 # Core backend (FastAPI, bot bilan integratsiya)
├── web/
│   ├── frontend/            # To‘liq React UI (CDN React)
│   ├── backend/             # Web uchun backend API (FastAPI)
│   │   ├── app.py
│   │   └── requirements.txt
│   └── package.json         # frontend/backend start skriptlari
├── db/
│   ├── app.db               # Umumiy baza
│   └── backups/
└── .env.example
```

## Nima uchun bu yondashuv?
- Front va backend bitta DB bilan ishlaydi.
- Tizim lokal/VPS’da sodda boshqariladi.
- Web backend `web/backend` ichida bo‘lgani uchun UI va API bitta modulga jamlangan.

## Ishga tushirish (alohida)

### 1) Umumiy tayyorgarlik
```bash
cp .env.example .env
mkdir -p db/backups
```

### 2) Web backend (alohida terminal)
```bash
cd web
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app:app --host 127.0.0.1 --port 8100
```

### 3) React frontend (alohida terminal)
```bash
cd web
python3 -m http.server 5173 -d frontend
```
Keyin brauzerda oching: `http://127.0.0.1:5173`

## Web API endpointlar (`web/backend/app.py`)
- `GET /api/dashboard/kpi`
- `GET /api/groups`
- `GET /api/users`

## React UI xususiyatlari
- Government uslub (blue/white)
- Fixed sidebar
- KPI kartalar
- Groups va Users jadvallari
- Shared DB’dan real ma’lumot olish

## Eslatma
Brauzerdagi frontend to‘g‘ridan-to‘g‘ri SQLite o‘qiy olmaydi, shuning uchun `web/backend` lokal API qatlam sifatida xizmat qiladi.
Bu tashqi tarmoq integratsiyasi emas, lokal jarayonlar o‘rtasida yagona DB asosida ishlashdir.
