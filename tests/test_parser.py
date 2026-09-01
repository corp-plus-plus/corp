"""
Unit tests for Corp++ Parser.
"""

import unittest
from corp.lexer.lexer import Lexer
from corp.parser.parser import Parser
from corp.parser.ast import (
    SyncAlignmentStmt, ActionItemStmt, CoreCompetencyStmt,
    AsPerOurDiscussionStmt, CircleBackStmt, DelegateStmt
)


class TestParser(unittest.TestCase):
    def test_sync_alignment_parsing(self):
        source = """
        sync_alignment {
            action_item budget = 50000;
            core_competency MAX_HEADCOUNT = 10;
        }
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source)
        program = parser.parse()

        self.assertEqual(len(program.statements), 1)
        sync_stmt = program.statements[0]
        self.assertIsInstance(sync_stmt, SyncAlignmentStmt)
        self.assertEqual(len(sync_stmt.body.statements), 2)
        self.assertIsInstance(sync_stmt.body.statements[0], ActionItemStmt)
        self.assertIsInstance(sync_stmt.body.statements[1], CoreCompetencyStmt)

    def test_control_flow_parsing(self):
        source = """
        sync_alignment {
            as_per_our_discussion (x > 10) {
                promote x;
            } pivot {
                demote x;
            }
            circle_back (x < 20) {
                promote x;
            }
        }
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source)
        program = parser.parse()

        sync_stmt = program.statements[0]
        self.assertIsInstance(sync_stmt.body.statements[0], AsPerOurDiscussionStmt)
        self.assertIsInstance(sync_stmt.body.statements[1], CircleBackStmt)


if __name__ == '__main__':
    unittest.main()
