# Django Project with PostgreSQL

This is a Django project configured to use PostgreSQL as the database backend.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration:**
   The `.env` file is already created with default values. Update the following variables in `.env`:
   - `DB_NAME`: Database name (default: django_project_db)
   - `DB_USER`: PostgreSQL username (default: nathanclark)
   - `DB_PASSWORD`: PostgreSQL password (update this!)
   - `DB_HOST`: Database host (default: localhost)
   - `DB_PORT`: Database port (default: 5432)
   - `SECRET_KEY`: Django secret key (already set)
   - `DEBUG`: Debug mode (default: True)

3. **Database Setup:**
   ```bash
   # Create the database (if not already created)
   createdb django_project_db
   
   # Run migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Database Configuration

The project uses PostgreSQL with the following configuration:
- **Engine**: django.db.backends.postgresql
- **Adapter**: psycopg2-binary
- **Environment Variables**: Database credentials are loaded from `.env` file

## Project Structure

- `config/`: Django project configuration
  - `settings.py`: Main settings file with database configuration
  - `urls.py`: URL routing
  - `wsgi.py`: WSGI application entry point
  - `asgi.py`: ASGI application entry point
- `blog/`: Example Django app
  - `models.py`: Database models
  - `views.py`: View functions
  - `admin.py`: Admin interface configuration
- `.env`: Environment variables (not committed to version control)
- `requirements.txt`: Python dependencies
- `manage.py`: Django management script

## Available Commands

```bash
# Development
python manage.py runserver          # Start development server
python manage.py shell              # Open Django shell

# Database
python manage.py migrate            # Run migrations
python manage.py makemigrations     # Create migration files
python manage.py createsuperuser    # Create admin user

# Apps
python manage.py startapp myapp     # Create new app

# Utilities
python manage.py collectstatic      # Collect static files
python manage.py check              # Check for problems
```

## Security Notes

- The `.env` file contains sensitive information and is excluded from version control
- Database passwords should be strong and unique
- In production, use environment variables or a secure secrets management system
- The SECRET_KEY fallback in settings.py should be removed in production 