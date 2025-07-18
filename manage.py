#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


# # Development
# python manage.py runserver          # Start dev server (like rails server)
# python manage.py shell              # Interactive Python shell (like rails console)

# # Database
# python manage.py migrate            # Run migrations (like rails db:migrate)
# python manage.py makemigrations     # Create migration files (like rails generate migration)
# python manage.py createsuperuser    # Create admin user (like rails admin:create)

# # Apps
# python manage.py startapp blog      # Create new app (like rails generate model)

# # Utilities
# python manage.py collectstatic      # Collect static files (like rails assets:precompile)
# python manage.py check              # Check for problems (like rails routes)

