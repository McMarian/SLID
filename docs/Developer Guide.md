# Developer Guide

## Introduction

Welcome to the SLID development team! This guide will help you understand our development workflow, code style guidelines, testing procedures, and contribution process. SLID is built as a Django web application with AI capabilities for unified social media management.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.9+
- PostgreSQL 14+
- Git
- Docker and Docker Compose (optional, but recommended)

### Setting Up Your Development Environment

1. **Clone the repository**

   ```bash
   git clone https://github.com/McMarian/SLID.git
   cd SLID
   ```

2. **Set up a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:

   ```
   DATABASE_URL=postgres://username:password@localhost:5432/slid
   OPENAI_API_KEY=your_openai_api_key
   INSTAGRAM_CLIENT_ID=your_instagram_client_id
   INSTAGRAM_CLIENT_SECRET=your_instagram_client_secret
   FACEBOOK_CLIENT_ID=your_facebook_client_id
   FACEBOOK_CLIENT_SECRET=your_facebook_client_secret
   ```

5. **Initialize the database**

   ```bash
   python manage.py migrate
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

### Using Docker for Development

Alternatively, you can use Docker for development:

```bash
docker-compose up
```

This will set up the entire development environment, including the database.

## Project Structure

SLID follows a modular Django app structure:

```
SLID/
├── SLID/               # Project settings and configuration
├── userauth/           # User authentication and profiles
├── oauth_integration/  # Social media OAuth connections
├── profile_management/ # User profile and connection management
├── content_management/ # Content creation and management
├── static/             # Static files (CSS, JS, images)
├── docs/               # Documentation
├── tests/              # Tests
└── manage.py           # Django management script
```

## Code Style Guidelines

### Python Style Guide

We follow PEP 8 with a few adjustments:

- **Line length**: Maximum 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Naming conventions**:
  - Classes: `PascalCase`
  - Functions and variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private methods and variables: `_leading_underscore`
- **Docstrings**: Use the Google style for docstrings
- **Imports**: Group imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application imports
  4. Sort imports alphabetically within each group

### Django-Specific Guidelines

- **Model names**: Singular `PascalCase` (e.g., `UserProfile` not `UserProfiles`)
- **Field names**: `snake_case`
- **URL names**: `snake_case`
- **Template names**: `snake_case.html`
- **View names**: End with `View` for class-based views (e.g., `ProfileView`)

### Example Code Style

```python
import os
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from .utils import generate_unique_code


class UserProfile(models.Model):
    """
    Extends the User model with additional profile information.
    
    Attributes:
        user (ForeignKey): One-to-one relationship with User model
        full_name (str): User's full name
        profile_picture (ImageField): User's profile picture
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    
    def generate_qr_code(self):
        """
        Generate a QR code for the user profile.
        
        Returns:
            str: Path to the generated QR code image
        """
        # Implementation here
        return path_to_qr_code
```

## Testing Procedures

### Testing Framework

SLID uses pytest for testing. We aim for high test coverage and require tests for all new features.

### Running Tests

To run the full test suite:

```bash
python run_all_tests.py
```

To run a specific test file:

```bash
pytest test_user_auth.py
```

### Test Structure

Our tests are organized into the following categories:

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test interactions between components
3. **Functional Tests**: Test complete features from user perspective
4. **System Tests**: Test the entire system workflow

### Writing Tests

When writing tests:

1. Use descriptive test names that explain what's being tested
2. Follow the Arrange-Act-Assert pattern
3. Keep tests independent of each other
4. Mock external services (social media APIs, etc.)
5. Test both success and failure cases

#### Example Test

```python
import pytest
from django.contrib.auth.models import User
from userauth.models import UserProfile

@pytest.mark.django_db
def test_user_profile_creation():
    """Test that a UserProfile is created for a new user."""
    # Arrange
    user = User.objects.create(username="testuser", password="password123")
    
    # Act
    profile = UserProfile.objects.create(user=user, full_name="Test User")
    
    # Assert
    assert profile.user == user
    assert profile.full_name == "Test User"
    assert UserProfile.objects.count() == 1
```

### Test Coverage

We use coverage.py to measure test coverage. Aim for at least 80% coverage for new code.

To generate a coverage report:

```bash
coverage run -m pytest
coverage report
coverage html  # For a detailed HTML report
```

## Contribution Guidelines

### Git Workflow

We follow a feature branch workflow:

1. Create a new branch for each feature or bugfix
   ```bash
   git checkout -b feature/feature-name
   ```
   or
   ```bash
   git checkout -b fix/bug-description
   ```

2. Make your changes, commit frequently with clear messages
   ```bash
   git commit -m "Add user profile QR code generation"
   ```

3. Push your branch and create a pull request
   ```bash
   git push -u origin feature/feature-name
   ```

4. After review and approval, your branch will be merged

### Commit Messages

Follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor" not "Moves cursor")
- Limit the first line to 72 characters
- Reference issues in the description, not the title

Example:
```
Add QR code generation for user profiles

- Implement QR code generation using qrcode library
- Add tests for the generation function
- Update profile view to include QR code

Fixes #123
```

### Pull Request Process

1. Update the documentation with details of your changes
2. Add tests for your changes and ensure all tests pass
3. Update the README.md or other docs if needed
4. Your PR needs approval from at least one maintainer
5. Once approved, a maintainer will merge your PR

### Code Review Guidelines

During code reviews, focus on:

- Code quality and adherence to style guidelines
- Test coverage and quality
- Documentation completeness
- Performance considerations
- Security implications

Be respectful and constructive in code reviews.

## Debugging and Troubleshooting

### Common Issues

1. **Database connection issues**
   - Check your PostgreSQL service is running
   - Verify DATABASE_URL in your .env file
   - Ensure the database exists and your user has proper permissions

2. **OAuth integration problems**
   - Verify your client IDs and secrets
   - Check redirect URIs are properly configured
   - Look for HTTPS requirements in development

3. **AI integration issues**
   - Ensure your OpenAI API key is valid
   - Check for rate limiting issues
   - Review the enhanced query format

### Debugging Tools

- Django Debug Toolbar for analyzing database queries and performance
- Python debugger (pdb) for stepping through code
- Django logging for capturing errors

## Documentation

### Documentation Standards

All code should be documented following these guidelines:

1. **Docstrings**: All modules, classes, and functions should have docstrings
2. **README**: Update the README.md when adding new features
3. **API documentation**: Update the API Reference when changing endpoints
4. **User guides**: Update user documentation for user-facing changes

### Building Documentation

We use MkDocs for documentation. To build and serve docs locally:

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

## Conclusion

Thank you for contributing to SLID! By following these guidelines, you'll help maintain a high-quality codebase that's easy to work with. If you have any questions, don't hesitate to reach out to the core development team.

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [pytest Documentation](https://docs.pytest.org/)
- [PEP 8 Style Guide](https://pep8.org/)
- [SLID API Reference](./API%20Reference.md) 