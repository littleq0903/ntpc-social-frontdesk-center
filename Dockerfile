FROM littleq0903/ntpc-frontdesk-env
MAINTAINER Colin Su

RUN mkdir src
ADD . src

WORKDIR src

RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('social', 'social@example.com', 'social26221020')" | python manage.py shell

EXPOSE 8000
