# Authentication settings
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# Security settings
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
