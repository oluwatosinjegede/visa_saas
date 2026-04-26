from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create superuser if not exists"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")

        if not (username and password and email):
            self.stdout.write("Superuser env vars not set, skipping.")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write("Superuser already exists.")
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write("Superuser created.")