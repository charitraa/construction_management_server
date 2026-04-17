# API Documentation

Complete API reference for the Construction Management Server.

## Base URL

- **Development**: `http://localhost:8000/api/`
- **Production**: `https://yourdomain.com/api/`

## Authentication

All API endpoints (except authentication endpoints) require a valid JWT token.

### Login

```http
POST /users/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Success Response (200 OK):**

```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "email": "user@example.com",
      "name": "John Doe",
      "role": "admin"
    }
  },
  "message": "Login successful"
}
```

### Using Tokens

Include the access token in the Authorization header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Response Format

All API responses follow this format:

### Success Response

```json
{
  "data": { /* response data */ },
  "message": "Success message"
}
```

### Error Response

```json
{
  "error": "Error message"
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Successful deletion
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

## Common Query Parameters

### Pagination

- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

### Filtering

- `?field=value`: Filter by field
- `?field__gte=value`: Greater than or equal
- `?field__lte=value`: Less than or equal
- `?field__icontains=value`: Contains text (case insensitive)

### Sorting

- `?ordering=field`: Ascending order
- `?ordering=-field`: Descending order

## API Endpoints

### User Management

#### Register User
```http
POST /users/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

#### Get User Profile
```http
GET /users/profile/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Refresh Token
```http
POST /users/refresh/
Content-Type: application/json

{
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

#### Logout
```http
POST /users/logout/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Employees

#### List All Employees
```http
GET /employees/list/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Query Parameters:
- `role`: Filter by role (`Mason`, `Labor`)

**Response:**
```json
{
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "John Doe",
      "role": "Mason",
      "daily_rate": 500.00,
      "phone": "+1234567890",
      "created_at": "2026-04-01T10:00:00Z",
      "updated_at": "2026-04-01T10:00:00Z"
    }
  ],
  "message": "Employee list retrieved successfully"
}
```

#### Create Employee
```http
POST /employees/create/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "name": "John Doe",
  "role": "Mason",
  "daily_rate": 500.00,
  "phone": "+1234567890"
}
```

#### Get Employee Statistics
```http
GET /employees/stats/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**
```json
{
  "data": {
    "total": 50,
    "Mason": 30,
    "Labor": 20
  },
  "message": "Employee statistics retrieved successfully"
}
```

#### Export Employees
```http
GET /employees/export/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Projects

#### List All Projects
```http
GET /projects/list/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Query Parameters:
- `status`: Filter by status (`ongoing`, `completed`, `delayed`)

#### Create Project
```http
POST /projects/create/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "name": "New Construction Project",
  "description": "Building new commercial complex",
  "start_date": "2026-05-01",
  "end_date": "2026-12-31",
  "status": "ongoing",
  "budget": 500000.00
}
```

#### Get Project Statistics
```http
GET /projects/stats/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Revenue

#### List All Revenue
```http
GET /revenue/list/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Query Parameters:
- `start_date`: Filter by start date (YYYY-MM-DD)
- `end_date`: Filter by end date (YYYY-MM-DD)
- `project`: Filter by project ID

#### Create Revenue
```http
POST /revenue/create/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "date": "2026-04-17",
  "description": "Payment for Phase 1",
  "amount": 50000.00,
  "project": "project_id"
}
```

### Expenses

#### List All Expenses
```http
GET /expense/list/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Query Parameters:
- `category`: Filter by category (`Labor`, `Materials`, `Equipment`, `Other`)
- `start_date`: Filter by start date (YYYY-MM-DD)
- `end_date`: Filter by end date (YYYY-MM-DD)
- `project`: Filter by project ID

#### Create Expense
```http
POST /expense/create/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "date": "2026-04-17",
  "description": "Building materials",
  "category": "Materials",
  "amount": 15000.00,
  "project": "project_id"
}
```

### Attendance

#### List All Attendance
```http
GET /attendance/list/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Query Parameters:
- `date`: Filter by date (YYYY-MM-DD)
- `start_date`: Filter by start date (YYYY-MM-DD)
- `end_date`: Filter by end date (YYYY-MM-DD)
- `employee_id`: Filter by employee ID
- `status`: Filter by status (`Present`, `Absent`)

#### Create Attendance
```http
POST /attendance/create/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "date": "2026-04-17",
  "employee": "employee_id",
  "status": "Present"
}
```

#### Get Attendance by Date
```http
GET /attendance/by-date/?date=2026-04-17
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Get Attendance Statistics
```http
GET /attendance/stats/?date=2026-04-17
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**
```json
{
  "data": {
    "total": 50,
    "present": 45,
    "absent": 5
  },
  "message": "Attendance statistics retrieved successfully"
}
```

