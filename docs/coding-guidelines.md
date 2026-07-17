# Coding Guidelines

To maintain an enterprise-grade codebase, all contributors must strictly adhere to the following guidelines.

## Naming Conventions
- **Python (Backend)**: PEP 8 compliant. `snake_case` for variables and functions. `PascalCase` for classes. `UPPER_SNAKE_CASE` for constants.
- **TypeScript (Frontend)**: `camelCase` for variables and functions. `PascalCase` for React components, Types, and Interfaces.
- **Database**: `snake_case` for table and column names.
- **Files/Folders (Frontend)**: `kebab-case` for file and directory names (e.g., `rule-editor.tsx`).
- **Files/Folders (Backend)**: `snake_case` for modules (e.g., `docx_parser.py`).

## SOLID Principles
All code must adhere to SOLID principles to ensure maintainability:
- **Single Responsibility**: Each validator (e.g., `MarginValidator`) should only validate its specific domain.
- **Open/Closed**: The validation pipeline must be open for extension (adding a `PDFValidator`) but closed for modification.
- **Liskov Substitution**: Any Parser subclass should be usable anywhere the base Parser interface is expected.
- **Interface Segregation**: Keep interfaces small and specific.
- **Dependency Inversion**: High-level modules (API routes) must depend on abstractions (Base Parser), not concrete implementations (docx parser). Dependency Injection is strictly enforced via FastAPI's `Depends`.

## Error Handling
- Never expose raw stack traces to the frontend.
- Backend: Use custom exception classes that map to specific HTTP status codes (e.g., `RuleNotFoundError -> 404`).
- Frontend: Use React Error Boundaries to catch unhandled exceptions in the component tree without crashing the app. Use toast notifications for user-facing API errors.

## Logging
- Structured JSON logging must be used in production for aggregation (e.g., DataDog, ELK).
- Always include `document_id` and `correlation_id` in logs for tracing.
- Levels: `DEBUG` for development, `INFO` for standard flow, `WARNING` for non-fatal issues, `ERROR` for unexpected exceptions.

## Testing Philosophy
- Write tests *alongside* implementation.
- Focus on behavior, not implementation details.
- Coverage should be minimum 80% for backend services.

## Git Strategy
- **Branch Naming**: `feature/[phase-id]-[feature-name]`, `bugfix/[issue-number]-[description]`
- **Commits**: Follow Conventional Commits format (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).
- **Merge**: Squash and merge PRs to keep the main history clean.

## Documentation Standards
- Python: Enforce Docstrings (Google format) for all public classes, methods, and complex functions. Type hints are mandatory.
- TypeScript: Type interfaces must be thoroughly documented using JSDoc.
