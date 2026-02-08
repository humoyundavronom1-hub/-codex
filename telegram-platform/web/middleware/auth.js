module.exports = function(req, res, next) {
  if (!req.cookies.token) return res.redirect('/login');
  next();
};
