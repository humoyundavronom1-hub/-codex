const { useEffect, useState } = React;

const api = {
  async get(path) {
    const r = await fetch(`http://127.0.0.1:8100/api${path}`);
    if (!r.ok) throw new Error('API xatolik');
    return r.json();
  }
};

function Sidebar() {
  const items = ['Dashboard','Groups','Rules Engine','Users','Leaderboards','Analytics','Logs','Alerts','Settings'];
  return (
    <aside className="hidden lg:flex lg:flex-col fixed inset-y-0 left-0 w-64 bg-blue-900 text-white">
      <div className="p-5 border-b border-white/20 font-bold">Davlat Admin Panel</div>
      <nav className="p-3 space-y-1 text-sm">
        {items.map(i => <a key={i} href="#" className="block rounded px-3 py-2 hover:bg-white/10">{i}</a>)}
      </nav>
    </aside>
  );
}

function App(){
  const [kpi,setKpi]=useState({total_groups:0,restricted_users:0,unlock_rate:0,invites_today:0,spam_alerts:0});
  const [groups,setGroups]=useState([]);
  const [users,setUsers]=useState([]);
  useEffect(()=>{
    api.get('/dashboard/kpi').then(setKpi).catch(()=>{});
    api.get('/groups').then(setGroups).catch(()=>{});
    api.get('/users').then(setUsers).catch(()=>{});
  },[]);
  return (
    <div className="min-h-screen lg:flex">
      <Sidebar />
      <main className="lg:ml-64 w-full p-4 md:p-6 space-y-6">
        <header className="bg-white border rounded-lg p-4 shadow-sm flex justify-between"><b>Telegram Moderation + Analytics</b><span>Admin</span></header>
        <section className="grid sm:grid-cols-2 lg:grid-cols-5 gap-4">
          <Card t="Total Groups" v={kpi.total_groups} />
          <Card t="Restricted Users" v={kpi.restricted_users} />
          <Card t="Unlock Rate" v={`${kpi.unlock_rate}%`} />
          <Card t="Invites Today" v={kpi.invites_today} />
          <Card t="Spam Alerts" v={kpi.spam_alerts} />
        </section>
        <section className="grid lg:grid-cols-2 gap-4">
          <Panel title="Groups">
            <table className="w-full text-sm"><thead><tr><th>Nomi</th><th>Invite</th><th>Status</th></tr></thead><tbody>{groups.map(g=><tr key={g.id}><td>{g.title}</td><td>{g.invite_required}</td><td>{String(g.is_enabled)}</td></tr>)}</tbody></table>
          </Panel>
          <Panel title="Users">
            <table className="w-full text-sm"><thead><tr><th>Foydalanuvchi</th><th>Invites</th><th>Risk</th></tr></thead><tbody>{users.map(u=><tr key={u.id}><td>{u.full_name}</td><td>{u.invites}</td><td>{u.risk_score}</td></tr>)}</tbody></table>
          </Panel>
        </section>
      </main>
    </div>
  )
}

function Card({t,v}){return <div className="bg-white border rounded-lg p-4 shadow-sm"><p className="text-slate-500 text-sm">{t}</p><p className="text-2xl font-semibold text-blue-900">{v}</p></div>}
function Panel({title,children}){return <div className="bg-white border rounded-lg p-4 shadow-sm"><h2 className="font-semibold mb-3">{title}</h2>{children}</div>}

ReactDOM.createRoot(document.getElementById('root')).render(<App />)
