echo "Starting Django Application with Apache..."
cd /home/ubuntu/jobfinderapi/
source /venv/bin/activate  # Activate virtualenv if used
python manage.py migrate  # Apply any migrations
python manage.py collectstatic --noinput  # Collect static files
sudo systemctl restart apache2 # Restart Apache to apply changes