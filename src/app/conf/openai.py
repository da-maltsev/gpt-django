from app.conf.environ import env

# OPENAI

OPENAI_API_KEY = env("OPENAI_API_KEY", cast=str, default="")
