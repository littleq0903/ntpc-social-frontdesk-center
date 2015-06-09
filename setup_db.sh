sudo docker-compose run web python manage.py migrate
sudo docker-compose run web python collectstatic
sudo docker-compose run web python manage.py 
echo "from django.contrib.auth.models import User; User.objects.create_superuser('social', 'social@example.com', 'social26221020')" | python manage.py shell
