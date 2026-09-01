"""
The Boardroom - Corp++ Interactive REPL.
Enterprise-grade interactive session for real-time alignment and synergy evaluation.
"""

import sys
import readline
from corp.lexer.lexer import Lexer
from corp.parser.parser import Parser
from corp.runtime.interpreter import Interpreter
from corp.telemetry.corporate_error import CorpError, CorpHardStop, CorpReturn


BANNER = """
╔══════════════════════════════════════════════════════════════════════╗
║               CORP++ ENTERPRISE BOARDROOM REPL (v1.0)                ║
║  "Where Systems Programming Meets Unapologetic Middle-Management"   ║
╚══════════════════════════════════════════════════════════════════════╝
Type Corp++ expressions, declarations, or enter corporate commands:
  /help       - View corporate alignment menu
  /layoffs    - Emergency headcount & scope purge
  /kpis       - Inspect active scope action items & core competencies
  /exit       - Hard stop boardroom session
"""


def start_boardroom_repl():
    print(BANNER)
    interpreter = Interpreter(file_path="<Boardroom_Live_Session>")
    prompt_num = 1

    while True:
        try:
            prompt = f"corp[Q{prompt_num}]> "
            line = input(prompt).strip()

            if not line:
                continue

            if line == "/exit" or line == "hard_stop":
                print("Leadership alignment concluded. Have a productive sprint!")
                break

            if line == "/help":
                print("""
Corporate Command Menu:
  action_item <var> = <val>;      - Allocate mutable budget
  core_competency <var> = <val>;  - Allocate immutable constant
  restructure <var> = <val>;      - Reassign budget
  promote <var>;                  - Increment metric
  demote <var>;                   - Decrement metric
  touch_base(<expr>);             - Output deliverable
  layoffs;                        - Scope headcount flush
  /kpis                           - Inspect active scope resources
  /layoffs                        - Emergency memory flush
  /exit                           - Hard stop
                """)
                continue

            if line == "/layoffs":
                interpreter.current_env.layoffs()
                continue

            if line == "/kpis":
                env = interpreter.current_env
                print("=== Active Corporate Scope Resources ===")
                print(f"Core Competencies: {list(env.core_competencies)}")
                print(f"All Allocated Assets: {list(env.values.keys())}")
                continue

            # Tokenize & Parse
            lexer = Lexer(line, file_path="<Boardroom>")
            tokens = lexer.tokenize()
            parser = Parser(tokens, source_code=line, file_path="<Boardroom>")
            program = parser.parse()

            # Execute
            interpreter.interpret(program)
            prompt_num += 1

        except EOFError:
            print("\nStakeholder quorum dismissed. Hard stop.")
            break
        except KeyboardInterrupt:
            print("\n[BUMP] Session interrupted by urgent executive escalation.")
            continue
        except CorpHardStop as hs:
            print(f"Boardroom session exited with status {hs.code}.")
            break
        except CorpError as ce:
            print(str(ce), file=sys.stderr)
        except Exception as ex:
            print(f"Unexpected operational anomaly: {ex}", file=sys.stderr)
