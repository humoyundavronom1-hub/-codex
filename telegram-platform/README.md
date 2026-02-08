# Telegram Admin Panel — Frontend Only (Node.js)

Bu versiya **faqat frontend** uchun tayyorlangan.
- Backend, bot, deploy, migration va boshqa ortiqcha qismlar olib tashlangan.
- Barcha UI bir joyda, professional gov-style ko‘rinishda ishlab turadi.
- Node.js (`express`) orqali frontend serve qilinadi.

## Stack
- Node.js 20+
- Express
- HTML/CSS/JS (modulli, professional dashboard UI)

## Ishga tushirish
```bash
cd web
npm install
npm run start
```

Brauzer: `http://127.0.0.1:3000`

## Strukturasi
```text
telegram-platform/
├── .env.example
├── README.md
└── web/
    ├── package.json
    ├── src/
    │   └── server.js
    └── public/
        ├── index.html
        ├── styles.css
        └── app.js
```

## UI bo‘limlari
- Dashboard (KPI, chart, filters, export)
- Groups
- Rules Engine
- Users
- Leaderboards
- Analytics
- Logs
- Alerts
- Settings

## Sifat va dizayn
- Blue/white government style
- Fixed sidebar + topbar
- Toza, minimal, professional layout
- Responsive (desktop/tablet/mobile)
- Reusable UI bloklar
