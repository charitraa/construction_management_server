# Quick Start Guide

Get the Construction Management Server up and running in minutes.

## 🚀 Prerequisites

- Python 3.12 or higher
- Git
- Virtual environment support
- Basic knowledge of command line

## 📦 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/construction-management-server.git
cd construction-management-server
```

### 2. Set Up Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env file with your settings
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Start the Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## 🧪 Testing the Installation

### 1. Test API Access

```bash
curl http://localhost:8000/api/
```

### 2. Create a Test User

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User"
  }'
```

### 3. Login

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

### 4. Access Admin Panel

Navigate to: `http://localhost:8000/admin/`

Use your superuser credentials to log in.

## 📝 Basic Operations

### Create an Employee

```bash
TOKEN="your_access_token_from_login"

curl -X POST http://localhost:8000/api/employees/create/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "role": "Mason",
    "daily_rate": 500.00,
    "phone": "+1234567890"
  }'
```

### Get Dashboard Data

```bash
curl -X GET http://localhost:8000/api/dashboard/overview/ \
  -H "Authorization: Bearer $TOKEN"
```

### Mark Attendance

```bash
curl -X POST http://localhost:8000/api/attendance/create/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-04-17",
    "employee": "employee_id",
    "status": "Present"
  }'
```

## 🛠️ Development Workflow

### Project Structure

```
construction-management-server/
├── attendance/      # Attendance tracking
├── advance/         # Employee advances
├── dashboard/       # Analytics dashboard
├── employee/        # Employee management
├── expense/         # Expense tracking
├── payroll/         # Payroll calculations
├── project/         # Project management
├── revenue/         # Revenue management
├── user/            # Authentication
└── core/           # Shared utilities
```

### Adding New Features

1. **Create a new app** (if needed)
   ```bash
   python manage.py startapp myfeature
   ```

2. **Follow the established pattern**:
   ```python
   # models.py - Define your data models
   class MyModel(models.Model):
       name = models.CharField(max_length=100)
       created_at = models.DateTimeField(auto_now_add=True)

   # serializers.py - Create serializers
   class MyModelSerializer(serializers.ModelSerializer):
       class Meta:
           model = MyModel
           fields = '__all__'

   # repository.py - Database operations
   class MyModelRepository:
       @staticmethod
       def get_all():
           return MyModel.objects.all()

   # services.py - Business logic
   class MyModelService:
       @staticmethod
       def get_all():
           return MyModelRepository.get_all()

   # views.py - API endpoints
   class MyModelView(APIView):
       def get(self, request):
           data = MyModelService.get_all()
           return Response({"data": data, "message": "Success"})
   ```

3. **Create URLs**:
   ```python
   # urls.py
   urlpatterns = [
       path('my-feature/', MyModelView.as_view()),
   ]
   ```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test attendance

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Code Quality

```bash
# Format code
black .

# Check code style
flake8 .

# Sort imports
isort .
```

## 📚 Common Tasks

### Reset Database

```bash
# Delete database
rm db.sqlite3  # or drop PostgreSQL tables

# Run migrations again
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Load Sample Data

```bash
# You can create a management command to load sample data
python manage.py load_sample_data
```

### Generate API Documentation

```bash
# Install drf-yasg
pip install drf-yasg

# Add to INSTALLED_APPS in settings.py
# 'drf_yasg',

# Add URLs
# path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

# Visit http://localhost:8000/swagger/
```

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python manage.py runserver 8001
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U postgres -d postgres

# Check DATABASE_URL in .env
```

### Import Errors

```bash
# Ensure virtual environment is activated
source env/bin/activate

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Migration Issues

```bash
# Reset migrations (WARNING: This deletes data)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

## 📖 Next Steps

1. **Read the full README** - Complete documentation
2. **Explore API endpoints** - Check API_DOCUMENTATION.md
3. **Review code structure** - Understand the architecture
4. **Set up development tools** - Configure IDE and debugging
5. **Run tests** - Ensure everything works
6. **Start building** - Add your features

## 🤝 Getting Help

- **Documentation**: Check README.md and API_DOCUMENTATION.md
- **Issues**: Create a GitHub issue
- **Discussions**: Join our community discussions
- **Email**: support@construction-management.com

## 🔗 Useful Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python Documentation](https://docs.python.org/3/)

---

**Happy Coding! 🎉**

*Need help? Check the documentation or reach out to the community.*
