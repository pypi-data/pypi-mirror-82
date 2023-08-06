# django-async-email

[![Actions Status](https://github.com/eltonplima/django-async-email/workflows/tox/badge.svg)](https://github.com/eltonplima/django-async-email/actions)
[![Actions Status](https://github.com/eltonplima/django-async-email/workflows/flake8/badge.svg)](https://github.com/eltonplima/django-async-email/actions)

```python
EMAILS_TEMPLATES = {
    "password_reset": {
        "subject": "registration/password_set_subject.txt",
        "body_html": "registration/password_set_email.html",
        "body_txt": "registration/password_set_email.txt",
    }
}
```

# Important notes

Be careful with the email configured on the settings.DEFAULT_FROM_EMAIL.

> An invalid email on settings.DEFAULT_FROM_EMAIL will not allow your project to run

python setup.py sdist bdist_wheel && pip uninstall -y django_async_email && python -m pip install dist/django_async_email-0.1.0-py2.py3-none-any.whl

## Demo project

```shell script
cd demo_project
# Build and run the docker image
docker-compose build && docker-compose up -d demo_project
# Run migrations
docker-compose exec demo_project python manage.py migrate
# Create the superuser
docker-compose exec demo_project python manage.py createsuperuser
```

```shell script
celery worker --app=demo_project.celery -l info --pool=eventlet
```
