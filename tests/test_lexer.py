"""
Unit tests for Corp++ Lexer.
"""

import unittest
from corp.lexer.tokens import TokenType
from corp.lexer.lexer import Lexer


class TestLexer(unittest.TestCase):
    def test_keywords_tokenization(self):
        source = """
        sync_alignment quarterly_deliverables hard_stop
        action_item core_competency restructure promote demote layoffs
        as_per_our_discussion pivot circle_back touch_every_base in table_this push_to_next_sprint
        touch_base please_advise broadcast_all_hands
        delegate loop_in deliverable
        let's_take_this_offline mitigate_risk opt_out
        aligned misaligned out_of_office synergizes_with
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        token_types = [t.type for t in tokens if t.type != TokenType.EOF]

        expected = [
            TokenType.SYNC_ALIGNMENT, TokenType.QUARTERLY_DELIVERABLES, TokenType.HARD_STOP,
            TokenType.ACTION_ITEM, TokenType.CORE_COMPETENCY, TokenType.RESTRUCTURE,
            TokenType.PROMOTE, TokenType.DEMOTE, TokenType.LAYOFFS,
            TokenType.AS_PER_OUR_DISCUSSION, TokenType.PIVOT, TokenType.CIRCLE_BACK,
            TokenType.TOUCH_EVERY_BASE, TokenType.IN, TokenType.TABLE_THIS, TokenType.PUSH_TO_NEXT_SPRINT,
            TokenType.TOUCH_BASE, TokenType.PLEASE_ADVISE, TokenType.BROADCAST_ALL_HANDS,
            TokenType.DELEGATE, TokenType.LOOP_IN, TokenType.DELIVERABLE,
            TokenType.LETS_TAKE_THIS_OFFLINE, TokenType.MITIGATE_RISK, TokenType.OPT_OUT,
            TokenType.ALIGNED, TokenType.MISALIGNED, TokenType.OUT_OF_OFFICE, TokenType.AND
        ]
        self.assertEqual(token_types, expected)

    def test_numbers_and_strings(self):
        source = 'action_item revenue = 1_000_000.50; action_item name = "Synergy Corp";'
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, TokenType.ACTION_ITEM)
        self.assertEqual(tokens[1].value, 'revenue')
        self.assertEqual(tokens[3].value, 1000000.50)
        self.assertEqual(tokens[8].value, "Synergy Corp")


if __name__ == '__main__':
    unittest.main()
