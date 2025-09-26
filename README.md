```markdown
# 🎬 NextWatch Backend

<div align="center">

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)](https://jwt.io)

*Django backend for the NextWatch project that serves as a proxy to the TMDB API while handling user authentication and features like watchlists and ratings.*

</div>

---

## ✨ Features

- 🔐 **User Authentication** - Secure JWT token-based authentication
- 🎭 **TMDB API Proxy** - Cached proxy for The Movie Database API
- 📺 **User Watchlists** - Personal content tracking and management
- ⭐ **Ratings & Reviews** - User-generated content ratings and reviews
- 🔍 **Content Discovery** - Advanced search and discovery features

---

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.8+
- pip package manager

### 🛠️ Installation

**1. Create and activate virtual environment:**

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

**2. Install dependencies:**

```bash
pip install -r requirements.txt
```

**3. Environment setup:**

```bash
cp .env.sample .env
```

**4. Run database migrations:**

```bash
python manage.py migrate
```

**5. Start the development server:**

```bash
python manage.py runserver
```

---

## ⚙️ Environment Configuration

### 🔧 Local Development Setup

Copy the sample environment file and configure your settings:

```bash
cp .env.sample .env
```

### 📝 Environment Variables

```env
# 🔑 Django Core Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# 🗄️ Database Configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# For PostgreSQL Production:
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=nextwatch
# DB_USER=your-db-user
# DB_PASSWORD=your-db-password
# DB_HOST=your-db-host
# DB_PORT=5432

# 🎬 TMDB API Configuration
TMDB_API_KEY=your-tmdb-api-key
TMDB_READ_ACCESS_TOKEN=your-tmdb-read-access-token

# 🌐 CORS Settings
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

> **📌 Production Note:** For Render deployment, configure these variables in the `render.yaml` file or Render dashboard.

---

## 🛠️ API Reference

### 🔐 Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | 👤 Register new user |
| `POST` | `/api/auth/login/` | 🔑 User login |
| `POST` | `/api/auth/refresh/` | 🔄 Refresh JWT token |

### 🎭 Content Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/discover/` | 🔍 Discover movies and TV shows |
| `GET` | `/api/search/` | 🔎 Search content |
| `GET` | `/api/trending/` | 📈 Get trending content |
| `GET` | `/api/movies/{id}/` | 🎬 Get movie details |
| `GET` | `/api/tv/{id}/` | 📺 Get TV show details |

### 👤 User Feature Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/watchlist/` | 📋 List user's watchlist |
| `POST` | `/api/watchlist/` | ➕ Add to watchlist |
| `DELETE` | `/api/watchlist/{id}/` | ❌ Remove from watchlist |
| `GET` | `/api/ratings/` | ⭐ List user's ratings |
| `POST` | `/api/ratings/` | ➕ Add rating |
| `PUT` | `/api/ratings/{id}/` | ✏️ Update rating |
| `DELETE` | `/api/ratings/{id}/` | 🗑️ Delete rating |

---

## 🚀 Production Deployment

### 🌐 Deploying to Render

<div align="center">

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

</div>

**Step-by-step deployment guide:**

1. **📂 Repository Setup**
   - Fork or clone this repository to your GitHub account

2. **🔗 Connect to Render**
   - Sign up for a [Render account](https://render.com)
   - Connect your GitHub account to Render

3. **⚡ Create Web Service**
   - Create a new Web Service and select your repository
   - Render will automatically detect the `render.yaml` configuration

4. **🔧 Configure Environment Variables**
   Update these variables in the Render dashboard:
   ```
   TMDB_API_KEY=your-tmdb-api-key
   TMDB_READ_ACCESS_TOKEN=your-tmdb-read-access-token
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
   CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.com
   ```

5. **🚀 Deploy**
   - Click deploy and let Render handle the rest!

The `render.yaml` configuration automatically handles:
- ✅ PostgreSQL database setup
- ✅ Build and start commands
- ✅ Environment variable configuration

### 🔧 Manual Deployment Checklist

For custom deployment environments:

- [ ] Set `DEBUG=False` in production
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure Redis for caching (optional)
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure CORS settings for your frontend domain
- [ ] Set up proper logging and monitoring

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

**Built with ❤️ using Django and the TMDB API**

[⭐ Star this repo](https://github.com/your-username/nextwatch-backend) • [🐛 Report Bug](https://github.com/your-username/nextwatch-backend/issues) • [💡 Request Feature](https://github.com/your-username/nextwatch-backend/issues)

</div>
```
