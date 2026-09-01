"""
Unit tests for Corp++ Runtime Interpreter.
"""

import unittest
from corp.lexer.lexer import Lexer
from corp.parser.parser import Parser
from corp.runtime.interpreter import Interpreter
from corp.telemetry.corporate_error import CorpHostileTakeoverError, CorpUnvettedResourceError


class TestInterpreter(unittest.TestCase):
    def run_corp(self, source: str) -> Interpreter:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source)
        program = parser.parse()
        interpreter = Interpreter(source_code=source)
        interpreter.interpret(program)
        return interpreter

    def test_variables_and_mutation(self):
        source = """
        sync_alignment {
            action_item count = 10;
            promote count;
            promote count;
            demote count;
            core_competency BASE = 100;
        }
        """
        interp = self.run_corp(source)
        self.assertEqual(interp.global_env.get("count"), 11)
        self.assertEqual(interp.global_env.get("BASE"), 100)

    def test_hostile_takeover_protection(self):
        source = """
        sync_alignment {
            core_competency PI = 3.14;
            restructure PI = 4.0;
        }
        """
        with self.assertRaises(CorpHostileTakeoverError):
            self.run_corp(source)

    def test_layoffs_scope_flush(self):
        source = """
        sync_alignment {
            core_competency IMMUTABLE_GOAL = "Win Market";
            action_item temporary_var = "To be fired";
            layoffs;
        }
        """
        interp = self.run_corp(source)
        self.assertEqual(interp.global_env.get("IMMUTABLE_GOAL"), "Win Market")
        with self.assertRaises(CorpUnvettedResourceError):
            interp.global_env.get("temporary_var")

    def test_delegate_execution(self):
        source = """
        delegate multiply_synergy(a, b) {
            deliverable a * b;
        }
        sync_alignment {
            action_item result = loop_in(multiply_synergy(6, 7));
        }
        """
        interp = self.run_corp(source)
        self.assertEqual(interp.global_env.get("result"), 42)

    def test_risk_mitigation_catch(self):
        source = """
        sync_alignment {
            action_item recovered = misaligned;
            let's_take_this_offline {
                opt_out "Out of bandwidth";
            } mitigate_risk (err) {
                restructure recovered = aligned;
            }
        }
        """
        interp = self.run_corp(source)
        self.assertEqual(interp.global_env.get("recovered"), True)


if __name__ == '__main__':
    unittest.main()
