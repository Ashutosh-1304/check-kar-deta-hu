# Objective
Construct the responsive, high-performance web interface using Next.js 15, React 19, and TailwindCSS to provide an exceptional user experience for uploading and configuring rules.

---

# Deliverables
1. Next.js App Router configuration and base layout.
2. File upload component with drag-and-drop and progress visualization.
3. Rule Editor utilizing React Hook Form for dynamic rule configuration.
4. TanStack Query integration for communicating with the Phase 6 APIs.

---

# Features Covered
- Frontend
- Dashboard
- Upload UI
- Rule Editor
- Issue Viewer
- Charts (Placeholder components)
- Dark Mode
- Responsive UI

---

# Folder Changes
- `[NEW]` frontend/package.json
- `[NEW]` frontend/app/layout.tsx
- `[NEW]` frontend/app/page.tsx
- `[NEW]` frontend/components/ui/
- `[NEW]` frontend/components/upload/
- `[NEW]` frontend/components/rules/
- `[NEW]` frontend/lib/api.ts

---

# Dependencies
- Phase 6 (REST APIs, required for local testing)

---

# Acceptance Criteria
- The application boots locally via `npm run dev`.
- Users can toggle between Dark and Light mode seamlessly.
- The Upload UI successfully sends a file to the backend API and handles the response.
- The UI is fully responsive across desktop and tablet views.

---

# Testing Strategy
- Jest unit tests for utility functions (e.g., file size formatting).
- React Testing Library to test component rendering and user interaction (e.g., clicking upload).

---

# Risks
- Over-fetching or stale data when modifying rules.
- *Mitigation*: Strictly configure TanStack Query invalidation keys to ensure the UI stays in sync with the backend.

---

# Estimated Complexity
Hard

---

# Estimated Duration
1 week

---

# Commit Milestone
`feat(frontend): initialize Next.js dashboard, upload, and rule editor UI`

---

# DO NOT START NEXT PHASE
**Do not proceed until Phase 7 has been fully completed and tested.**
