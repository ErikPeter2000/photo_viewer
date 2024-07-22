# Setup for Linux

echo "Setting up Django Photo Viewer..."
pip install django
pip install pillow

cd photo_viewer
python manage.py makemigrations photo_viewer
python manage.py migrate

# Prompt to create super user
read -p "Would you like to create a super user? (y/n) " res
res=${res,,} # Convert to lowercase
if [ "$res" = "y" ]; then
    python manage.py createsuperuser
fi