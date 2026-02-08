import os
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = os.getenv('SHARED_DB_PATH', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'app.db')))

app = FastAPI(title='Web Internal Backend', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])


def q(sql, params=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(sql, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


@app.get('/api/dashboard/kpi')
def kpi():
    total_groups = q('SELECT COUNT(*) c FROM groups')[0]['c'] if os.path.exists(DB_PATH) else 0
    restricted_users = q('SELECT COUNT(*) c FROM user_progress WHERE unlocked=0')[0]['c'] if os.path.exists(DB_PATH) else 0
    total_progress = q('SELECT COUNT(*) c FROM user_progress')[0]['c'] if os.path.exists(DB_PATH) else 0
    unlocked = q('SELECT COUNT(*) c FROM user_progress WHERE unlocked=1')[0]['c'] if os.path.exists(DB_PATH) else 0
    invites_today = q("SELECT COUNT(*) c FROM invite_logs WHERE date(created_at)=date('now')")[0]['c'] if os.path.exists(DB_PATH) else 0
    unlock_rate = round((unlocked / total_progress) * 100, 2) if total_progress else 0
    return {
        'total_groups': total_groups,
        'restricted_users': restricted_users,
        'unlock_rate': unlock_rate,
        'invites_today': invites_today,
        'spam_alerts': 0
    }


@app.get('/api/groups')
def groups():
    if not os.path.exists(DB_PATH):
        return []
    return q('SELECT id, title, invite_required, is_enabled FROM groups ORDER BY id DESC LIMIT 100')


@app.get('/api/users')
def users():
    if not os.path.exists(DB_PATH):
        return []
    return q('''
        SELECT u.id, u.full_name,
               COALESCE(SUM(p.invites_count),0) invites,
               COALESCE(MAX(r.score),0) risk_score
        FROM users u
        LEFT JOIN user_progress p ON p.user_id=u.id
        LEFT JOIN risk_scores r ON r.user_id=u.id
        GROUP BY u.id
        ORDER BY u.id DESC
        LIMIT 200
    ''')
