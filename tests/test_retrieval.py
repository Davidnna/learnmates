import unittest
from app import retrieve_passages

SAMPLE_NOTES = """[Page 1]
A stack is a linear data structure that follows the last in, first out principle.
The push operation adds an item to the top of the stack. The pop operation removes the top item.

[Page 2]
A queue is a linear data structure that follows the first in, first out principle.
Enqueue adds an item to the rear of a queue.
"""


class RetrievalTests(unittest.TestCase):
    def test_stack_question_retrieves_stack_page(self):
        results = retrieve_passages(SAMPLE_NOTES, "Explain the push and pop operations in a stack")
        self.assertTrue(results)
        self.assertEqual(results[0]["location"], "page 1")
        self.assertIn("push operation", results[0]["text"])

    def test_queue_question_retrieves_queue_page(self):
        results = retrieve_passages(SAMPLE_NOTES, "What does enqueue mean in a queue")
        self.assertTrue(results)
        self.assertEqual(results[0]["location"], "page 2")

    def test_unrelated_question_returns_no_passages(self):
        self.assertEqual(retrieve_passages(SAMPLE_NOTES, "How does photosynthesis work"), [])


if __name__ == "__main__":
    unittest.main()
