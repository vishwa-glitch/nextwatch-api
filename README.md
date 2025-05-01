# NextWatch Backend

Django backend for the NextWatch project that serves as a proxy to the TMDB API while handling user authentication and features like watchlists and ratings.

## Features

- User authentication with JWT tokens
- TMDB API proxy with caching
- User watchlists
- User ratings and reviews
- Content discovery and search

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file with required environment variables (see Environment Variables section)

4. Run migrations:
```bash
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```

## Environment Variables

For local development, copy the `.env.sample` file to `.env` and update the values:

```bash
cp .env.sample .env
```

Then edit the `.env` file with your specific values:

```
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database settings
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
# For PostgreSQL:
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=nextwatch
# DB_USER=your-db-user
# DB_PASSWORD=your-db-password
# DB_HOST=your-db-host
# DB_PORT=5432

# TMDB API settings
TMDB_API_KEY=your-tmdb-api-key
TMDB_READ_ACCESS_TOKEN=your-tmdb-read-access-token

# CORS settings
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

For production deployment on Render, these variables are configured in the `render.yaml` file and can be updated in the Render dashboard.

## API Endpoints

### Authentication
- POST /api/auth/register/ - Register new user
- POST /api/auth/login/ - Login user
- POST /api/auth/refresh/ - Refresh JWT token

### Content
- GET /api/discover/ - Discover movies and TV shows
- GET /api/search/ - Search content
- GET /api/trending/ - Get trending content
- GET /api/movies/{id}/ - Get movie details
- GET /api/tv/{id}/ - Get TV show details

### User Features
- GET /api/watchlist/ - List user's watchlist
- POST /api/watchlist/ - Add to watchlist
- DELETE /api/watchlist/{id}/ - Remove from watchlist
- GET /api/ratings/ - List user's ratings
- POST /api/ratings/ - Add rating
- PUT /api/ratings/{id}/ - Update rating
- DELETE /api/ratings/{id}/ - Delete rating

## Production Deployment

### Deploying to Render

This project is configured for easy deployment to Render.com:

1. Fork or clone this repository to your GitHub account
2. Sign up for a Render account at https://render.com
3. Connect your GitHub account to Render
4. Create a new Web Service and select your repository
5. Render will automatically detect the `render.yaml` configuration
6. Update the environment variables in the Render dashboard:
   - Set `TMDB_API_KEY` to your TMDB API key
   - Set `TMDB_READ_ACCESS_TOKEN` to your TMDB read access token
   - Update `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` with your frontend domain
7. Deploy the service

The `render.yaml` file will automatically:
- Set up a PostgreSQL database
- Configure the build and start commands
- Set up environment variables

### Manual Deployment

If you prefer to deploy manually:

1. Set DEBUG=False in .env
2. Configure proper ALLOWED_HOSTS
3. Set up PostgreSQL database
4. Configure Redis for caching (optional)
5. Set up HTTPS
6. Configure CORS settings for your frontend domain