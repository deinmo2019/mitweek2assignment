import unittest
from game_logic import QUESTIONS, PATTERNS, chatbot_answer, predict_pattern

class LogicTests(unittest.TestCase):
    def test_quiz_demonstrates_context_failures(self):
        correct = sum(chatbot_answer(q.text)[0] == q.correct for q in QUESTIONS)
        self.assertEqual(correct, 4)
        self.assertEqual(chatbot_answer('It is NOT raining.')[0], 'An umbrella')
        self.assertEqual(chatbot_answer('What is the time?')[0], 'I do not know')
    def test_rule_order_and_word_boundaries(self):
        self.assertEqual(chatbot_answer('Traffic in the rain')[0], 'An umbrella')
        self.assertEqual(chatbot_answer('My brain is working')[0], 'I do not know')
    def test_patterns_and_abstention(self):
        self.assertEqual(predict_pattern(PATTERNS[0].terms)[0], 10)
        self.assertEqual(predict_pattern(PATTERNS[1].terms)[0], 48)
        for pattern in PATTERNS[2:]:
            self.assertIsNone(predict_pattern(pattern.terms)[0])
        self.assertEqual(predict_pattern((0, 0, 0))[0], 0)
        self.assertIsNone(predict_pattern((1, 2))[0])

if __name__ == '__main__':
    unittest.main()
