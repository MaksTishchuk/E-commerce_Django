<h2 align="center">E-commerce</h2>


### Development Tools

**Stack:**
- Python >= 3;
- Django >= 3;
- Postgresql;
- Packages from file requirements.txt;

### Development

##### 1) Clone repository

    git clone <link generated in your repository>

##### 2) Create a virtual environment

    python -m venv venv
    
##### 3) Activate virtual environment

##### 4) Install requirements:

    pip install -r requirements.txt

##### 5) Create PostgreSQL database and make file .env.dev in ecommerce folder

    DEBUG=1
    SECRET_KEY=<your secret key>
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

    # Data Base
    POSTGRES_ENGINE=django.db.backends.postgresql_psycopg2
    POSTGRES_DB=your_db
    POSTGRES_USER=your_user
    POSTGRES_PASSWORD=your_password
    POSTGRES_HOST=your_host
    POSTGRES_PORT=5432
    DATABASE=postgres
    
    # Email
    DEFAULT_FROM_EMAIL=your@your.com
    EMAIL_USE_TLS=True
    EMAIL_HOST=your_smtp
    EMAIL_HOST_USER=your@your.com
    EMAIL_HOST_PASSWORD=pass
    EMAIL_PORT=587

##### 6) Run command to apply migrations

    python manage.py migrate
    
##### 7) Create superuser

    python manage.py createsuperuser
    
##### 8) Run server

    python manage.py runserver
    
##### 9) Commands for update locale:
    django-admin makemessages --locale=uk --symlinks
    django-admin compilemessages


Copyright (c) 2022-present, Tishchyk Maksym
