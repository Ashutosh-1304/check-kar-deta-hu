# Database Design

This document details the PostgreSQL schema required to support the Document Compliance Platform.

*Note: No SQL is provided. Alembic will manage migrations based on SQLAlchemy ORM models.*

## Tables

### 1. `users` (Future phase)
Stores user authentication and profile data.
- `id` (UUID, Primary Key)
- `email` (String, Unique, Indexed)
- `hashed_password` (String)
- `role` (Enum: ADMIN, USER)
- `created_at` (Timestamp)

### 2. `rule_templates`
Stores configured formatting and structural rules.
- `id` (UUID, Primary Key)
- `name` (String, Indexed) - e.g., "IEEE Standard", "Internal Policy V2"
- `description` (String, Nullable)
- `rules_payload` (JSONB) - The actual rule definitions (margins, fonts, etc.)
- `version` (Integer) - Increments on modification
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### 3. `documents`
Stores metadata for uploaded documents (the physical files are temporarily held on disk or object storage).
- `id` (UUID, Primary Key)
- `filename` (String)
- `file_size` (Integer) - Size in bytes
- `uploaded_at` (Timestamp)
- `status` (Enum: UPLOADED, PARSING, VALIDATING, COMPLETED, FAILED)

### 4. `compliance_reports`
Stores the overall result and aggregate metrics of a validation run.
- `id` (UUID, Primary Key)
- `document_id` (UUID, Foreign Key -> `documents.id`, Indexed)
- `rule_template_id` (UUID, Foreign Key -> `rule_templates.id`)
- `overall_score` (Float) - E.g., 94.5
- `total_errors` (Integer)
- `total_warnings` (Integer)
- `total_passed` (Integer)
- `created_at` (Timestamp)

### 5. `validation_issues`
Stores detailed row-by-row issues identified during validation for timeline and filtering display.
- `id` (UUID, Primary Key)
- `report_id` (UUID, Foreign Key -> `compliance_reports.id`, Indexed)
- `severity` (Enum: ERROR, WARNING)
- `category` (String) - e.g., "Margin", "Font", "Heading"
- `page_number` (Integer, Nullable)
- `paragraph_index` (Integer, Nullable)
- `expected_value` (String, Nullable)
- `actual_value` (String, Nullable)
- `suggestion` (String)
- `created_at` (Timestamp)

## Relationships

- A `Document` has one `ComplianceReport`.
- A `ComplianceReport` belongs to one `Document` and one `RuleTemplate`.
- A `ComplianceReport` has many `ValidationIssues`.

## Indexes
- `idx_reports_document_id`: Fast lookup of a report for a specific document.
- `idx_issues_report_id`: Fast retrieval of all timeline issues for a specific report.
- `idx_rule_templates_name`: Efficient search by rule template name.
