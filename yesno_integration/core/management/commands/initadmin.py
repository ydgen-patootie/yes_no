from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        if get_user_model().objects.count() == 0:
            admin = get_user_model().objects.create_superuser(email=os.environ.get("admin_email", "admin_email"),
                                                              username=os.environ.get("admin_username",
                                                                                      "admin_username"),
                                                              password=os.environ.get("admin_password",
                                                                                      "admin_password"))
            admin.is_active = True
            admin.is_admin = True
            admin.save()
