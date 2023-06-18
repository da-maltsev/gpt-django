from app.conf.environ import env

ALLOWED_HOSTS = ["*"]  # host validation is not necessary in 2020
CSRF_TRUSTED_ORIGINS = [
    "https://your.app.origin",
    "http://*.127.0.0.1:8000",
    "https://urf4cknmt.space",
]

if env("DEBUG"):
    ABSOLUTE_HOST = "http://localhost:3000"
else:
    ABSOLUTE_HOST = "https://your.app.com"
