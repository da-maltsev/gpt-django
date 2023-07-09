from app.conf.environ import env

ALLOWED_HOSTS = ["*"]  # host validation is not necessary in 2020

if env("DEBUG"):
    ABSOLUTE_HOST = "http://localhost:8000"
else:
    ABSOLUTE_HOST = "https://urf4cknmt.space"
