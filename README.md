# Construction Management Server

A comprehensive REST API server for construction management, built with Django and Django REST Framework. This backend system provides complete solutions for managing employees, projects, attendance, payroll, expenses, revenue, and more, with a focus on construction industry workflows.

## 🚀 Features

### Core Modules
- **Employee Management**: Complete employee lifecycle management with role-based organization
- **Project Management**: Track construction projects from start to completion
- **Attendance Tracking**: Daily attendance monitoring with comprehensive statistics
- **Payroll Processing**: Automated payroll calculations based on attendance and advances
- **Financial Management**: Expense tracking, revenue recording, and financial analytics
- **Dashboard Analytics**: Real-time business intelligence and performance metrics

### Key Capabilities
- ✅ RESTful API architecture with standardized response formats
- ✅ JWT-based authentication with refresh token support
- ✅ Role-based access control and permissions
- ✅ CSV export functionality for reporting
- ✅ Real-time statistics and trend analysis
- ✅ Automated payroll calculations
- ✅ Expense categorization and tracking
- ✅ Project status management
- ✅ Attendance rate monitoring
- ✅ Financial forecasting and analysis

## 🛠️ Tech Stack

- **Backend Framework**: Django 5.2.8
- **API Framework**: Django REST Framework 3.16.1
- **Authentication**: Django REST Framework SimpleJWT 5.5.1
- **Database**: PostgreSQL (via Django ORM)
- **API Documentation**: Swagger/OpenAPI compatible
- **CORS**: django-cors-headers 4.9.0
- **Caching**: Redis (via django-redis 6.0.0)
- **Validation**: django-filter 25.2
- **Deployment**: Gunicorn 23.0.0

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL 12+
- Redis 6+
- Virtual Environment

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd construction-management-server
```

### 2. Create Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Configure your `.env` file:

```env
# Environment
environment=development

# Security
SECRET_KEY='your-secret-key-here'
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/construction_db

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
FRONTEND_URL="http://localhost:8080"
CORS_ALLOWED_ORIGINS="http://localhost:8080"

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True
```

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## 🐳 Docker Setup

### Quick Start with Docker Compose

```bash
# Build and start all services
make build
make up

# Or using docker-compose directly
docker-compose up -d
```

### Docker Services

The docker-compose setup includes:
- **app**: Django application with Gunicorn
- **db**: PostgreSQL database
- **redis**: Redis cache and message broker
- **celery_worker**: Celery worker for background tasks
- **celery_beat**: Celery beat scheduler for periodic tasks

### Common Docker Commands

```bash
# Show logs
make logs           # All services
make logs-app       # App service only
make logs-db        # Database only

# Run commands inside containers
make shell          # Django shell
make bash           # Bash shell
make db             # PostgreSQL shell

# Database operations
make migrate        # Run migrations
make makemigrations # Create migrations
make createsuperuser  # Create admin user

# Development
make test           # Run tests
make clean          # Remove all containers and volumes
make rebuild        # Rebuild and restart services
```

### Environment Variables for Docker

Ensure your `.env` file contains these Docker-specific variables:

```env
# Database (for Docker)
POSTGRES_DB=construction_management
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Application
DEBUG=True
SECRET_KEY='your-secret-key-here'
DATABASE_URL=postgresql://postgres:postgres@db:5432/construction_management
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production Docker Deployment

For production deployment:

1. Use production environment variables
2. Configure proper secret keys
3. Use proper database passwords
4. Set `DEBUG=False`
5. Configure proper CORS origins
6. Use persistent volumes for data
7. Set up proper monitoring and logging

```bash
# Production compose (optional)
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 API Documentation

### Base URL
- **Development**: `http://localhost:8000/api/`
- **Production**: `https://your-domain.com/api/`

### Authentication

All API endpoints (except authentication endpoints) require a valid JWT token.

**Login Request:**
```http
POST /api/users/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe"
    }
  },
  "message": "Login successful"
}
```

## 🏗️ Project Structure

