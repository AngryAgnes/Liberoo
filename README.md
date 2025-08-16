# Liberoo

A modern FastAPI application for user management and travel companion services with PostgreSQL database backend.

## 🚀 Features

- **FastAPI Framework**: High-performance async API with automatic documentation
- **User Authentication**: JWT-based authentication with bcrypt password hashing
- **User Profiles**: Comprehensive user profile management with travel companions
- **Database Migrations**: Alembic-powered database schema versioning
- **Multi-language Support**: Internationalization capabilities
- **Accessibility Features**: Built-in accessibility support
- **Docker Support**: Full containerization for development and production
- **Type Safety**: Full type hints with Pydantic models

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+**: [Download Python](https://www.python.org/downloads/)
- **Poetry**: [Install Poetry](https://python-poetry.org/docs/#installation)
- **Docker & Docker Compose**: [Install Docker](https://docs.docker.com/get-docker/)
- **Git**: [Install Git](https://git-scm.com/downloads)

## 🛠️ Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AngryAgnes/Liberoo.git
cd Liberoo
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env  # If you have an example file
# OR create a new .env file
touch .env
```

Add the following environment variables to your `.env` file:

```env
# Application Settings
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true
SECRET_KEY=your-super-secret-key-change-this-in-production

# Database Configuration
POSTGRES_USER=liberoo_user
POSTGRES_PASSWORD=liberoo_password
POSTGRES_DB=liberoo_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# For local development (when running outside Docker)
# POSTGRES_HOST=localhost
```

### 3. Installation Methods

Choose one of the following installation methods:

#### Option A: Docker Development (Recommended)

```bash
# Start the application with Docker Compose
docker compose up -d

# View logs
docker compose logs -f web

# Stop the application
docker compose down
```

#### Option B: Local Development

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Start PostgreSQL with Docker
docker compose up -d db

# Update environment for local development
export POSTGRES_HOST=localhost

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🗄️ Database Setup

### Initial Migration

```bash
# If using Docker
docker compose exec web alembic upgrade head

# If running locally
alembic upgrade head
```

### Creating New Migrations

When you modify database models:

```bash
# Generate a new migration
alembic revision --autogenerate -m "Description of your changes"

# Apply the migration
alembic upgrade head
```

For detailed migration instructions, see [ALEMBIC_MIGRATION_GUIDE.md](ALEMBIC_MIGRATION_GUIDE.md).

## 🚦 Usage

### Access the Application

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **API Base URL**: http://localhost:8000/api

### API Endpoints

| Endpoint                | Method | Description       | Auth Required |
| ----------------------- | ------ | ----------------- | ------------- |
| `/api/v1/auth/login`    | POST   | User login        | No            |
| `/api/v1/auth/register` | POST   | User registration | No            |
| `/api/v1/users/`        | GET    | List users        | Yes           |
| `/api/v1/users/me`      | GET    | Current user info | Yes           |

### Authentication

1. **Register a new user**:

   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/register" \
        -H "Content-Type: application/json" \
        -d '{"username": "testuser", "password": "testpassword"}'
   ```

2. **Login**:

   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "testuser", "password": "testpassword"}'
   ```

3. **Access protected endpoints**:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/users/me" \
        -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## 🧪 Testing

### Running Tests

```bash
# If using Docker
docker compose exec web pytest

# If running locally
poetry run pytest

# Run with coverage
poetry run pytest --cov=app tests/

# Run specific test file
poetry run pytest tests/test_users.py
```

### Test Database

Tests use a separate test database. Ensure your test configuration is properly set up in the test files.

## 🔧 Development

### Code Formatting

This project uses Black for code formatting:

```bash
# Format all Python files
poetry run black .

# Check formatting without making changes
poetry run black --check .
```

### Project Structure

```
Liberoo/
├── alembic/                 # Database migrations
│   ├── versions/           # Migration files
│   └── env.py             # Alembic configuration
├── app/                    # Main application code
│   ├── api/               # API routes
│   │   └── v1/           # API version 1
│   │       └── endpoints/ # Route handlers
│   ├── core/             # Core functionality
│   │   ├── auth.py       # Authentication logic
│   │   ├── config.py     # Configuration settings
│   │   └── security.py   # Security utilities
│   ├── db/               # Database related code
│   │   ├── models/       # SQLAlchemy models
│   │   └── base.py       # Database base configuration
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic services
│   └── main.py           # FastAPI application entry point
├── tests/                 # Test files
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile            # Docker image definition
├── pyproject.toml        # Python project configuration
└── alembic.ini           # Alembic configuration file
```

### Adding New Features

1. **Create database models** in `app/db/models/`
2. **Define Pydantic schemas** in `app/schemas/`
3. **Implement business logic** in `app/services/`
4. **Create API endpoints** in `app/api/v1/endpoints/`
5. **Generate migrations** with `alembic revision --autogenerate`
6. **Write tests** in `tests/`

## 🚀 Deployment

### Production Build

```bash
# Build production image
docker build --target prod -t liberoo:latest .

# Run production container
docker run -p 8000:8000 --env-file .env liberoo:latest
```

### Production Environment Variables

For production, ensure you update these critical settings:

```env
APP_ENV=production
DEBUG=false
SECRET_KEY=your-very-secure-secret-key-for-production
# Use strong database credentials
POSTGRES_PASSWORD=very-secure-password
```

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Errors

```bash
# Check if PostgreSQL is running
docker compose ps db

# View database logs
docker compose logs db

# Restart database
docker compose restart db
```

#### Migration Issues

```bash
# Check migration status
alembic current

# View migration history
alembic history --verbose

# Reset migrations (⚠️ Development only)
alembic downgrade base
alembic upgrade head
```

#### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process (replace PID with actual process ID)
kill -9 PID

# Or use different port
uvicorn app.main:app --port 8001
```

### Debug Mode

Enable debug logging by setting:

```env
DEBUG=true
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Poetry Documentation](https://python-poetry.org/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

- **Project**: Liberoo
- **Email**: contact@liberoo.xyz
- **Repository**: https://github.com/AngryAgnes/Liberoo

---

**Happy coding! 🎉**
