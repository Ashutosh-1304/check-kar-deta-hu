# Document Compliance Checker

## Project Overview
The Document Compliance Platform is a production-grade, highly scalable enterprise solution designed to validate Microsoft Word (.docx) documents against configurable formatting and structural rules. It generates detailed compliance reports pinpointing specific issues. Built for extensibility, the architecture accommodates future integrations such as PDF validation, AI grammar review, citation checking, and enterprise collaboration without altering the core validation engine.

## Architecture
The platform utilizes a modular, decoupled architecture:
- **Frontend**: A highly interactive, responsive dashboard built with Next.js 15, React 19, and TailwindCSS, utilizing TanStack Query for state management.
- **Backend**: A high-performance RESTful API powered by FastAPI (Python 3.12) with asynchronous request handling.
- **Rule Engine**: An independent, configurable rule definition system supporting templates (JSON/YAML) and versioning.
- **Validation Engine**: A pipeline-based validation module allowing separate, isolated validators (e.g., MarginValidator, FontValidator) to process specific compliance rules.
- **Database**: PostgreSQL paired with SQLAlchemy for persistent storage of templates, compliance reports, and user configuration.

## Features
- **Document Upload**: Support for DOCX format with temporary storage and visual upload progress.
- **Rule Configuration**: Create, save, edit, and version formatting rules using JSON/YAML.
- **Extensive Validation**: Validates Page, Margins, Fonts, Headings, Paragraphs, Tables, Images, Header/Footer, and Lists.
- **Advanced Dashboard**: Visualizes overall compliance score, rule passes/failures (via pie/bar charts), and an interactive issue timeline.
- **Reporting**: Exports validation results in JSON and HTML (with PDF planned for the future).
- **Rule Management**: Support for creating, duplicating, exporting, and importing rule templates.

## Folder Structure
The project is strictly organized to maintain separation of concerns. The primary directories include:
- `frontend/`: Contains the Next.js application, components, and hooks.
- `backend/`: Contains the FastAPI application, parsing logic, validation engine, and rule definitions.
- `configs/`: Stores environment and application-level configuration files.
- `docs/`: Contains all comprehensive architectural, planning, and structural documentation.

## Tech Stack
**Frontend:** Next.js 15, React 19, TypeScript, TailwindCSS, shadcn/ui, TanStack Query, React Hook Form, Framer Motion.
**Backend:** FastAPI, Python 3.12, Pydantic v2, SQLAlchemy, PostgreSQL, Alembic.
**Document Processing:** python-docx, lxml, Pillow.
**Infrastructure:** Docker, Docker Compose, GitHub Actions, Nginx, CI/CD pipelines.

## Roadmap
1. Phase 1-6: Core parsing, rule engine, validation pipeline, and REST APIs.
2. Phase 7-8: Advanced frontend dashboard and comprehensive reporting.
3. Phase 9: Testing, hardening, and CI/CD pipelines.
4. Phase 10: Scalability, enterprise features, and readiness for future plugins.

## Setup (Planned)
*Note: Setup instructions will be provided once Phase 2 is fully implemented. The project will rely on Docker Compose for localized deployment.*

## Development Workflow
Development is strictly divided into 10 sequential phases. **No phase may begin until the preceding phase is fully completed and tested.** 
- Branching follows `feature/phase-XX-feature-name`.
- Commits must follow standardized commit messages.
- Pull requests require code review and adherence to the Definition of Done.

## Contribution Guide
1. Fork the repository.
2. Create a branch matching the current phase requirements.
3. Ensure all tests (Unit/Integration) pass before opening a PR.
4. Obtain approval from the Solutions Architect before merging.

## License
Proprietary / Enterprise (To be determined)

## Future Vision
The platform is designed with a plugin architecture to eventually support:
- PDF and OCR validation.
- AI-powered grammar and writing suggestions.
- Plagiarism and citation validation.
- Multi-language support and team workspaces.
