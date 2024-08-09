# Alive365

## Project Configuration
Install required dependencies by running the following commands:
    
    pip install django-restframework
    pip install djangorestframework_simplejwt
    pip install django-cors-headers
    pip install python-decouple

## Project Setup

- Firstly Change the .env file to put your credentials

- Set up the Django project and apps by running the necessary migrations. Navigate to the project directory containing the manage.py file and execute the following command:

      python manage.py makemigrations
      python manage.py migrate

- Once the migrations have been applied successfully, start the Django development server:

      python manage.py runserver
The server should now be running at http://localhost:8000.