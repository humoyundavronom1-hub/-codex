const api = require('../services/apiClient');

function authHeader(req) { return { Authorization: `Bearer ${req.cookies.token}` }; }

exports.dashboard = async (req, res) => {
  const kpi = (await api.get('/dashboard/kpi', { headers: authHeader(req) })).data;
  const lb = (await api.get('/leaderboards', { headers: authHeader(req) })).data;
  const logs = (await api.get('/logs', { headers: authHeader(req) })).data.slice(0, 10);
  res.render('dashboard', { kpi, lb, logs });
};

exports.groups = async (req, res) => {
  const groups = (await api.get('/groups', { headers: authHeader(req) })).data;
  res.render('groups', { groups });
};

exports.users = async (req, res) => {
  const users = (await api.get('/users', { headers: authHeader(req) })).data;
  res.render('users', { users });
};

exports.analytics = async (req, res) => {
  const funnel = (await api.get('/analytics/unlock-funnel', { headers: authHeader(req) })).data;
  res.render('analytics', { funnel });
};
