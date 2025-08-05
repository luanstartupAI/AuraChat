# src/celery_app.py

from celery import Celery
import os

# Configure Redis URL (assuming default Redis install on localhost)
# In a real application, use configuration management (e.g., environment variables)
redis_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')

celery_app = Celery(
    'aura_tasks', # Name of the Celery application
    broker=redis_url,
    backend=redis_url,
    include=['src.tasks'] # List of modules to import tasks from
)

# Optional Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # Add other configurations as needed
    # Example: task_routes for routing tasks to specific queues
)

# Optional: Configure Celery to work with Flask context if needed
# This might be necessary if tasks need access to Flask app context
# Example (adjust based on actual Flask app structure in main.py):
# class ContextTask(celery_app.Task):
#     def __call__(self, *args, **kwargs):
#         from src.main import app # Import Flask app instance
#         with app.app_context():
#             return self.run(*args, **kwargs)
# celery_app.Task = ContextTask

if __name__ == '__main__':
    # This allows running the worker directly for testing:
    # celery -A src.celery_app worker --loglevel=info
    celery_app.start()

