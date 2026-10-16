# LearnMates AI — Requirements Traceability and Verification

This checklist records the intended scope of the current prototype. It does not replace the departmental project specification or a complete manual test session.

| ID | Functional requirement | Implementation area | Current verification status |
|---|---|---|---|
| FR-01 | A visitor can create a student account | `/register`, `User` model | Automated smoke test exists; run locally |
| FR-02 | A registered student can log in and log out | `/login`, `/logout`, Flask-Login | Login page/CSRF smoke tests exist; full browser workflow must be run locally |
| FR-03 | Students can upload PDF/TXT notes within the configured size limit | `/materials`, text extraction | Implemented; manually test valid, invalid, oversized, empty-text and scanned PDFs |
| FR-04 | Students can view and delete only their own notes | `/materials`, `/materials/<id>/delete` | Ownership checks should be verified with two separate accounts |
| FR-05 | Students can ask the tutor questions | `/chat`, optional Ollama/OpenAI provider | Implemented; live AI requires a running Ollama model or a valid hosted-provider key/network; test offline and API-failure paths |
| FR-06 | Tutor can retrieve relevant passages from a selected note | `retrieve_passages` and `/chat` | Retrieval unit tests exist; relevance quality needs representative course notes |
| FR-07 | Students can generate summaries and flashcards | `/study-tools` | Implemented with fallback; validate output quality with multiple source types |
| FR-08 | Students can generate, submit, score and review quizzes | `/quiz`, quiz generation helpers | Quiz logic tests exist; manually test a complete session and expired session |
| FR-09 | Quiz questions based on notes show source evidence | quiz validation and result template | Isolated validation checks exist; test with varied notes and insufficient evidence |
| FR-10 | Students can see prior scores and study recommendations | `/dashboard`, `QuizAttempt` | Implemented; verify chart/table match stored attempt values |
| FR-11 | Administrator can view basic aggregate usage and account list | `/admin` | Implemented; verify student receives 403 and administrator can access |
| FR-12 | State-changing forms are protected against missing/invalid CSRF tokens | `protect_state_changing_requests` | Missing-token smoke test exists; test invalid and valid tokens locally |
| FR-13 | Core UI supports keyboard and screen-reader navigation | shared template and styles | Accessibility improvements implemented; requires manual assistive-technology testing |
| FR-14 | UI reflows on mobile and supports optional display preferences | `static/style.css`, shared settings script | Responsive CSS and preferences implemented; verify at 320/375/768/1024 px widths |
| FR-15 | Navigation remains usable on narrow screens and by keyboard | `templates/base.html`, `static/style.css` | Mobile disclosure button exposes `aria-expanded`, closes with Escape, and is covered by static regression checks; verify in a real browser |
| FR-16 | Students can use a free local language model without an OpenAI key | `ai_response`, `.env.example` | Ollama-compatible chat completion path added; requires installing Ollama/model and running an end-to-end request locally |

## Important limitations and acceptance gates

- Do not mark all requirements “passed” until the full test suite and manual test matrix have been run on the target machine.
- Live AI, account creation, upload parsing, chart rendering, and all browser workflows depend on the installed packages and environment configuration.
- Password reset, email verification, login rate limiting, OCR for scanned PDFs, database migrations, malware scanning, and production deployment/monitoring are not part of this prototype yet.
- Accessibility is an implementation target, not a certification. Check WCAG 2.2 AA criteria using both automated tools and human testing, especially contrast, keyboard order, focus visibility, reflow, labels/errors, screen-reader announcements, and zoom.
- Test that users cannot read, delete, or query another student's documents by changing document IDs in requests.
