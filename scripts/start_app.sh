#!/usr/bin/bash 

sudo sed -i 's/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \["3.92.227.157", "127.0.0.1" ,"localhost"\]/' /home/ubuntu/jobfinderapi/config/settings.py

sudo mkdir -p /home/ubuntu/jobfinderapi/staticfiles
sudo mkdir -p /home/ubuntu/jobfinderapi/static

# Navigate to the project directory
cd /home/ubuntu/jobfinderapi || exit

# Ensure correct permissions for staticfiles directory
sudo chown -R ubuntu:www-data /home/ubuntu/jobfinderapi/staticfiles
sudo chmod -R 755 /home/ubuntu/jobfinderapi/staticfiles

# Run Django management commands
/home/ubuntu/venv/bin/python manage.py migrate
/home/ubuntu/venv/bin/python manage.py makemigrations
/home/ubuntu/venv/bin/python manage.py collectstatic --noinput

# Restart Gunicorn and Nginx services
sudo service gunicorn restart
sudo service nginx restart
