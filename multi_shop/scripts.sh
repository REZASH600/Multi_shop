#!/bin/bash

python manage.py makemigrations --noinput && \
python manage.py migrate --noinput




if [ ! -z "$DJANGO_SUPERUSER_USERNAME" ]; then
   echo "Creating superuser...";
   python manage.py createsuperuser --noinput --phone "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" 2>/dev/null ;
   if [ $? -eq 0 ]; then
     echo "Superuser created successfully."
   else
     echo "Superuser created failed."
   fi

fi


python manage.py runserver 0.0.0.0:8000

