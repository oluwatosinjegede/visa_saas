import os

environment = os.getenv("DJANGO_ENV", "dev").lower()

if environment == "prod":
    from .prod import *  # noqa: F403
else:
    from .dev import *  # noqa: F403