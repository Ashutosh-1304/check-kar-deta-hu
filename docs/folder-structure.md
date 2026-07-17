# Folder Structure

This document outlines the strict production-ready folder structure for the Document Compliance Platform.

```text
document-checker/
├── docs/                        # Planning and architectural documentation
│   ├── phase-*.md
│   ├── architecture.md
│   ├── tech-stack.md
│   ├── api-design.md
│   └── README.md
│
├── frontend/                    # Next.js Application
│   ├── app/                     # App Router
│   │   ├── (auth)/              # Authentication routes
│   │   ├── dashboard/           # Dashboard routes
│   │   ├── report/[id]/         # Dynamic report view
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── ui/                  # shadcn/ui generic components
│   │   ├── dashboard/           # Specific dashboard components
│   │   ├── rules/               # Rule editor components
│   │   └── report/              # Issue viewer & timeline components
│   ├── lib/                     # Utilities and axios configurations
│   ├── hooks/                   # Custom React hooks (useUpload, useRules)
│   ├── styles/                  # Global CSS and Tailwind directives
│   └── types/                   # Frontend TypeScript interfaces
│
├── backend/                     # FastAPI Application
│   ├── app/
│   │   ├── api/                 # Route handlers (Controllers)
│   │   │   ├── v1/
│   │   │   │   ├── upload.py
│   │   │   │   ├── validate.py
│   │   │   │   ├── reports.py
│   │   │   │   └── rules.py
│   │   ├── core/                # Configuration, logging, dependencies
│   │   ├── db/                  # Database connections and Session
│   │   │   ├── models/          # SQLAlchemy ORM models
│   │   │   └── migrations/      # Alembic migration scripts
│   │   ├── parser/              # Document Parsing Engine
│   │   │   ├── docx_parser.py
│   │   │   ├── models.py        # Internal Document Model
│   │   │   └── base.py          # Abstract parser interface
│   │   ├── rules/               # Rule Engine
│   │   │   ├── schemas.py       # Pydantic schemas for rule validation
│   │   │   └── loader.py
│   │   ├── validators/          # Validation Pipeline
│   │   │   ├── base.py
│   │   │   ├── margin.py
│   │   │   ├── font.py
│   │   │   └── heading.py
│   │   ├── report/              # Report generation (JSON/HTML)
│   │   └── main.py              # Application entry point
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   │
│   ├── uploads/                 # Temporary storage for uploaded documents
│   └── reports/                 # Stored generated reports
│
├── configs/                     # Application configurations (e.g. Nginx, Linting rules)
│
├── examples/                    # Sample files for testing (Sample docs, Sample rule JSONs)
│
└── docker-compose.yml           # Local development orchestration
```
