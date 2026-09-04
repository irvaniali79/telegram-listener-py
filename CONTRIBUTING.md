# Contributing to Telegram Listener

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip or conda for package management

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/irvaniali79/telegram-listener-py.git
cd telegram-listener-py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-feature
# or for bug fixes:
git checkout -b fix/issue-description
```

### 2. Make Your Changes

- Write clean, readable code
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Include type hints

### 3. Write Tests

Add tests for any new functionality:

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=telegram_listener --cov-report=html
```

### 4. Code Quality

```bash
# Format code
black telegram_listener/ tests/ examples/

# Lint
flake8 telegram_listener/ tests/ examples/

# Type checking
mypy telegram_listener/
```

### 5. Commit Messages

Write clear, descriptive commit messages:

```
feat: Add support for message reactions

- Implement ReactionEvent dataclass
- Update MessageEvent with reactions field
- Add on_reaction callback to ChatListener

Closes #42
```

**Format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style (formatting, missing semicolons, etc)
- `refactor:` - Code refactoring without feature changes
- `test:` - Adding tests
- `chore:` - Dependency updates, build changes

### 6. Push and Create Pull Request

```bash
git push origin feature/my-feature
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Link to related issues
- Reference to any breaking changes

## Pull Request Guidelines

### Before Submitting

- [ ] Tests pass: `pytest tests/`
- [ ] Code formatted: `black telegram_listener/`
- [ ] No linting issues: `flake8 telegram_listener/`
- [ ] Type checking passes: `mypy telegram_listener/`
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)

### PR Title Format

```
[TYPE] Short description (50 chars max)
```

Examples:
- `[FEATURE] Add support for message reactions`
- `[FIX] Handle connection timeout gracefully`
- `[DOCS] Update API reference`

### PR Description Template

```markdown
## Description
Brief explanation of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #(issue number)

## Testing
How was this tested?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Code reviewed
```

## Testing

### Writing Tests

Place tests in `tests/` directory:

```python
import pytest
from telegram_listener import ChatListener

class TestMyFeature:
    """Test my new feature."""
    
    def test_something(self):
        """Test description."""
        # Arrange
        listener = ChatListener(chat_id=123456789)
        
        # Act
        result = listener.some_method()
        
        # Assert
        assert result is True
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_client.py

# Run specific test
pytest tests/test_client.py::TestChatListener::test_init_valid

# Run with coverage
pytest --cov=telegram_listener --cov-report=term-missing

# Run with verbose output
pytest -v
```

### Test Coverage

Aim for at least 80% coverage. Check with:

```bash
pytest --cov=telegram_listener --cov-report=html
# Open htmlcov/index.html in browser
```

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """Brief description.
    
    Longer description explaining what the function does,
    any important notes, and usage examples.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is wrong
        
    Example:
        >>> result = my_function("test", 42)
        >>> print(result)
        True
    """
    pass
```

### Updating README

If adding user-facing features, update README.md with:
- Feature description
- Usage example
- New API documentation

### Updating CHANGELOG

Add entry to top of `CHANGELOG.md` for each release:

```markdown
## [Unreleased]

### Added
- New feature description

### Fixed
- Bug fix description

### Changed
- API change description
```

## Areas for Contribution

### High Priority

- [ ] Bidirectional messaging (send messages from Python)
- [ ] Media file handling and downloads
- [ ] Reaction event support
- [ ] Typing indicator detection
- [ ] User presence tracking
- [ ] Message history queries

### Medium Priority

- [ ] Rich message formatting (Markdown/HTML)
- [ ] Message forwarding
- [ ] Pinned message tracking
- [ ] Forum topic support
- [ ] Performance optimizations

### Nice to Have

- [ ] Plugin system
- [ ] Message filtering/routing
- [ ] Async/await support
- [ ] Rate limiting per chat
- [ ] Replay/debug mode

## Reporting Issues

### Bug Reports

Include:
- Python version
- Telegram Desktop version
- Minimal reproduction case
- Expected vs actual behavior
- Error message and traceback

### Feature Requests

Include:
- Use case / motivation
- Proposed API / design
- Examples
- Alternatives considered

## Style Guide

### Code Style

- Use `black` for formatting (line length: 88)
- Follow PEP 8
- Use type hints
- Use meaningful variable names

### Naming Conventions

```python
# Constants
MAX_RETRIES = 3
DEFAULT_PORT = 9000

# Functions/methods
def register_listener(chat_id: int) -> None:
    pass

# Classes
class ChatListener:
    pass

# Private methods/attributes
def _internal_method(self):
    pass

self._private_attr = value
```

### Import Order

```python
# 1. Standard library
import json
import socket
import threading

# 2. Third-party
import pytest

# 3. Local
from .events import MessageEvent
from .exceptions import TelegramListenerError
```

## Git Workflow

### Keeping Fork Updated

```bash
# Add upstream remote
git remote add upstream https://github.com/irvaniali79/telegram-listener-py.git

# Fetch upstream
git fetch upstream

# Rebase your branch
git rebase upstream/main
```

### Before Final Push

```bash
# Ensure you're on feature branch
git checkout feature/my-feature

# Rebase on latest main
git rebase main

# Interactive rebase to clean up commits (optional)
git rebase -i main

# Force push if rebased
git push -f origin feature/my-feature
```

## Review Process

1. **Automated Checks**: Tests, linting, and type checking must pass
2. **Code Review**: At least one maintainer review
3. **Feedback**: Address any requested changes
4. **Approval**: Get approval from maintainers
5. **Merge**: Squash and merge to main branch

## Release Process

Maintainers handle releases:

1. Update version in `setup.py` and `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v0.2.0`
4. Push tag: `git push origin v0.2.0`
5. Build and publish to PyPI

## Questions?

- Open an issue on GitHub
- Check existing discussions
- Email: irvaniali79@gmail.com

## License

By contributing, you agree your code will be licensed under MIT License.

Thank you for contributing! 🎉
