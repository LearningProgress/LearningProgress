import os
import re
import sys

from django.utils.crypto import get_random_string


def create_settings():
    """
    Creates a new learningprogress_settings.py file in the base directory
    if inexistent.
    """
    base_dir = os.path.dirname(__file__)
    if not os.path.exists(os.path.join(base_dir, 'learningprogress_settings.py')):
        default_settings_path = os.path.join(base_dir, 'learningprogress', 'default_settings.py')
        with open(default_settings_path) as default_settings:
            key = get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
            settings = re.sub(
                r"SECRET_KEY = ''",
                "SECRET_KEY = '%s'" % key,
                default_settings.read())
            with open(os.path.join(base_dir, 'learningprogress_settings.py'), 'w') as new_settings:
                new_settings.write(settings)


if __name__ == '__main__':
    create_settings()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learningprogress_settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
