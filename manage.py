#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Ensure the correct settings module is used. Some environments may have
    # DJANGO_SETTINGS_MODULE set to a different value (for example 'controller.settings')
    # which causes ImportError. Force the project setting here so manage.py always
    # uses the local project's settings.
    os.environ['DJANGO_SETTINGS_MODULE'] = 'string_analyzer_project.settings'
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
