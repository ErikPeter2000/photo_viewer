# Setup for Linux

echo "Setting up Django Photo Viewer..."
pip install -r requirements.txt

touch .env
length=64

# Generate a secure random string
secret_key=$(openssl rand -base64 $length | tr -d '\n')

# Save the secret key to .env file
echo "SECRET_KEY=$secret_key" > .env
echo "CREDITS=[]" >> .env
echo "ALLOWS_HOSTS=[]" >> .env

# Navigate to the photo_viewer directory and run Django management commands
cd photo_viewer
python manage.py makemigrations photo_viewer
python manage.py migrate

# Prompt to create super user
read -p "Would you like to create a super user? (y/n) "
res=${res,,}
if [ "$res" = "y" ]; then
    python manage.py createsuperuser
fi

cd -