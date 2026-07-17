# API Design

This document details the RESTful API endpoints for the Document Compliance Platform. All endpoints will be implemented using FastAPI and comply with OpenAPI standards.

## 1. Document Upload
**Endpoint:** `POST /api/v1/upload`
**Description:** Uploads a DOCX file for temporary storage and returns a tracking ID.
- **Request:** `multipart/form-data` (file: `file`)
- **Response (200 OK):**
  ```json
  {
    "document_id": "uuid",
    "filename": "document.docx",
    "status": "UPLOADED"
  }
  ```
- **Errors:** 400 (Invalid file type), 413 (Payload too large)

## 2. Validation
**Endpoint:** `POST /api/v1/validate`
**Description:** Triggers the validation pipeline for a previously uploaded document against a specific rule template.
- **Request (JSON):**
  ```json
  {
    "document_id": "uuid",
    "rule_template_id": "uuid"
  }
  ```
- **Response (202 Accepted):**
  ```json
  {
    "report_id": "uuid",
    "status": "VALIDATING"
  }
  ```
- **Errors:** 404 (Document/Rule not found), 400 (Validation already in progress)

## 3. Get Report
**Endpoint:** `GET /api/v1/reports/{report_id}`
**Description:** Retrieves the comprehensive compliance report and issue timeline.
- **Request:** None
- **Response (200 OK):**
  ```json
  {
    "report_id": "uuid",
    "status": "COMPLETED",
    "overall_score": 94.5,
    "metrics": {
      "errors": 2,
      "warnings": 5,
      "passed_checks": 120
    },
    "issues": [
      {
        "id": "uuid",
        "severity": "ERROR",
        "category": "Margin",
        "page": 1,
        "paragraph": null,
        "expected": "1 inch",
        "actual": "0.5 inch",
        "suggestion": "Increase bottom margin to 1 inch."
      }
    ]
  }
  ```
- **Errors:** 404 (Report not found)

## 4. Rule Templates

### List Rules
**Endpoint:** `GET /api/v1/rules`
**Description:** Returns a list of all configured rule templates.
- **Response (200 OK):**
  ```json
  [
    {
      "id": "uuid",
      "name": "Standard Policy",
      "version": 1
    }
  ]
  ```

### Create Rule
**Endpoint:** `POST /api/v1/rules`
**Description:** Creates a new rule template.
- **Request (JSON):** Payload matching the Rule YAML/JSON specification.
- **Response (201 Created):** Includes the assigned rule `id`.

### Update Rule
**Endpoint:** `PUT /api/v1/rules/{rule_id}`
**Description:** Updates an existing rule template (bumps version).
- **Request (JSON):** Updated Rule specification.
- **Response (200 OK):** Updated rule data.

### Delete Rule
**Endpoint:** `DELETE /api/v1/rules/{rule_id}`
**Description:** Soft-deletes a rule template.
- **Response (204 No Content)**

## Future Endpoints
- `GET /api/v1/reports/{report_id}/export/html`
- `GET /api/v1/reports/{report_id}/export/pdf`
- `POST /api/v1/auth/login` (For enterprise user access)
