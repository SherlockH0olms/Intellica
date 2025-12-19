# Contributing to Intellica

Thank you for your interest in contributing to Intellica! This document provides guidelines for contributing to the project.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Commit Guidelines](#commit-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Testing](#testing)

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:
- Be respectful and professional
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards others

---

## Getting Started

### Prerequisites
- Docker 24+
- Docker Compose 2.0+
- Git
- (Optional) Python 3.11+, Node.js 18+ for local development

### Fork and Clone

```bash
# Fork the repository on GitHub

# Clone your fork
git clone https://github.com/YOUR_USERNAME/Intellica.git
cd Intellica

# Add upstream remote
git remote add upstream https://github.com/SherlockH0olms/Intellica.git
```

### Setup Development Environment

```bash
# Copy environment variables
cp .env.example .env

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f backend
```

---

## Development Workflow

### 1. Create a Feature Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the [Coding Standards](#coding-standards) section below.

### 3. Test Your Changes

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
cd frontend && npm test

# Linting
docker-compose exec backend flake8
cd frontend && npm run lint
```

### 4. Commit Your Changes

Follow the [Commit Guidelines](#commit-guidelines) section.

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## Coding Standards

### Python (Backend)

**Style Guide**: PEP 8

```python
# Good
def calculate_anomaly_score(sensor_data: dict) -> float:
    """
    Calculate anomaly score using Isolation Forest.
    
    Args:
        sensor_data: Dictionary containing sensor readings
        
    Returns:
        Anomaly score (float)
    """
    # Implementation
    return score

# Bad
def calc(d):
    # No docstring, unclear naming
    return d['score']
```

**Tools**:
- `black` for formatting
- `flake8` for linting
- `mypy` for type checking

### TypeScript (Frontend)

**Style Guide**: Airbnb TypeScript Style Guide

```typescript
// Good
interface SensorData {
  timestamp: string;
  machineId: string;
  sensors: Record<string, number>;
}

const fetchSensorData = async (machineId: string): Promise<SensorData> => {
  const response = await api.get(`/machines/${machineId}/sensors`);
  return response.data;
};

// Bad
function getData(id) {
  // No types, unclear naming
  return api.get('/data/' + id);
}
```

**Tools**:
- `eslint` for linting
- `prettier` for formatting

### SQL

```sql
-- Good: Clear, readable
SELECT 
    m.name AS machine_name,
    AVG(sd.value) AS avg_temperature
FROM machines m
JOIN sensor_data sd ON m.id = sd.machine_id
WHERE sd.sensor_name = 'temperature'
  AND sd.time > NOW() - INTERVAL '1 hour'
GROUP BY m.name
ORDER BY avg_temperature DESC;

-- Bad: Hard to read
select m.name,avg(sd.value) from machines m join sensor_data sd on m.id=sd.machine_id where sd.sensor_name='temperature' group by m.name;
```

---

## Commit Guidelines

We follow **Conventional Commits** specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```bash
# Feature
git commit -m "feat(ml): add defect detection model"

# Bug fix
git commit -m "fix(api): resolve sensor data timestamp issue"

# Documentation
git commit -m "docs(readme): update installation instructions"

# With body
git commit -m "feat(dashboard): add real-time alerts feed

Implemented WebSocket connection for live alerts.
Added visual notifications with severity indicators.

Closes #123"
```

---

## Pull Request Process

### Before Submitting

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Run all tests** and ensure they pass
4. **Update CHANGELOG.md** if applicable
5. **Ensure no merge conflicts** with main branch

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No new warnings

## Screenshots (if applicable)

## Related Issues
Closes #XXX
```

### Review Process

1. **Automated checks** run (CI/CD)
2. **Code review** by maintainers
3. **Address feedback** if requested
4. **Approval** from at least one maintainer
5. **Merge** (squash and merge preferred)

---

## Testing

### Backend Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run specific test file
docker-compose exec backend pytest tests/test_api.py

# With coverage
docker-compose exec backend pytest --cov=. --cov-report=html
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

### Writing Tests

**Backend (pytest)**:
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

**Frontend (Jest)**:
```typescript
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Intellica heading', () => {
  render(<App />);
  const heading = screen.getByText(/Intellica/i);
  expect(heading).toBeInTheDocument();
});
```

---

## Documentation

### Code Comments

- **Python**: Use docstrings (Google style)
- **TypeScript**: Use JSDoc comments
- Focus on **why**, not **what**

### Documentation Files

- **README.md**: Project overview, quickstart
- **ARCHITECTURE.md**: System design
- **API_DOCUMENTATION.md**: API reference
- **USER_GUIDE.md**: End-user documentation

---

## Questions?

If you have questions:
1. Check existing [Issues](https://github.com/SherlockH0olms/Intellica/issues)
2. Search [Discussions](https://github.com/SherlockH0olms/Intellica/discussions)
3. Create a new issue with the "question" label

---

Thank you for contributing to Intellica! 🚀