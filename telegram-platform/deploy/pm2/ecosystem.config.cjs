module.exports = {
  apps: [
    {
      name: 'telegram-web',
      cwd: '/opt/telegram-platform/web',
      script: 'src/server.js',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: {
        NODE_ENV: 'production',
        WEB_PORT: 3000,
        BACKEND_URL: 'http://127.0.0.1:8000/api'
      }
    }
  ]
};
