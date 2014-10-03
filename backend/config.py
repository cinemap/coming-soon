import os

# flask config
if 'FLASK_DEBUG' in os.environ:
    DEBUG = True
SRF_ENABLED = True
SECRET_KEY = '***TODO***'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Configure Flask-Mail -- Required for Confirm email and Forgot password features
# MAIL_SERVER   = 'smtp.cinemap.org'
# MAIL_PORT     = 587
# MAIL_USE_SSL  = True                            # Some servers use MAIL_USE_TLS=True instead
# MAIL_USERNAME = 'feedback@cinemap.org'
# MAIL_PASSWORD = 'HJifxNW7LM3XQr'
# MAIL_DEFAULT_SENDER = 'Stan (yo!)'

# Configure Flask-User
USER_PRODUCT_NAME           = "Stan"     # Used by email templates
USER_ENABLE_USERNAME        = True             # Register and Login with username
USER_ENABLE_CHANGE_USERNAME = False
USER_ENABLE_EMAIL           = False              # Register and Login with email
USER_LOGIN_TEMPLATE         = 'flask_user/login_or_register.html'
USER_REGISTER_TEMPLATE      = 'flask_user/login_or_register.html'
USER_AFTER_LOGIN_ENDPOINT   = 'profile_page'
USER_AFTER_CONFIRM_ENDPOINT = 'profile_page'


TMDB_KEY = '95a5e0f59034242b05d55145c16a1c35'
