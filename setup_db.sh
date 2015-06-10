python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('social', 'social@example.com', 'social26221020')" | python manage.py shell
