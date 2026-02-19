# CLI Commands

Flet-Easy provides a powerful command-line interface (CLI) to streamline development workflows. The CLI helps you create project structures, manage dependencies, and automate common tasks.

## Overview

The Flet-Easy CLI (`fs`) offers:

- **Project Scaffolding**: Create new projects with MVC structure
- **Template Management**: Use pre-built project templates
- **Development Tools**: Utilities for building and testing
- **Code Generation**: Generate boilerplate code automatically

## Installation

The CLI is automatically installed with Flet-Easy when using the full installation:

```bash
pip install flet-easy[all] --upgrade
```

Or install just the CLI dependencies:

```bash
pip install flet-easy cookiecutter rich-argparse
```

## Basic Usage

### Check Version

```bash
fs --version
# or
fs -v
```

### Get Help

```bash
fs --help
```

## Commands

### `fs init` - Create New Project

Create a new Flet-Easy project with a complete MVC structure.

**Syntax:**

```bash
fs init
# or
fs i
```

**Interactive Setup:**
When you run `fs init`, you'll be prompted for:

1. **Project Name**: The name of your project directory
2. **App Name**: The main application name
3. **Author**: Your name or organization
4. **Description**: Brief project description
5. **License**: Choose from common licenses (MIT, Apache, etc.)
6. **Python Version**: Minimum Python version requirement

**Example Session:**

```bash
$ fs init
[1/6] Project name (my-flet-app): todo-app
[2/6] App name (TodoApp): Task Manager
[3/6] Author (Your Name): John Doe
[4/6] Description: A simple task management application
[5/6] License [MIT]: MIT
[6/6] Python version (3.8): 3.9

✅ Project created successfully!
📁 Project location: ./todo-app/
```

**Generated Project Structure:**

```
todo-app/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py              # Main application entry
│       ├── config.py            # Configuration settings
│       ├── controllers/         # Route handlers
│       │   ├── __init__.py
│       │   ├── home.py
│       │   └── auth.py
│       ├── models/              # Data models
│       │   ├── __init__.py
│       │   └── user.py
│       ├── views/               # Page views
│       │   ├── __init__.py
│       │   ├── home.py
│       │   ├── login.py
│       │   └── dashboard.py
│       ├── middleware/          # Custom middleware
│       │   ├── __init__.py
│       │   └── auth.py
│       ├── utils/               # Utility functions
│       │   ├── __init__.py
│       │   └── helpers.py
│       └── static/              # Static assets
│           ├── css/
│           ├── js/
│           └── images/
├── tests/                       # Test files
│   ├── __init__.py
│   ├── test_controllers.py
│   └── test_models.py
├── docs/                        # Documentation
│   └── README.md
├── requirements.txt             # Dependencies
├── pyproject.toml              # Project configuration
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment variables template
└── README.md                   # Project documentation
```

## Generated Files Explained

### `src/app/main.py`

The main application entry point:

```python
import flet as ft
import flet_easy as fs
from pathlib import Path

from app.config import Config
from app.controllers import register_routes

# Initialize FletEasy app
app = fs.FletEasy(
    route_prefix=Config.ROUTE_PREFIX,
    route_init=Config.ROUTE_INIT,
    route_login=Config.ROUTE_LOGIN,
    secret_key=fs.SecretKey(Config.SECRET_KEY),
    auto_logout=Config.AUTO_LOGOUT,
    path_views=Path("app/views"),
    logger=Config.DEBUG
)

# Register all routes
register_routes(app)

# Configure global view
@app.view
def main_view(data: fs.Datasy):
    return fs.Viewsy(
        appbar=ft.AppBar(
            title=ft.Text(Config.APP_NAME),
            bgcolor=ft.Colors.BLUE,
            actions=[
                ft.IconButton(
                    ft.Icons.HOME,
                    on_click=data.go(data.route_init)
                )
            ]
        ),
        bgcolor=ft.Colors.GREY_50,
        padding=ft.padding.all(20)
    )

# Authentication handler
@app.login
def check_auth(data: fs.Datasy):
    token = data.page.client_storage.get("auth_token")
    return token is not None

if __name__ == "__main__":
    app.run(
        view=ft.AppView.WEB_BROWSER,
        port=Config.PORT,
        host=Config.HOST
    )
```

### `src/app/config.py`

Configuration management:

```python
import os
from pathlib import Path

class Config:
    """Application configuration"""
    
    # App Settings
    APP_NAME = "Task Manager"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server Settings
    HOST = os.getenv("HOST", "localhost")
    PORT = int(os.getenv("PORT", 8000))
    
    # Route Settings
    ROUTE_PREFIX = os.getenv("ROUTE_PREFIX", "")
    ROUTE_INIT = os.getenv("ROUTE_INIT", "/")
    ROUTE_LOGIN = os.getenv("ROUTE_LOGIN", "/login")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    AUTO_LOGOUT = os.getenv("AUTO_LOGOUT", "True").lower() == "true"
    
    # Database (if using)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    STATIC_DIR = BASE_DIR / "app" / "static"
```

### `src/app/controllers/home.py`

Example controller:

```python
import flet as ft
import flet_easy as fs

def register_home_routes(app: fs.FletEasy):
    """Register home-related routes"""
    
    @app.page("/", title="Home")
    def home_page(data: fs.Datasy):
        return ft.View(
            "/",
            controls=[
                ft.Text("Welcome to Task Manager!", size=30),
                ft.Text("Manage your tasks efficiently", size=16),
                ft.ElevatedButton(
                    "Get Started",
                    on_click=data.go("/dashboard")
                ),
                ft.ElevatedButton(
                    "Login",
                    on_click=data.go("/login")
                )
            ],
            appbar=data.view.appbar,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    @app.page("/about", title="About")
    def about_page(data: fs.Datasy):
        return ft.View(
            "/about",
            controls=[
                ft.Text("About Task Manager", size=24),
                ft.Text(
                    "A simple and efficient task management application "
                    "built with Flet-Easy framework.",
                    size=14
                ),
                ft.ElevatedButton(
                    "← Back to Home",
                    on_click=data.go("/")
                )
            ],
            appbar=data.view.appbar
        )
```

