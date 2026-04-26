diff --git a/backend/config/settings/base.py b/backend/config/settings/base.py
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..0369be3572976df8e6ded95a42b1e31ccf96cf47 100644
--- a/backend/config/settings/base.py
+++ b/backend/config/settings/base.py
@@ -0,0 +1,101 @@
+from pathlib import Path
+import os
+
+BASE_DIR = Path(__file__).resolve().parent.parent.parent
+
+SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-dev-secret-key")
+DEBUG = False
+ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]
+
+INSTALLED_APPS = [
+    "django.contrib.admin",
+    "django.contrib.auth",
+    "django.contrib.contenttypes",
+    "django.contrib.sessions",
+    "django.contrib.messages",
+    "django.contrib.staticfiles",
+    "rest_framework",
+    "rest_framework_simplejwt",
+    "apps.accounts",
+    "apps.visa",
+    "apps.relocation",
+    "apps.study",
+    "apps.analytics",
+    "apps.documents",
+    "apps.ai_assistant",
+    "apps.payments",
+    "apps.notifications",
+    "apps.admin_portal",
+    "apps.compliance",
+    "apps.scoring",
+]
+
+MIDDLEWARE = [
+    "django.middleware.security.SecurityMiddleware",
+    "django.contrib.sessions.middleware.SessionMiddleware",
+    "django.middleware.common.CommonMiddleware",
+    "django.middleware.csrf.CsrfViewMiddleware",
+    "django.contrib.auth.middleware.AuthenticationMiddleware",
+    "django.contrib.messages.middleware.MessageMiddleware",
+    "django.middleware.clickjacking.XFrameOptionsMiddleware",
+]
+
+ROOT_URLCONF = "config.urls"
+
+TEMPLATES = [
+    {
+        "BACKEND": "django.template.backends.django.DjangoTemplates",
+        "DIRS": [BASE_DIR / "templates"],
+        "APP_DIRS": True,
+        "OPTIONS": {
+            "context_processors": [
+                "django.template.context_processors.request",
+                "django.contrib.auth.context_processors.auth",
+                "django.contrib.messages.context_processors.messages",
+            ]
+        },
+    }
+]
+
+WSGI_APPLICATION = "config.wsgi.application"
+ASGI_APPLICATION = "config.asgi.application"
+
+DATABASES = {
+    "default": {
+        "ENGINE": "django.db.backends.postgresql",
+        "NAME": os.getenv("POSTGRES_DB", "visa_saas"),
+        "USER": os.getenv("POSTGRES_USER", "visa_saas"),
+        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "visa_saas"),
+        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
+        "PORT": os.getenv("POSTGRES_PORT", "5432"),
+    }
+}
+
+AUTH_PASSWORD_VALIDATORS = [
+    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
+    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
+    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
+    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
+]
+
+LANGUAGE_CODE = "en-us"
+TIME_ZONE = "UTC"
+USE_I18N = True
+USE_TZ = True
+
+STATIC_URL = "/static/"
+STATIC_ROOT = BASE_DIR / "staticfiles"
+MEDIA_URL = "/media/"
+MEDIA_ROOT = BASE_DIR / "media"
+
+DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
+AUTH_USER_MODEL = "accounts.User"
+
+REST_FRAMEWORK = {
+    "DEFAULT_AUTHENTICATION_CLASSES": (
+        "rest_framework_simplejwt.authentication.JWTAuthentication",
+    ),
+    "DEFAULT_PERMISSION_CLASSES": (
+        "rest_framework.permissions.IsAuthenticated",
+    ),
+}