```
construction-management-server/
├── attendance/          # Attendance tracking module
├── advance/             # Employee advance management
├── dashboard/           # Analytics and reporting
├── employee/            # Employee management
├── expense/             # Expense tracking
├── payroll/             # Payroll processing
├── project/             # Project management
├── revenue/             # Revenue recording
├── user/                # Authentication and user management
├── core/               # Shared utilities and middleware
├── construction_server/ # Django project settings
├── env/                # Virtual environment
├── logs/               # Application logs
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── .env              # Environment variables
```

### Module Architecture

Each module follows a consistent architecture pattern:

```
module/
├── models.py          # Django ORM models
├── serializers.py     # DRF serializers for validation
├── repository.py      # Database operations layer
├── services.py        # Business logic layer
├── views.py          # API view classes
├── urls.py           # URL routing
├── exceptions.py      # Custom exceptions
└── admin.py          # Django admin configuration
```

## 📊 API Endpoints

### Authentication (`/api/users/`)
- `POST /register/` - Register new user
- `POST /login/` - User authentication
- `POST /logout/` - User logout
- `POST /refresh/` - Refresh access token
- `GET /profile/` - Get user profile

### Employees (`/api/employees/`)
- `GET /list/` - Get all employees (with role filtering)
- `POST /create/` - Create new employee
- `GET /stats/` - Get employee statistics
- `GET /export/` - Export employee data as CSV
- `GET /details/<id>/` - Get specific employee
- `PUT /update/<id>/` - Update employee
- `DELETE /delete/<id>/` - Delete employee

### Projects (`/api/projects/`)
- `GET /list/` - Get all projects (with status filtering)
- `POST /create/` - Create new project
- `GET /stats/` - Get project statistics
- `GET /export/` - Export project data as CSV
- `GET /details/<id>/` - Get specific project
- `PUT /update/<id>/` - Update project
- `DELETE /delete/<id>/` - Delete project

### Revenue (`/api/revenue/`)
- `GET /list/` - Get all revenue records
- `POST /create/` - Record new revenue
- `GET /stats/` - Get revenue statistics
- `GET /export/` - Export revenue data as CSV
- `GET /details/<id>/` - Get specific record
- `PUT /update/<id>/` - Update record
- `DELETE /delete/<id>/` - Delete record

### Expenses (`/api/expense/`)
- `GET /list/` - Get all expenses (with category filtering)
- `POST /create/` - Record new expense
- `GET /stats/` - Get expense statistics
- `GET /export/` - Export expense data as CSV
- `GET /details/<id>/` - Get specific expense
- `PUT /update/<id>/` - Update expense
- `DELETE /delete/<id>/` - Delete expense

### Attendance (`/api/attendance/`)
- `GET /list/` - Get all attendance records (with filtering)
- `POST /create/` - Record attendance
- `GET /by-date/?date=YYYY-MM-DD` - Get attendance by date
- `GET /stats/?date=YYYY-MM-DD` - Get attendance statistics
- `GET /export/` - Export attendance data as CSV
- `GET /details/<id>/` - Get specific record
- `PUT /update/<id>/` - Update attendance
- `DELETE /delete/<id>/` - Delete record

### Advances (`/api/advance/`)
- `GET /list/` - Get all advance records
- `POST /create/` - Record new advance
- `GET /stats/` - Get advance statistics
- `GET /export/` - Export advance data as CSV
- `GET /details/<id>/` - Get specific advance
- `DELETE /delete/<id>/` - Delete advance

### Payroll (`/api/payroll/`)
- `GET /by-month/?month=YYYY-MM` - Get payroll for month
- `GET /summary/?month=YYYY-MM` - Get payroll summary
- `GET /export/?month=YYYY-MM` - Export payroll as CSV

### Dashboard (`/api/dashboard/`)
- `GET /overview/` - Get complete dashboard data
- `GET /stats/` - Get main statistics
- `GET /trends/?months=6` - Get monthly trends
- `GET /expenses/` - Get expense distribution
- `GET /quick-stats/` - Get quick statistics
- `GET /export/?type=overview` - Export dashboard data

