from app.conf.environ import env

# OPENAI

OPENAI_TOKEN = env("OPENAI_TOKEN", cast=str, default="")
