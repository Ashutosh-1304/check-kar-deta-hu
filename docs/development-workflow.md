# Development Workflow

This document outlines the strict phase-by-phase development lifecycle for the Document Compliance Platform.

## 1. Phase Progression Rule
**CRITICAL**: No code for a subsequent phase may be written until the current phase is marked 100% complete.
- Complete = Code written, tests passed, reviewed, merged, and manual QA verified.

## 2. Branching Strategy
We use a feature-branching model based on GitFlow principles.
- **Main Branch**: `main` (Production ready, highly stable).
- **Development Branch**: `develop` (Integration branch for completed phases).
- **Phase/Feature Branches**: 
  - `phase-02-backend-setup`
  - `phase-03-docx-parser`
  - `fix/parser-crash-on-empty-table`

## 3. Commit Strategy
Commits must be small, atomic, and follow Conventional Commits:
- `feat:` A new feature.
- `fix:` A bug fix.
- `docs:` Documentation only changes.
- `refactor:` Code change that neither fixes a bug nor adds a feature.
- `test:` Adding missing tests or correcting existing tests.
- `chore:` Changes to the build process or auxiliary tools.

*Example:* `feat(parser): add support for extracting nested tables`

## 4. Pull Request (PR) Workflow
1. Developer pushes a branch and opens a PR against `develop`.
2. CI automatically runs linters, unit tests, and type checks.
3. PR must receive at least one approval from a peer or Solutions Architect.
4. **Code Review Checklist**:
   - Does this violate SOLID principles?
   - Are there sufficient tests?
   - Are edge cases handled?
   - Are typing and docstrings present?
   - Is there any leaked scope (features belonging to future phases)?
5. Once approved, Squash and Merge.

## 5. Definition of Done (DoD)
A feature or phase is only considered "Done" when:
1. Code compiles and runs without warnings.
2. Type checking (MyPy/TypeScript) passes 100%.
3. Unit and Integration tests are written and pass.
4. Code passes formatting and linting rules (Black/Ruff/ESLint).
5. No new technical debt is introduced without explicit tracking.
6. Acceptance criteria for the phase (defined in `phase-XX.md`) are met.
