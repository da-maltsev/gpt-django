from app.conf.environ import env

SOCIAL_AUTH_VK_OAUTH2_KEY=env("SOCIAL_AUTH_VK_OAUTH2_KEY", cast=str, default="")
SOCIAL_AUTH_VK_OAUTH2_SECRET=env("SOCIAL_AUTH_VK_OAUTH2_SECRET", cast=str, default="")

SOCIAL_AUTH_BACKENDS = [
    "social_core.backends.vk.VKOAuth2",
]

SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

# If this is not set, PSA constructs a plausible username from the first portion of the
# user email, plus some random disambiguation characters if necessary.
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_PIPELINE = [
  'social_core.pipeline.social_auth.social_details',
  'social_core.pipeline.social_auth.social_uid',
  'social_core.pipeline.social_auth.auth_allowed',
  'social_core.pipeline.social_auth.social_user',
  'social_core.pipeline.user.get_username',
  'social_core.pipeline.social_auth.associate_by_email',
  'social_core.pipeline.user.create_user',
  'social_core.pipeline.social_auth.associate_user',
  'social_core.pipeline.social_auth.load_extra_data',
  'social_core.pipeline.user.user_details',
]