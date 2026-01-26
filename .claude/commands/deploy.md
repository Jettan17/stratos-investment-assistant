---
description: Docker and Kubernetes deployment setup. Containerize applications with production best practices.
---

# /deploy - Deployment Setup

Set up Docker and Kubernetes deployment for the application.

## Deployment Options

### Docker
- Dockerfile creation
- Docker Compose setup
- Multi-stage builds
- Health checks

### Kubernetes
- Deployment manifests
- Service configuration
- ConfigMaps and Secrets
- Ingress setup

## Dockerfile Template

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

## Docker Compose Template

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Best Practices

| Do | Don't |
|----|-------|
| ✅ Multi-stage builds | ❌ Copy everything in one layer |
| ✅ Non-root user | ❌ Run as root |
| ✅ Health checks | ❌ Skip health checks |
| ✅ Pin version tags | ❌ Use :latest in production |
| ✅ Use secrets | ❌ Hardcode credentials |

## Execution

When running /deploy:

1. Detect project type (Python, Node.js, etc.)
2. Create appropriate Dockerfile
3. Set up Docker Compose if needed
4. Add health check endpoints
5. Create .dockerignore
6. Optionally create Kubernetes manifests
7. Document deployment process

## Agent Escalation

This command automatically escalates to specialized agents when:

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Production deployment | **deployment-specialist** | Full production configuration, security hardening |
| Kubernetes setup | **deployment-specialist** | K8s manifests, Helm charts, scaling strategies |
| Multi-environment | **deployment-specialist** | Dev/staging/prod environment management |

### Escalation Triggers
- **deployment-specialist**: Use for production deployments, complex orchestration, CI/CD pipelines, or when security hardening is required
