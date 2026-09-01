"""
Unit tests for Corp++ Bytecode Compiler & Virtual Machine (CVM).
"""

import unittest
from corp.lexer.lexer import Lexer
from corp.parser.parser import Parser
from corp.compiler.compiler import Compiler
from corp.compiler.vm import CorpVM


class TestVM(unittest.TestCase):
    def test_vm_execution(self):
        source = """
        sync_alignment {
            action_item total = 0;
            action_item i = 1;
            circle_back (i <= 5) {
                restructure total = total + i;
                promote i;
            }
        }
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source)
        program = parser.parse()
        compiler = Compiler(source_code=source)
        chunk = compiler.compile(program)

        vm = CorpVM(source_code=source)
        vm.run(chunk)

        self.assertEqual(vm.global_env.get("total"), 15)
        self.assertEqual(vm.global_env.get("i"), 6)


if __name__ == '__main__':
    unittest.main()
