# Pandemic Planner

# Authors: 
Alex Cogelja, Nathan Lamb, James Truong

# Purpose:
Calendar project to help students organize all their assignments, lectures, and exams for classes. An alternative for brightspace. Project made for CS348.

# Description:
The project is a local django website that uses an instance of PostgreSQL in Google Cloud as its database. Users are able to signup, login, add classes, add courses, add exams, add lectures, and add assignments to their account very quickly. All of those objects will be shown in the calendar tab. There is also a reports tab that uses SQL queries to generate information that will aid students with their upcoming assignments and etcetera.

# Add a table:
    1) add class in models.py under pandemic_app
    2) run python manage.py migrate pandemic_app
    3) python manage.py makemigrations pandemic_app
    4) python manage.py migrate pandemic_app
    5) table is now in google cloud under proj_tables database, table name is pandemic_app_<CLASS NAME>

# Dependencies:
    - psycopg2-binary (can get with pip)
    - Django

# Deploy/Test:
    - python manage.py runserver
    - open the server 127.0.0.1:8000/ (default page is changed)

# Connect to postgres in google cloud shell:
 - gcloud sql connect project --user=postgres
 - password is pandemic

