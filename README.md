# Glide Django Backend

A comprehensive Django REST Framework backend for project and task management with JWT authentication. This project provides a robust API for managing users, projects, and tasks, featuring secure authentication, full CRUD operations, and admin integration.

## Features

- **Custom User Model**: Extended AbstractUser with unique email validation and creation timestamps
- **Project Management**: Complete CRUD operations for projects with ownership tracking
- **Task Management**: Manage tasks within projects with status tracking (todo, in_progress, done) and assignment capabilities
- **JWT Authentication**: Secure token-based authentication with access and refresh tokens
- **RESTful APIs**: Full CRUD operations via Django REST Framework with automatic API documentation
- **Admin Integration**: Django admin interface for data management and superuser access
- **Modular Architecture**: Organized into separate apps for better maintainability

## Project Setup

This project was initialized using Django 6.0.3 with the following steps:

1. Created Django project named `glide`
2. Set up virtual environment for Windows PowerShell
3. Installed core dependencies: Django, Django REST Framework, and Simple JWT
4. Configured project structure with modular Django apps

### Dependencies

The project requires the following Python packages:

- Django >= 6.0.3
- djangorestframework >= 3.14
- djangorestframework-simplejwt >= 5.3

To install dependencies, create a `requirements.txt` file with:

```
Django>=6.0.3
djangorestframework>=3.14
djangorestframework-simplejwt>=5.3
```

Then run: `pip install -r requirements.txt`

## Apps Created

The project is organized into three main Django apps:

### users
Handles custom user model and authentication base functionality.

### projects
Contains the core domain logic for projects and tasks, including models, serializers, and API views.

### authentication
Manages user registration and JWT authentication endpoints.

## Custom User Model

The custom user model extends Django's `AbstractUser` to add additional fields:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
```

**Key Features:**
- Unique email field for better user identification
- Automatic timestamp tracking with `createdAt`
- Configured as `AUTH_USER_MODEL = 'users.User'` in Django settings
- Registered in Django admin for management

## Core Domain Models

### Project Model

```python
class Project(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects"
    )
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

**Fields:**
- `name`: Project title (required, max 256 characters)
- `description`: Optional project description
- `owner`: Foreign key to User model with cascade delete
- `createdAt`: Automatic timestamp on creation
- Reverse relation: `owned_projects` (accessible via `user.owned_projects`)

### Task Model

```python
class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="todo"
    )
    due_date = models.DateField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

**Fields:**
- `title`: Task title (required, max 255 characters)
- `description`: Optional task description
- `project`: Foreign key to Project with cascade delete
- `assigned_to`: Optional foreign key to User (set to null on user deletion)
- `status`: Choice field with predefined statuses (default: "todo")
- `due_date`: Optional due date
- `createdAt`: Automatic timestamp on creation
- Reverse relations: `tasks` (via project), `assigned_tasks` (via user)

## Admin Integration

All models are registered with Django's admin interface for easy data management:

- User model: Full CRUD with custom display
- Project model: Manage projects with owner filtering
- Task model: Task management with project and assignee relations

Access admin at `/admin/` after creating a superuser.

## Django REST Framework Integration

DRF is configured with JWT authentication:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "AUTH_HEADER_TYPES": ("Bearer",),
}
```

### Serializers

Model-based serializers for API data validation:

```python
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
```

## API Views

DRF ModelViewSets provide automatic CRUD operations:

```python
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

**Supported Operations:**
- `list`: GET all items
- `retrieve`: GET single item by ID
- `create`: POST new item
- `update`: PUT/PATCH existing item
- `destroy`: DELETE item

## Routing

Uses DRF DefaultRouter for automatic URL generation:

```python
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
urlpatterns = router.urls
```

**Generated Endpoints:**
- `GET/POST /api/projects/` - List/Create projects
- `GET/PUT/PATCH/DELETE /api/projects/{id}/` - Retrieve/Update/Delete project
- `GET/POST /api/tasks/` - List/Create tasks
- `GET/PUT/PATCH/DELETE /api/tasks/{id}/` - Retrieve/Update/Delete task

## Authentication System

### Registration
Custom registration endpoint using DRF generics:

```python
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
```

**Serializer:**
```python
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
```

### JWT Authentication
Integrated with `djangorestframework-simplejwt`:

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - Obtain access/refresh tokens
- `POST /api/auth/refresh/` - Refresh access token

## Security

- JWT Bearer token authentication required for protected endpoints
- `request.user` automatically available in authenticated views
- Password hashing handled by Django's auth system
- CSRF protection enabled for admin interface

## Database

SQLite database with migrations for all models:

- `db.sqlite3` - Main database file
- Migrations in each app's `migrations/` directory
- Foreign key relationships with proper cascade/delete behavior

## Development Utilities

- Django admin dashboard at `/admin/`
- DRF browsable API for testing endpoints
- SQLite database browser support
- Debug mode enabled for development

## API Documentation

### Authentication Endpoints

#### Register User
```
POST /api/auth/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
}
```

Response:
```json
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
}
```

#### Login
```
POST /api/auth/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "securepassword123"
}
```

Response:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Refresh Token
```
POST /api/auth/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Project Endpoints

#### List Projects
```
GET /api/projects/
Authorization: Bearer <access_token>
```

#### Create Project
```
POST /api/projects/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "My Project",
    "description": "Project description"
}
```

#### Get Project
```
GET /api/projects/{id}/
Authorization: Bearer <access_token>
```

#### Update Project
```
PUT /api/projects/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Updated Project",
    "description": "Updated description"
}
```

#### Delete Project
```
DELETE /api/projects/{id}/
Authorization: Bearer <access_token>
```

### Task Endpoints

#### List Tasks
```
GET /api/tasks/
Authorization: Bearer <access_token>
```

#### Create Task
```
POST /api/tasks/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "My Task",
    "description": "Task description",
    "project": 1,
    "assigned_to": 1,
    "status": "todo",
    "due_date": "2026-12-31"
}
```

#### Update Task Status
```
PATCH /api/tasks/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "status": "in_progress"
}
```

## Current API Capabilities

- ✅ User registration and JWT authentication
- ✅ Token refresh functionality
- ✅ Full CRUD operations for projects
- ✅ Full CRUD operations for tasks
- ✅ Task assignment and status tracking
- ✅ Admin-based data management
- ✅ Automatic API documentation via DRF

## Architecture

```
Client Request
    ↓
HTTP Request → Django URL Router
    ↓
ViewSet (ModelViewSet)
    ↓
Serializer (ModelSerializer)
    ↓
Model (Django Model)
    ↓
Database (SQLite/PostgreSQL)
    ↓
Response ← JSON Response
```

**Data Flow:**
1. Client sends HTTP request with JWT token
2. Django routes to appropriate ViewSet
3. ViewSet uses Serializer for validation/serialization
4. Serializer interacts with Model
5. Model queries/updates database
6. Response serialized back to JSON

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd glide
   ```

2. **Create virtual environment**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install Django djangorestframework djangorestframework-simplejwt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/api/`

## Usage

### Development
- Access Django admin at `http://127.0.0.1:8000/admin/`
- API endpoints at `http://127.0.0.1:8000/api/`
- Use tools like Postman or curl for API testing
- DRF browsable API available for interactive testing

### Authentication
1. Register a new user via `/api/auth/register/`
2. Login to get JWT tokens via `/api/auth/login/`
3. Include `Authorization: Bearer <access_token>` in API requests
4. Refresh tokens as needed via `/api/auth/refresh/`

### Example Workflow
1. Register/Login to get authentication token
2. Create a project
3. Add tasks to the project
4. Assign tasks to users
5. Update task statuses as work progresses

## Contributing

1. Follow Django and DRF best practices
2. Write tests for new features
3. Update documentation for API changes
4. Use meaningful commit messages

## License

This project is licensed under the MIT License.