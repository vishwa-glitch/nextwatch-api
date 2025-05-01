from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser for AWS Elastic Beanstalk deployment'

    def handle(self, *args, **options):
        admin_username = config('ADMIN_USERNAME', default='admin')
        admin_email = config('ADMIN_EMAIL', default='admin@example.com')
        admin_password = config('ADMIN_PASSWORD', default='changeme123')

        if not User.objects.filter(username=admin_username).exists():
            self.stdout.write(self.style.SUCCESS(f'Creating superuser {admin_username}'))
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser {admin_username} already exists'))
