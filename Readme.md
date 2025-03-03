# Restaurant Table Booking System

A Django REST Framework (DRF) application for managing restaurant table bookings with role-based access control.

## Features

- JWT Authentication with djangorestframework-simplejwt
- Role-based access control (Admin and User roles)
- Complete table management system
- Reservation handling with conflict detection
- Comprehensive test suite using pytest
- Pydantic models for validation

## Project Structure

```
restaurant_booking/
│
├── authentication/              
│   ├── management/
│   │   └── commands/
│   │       └── create_admin.py  
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
│       ├── __init__.py
│       └── test_auth.py
│
├── table_management/           
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
│       ├── __init__.py
│       ├── test_tables.py
│       └── test_reservations.py
│
├── restaurant_booking/         
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
│
├── conftest.py                 
├── pytest.ini                  
└── requirements.txt            
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd restaurant_booking
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MySQL database:
```bash
mysql -u root -p
CREATE DATABASE restaurant_booking;
EXIT;
```

5. Configure database settings in `restaurant_booking/settings.py` or use environment variables:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'restaurant_booking'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```

6. Run migrations:
```bash
python manage.py makemigrations authentication table_management
python manage.py migrate
```

7. Create default admin user:
```bash
python manage.py create_admin
```
This will create an admin with:
- Username: `admin`
- Email: `admin@example.com`
- Password: `adminpassword`

8. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication

- `POST /auth/signup` - Register a new user
- `POST /auth/login` - Get access & refresh tokens
- `POST /auth/refresh` - Refresh token
- `POST /auth/logout` - Logout
- `GET /auth/me` - Get user details

### Admin Endpoints (requires is_admin=True)

- `POST /admin/tables` - Add a table
- `PUT /admin/tables/{id}` - Update table details
- `DELETE /admin/tables/{id}` - Delete a table
- `GET /admin/tables` - View all tables
- `GET /admin/reservations` - View all reservations

### User Endpoints

- `GET /tables` - View available tables
- `POST /tables/{id}/reserve` - Reserve a table
- `DELETE /tables/{id}/cancel` - Cancel reservation
- `GET /tables/history` - View reservation history

## Authentication

The application uses JWT authentication provided by `djangorestframework-simplejwt`:

```python
# Login and get tokens
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "adminpassword"}'

# Use the access token in subsequent requests
curl -X GET http://localhost:8000/auth/me/ \
  -H "Authorization: Bearer <access_token>"
```

## Testing

Run tests using pytest:

```bash
# Run all tests
pytest

# Run tests with specific markers
pytest -m auth
pytest -m tables
pytest -m reservations
pytest -m admin
pytest -m user
```

## Test Coverage

The test suite demonstrates the following Pytest concepts:

1. **Markers** - Tests are categorized using markers (auth, tables, reservations, admin, user)
2. **Fixtures** - Reusable setup logic for API clients, users, tables, etc.
3. **Parameterization** - Tests that run with multiple data sets
4. **Assertions** - Various assertions to validate expected outcomes
5. **Test Discovery** - Organized tests that Pytest can automatically discover
6. **Mocking** - Simulated dependencies to isolate test behavior

## Development

For local development, make sure to:

1. Run tests before committing: `pytest`
2. Check code quality: `flake8`
3. Format code: `black .`