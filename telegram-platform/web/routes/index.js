const router = require('express').Router();
const auth = require('../middleware/auth');
const authController = require('../controllers/authController');
const dashboardController = require('../controllers/dashboardController');

router.get('/login', authController.loginPage);
router.post('/login', authController.login);
router.get('/logout', authController.logout);

router.get('/', auth, (_req, res) => res.redirect('/dashboard'));
router.get('/dashboard', auth, dashboardController.dashboard);
router.get('/groups', auth, dashboardController.groups);
router.get('/users', auth, dashboardController.users);
router.get('/analytics', auth, dashboardController.analytics);

module.exports = router;
