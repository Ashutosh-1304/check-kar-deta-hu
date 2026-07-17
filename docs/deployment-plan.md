# Deployment Plan

This document outlines the deployment architecture for the Document Compliance Platform, targeting a containerized, cloud-agnostic approach.

## 1. Containerization
The entire stack is containerized using Docker to ensure consistency across development, staging, and production environments.

- **Frontend Image**: Multi-stage Dockerfile. Builds the Next.js static bundle and runs it via a lightweight Node.js alpine image.
- **Backend Image**: Python 3.12 slim image. Installs dependencies and runs FastAPI via Uvicorn.
- **Database Image**: Official PostgreSQL image.

## 2. Local Development & Staging
- Orchestrated via `docker-compose.yml`.
- Boots the Frontend, Backend, and PostgreSQL database with a single command (`docker-compose up`).
- Mounts local volumes for hot-reloading (Frontend/Backend).

## 3. Production Architecture

### A. Reverse Proxy / Web Server
- **Nginx** will act as the edge server and reverse proxy.
- Responsibilities:
  - Terminating SSL (HTTPS).
  - Serving static frontend assets (if Next.js is configured for static export) or routing to the Next.js SSR container.
  - Routing `/api/` traffic to the backend FastAPI container.
  - Enforcing rate limiting to prevent abuse.
  - Setting max client body size (to handle document uploads safely).

### B. Scalability (Future Kubernetes Migration)
- As traffic increases, the architecture is designed to map directly to Kubernetes:
  - **Deployments**: Separate deployments for API and Frontend.
  - **State**: PostgreSQL managed via StatefulSets or externalized to a Managed Database (e.g., AWS RDS).
  - **Storage**: Uploaded documents transitioned from local disk to S3/Blob storage for stateless API scaling.

## 4. CI/CD Pipeline
**Tool**: GitHub Actions
- **On Push to `main`**:
  1. Run comprehensive test suite.
  2. Build Docker images.
  3. Tag images with Git commit hash.
  4. Push images to a Container Registry (e.g., Docker Hub, AWS ECR).
  5. Trigger remote server deployment via SSH to pull new images and restart Docker Compose.

## 5. Database Migrations
- Executed automatically during the CI/CD deployment phase.
- The pipeline will run `alembic upgrade head` against the production database before booting the new application containers, ensuring schema compatibility.

## 6. Monitoring & Logging
- **Logs**: Docker containers configured to route stdout/stderr to a centralized logging service (e.g., Fluentd, ELK stack, or DataDog).
- **Metrics**: FastAPI will expose a `/metrics` endpoint for Prometheus scraping to monitor response times and error rates.
