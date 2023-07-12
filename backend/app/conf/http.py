from app.conf.environ import env

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://www.urf4cknmt.space",
    "https://urf4cknmt.space",
]
CORS_ALLOWED_ORIGINS = [
    "https://www.urf4cknmt.space",
]

if env("DEBUG"):
    ABSOLUTE_HOST = "http://localhost:8000"
else:
    ABSOLUTE_HOST = "https://urf4cknmt.space"
