from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

from customuser import utils

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?',
                            default=10, type=int)
        parser.add_argument("--show-total", action='store_true', default=False)
    def handle(self, *args, **options):
        count = options.get("count")
        users = utils.get_fake_users(count=count)
        show_total = options.get("show_total")
        new_users = []
        for user in users:
            new_users.append(
                User(**user)
                )
        user_bulk = User.objects.bulk_create(new_users, ignore_conflicts=True)
        print(f"{len(user_bulk)} new users just created")
        if show_total:
            print(f"Total users: {User.objects.count()}")