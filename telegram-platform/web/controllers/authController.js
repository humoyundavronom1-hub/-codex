const api = require('../services/apiClient');

exports.loginPage = (req, res) => res.render('login');

exports.login = async (req, res) => {
  try {
    const { data } = await api.post('/auth/login', { email: req.body.email, password: req.body.password });
    res.cookie('token', data.access_token, { httpOnly: true, sameSite: 'lax' });
    return res.redirect('/dashboard');
  } catch (e) {
    return res.status(401).render('login', { error: 'Login xato' });
  }
};

exports.logout = (req, res) => { res.clearCookie('token'); res.redirect('/login'); };
