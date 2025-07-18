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

## Celery Task Monitoring

This project uses Celery for background task processing. Here are the different ways to monitor your tasks and jobs:

### 1. **Flower - Real-time Web Monitoring (Recommended)**

Flower provides a web-based interface for monitoring Celery tasks in real-time.

**Start Flower:**
```bash
source venv/bin/activate
celery -A config flower
```

**Access Flower Dashboard:**
- URL: http://127.0.0.1:5555
- **Tasks Tab**: View all queued, running, and completed tasks
- **Workers Tab**: Monitor active Celery workers and performance
- **Broker Tab**: Check Redis queue status and lengths
- **Monitor Tab**: Real-time task execution and success/failure rates

### 2. **Django Admin Interface**

Access task results and logs through Django admin:

**Start Django Server:**
```bash
source venv/bin/activate
python manage.py runserver
```

**Admin URLs:**
- **Main Admin**: http://127.0.0.1:8000/admin/
- **Automation Logs**: http://127.0.0.1:8000/admin/linkedin_automation/automationlog/
- **Automation Jobs**: http://127.0.0.1:8000/admin/linkedin_automation/automationjob/
- **LinkedIn Sessions**: http://127.0.0.1:8000/admin/linkedin_automation/linkedinsession/
- **Periodic Tasks**: http://127.0.0.1:8000/admin/django_celery_beat/periodictask/

### 3. **Command Line Monitoring**

Monitor tasks directly from the command line:

```bash
# Check active tasks
celery -A config inspect active

# Check scheduled tasks
celery -A config inspect scheduled

# Check reserved tasks (waiting in queue)
celery -A config inspect reserved

# Check worker statistics
celery -A config inspect stats

# Check registered tasks
celery -A config inspect registered
```

### 4. **Starting Required Services**

To monitor tasks, you need these services running:

```bash
# Terminal 1: Start Redis (if not already running)
redis-server

# Terminal 2: Start Django server
source venv/bin/activate
python manage.py runserver

# Terminal 3: Start Celery worker
source venv/bin/activate
celery -A config worker --loglevel=info

# Terminal 4: Start Celery Beat (for scheduled tasks)
source venv/bin/activate
celery -A config beat --loglevel=info

# Terminal 5: Start Flower (for web monitoring)
source venv/bin/activate
celery -A config flower
```

### 5. **What You Can Monitor**

**In Flower:**
- ✅ Real-time task queue status
- ✅ Currently running tasks
- ✅ Task execution time and performance
- ✅ Failed tasks with error details
- ✅ Worker health and statistics

**In Django Admin:**
- ✅ Completed task results and logs
- ✅ LinkedIn automation job status
- ✅ Session history and success rates
- ✅ Scheduled periodic tasks

**In Command Line:**
- ✅ Quick status checks
- ✅ Worker availability
- ✅ Queue lengths

### 6. **Task Status Meanings**

- **PENDING**: Task is queued and waiting to be processed
- **STARTED**: Task is currently being executed by a worker
- **SUCCESS**: Task completed successfully
- **FAILURE**: Task failed with an error
- **RETRY**: Task failed and is being retried
- **REVOKED**: Task was cancelled

## Security Notes

- The `.env` file contains sensitive information and is excluded from version control
- Database passwords should be strong and unique
- In production, use environment variables or a secure secrets management system
- The SECRET_KEY fallback in settings.py should be removed in production 