# HealthMateAI

An AI-powered healthcare platform built with Django and Django Rest Framework.

## Features

- User authentication (patients and doctors)
- Medical records management
- AI-powered health assistant
- Doctor profiles and search
- Appointment scheduling and management
- Notifications and reminders (via Celery)

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL (SQLite in development)
- **AI**: OpenAI API
- **Task Queue**: Celery with Redis
- **Documentation**: Swagger/ReDoc via drf-yasg

## Setup Instructions

### Prerequisites

- Python 3.8+
- Redis (for Celery)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/healthmateai.git
cd healthmateai
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file in the project root with the following variables:

```
DEBUG=True
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```

8. Start Celery worker (in a separate terminal):

```bash
celery -A healthmateai worker -l info
```

### API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs/
- ReDoc: http://localhost:8000/redoc/

## Heroku Deployment

This application is configured for deployment on Heroku. Follow these steps to deploy:

### Prerequisites for Deployment

1. Create a Heroku account
2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

### Deployment Steps

1. Login to Heroku:

```bash
heroku login
```

2. Create a new Heroku app:

```bash
heroku create your-app-name
```

3. Add PostgreSQL and Redis add-ons:

```bash
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
```

4. Set environment variables:

```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set OPENAI_API_KEY=your-openai-api-key
```

5. Push your code to Heroku:

```bash
git push heroku main
```

6. Run migrations:

```bash
heroku run python manage.py migrate
```

7. Create a superuser:

```bash
heroku run python manage.py createsuperuser
```

### Alternative Deployment via Heroku Dashboard

1. Create a new app on Heroku Dashboard
2. Connect your GitHub repository
3. Enable automatic deploys from your preferred branch
4. Add the required environment variables under "Settings" > "Config Vars"
5. Add the PostgreSQL and Redis add-ons under "Resources"
6. Deploy your application

### Scaling Workers

To ensure Celery workers are running:

```bash
heroku ps:scale worker=1
```

## License

MIT 