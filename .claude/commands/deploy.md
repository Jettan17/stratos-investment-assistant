---
description: Deploy applications to Docker, Kubernetes, Vercel, Railway, and other platforms.
ecc_base_version: "5230892"
last_synced: "2026-01-27"
customizations: "Added Vercel, Railway, Fly.io, Cloudflare targets"
---

# /deploy - Deployment Setup

Set up deployment for the application across multiple platforms.

## Usage

```bash
/deploy                 # Auto-detect best deployment target
/deploy docker          # Docker/Docker Compose setup
/deploy kubernetes      # Kubernetes manifests
/deploy vercel          # Vercel deployment
/deploy railway         # Railway deployment
/deploy fly             # Fly.io deployment
/deploy cloudflare      # Cloudflare Workers/Pages
```

---

## Deployment Targets

### Docker (Self-hosted)
- Dockerfile creation
- Docker Compose setup
- Multi-stage builds
- Health checks
- Non-root user security

### Kubernetes (Self-hosted)
- Deployment manifests
- Service configuration
- ConfigMaps and Secrets
- Ingress setup
- Helm charts (optional)

### Vercel (Recommended for Next.js)
- `vercel.json` configuration
- Environment variables setup
- Preview deployments
- Edge functions
- Serverless functions

### Railway
- `railway.toml` configuration
- Database provisioning
- Environment variables
- Health checks
- Auto-scaling

### Fly.io
- `fly.toml` configuration
- Multi-region deployment
- Scaling configuration
- Secrets management

### Cloudflare
- `wrangler.toml` for Workers
- Pages deployment
- KV/D1 database setup
- R2 storage configuration

---

## Auto-Detection

When running `/deploy` without arguments, the command auto-detects:

| Project Type | Recommended Target |
|--------------|-------------------|
| Next.js | Vercel |
| Static site (Astro, Hugo) | Vercel or Cloudflare Pages |
| Node.js API | Railway or Fly.io |
| Python/FastAPI | Railway or Docker |
| Full-stack with DB | Railway (has DB) or Docker |
| Microservices | Kubernetes |

---

## Docker Template

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

---

## Vercel Configuration

```json
// vercel.json
{
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "DATABASE_URL": "@database-url"
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store" }
      ]
    }
  ]
}
```

---

## Railway Configuration

```toml
# railway.toml
[build]
builder = "nixpacks"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "on_failure"

[service]
internalPort = 3000
```

---

## Best Practices

| Do | Don't |
|----|-------|
| Multi-stage builds | Copy everything in one layer |
| Non-root user | Run as root |
| Health checks | Skip health checks |
| Pin version tags | Use :latest in production |
| Use secrets | Hardcode credentials |
| Environment variables | Commit .env files |

---

## Execution

When running /deploy:

1. Detect project type (Next.js, Python, Node.js, etc.)
2. Recommend deployment target
3. Create configuration files for chosen platform
4. Set up health check endpoints
5. Create .dockerignore / .vercelignore as needed
6. Configure environment variables
7. Document deployment process

---

## Arguments

| Argument | Target Platform |
|----------|-----------------|
| *(none)* | Auto-detect best platform |
| `docker` | Docker/Docker Compose |
| `kubernetes` | Kubernetes manifests |
| `vercel` | Vercel |
| `railway` | Railway |
| `fly` | Fly.io |
| `cloudflare` | Cloudflare Workers/Pages |

---

## Examples

```bash
# Auto-detect for Next.js project
/deploy
# → Recommends Vercel, creates vercel.json

# Explicit Docker setup
/deploy docker
# → Creates Dockerfile, docker-compose.yml

# Railway for full-stack app
/deploy railway
# → Creates railway.toml, provisions DB
```

---

## Agent Escalation

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Production deployment | **deployment-specialist** | Security hardening, scaling |
| Kubernetes setup | **deployment-specialist** | K8s manifests, Helm charts |
| Multi-environment | **deployment-specialist** | Dev/staging/prod management |
| CI/CD pipelines | **deployment-specialist** | GitHub Actions, GitLab CI |

---

## Related Commands

- `/verify` - Run verification before deployment
- `/code-review` - Review before deploying
- `/tdd` - Ensure tests pass before deploy
