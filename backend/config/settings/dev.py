diff --git a/backend/config/settings/dev.py b/backend/config/settings/dev.py
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..704cd60199d22ff5a31ea66dadf8410221f02db8 100644
--- a/backend/config/settings/dev.py
+++ b/backend/config/settings/dev.py
@@ -0,0 +1,18 @@
+import os
+
+from .base import *
+
+DEBUG = True
+ALLOWED_HOSTS = ["*"]
+
+if os.getenv("DEV_DB", "sqlite").lower() == "sqlite":
+    DATABASES = {
+        "default": {
+            "ENGINE": "django.db.backends.sqlite3",
+            "NAME": BASE_DIR / "db.sqlite3",
+        }
+    }
+
+REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = (
+    "rest_framework.permissions.AllowAny",
+)
