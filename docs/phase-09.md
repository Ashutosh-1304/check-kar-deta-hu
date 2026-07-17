# Objective
Harden the application for production deployment by increasing test coverage, configuring automated CI/CD pipelines, and finalizing Docker compose setups.

---

# Deliverables
1. GitHub Actions workflow for CI (linting, tests, build).
2. End-to-End test suite utilizing Playwright.
3. Optimized Dockerfiles for production builds (multi-stage).

---

# Features Covered
- Testing
- Unit Tests (Audit & Fill Gaps)
- Integration Tests
- E2E Tests
- CI/CD
- Docker (Production configs)
- Production hardening

---

# Folder Changes
- `[NEW]` .github/workflows/ci.yml
- `[NEW]` frontend/playwright.config.ts
- `[NEW]` frontend/tests/e2e/
- `[NEW]` docker-compose.prod.yml
- `[NEW]` nginx/nginx.conf

---

# Dependencies
- All previous phases (1-8).

---

# Acceptance Criteria
- A Pull Request triggers the GitHub Action which successfully runs backend pytest and frontend E2E tests.
- Docker containers can be built and run in a production-like environment using `docker-compose.prod.yml`.
- Minimum overall code coverage metric (80%) is achieved.

---

# Testing Strategy
- Ensure all CI jobs execute flawlessly in the remote environment.
- Validate Nginx reverse proxy routing manually.

---

# Risks
- Flaky E2E tests blocking the CI pipeline.
- *Mitigation*: Ensure Playwright tests have appropriate timeouts and wait for explicit network/DOM events, avoiding arbitrary `sleep()` calls.

---

# Estimated Complexity
Medium

---

# Estimated Duration
1 week

---

# Commit Milestone
`chore(infra): configure CI/CD pipelines, E2E tests, and production Docker setup`

---

# DO NOT START NEXT PHASE
**Do not proceed until Phase 9 has been fully completed and tested.**
