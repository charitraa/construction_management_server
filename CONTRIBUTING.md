# Contributing to Construction Management Server

Thank you for your interest in contributing to the Construction Management Server! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Focus on what is best for the community
- Show empathy toward other community members

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 12+
- Redis 6+
- Git

### Setup Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/construction-management-server.git
   cd construction-management-server
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

5. **Setup Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Development Data**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Development Workflow

### Branch Naming

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical production fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Test additions or updates

### Example Branch Names

```bash
feature/payroll-calculation-improvement
bugfix/attendance-date-filter
hotfix/security-vulnerability-fix
refactor/database-optimization
docs/api-documentation-update
test/employee-validation-tests
```

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```bash
feat(attendance): Add bulk attendance import feature
fix(payroll): Correct overtime calculation formula
docs(readme): Update API endpoint documentation
test(employee): Add validation tests for employee creation
refactor(database): Optimize queries in dashboard statistics
```

## 📏 Coding Standards

### Python Code Style

- Follow **PEP 8** guidelines
- Use **Black** for code formatting
- Use **flake8** for linting
- Maximum line length: 88 characters

### Code Quality

```bash
# Format code with Black
black .

# Check code style with flake8
flake8 .

# Sort imports with isort
isort .

# Check for security issues
bandit -r .
```

### Module Structure

Each module should follow this structure:

```
module_name/
├── __init__.py
├── models.py          # Django models
├── serializers.py     # DRF serializers
├── repository.py      # Database operations
├── services.py        # Business logic
├── views.py          # API views
├── urls.py           # URL routing
├── exceptions.py      # Custom exceptions
├── admin.py          # Admin configuration
└── tests.py          # Module tests
```

### API Response Format

All API responses should follow this format:

```python
# Success Response
{
    "data": {...},
    "message": "Success message"
}

# Error Response
{
    "error": "Error message"
}
```

### Error Handling

Use custom exceptions for module-specific errors:

```python
# In exceptions.py
class ModuleSpecificException(APIException):
    status_code = 400
    default_detail = "Default error message"

# In views.py
raise ModuleSpecificException("Specific error message")
```

## 🧪 Testing Guidelines

### Test Structure

```python
class ModelNameTest(TestCase):
    """Test suite for ModelName"""

    def setUp(self):
        # Setup test data
        pass

    def test_method(self):
        # Test implementation
        self.assertEqual(result, expected)
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
coverage html  # Generate HTML coverage report

# Run specific test class
python manage.py test attendance.tests.AttendanceModelTest

# Run specific test method
python manage.py test attendance.tests.AttendanceModelTest.test_create_attendance
```

### Test Coverage

- Aim for **80%+** code coverage
- Write tests for all new features
- Update tests when modifying existing code
- Include both positive and negative test cases

### Test Data Management

- Use Django's test database (automatic)
- Clean up test data in `tearDown()` methods
- Use factories for creating test data
- Avoid hardcoding test data

## 📝 Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Use Google-style docstrings
- Include parameter types and return values

```python
def calculate_payroll(employee_id: str, month: str) -> dict:
    """
    Calculate payroll for an employee for a specific month.

    Args:
        employee_id: UUID of the employee
        month: Month in YYYY-MM format

    Returns:
        Dictionary containing payroll details:
        - days_worked: Number of days worked
        - total_wage: Total wage earned
        - advances: Total advance amount
        - net_pay: Net payment amount

    Raises:
        ValueError: If month format is invalid
        EmployeeNotFoundException: If employee not found
    """
    pass
```

### API Documentation

Update API documentation when:
- Adding new endpoints
- Modifying existing endpoints
- Changing request/response formats
- Adding new query parameters

### README Updates

Update README.md for:
- New features
- API changes
- Configuration updates
- Installation changes

## 🔄 Pull Request Process

### Before Submitting

1. **Test thoroughly**
   ```bash
   python manage.py test
   coverage report
   ```

2. **Code quality checks**
   ```bash
   black .
   flake8 .
   ```

3. **Documentation review**
   - API documentation updated
   - Code comments added
   - README updated if needed

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests passing
```

### Pull Request Process

1. Update your branch with latest main
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. Create Pull Request with clear description

3. Address review comments promptly

4. Ensure CI/CD checks pass

5. Wait for approval and merge

## 🐛 Bug Reports

When reporting bugs, include:

1. **Clear title**
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Environment details**
6. **Screenshots/logs** (if applicable)

### Bug Report Template

```markdown
**Title:** Brief description of the issue

**Description:**
Detailed description of the issue

**Steps to Reproduce:**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior:**
What you expected to happen

**Actual Behavior:**
What actually happened

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python Version: [e.g. 3.12]
- Django Version: [e.g. 5.2.8]
- Database: [e.g. PostgreSQL 14]

**Logs/Error Messages:**
```
Paste error messages here
```
```

## 💡 Feature Requests

When requesting features:

1. **Clear title**
2. **Problem statement**
3. **Proposed solution**
4. **Alternatives considered**
5. **Additional context**

### Feature Request Template

```markdown
**Title:** Brief feature title

**Problem Statement:**
Describe the problem this feature would solve

**Proposed Solution:**
Describe the proposed solution in detail

**Alternatives:**
Describe any alternative solutions you've considered

**Additional Context:**
Add any other context about the feature request
```

## 📞 Getting Help

- Open an issue for bugs or questions
- Check existing documentation
- Review similar issues or PRs
- Contact maintainers directly for urgent matters

## 🎉 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

---

Thank you for contributing to Construction Management Server! 🚀
