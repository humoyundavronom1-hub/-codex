const kpis=[
  ['Total Groups','142'],['Restricted Users','54'],['Unlock Rate','87.4%'],['Invites Today','1,329'],['Spam Alerts','18']
];
const groups=[
  {name:'Public Works',id:'-10029188473',status:'Active',invite:'3/week',active:'1024'},
  {name:'Security Alerts',id:'-10039123333',status:'Active',invite:'5/week',active:'881'}
];
const users=[
  {name:'Aziz Diyorov',invites:14,msg:263,risk:'0.34'},
  {name:'Madina Karimova',invites:9,msg:188,risk:'0.49'}
];
const leaders=['🥇 Team Alpha','🥈 Team Bravo','🥉 Team Charlie'];

const kpiGrid=document.getElementById('kpiGrid');
kpis.forEach(([t,v])=>{const d=document.createElement('div');d.className='kpi';d.innerHTML=`<p>${t}</p><h3>${v}</h3>`;kpiGrid.appendChild(d);});

document.getElementById('groupsBody').innerHTML=groups.map(g=>`<tr><td>${g.name}</td><td>${g.id}</td><td>${g.status}</td><td>${g.invite}</td><td>${g.active}</td><td>Edit / Disable / Stats</td></tr>`).join('');
document.getElementById('usersBody').innerHTML=users.map(u=>`<tr><td>${u.name}</td><td>${u.invites}</td><td>${u.msg}</td><td>${u.risk}</td><td>Unlock / Reset</td></tr>`).join('');
document.getElementById('leaderboardList').innerHTML=leaders.map(l=>`<li>${l}</li>`).join('');

function draw(canvasId,data,color){
  const c=document.getElementById(canvasId);const ctx=c.getContext('2d');const w=c.width=c.clientWidth,h=c.height=140;
  ctx.strokeStyle='#cbd5e1';ctx.beginPath();ctx.moveTo(10,h-12);ctx.lineTo(w-10,h-12);ctx.stroke();
  const step=(w-30)/(data.length-1);ctx.strokeStyle=color;ctx.lineWidth=3;ctx.beginPath();
  data.forEach((v,i)=>{const x=15+i*step,y=(h-20)-(v/100)*(h-40);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y)});ctx.stroke();
}

draw('lineChart',[35,44,48,58,66,72,84],'#1d4ed8');
draw('barChart',[20,82,51,63],'#0f3f99');
