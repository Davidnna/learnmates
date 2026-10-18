"""Static accessibility regression checks; manual AT checks are still required."""
from pathlib import Path
import unittest
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]

class AccessibilityTemplateChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = Environment(loader=FileSystemLoader(str(ROOT / "templates")))
        cls.env.filters["markdown"] = lambda value: value
        cls.css = (ROOT / "static" / "style.css").read_text(encoding="utf-8")
        cls.base = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")

    def test_all_templates_parse(self):
        for path in (ROOT / "templates").glob("*.html"):
            with self.subTest(template=path.name):
                self.env.get_template(path.name)

    def test_skip_link_and_landmarks_exist(self):
        self.assertIn('class="skip-link" href="#main-content"', self.base)
        self.assertIn('id="primary-navigation" aria-label="Primary navigation"', self.base)
        self.assertIn('aria-controls="primary-navigation"', self.base)
        self.assertIn('aria-expanded="false"', self.base)
        self.assertIn('Escape', self.base)
        self.assertIn('max-width: 1100px', self.css)
        self.assertIn('<main id="main-content"', self.base)
        self.assertIn('aria-current="page"', self.base)

    def test_brand_favicon_and_preferences_removal(self):
        self.assertIn("filename='favicon.svg'", self.base)
        self.assertIn("filename='brand-mark.svg'", self.base)
        self.assertIn('class="brand-icon"', self.base)
        self.assertNotIn("Display preferences", self.base)
        self.assertNotIn("learnmates-display-preferences", self.base)
        self.assertNotIn("data-pref=", self.base)
        self.assertNotIn("localStorage", self.base)

    def test_public_information_navigation_and_ai_retry_support(self):
        for endpoint in ("about", "features", "how_it_works", "faq", "privacy"):
            self.assertIn("url_for('" + endpoint + "')", self.base)
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn("def _chat_completion_with_retries", app_source)
        self.assertIn("retryable_statuses = {429, 500, 502, 503, 504}", app_source)
        self.assertIn("GROQ_FALLBACK_MODEL", app_source)
        self.assertIn("https://api.groq.com/openai/v1", app_source)
        self.assertIn("GROQ_API_KEY", app_source)
        self.assertFalse((ROOT / "render.yaml").exists())

    def test_tutor_markdown_and_conversation_ui(self):
        chat = (ROOT / "templates" / "chat.html").read_text(encoding="utf-8")
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn("class=\"chat-transcript\"", chat)
        self.assertIn("m.content|markdown|safe", chat)
        self.assertIn("def render_markdown(value)", app_source)
        self.assertIn("bleach.clean", app_source)
        self.assertIn("class=\"chat-composer\"", chat)

    def test_quiz_question_count_and_student_facing_copy(self):
        quiz = (ROOT / "templates" / "quiz.html").read_text(encoding="utf-8")
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('name="question_count"', quiz)
        self.assertIn('value="{{ question_count or 10 }}"', quiz)
        self.assertIn('count=question_count', app_source)
        for template in (ROOT / "templates").glob("*.html"):
            content = template.read_text(encoding="utf-8").lower()
            self.assertNotIn("groq_api_key", content)
            self.assertNotIn("gemini_api_key", content)
            self.assertNotIn("openai_api_key", content)
            self.assertNotIn(".env", content)

    def test_keyboard_and_motion_support(self):
        self.assertIn(":focus-visible", self.css)
        self.assertIn("prefers-reduced-motion: reduce", self.css)
        self.assertIn("forced-colors: active", self.css)

    def test_chart_has_table_alternative(self):
        dashboard = (ROOT / "templates" / "dashboard.html").read_text(encoding="utf-8")
        self.assertIn("View chart data as a table", dashboard)
        self.assertIn('<table>', dashboard)

    def test_tutor_suggestions_do_not_require_inline_handlers(self):
        chat = (ROOT / "templates" / "chat.html").read_text(encoding="utf-8")
        self.assertIn("data-prompt=", chat)
        self.assertNotIn("onclick=", chat.lower())

if __name__ == "__main__":
    unittest.main()
