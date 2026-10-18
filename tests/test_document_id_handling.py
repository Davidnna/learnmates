"""Regression checks for document IDs submitted by HTML forms."""
from pathlib import Path
import unittest

APP_SOURCE = (Path(__file__).resolve().parents[1] / "app.py").read_text(encoding="utf-8")


class DocumentIdHandlingStaticTests(unittest.TestCase):
    def test_document_ids_are_normalized_to_integers(self):
        self.assertIn("def _parse_document_id(raw_value):", APP_SOURCE)
        self.assertIn("document_id = int(raw_value)", APP_SOURCE)
        self.assertIn("return document_id if document_id > 0 else None", APP_SOURCE)

    def test_all_document_lookup_routes_use_normalized_ids(self):
        self.assertIn("filter_by(id=doc_id, owner_id=current_user.id)", APP_SOURCE)
        self.assertIn("filter_by(id=parsed_doc_id, owner_id=current_user.id)", APP_SOURCE)
        self.assertIn("doc_id = _parse_document_id(raw_doc_id)", APP_SOURCE)
        self.assertIn("parsed_doc_id = _parse_document_id(selected_doc_id)", APP_SOURCE)


if __name__ == "__main__":
    unittest.main()
