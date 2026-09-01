"""
Corp++ Enterprise Command-Line Interface (CLI).
Command: `corp`
"""

import sys
import os
import argparse
from corp import __version__
from corp.lexer.lexer import Lexer
from corp.parser.parser import Parser
from corp.runtime.interpreter import Interpreter
from corp.compiler.compiler import Compiler
from corp.compiler.vm import CorpVM
from corp.telemetry.corporate_error import CorpError, CorpHardStop
from corp.telemetry.audit import audit_source
from corp.cli.repl import start_boardroom_repl


def run_file(file_path: str, use_vm: bool = False):
    if not os.path.exists(file_path):
        print(f"[FATAL BLOCKER] File '{file_path}' could not be onboarded. Check filepath.", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    try:
        lexer = Lexer(source_code, file_path=file_path)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source_code, file_path=file_path)
        program = parser.parse()

        if use_vm:
            compiler = Compiler(source_code=source_code, file_path=file_path)
            chunk = compiler.compile(program)
            vm = CorpVM(source_code=source_code, file_path=file_path)
            vm.run(chunk)
        else:
            interpreter = Interpreter(source_code=source_code, file_path=file_path)
            interpreter.interpret(program)

    except CorpHardStop as hs:
        sys.exit(hs.code)
    except CorpError as ce:
        print(str(ce), file=sys.stderr)
        sys.exit(1)
    except Exception as ex:
        print(f"[UNEXPECTED ANOMALY] {ex}", file=sys.stderr)
        sys.exit(1)


def compile_file(file_path: str, disassemble: bool = False, output_path: str = None):
    if not os.path.exists(file_path):
        print(f"[FATAL BLOCKER] File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    try:
        lexer = Lexer(source_code, file_path=file_path)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source_code, file_path=file_path)
        program = parser.parse()
        compiler = Compiler(source_code=source_code, file_path=file_path)
        chunk = compiler.compile(program)

        if disassemble:
            print(chunk.disassemble())
        else:
            print(f"Compilation successful! Verified {len(chunk.code)} enterprise opcodes.")

    except CorpError as ce:
        print(str(ce), file=sys.stderr)
        sys.exit(1)


def audit_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"[FATAL BLOCKER] File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    try:
        results = audit_source(source_code, file_path=file_path)
        print("\n═══════════════════════════════════════════════════════════════")
        print("          CORP++ ENTERPRISE STATIC AUDIT REPORT               ")
        print("═══════════════════════════════════════════════════════════════")
        print(f"Target File:              {results['file_path']}")
        print(f"Total Corporate Tokens:   {results['total_tokens']}")
        print(f"Action Items (let):       {results['action_items']}")
        print(f"Core Competencies (const):{results['core_competencies']}")
        print(f"Risk Mitigations (try):   {results['risk_mitigations']}")
        print(f"Layoffs Events (flush):   {results['layoffs_count']}")
        print(f"Main Entry Alignment:     {'ALIGNED' if results['has_sync_alignment'] else 'MISALIGNED'}")
        print(f"Synergy Score:            {results['synergy_score']} / 100")
        print(f"ESG Governance Rating:    {results['esg_compliance_rating']}")
        print("═══════════════════════════════════════════════════════════════\n")
    except CorpError as ce:
        print(str(ce), file=sys.stderr)
        sys.exit(1)


def package_binary():
    """Packages the Corp++ compiler into a standalone single-file binary."""
    from scripts.build_binary import build_standalone_binary
    build_standalone_binary()


def main():
    parser = argparse.ArgumentParser(
        prog="corp",
        description="Corp++ (corp) - Enterprise-Grade Systems Programming Language Toolchain",
        epilog="Remember: Align early, touch base often, and protect core competencies."
    )
    parser.add_argument("-v", "--version", action="version", version=f"Corp++ Toolchain v{__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Corporate Commands")

    # run command
    run_parser = subparsers.add_parser("run", help="Execute a Corp++ (.corp) deliverable file")
    run_parser.add_argument("file", help="Path to .corp file")
    run_parser.add_argument("--vm", action="store_true", help="Execute on Corporate Virtual Machine (CVM)")

    # compile command
    compile_parser = subparsers.add_parser("compile", help="Compile .corp file to bytecode / inspect disassembly")
    compile_parser.add_argument("file", help="Path to .corp file")
    compile_parser.add_argument("-d", "--disassemble", action="store_true", help="Disassemble bytecode instructions")
    compile_parser.add_argument("-o", "--output", help="Output file path")

    # repl command
    subparsers.add_parser("repl", help="Launch 'The Boardroom' interactive alignment REPL")

    # audit command
    audit_parser = subparsers.add_parser("audit", help="Audit .corp file for enterprise KPI compliance")
    audit_parser.add_argument("file", help="Path to .corp file")

    # package command
    subparsers.add_parser("package", help="Build standalone executable binary (dist/corp) to send to friends")

    # Direct file argument fallback (e.g. `corp script.corp`)
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-") and sys.argv[1] not in subparsers.choices:
        run_file(sys.argv[1])
        return

    args = parser.parse_args()

    if args.command == "run":
        run_file(args.file, use_vm=args.vm)
    elif args.command == "compile":
        compile_file(args.file, disassemble=args.disassemble, output_path=args.output)
    elif args.command == "repl" or args.command is None:
        start_boardroom_repl()
    elif args.command == "audit":
        audit_file(args.file)
    elif args.command == "package":
        package_binary()


if __name__ == "__main__":
    main()