## 💡 Usage Examples

### Create Employee

```bash
curl -X POST http://localhost:8000/api/employees/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "John Doe",
    "role": "Mason",
    "daily_rate": 500.00,
    "phone": "+1234567890"
  }'
```

### Get Attendance for Date

```bash
curl -X GET "http://localhost:8000/api/attendance/by-date/?date=2026-04-17" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Payroll for Month

```bash
curl -X GET "http://localhost:8000/api/payroll/by-month/?month=2026-04" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Export Revenue Data

```bash
curl -X GET "http://localhost:8000/api/revenue/export/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  --output revenue.csv
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Refresh Token Management**: Automatic token refresh
- **CORS Protection**: Configurable cross-origin resource sharing
- **Input Validation**: Comprehensive data validation at all layers
- **SQL Injection Prevention**: Django ORM parameterized queries
- **XSS Protection**: Built-in Django security middleware
- **CSRF Protection**: Enabled for form submissions

## 📊 Database Schema

### Core Models

**Employee**
- `id` (UUID, Primary Key)
- `name` (String)
- `role` (Enum: Mason, Labor)
- `daily_rate` (Decimal)
- `phone` (String)
- `created_at`, `updated_at` (DateTime)

**Project**
- `id` (UUID, Primary Key)
- `name` (String)
- `description` (Text)
- `start_date`, `end_date` (Date)
- `status` (Enum: ongoing, completed, delayed)
- `budget` (Decimal)
- `created_at`, `updated_at` (DateTime)

**Attendance**
- `id` (UUID, Primary Key)
- `date` (Date)
- `employee` (Foreign Key to Employee)
- `status` (Enum: Present, Absent)
- `created_at`, `updated_at` (DateTime)

**Expense**
- `id` (UUID, Primary Key)
- `date` (Date)
- `description` (String)
- `category` (Enum: Labor, Materials, Equipment, Other)
- `amount` (Decimal)
- `project` (Foreign Key to Project, Optional)
- `created_at`, `updated_at` (DateTime)

**Revenue**
- `id` (UUID, Primary Key)
- `date` (Date)
- `description` (String)
- `amount` (Decimal)
- `project` (Foreign Key to Project, Optional)
- `created_at`, `updated_at` (DateTime)

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test attendance

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Production Setup

1. **Environment Variables**
   ```env
   environment=production
   DEBUG=False
   SECRET_KEY=<production-secret-key>
   ```

2. **Database Configuration**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'production_db',
           'USER': 'db_user',
           'PASSWORD': 'secure_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

4. **Run with Gunicorn**
   ```bash
   gunicorn construction_server.wsgi:application --bind 0.0.0.0:8000
   ```

5. **Redis Configuration**
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
           'OPTIONS': {
               'CLIENT_CLASS': 'django_redis.client.DefaultClient',
           }
       }
   }
   ```

## 📈 Performance Optimization

- **Database Query Optimization**: `select_related()` and `prefetch_related()` usage
- **Caching Strategy**: Redis caching for frequently accessed data
- **Pagination**: Default pagination for large datasets
- **Database Indexing**: Strategic indexes on frequently queried fields
- **Connection Pooling**: Efficient database connection management

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Add tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

**Development Team**
- Backend Development
- API Design and Architecture
- Database Design
- Testing and Quality Assurance

## 📞 Support

For support, email support@construction-management.com or open an issue in the repository.

## 🙏 Acknowledgments

- Django Project for the amazing framework
- Django REST Framework for powerful API capabilities
- All contributors who have helped shape this project

## 📝 Changelog

### Version 1.0.0
- Initial release
- Complete API implementation
- All core modules functional
- Authentication and authorization
- Dashboard analytics
- CSV export functionality
- Comprehensive testing

---

**Built with ❤️ for construction management professionals**
