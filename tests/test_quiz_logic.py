import unittest

from app import _source_based_questions, _validate_questions, retrieve_passages


class QuizLogicTests(unittest.TestCase):
    def setUp(self):
        self.notes = (
            "A stack is a linear data structure that follows the last in first out principle. "
            "A queue is a linear data structure that follows the first in first out principle. "
            "A linked list consists of nodes where each node stores data and a reference to another node. "
            "Binary search works on sorted collections by repeatedly dividing the search interval in half. "
            "A database index can improve the speed of data retrieval operations."
        )

    def test_offline_quiz_questions_are_derived_from_notes(self):
        questions = _source_based_questions("Data Structures", self.notes)
        self.assertGreaterEqual(len(questions), 3)
        for question in questions:
            self.assertEqual(len(question["options"]), 4)
            self.assertEqual(len(set(question["options"])), 4)
            correct = question["options"][question["answer"]]
            self.assertIn(correct, self.notes)
            self.assertEqual(correct, question["evidence"])
            for index, option in enumerate(question["options"]):
                if index != question["answer"]:
                    self.assertTrue(option.startswith("The selected notes do not"))

    def test_schema_validation_rejects_non_source_evidence(self):
        items = [{"question": "Which fact is stated?", "options": ["A", "B", "C", "D"],
                  "answer": 0, "explanation": "Explanation", "evidence": "Invented evidence absent from notes."}]
        self.assertEqual(_validate_questions(items, self.notes), [])

    def test_schema_validation_accepts_verbatim_evidence(self):
        quote = "A stack is a linear data structure that follows the last in first out principle."
        items = [{"question": "Which statement is supported?", "options": [quote, "Option B", "Option C", "Option D"],
                  "answer": 0, "explanation": "Model explanation", "evidence": quote}]
        validated = _validate_questions(items, self.notes)
        self.assertEqual(len(validated), 1)
        self.assertIn(quote, validated[0]["explanation"])

    def test_schema_validation_allows_paraphrased_answer_with_verbatim_evidence(self):
        quote = "A stack is a linear data structure that follows the last in first out principle."
        items = [{"question": "Which principle describes how a stack removes items?",
                  "options": ["The newest item is removed first", "The oldest item is removed first",
                              "Items are removed in alphabetical order", "Items are removed at random"],
                  "answer": 0, "explanation": "A stack removes the most recently added item first.", "evidence": quote}]
        validated = _validate_questions(items, self.notes)
        self.assertEqual(len(validated), 1)
        self.assertNotEqual(validated[0]["options"][validated[0]["answer"]], quote)
        self.assertIn(quote, validated[0]["explanation"])

    def test_retrieval_returns_relevant_passage(self):
        results = retrieve_passages(self.notes, "How does a stack work?")
        self.assertTrue(results)
        self.assertIn("stack", results[0]["text"].lower())


if __name__ == "__main__":
    unittest.main()