### `src/app/controllers/__init__.py`

Route registration:

```python
from .home import register_home_routes
from .auth import register_auth_routes

def register_routes(app):
    """Register all application routes"""
    register_home_routes(app)
    register_auth_routes(app)
```

### `src/app/models/user.py`

Example data model:

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    """User data model"""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    created_at: Optional[datetime] = None
    is_active: bool = True
    
    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create user from dictionary"""
        return cls(
            id=data.get("id"),
            username=data.get("username", ""),
            email=data.get("email", ""),
            password_hash=data.get("password_hash", ""),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            is_active=data.get("is_active", True)
        )
```

### `src/app/middleware/auth.py`

Authentication middleware:

```python
import flet_easy as fs

class AuthMiddleware(fs.MiddlewareRequest):
    """Authentication middleware"""
    
    def before_request(self):
        """Check authentication before request"""
        # Skip auth check for public routes
        public_routes = ["/", "/login", "/register", "/about"]
        
        if self.data.route in public_routes:
            return None
        
        # Check if user is authenticated
        auth_token = self.data.page.client_storage.get("auth_token")
        if not auth_token:
            return fs.Redirect("/login")
        
        # Validate token (implement your validation logic)
        if not self._validate_token(auth_token):
            self.data.logout("auth_token")
            return fs.Redirect("/login")
        
        return None
    
    def after_request(self):
        """Log request after processing"""
        user_id = self.data.page.client_storage.get("user_id", "anonymous")
        print(f"User {user_id} accessed {self.data.route}")
    
    def _validate_token(self, token: str) -> bool:
        """Validate authentication token"""
        # Implement your token validation logic here
        # This is a placeholder implementation
        try:
            # Example: decode JWT token
            # decoded = fs.decode(token, secret_key)
            # return decoded is not None
            return len(token) > 10  # Placeholder validation
        except Exception:
            return False
```

### `requirements.txt`

Project dependencies:

```txt
flet>=0.25.0
flet-easy>=0.2.8
python-dotenv>=1.0.0
pydantic>=2.0.0
sqlalchemy>=2.0.0
alembic>=1.12.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.0.0
flake8>=6.0.0
```

### `pyproject.toml`

Project configuration:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "task-manager"
version = "0.1.0"
description = "A simple task management application"
authors = [{name = "John Doe", email = "john@example.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "flet>=0.25.0",
    "flet-easy>=0.2.8",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
]

[project.scripts]
task-manager = "app.main:main"

[tool.black]
line-length = 88
target-version = ["py39"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

## Development Workflow

### Create Project

```bash
fs init
cd my-project
```

### Set Up Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
# Update SECRET_KEY, DATABASE_URL, etc.
```

### Run Application

```bash
python src/app/main.py
```

### Run Tests

```bash
pytest tests/
```

## Advanced Usage

### Custom Templates

You can create custom project templates by forking the default template repository:

```bash
# Use custom template
fs init --template https://github.com/yourusername/custom-flet-template
```

### Environment Variables

The generated project supports environment-based configuration:

```bash
# .env file
DEBUG=True
HOST=0.0.0.0
PORT=8080
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
ROUTE_PREFIX=/api/v1
```

### Docker Support

Add Docker support to your generated project:

**Dockerfile:**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY .env .

EXPOSE 8080

CMD ["python", "src/app/main.py"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DEBUG=False
      - HOST=0.0.0.0
      - PORT=8080
    volumes:
      - ./src:/app/src
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: taskmanager
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## Best Practices

### **Project Structure**

- Keep controllers focused on routing logic
- Use models for data structures and validation
- Implement business logic in separate service classes
- Use middleware for cross-cutting concerns

### **Configuration Management**

- Use environment variables for sensitive data
- Provide sensible defaults in config.py
- Document all configuration options

### **Security**

- Change default SECRET_KEY in production
- Use environment variables for secrets
- Implement proper authentication middleware
- Validate all user inputs

### **Testing**

- Write tests for all controllers
- Test middleware functionality
- Use fixtures for common test data
- Implement integration tests

### **Documentation**

- Update README.md with project-specific information
- Document API endpoints
- Include setup and deployment instructions
- Maintain changelog for releases

## Troubleshooting

### Common Issues

**1. Import Errors**

```bash
# Ensure you're in the correct directory
cd src/
python -m app.main

# Or add src to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:./src"
python app/main.py
```

**2. Missing Dependencies**

```bash
# Install all dependencies including optional ones
pip install flet-easy[all] --upgrade

# Or install specific CLI dependencies
pip install cookiecutter rich-argparse
```

**3. Template Download Issues**

```bash
# Clear cookiecutter cache
rm -rf ~/.cookiecutter_replay/

# Use specific template version
fs init --checkout v1.0.0
```

**4. Port Already in Use**

```bash
# Change port in .env file
PORT=8081

# Or set environment variable
export PORT=8081
python src/app/main.py
```

### Getting Help

- Check the [GitHub Issues](https://github.com/Daxexs/flet-easy/issues)
- Read the [documentation](https://daxexs.github.io/flet-easy/)
- Join the community discussions

The Flet-Easy CLI streamlines project creation and follows industry best practices for Python application structure. Use it to quickly bootstrap new projects and maintain consistency across your Flet-Easy applications.