### Advances

#### List All Advances
```http
GET /advance/list/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Create Advance
```http
POST /advance/create/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "date": "2026-04-17",
  "employee": "employee_id",
  "amount": 5000.00
}
```

#### Get Advance Statistics
```http
GET /advance/stats/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Payroll

#### Get Payroll for Month
```http
GET /payroll/by-month/?month=2026-04
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**
```json
{
  "data": [
    {
      "id": "employee_id",
      "name": "John Doe",
      "role": "Mason",
      "days_worked": 20,
      "daily_rate": 500.00,
      "total_wage": 10000.00,
      "advance": 2000.00,
      "net_pay": 8000.00
    }
  ],
  "message": "Payroll data retrieved successfully"
}
```

#### Get Payroll Summary
```http
GET /payroll/summary/?month=2026-04
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**
```json
{
  "data": {
    "total_wages": 500000.00,
    "total_advances": 50000.00,
    "total_net_pay": 450000.00
  },
  "message": "Payroll summary retrieved successfully"
}
```

### Dashboard

#### Get Complete Dashboard
```http
GET /dashboard/overview/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**
```json
{
  "data": {
    "main_stats": {
      "total_revenue": 1000000.00,
      "total_expenses": 750000.00,
      "profit": 250000.00,
      "labor_cost": 500000.00,
      "material_cost": 200000.00,
      "revenue_trend": 12.5,
      "expenses_trend": -5.2,
      "profit_trend": 18.0
    },
    "monthly_trends": [
      {
        "month": "Jan",
        "revenue": 50000.00,
        "expenses": 40000.00
      }
    ],
    "expense_distribution": [
      {
        "name": "Labor",
        "value": 50.0,
        "color": "#3B82F6",
        "amount": 250000.00
      }
    ],
    "quick_stats": {
      "active_projects": 12,
      "total_employees": 50,
      "attendance_rate": 94.5
    }
  },
  "message": "Dashboard overview retrieved successfully"
}
```

## Error Handling

### Common Error Responses

#### Validation Error
```json
{
  "error": {
    "field_name": ["Error message for this field"]
  }
}
```

#### Not Found Error
```json
{
  "error": "Resource not found"
}
```

#### Authentication Error
```json
{
  "error": "Authentication credentials were not provided"
}
```

#### Permission Error
```json
{
  "error": "You do not have permission to perform this action"
}
```

## Rate Limiting

API requests are limited to 60 requests per minute per user.

**Rate Limit Exceeded Response:**
```json
{
  "error": "Rate limit exceeded. Please try again later."
}
```

## SDK Examples

### Python

```python
import requests

# Setup
BASE_URL = "https://yourdomain.com/api"
TOKEN = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Get employees
response = requests.get(f"{BASE_URL}/employees/list/", headers=headers)
employees = response.json()["data"]

# Create attendance
attendance_data = {
    "date": "2026-04-17",
    "employee": "employee_id",
    "status": "Present"
}
response = requests.post(
    f"{BASE_URL}/attendance/create/",
    json=attendance_data,
    headers=headers
)
```

### JavaScript

```javascript
// Setup
const BASE_URL = "https://yourdomain.com/api";
const TOKEN = "YOUR_ACCESS_TOKEN";
const headers = { Authorization: `Bearer ${TOKEN}` };

// Get employees
const response = await fetch(`${BASE_URL}/employees/list/`, { headers });
const data = await response.json();
const employees = data.data;

// Create attendance
const attendanceData = {
    date: "2026-04-17",
    employee: "employee_id",
    status: "Present"
};
const response = await fetch(`${BASE_URL}/attendance/create/`, {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify(attendanceData)
});
```

## Testing API

### Using cURL

```bash
# Login
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Get employees with token
curl -X GET http://localhost:8000/api/employees/list/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Create employee
curl -X POST http://localhost:8000/api/employees/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","role":"Mason","daily_rate":500.00,"phone":"+1234567890"}'
```

### Using Postman

1. **Authentication**
   - Set up login request to get token
   - Save token as environment variable

2. **API Requests**
   - Add Authorization header with Bearer token
   - Set appropriate Content-Type
   - Include request body for POST/PUT requests

## Support

For API support and questions:
- **Email**: api-support@construction-management.com
- **Documentation**: https://docs.construction-management.com
- **Issues**: https://github.com/your-org/construction-management-server/issues

---

**Version**: 1.0.0
**Last Updated**: 2026-04-17
