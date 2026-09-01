"""
Corp++ Tree-Walking Interpreter & Runtime Engine.
Executes Corp++ AST nodes with corporate runtime semantics and telemetry.
"""

import sys
import math
from typing import Any, List, Optional
from corp.parser.ast import (
    ASTNode, Expr, Stmt, Program, BlockStmt,
    LiteralExpr, ArrayExpr, IdentifierExpr, BinaryExpr, UnaryExpr,
    CallExpr, PleaseAdviseExpr, IndexExpr,
    QuarterlyDeliverablesStmt, SyncAlignmentStmt, HardStopStmt,
    ActionItemStmt, CoreCompetencyStmt, RestructureStmt,
    PromoteStmt, DemoteStmt, LayoffsStmt,
    AsPerOurDiscussionStmt, CircleBackStmt, TouchEveryBaseStmt,
    TableThisStmt, PushToNextSprintStmt,
    TouchBaseStmt, BroadcastAllHandsStmt, DelegateStmt, DeliverableStmt,
    RiskMitigationStmt, OptOutStmt, ExprStmt
)
from corp.telemetry.corporate_error import (
    CorpRuntimeError,
    CorpTypeError,
    CorpOptOutException,
    CorpHardStop,
    CorpReturn,
    CorpBreak,
    CorpContinue
)
from .environment import Environment
from .values import CorpFunction, CorpBuiltinFunction, CorpModule, corp_stringify


class Interpreter:
    def __init__(self, source_code: Optional[str] = None, file_path: Optional[str] = None):
        self.source_code = source_code
        self.file_path = file_path or "<corporate_memo.corp>"
        self.global_env = Environment(name="CorporateGlobalAlignment")
        self.current_env = self.global_env
        self.sync_alignment_node: Optional[SyncAlignmentStmt] = None
        self._init_builtins()

    def _init_builtins(self):
        def _builtin_len(interpreter, args):
            if not args or not isinstance(args[0], (list, str)):
                return 0
            return len(args[0])

        def _builtin_headcount(interpreter, args):
            """Returns the headcount (length) of a team array or string."""
            return _builtin_len(interpreter, args)

        def _builtin_range(interpreter, args):
            if len(args) == 1:
                return list(range(int(args[0])))
            elif len(args) >= 2:
                return list(range(int(args[0]), int(args[1])))
            return []

        def _builtin_str(interpreter, args):
            return corp_stringify(args[0]) if args else ""

        def _builtin_num(interpreter, args):
            try:
                val = args[0] if args else 0
                if isinstance(val, (int, float)):
                    return val
                val_str = str(val).strip()
                return float(val_str) if '.' in val_str else int(val_str)
            except Exception:
                return 0

        self.global_env.define("headcount", CorpBuiltinFunction("headcount", _builtin_headcount, 1), is_core=True)
        self.global_env.define("range", CorpBuiltinFunction("range", _builtin_range, 2), is_core=True)
        self.global_env.define("corporate_string", CorpBuiltinFunction("corporate_string", _builtin_str, 1), is_core=True)
        self.global_env.define("synergy_number", CorpBuiltinFunction("synergy_number", _builtin_num, 1), is_core=True)

    def interpret(self, program: Program) -> Any:
        try:
            # First pass: collect declarations and look for sync_alignment
            sync_nodes = []
            for stmt in program.statements:
                if isinstance(stmt, SyncAlignmentStmt):
                    sync_nodes.append(stmt)
                else:
                    self.execute(stmt)

            # If sync_alignment is present, execute its main body
            if sync_nodes:
                for sync in sync_nodes:
                    self.execute_block(sync.body.statements, self.current_env)
            return 0
        except CorpHardStop as hs:
            return hs.code

    def execute(self, stmt: Stmt):
        method_name = f"visit_{stmt.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(stmt)

    def evaluate(self, expr: Expr) -> Any:
        method_name = f"visit_{expr.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(expr)

    def generic_visit(self, node: ASTNode):
        raise CorpRuntimeError(
            f"Unhandled AST node during executive execution: {node.__class__.__name__}",
            line=getattr(node, 'line', 1),
            column=getattr(node, 'column', 1),
            source_code=self.source_code,
            file_path=self.file_path
        )

    # --- Statement Visitors ---

    def visit_BlockStmt(self, stmt: BlockStmt):
        new_env = Environment(parent=self.current_env, name="CorporateSubScope")
        return self.execute_block(stmt.statements, new_env)

    def execute_block(self, statements: List[Stmt], env: Environment):
        prev_env = self.current_env
        self.current_env = env
        try:
            for statement in statements:
                self.execute(statement)
        finally:
            self.current_env = prev_env

    def visit_QuarterlyDeliverablesStmt(self, stmt: QuarterlyDeliverablesStmt):
        mod_env = Environment(parent=self.current_env, name=f"Module_{stmt.name or 'Deliverables'}")
        self.execute_block(stmt.body.statements, mod_env)
        if stmt.name:
            self.current_env.define(stmt.name, CorpModule(stmt.name, mod_env), is_core=True)

    def visit_SyncAlignmentStmt(self, stmt: SyncAlignmentStmt):
        return self.visit_BlockStmt(stmt.body)

    def visit_HardStopStmt(self, stmt: HardStopStmt):
        exit_code = 0
        if stmt.exit_code:
            code_val = self.evaluate(stmt.exit_code)
            if isinstance(code_val, (int, float)):
                exit_code = int(code_val)
        raise CorpHardStop(exit_code)

    def visit_ActionItemStmt(self, stmt: ActionItemStmt):
        val = None
        if stmt.initializer is not None:
            val = self.evaluate(stmt.initializer)
        self.current_env.define(stmt.name, val, is_core=False)

    def visit_CoreCompetencyStmt(self, stmt: CoreCompetencyStmt):
        val = self.evaluate(stmt.initializer)
        self.current_env.define(stmt.name, val, is_core=True)

    def visit_RestructureStmt(self, stmt: RestructureStmt):
        val = self.evaluate(stmt.value)
        self.current_env.assign(
            stmt.name,
            val,
            line=stmt.line,
            col=stmt.column,
            source_code=self.source_code,
            file_path=self.file_path
        )
        return val

    def visit_PromoteStmt(self, stmt: PromoteStmt):
        curr = self.current_env.get(
            stmt.name,
            line=stmt.line,
            col=stmt.column,
            source_code=self.source_code,
            file_path=self.file_path
        )
        if not isinstance(curr, (int, float)):
            raise CorpTypeError(
                f"Cannot promote non-numeric action item '{stmt.name}' (current value: {corp_stringify(curr)}).",
                line=stmt.line,
                column=stmt.column,
                source_code=self.source_code,
                file_path=self.file_path
            )
        new_val = curr + stmt.amount
        self.current_env.assign(
            stmt.name,
            new_val,
            line=stmt.line,
            col=stmt.column,
            source_code=self.source_code,
            file_path=self.file_path
        )
        return new_val

    def visit_DemoteStmt(self, stmt: DemoteStmt):
        curr = self.current_env.get(
            stmt.name,
            line=stmt.line,
            col=stmt.column,
            source_code=self.source_code,
            file_path=self.file_path
        )
        if not isinstance(curr, (int, float)):
            raise CorpTypeError(
                f"Cannot demote non-numeric action item '{stmt.name}' (current value: {corp_stringify(curr)}).",
                line=stmt.line,
                column=stmt.column,
                source_code=self.source_code,
                file_path=self.file_path
            )
        new_val = curr - stmt.amount
        self.current_env.assign(
            stmt.name,
            new_val,
            line=stmt.line,
            col=stmt.column,
            source_code=self.source_code,
            file_path=self.file_path
        )
        return new_val

    def visit_LayoffsStmt(self, stmt: LayoffsStmt):
        return self.current_env.layoffs(
            line=stmt.line,
            col=stmt.column,
            source_code=self.source_code,
            file_path=self.file_path
        )

    def visit_AsPerOurDiscussionStmt(self, stmt: AsPerOurDiscussionStmt):
        cond_val = self.evaluate(stmt.condition)
        if self._is_truthy(cond_val):
            self.execute(stmt.then_branch)
        elif stmt.pivot_branch is not None:
            self.execute(stmt.pivot_branch)

    def visit_CircleBackStmt(self, stmt: CircleBackStmt):
        while self._is_truthy(self.evaluate(stmt.condition)):
            try:
                self.execute(stmt.body)
            except CorpBreak:
                break
            except CorpContinue:
                continue

    def visit_TouchEveryBaseStmt(self, stmt: TouchEveryBaseStmt):
        collection = self.evaluate(stmt.collection)
        if not isinstance(collection, (list, tuple, str)):
            raise CorpTypeError(
                f"Cannot touch base over non-iterable stakeholder collection of type {type(collection).__name__}.",
                line=stmt.line,
                column=stmt.column,
                source_code=self.source_code,
                file_path=self.file_path
            )

        loop_env = Environment(parent=self.current_env, name="TouchEveryBaseLoopScope")
        prev_env = self.current_env
        self.current_env = loop_env
        try:
            for item in collection:
                loop_env.define(stmt.item_name, item, is_core=False)
                try:
                    self.execute(stmt.body)
                except CorpBreak:
                    break
                except CorpContinue:
                    continue
        finally:
            self.current_env = prev_env

    def visit_TableThisStmt(self, stmt: TableThisStmt):
        raise CorpBreak()

    def visit_PushToNextSprintStmt(self, stmt: PushToNextSprintStmt):
        raise CorpContinue()

    def visit_TouchBaseStmt(self, stmt: TouchBaseStmt):
        outputs = [corp_stringify(self.evaluate(arg)) for arg in stmt.arguments]
        print(" ".join(outputs))

    def visit_BroadcastAllHandsStmt(self, stmt: BroadcastAllHandsStmt):
        outputs = [corp_stringify(self.evaluate(arg)) for arg in stmt.arguments]
        msg = " ".join(outputs)
        is_tty = hasattr(sys.stderr, 'isatty') and sys.stderr.isatty()
        RED = "\033[1;31m" if is_tty else ""
        BOLD = "\033[1m" if is_tty else ""
        RESET = "\033[0m" if is_tty else ""
        print(f"{RED}{BOLD}[ALL-HANDS BROADCAST]{RESET} {msg}", file=sys.stderr)

    def visit_DelegateStmt(self, stmt: DelegateStmt):
        func = CorpFunction(declaration=stmt, closure=self.current_env, is_delegate=True)
        self.current_env.define(stmt.name, func, is_core=False)

    def visit_DeliverableStmt(self, stmt: DeliverableStmt):
        val = None
        if stmt.value is not None:
            val = self.evaluate(stmt.value)
        raise CorpReturn(val)

    def visit_RiskMitigationStmt(self, stmt: RiskMitigationStmt):
        try:
            self.visit_BlockStmt(stmt.try_body)
        except CorpOptOutException as opt_err:
            catch_env = Environment(parent=self.current_env, name="RiskMitigationScope")
            catch_env.define(stmt.error_param, opt_err.value, is_core=False)
            self.execute_block(stmt.catch_body.statements, catch_env)
        except Exception as ex:
            catch_env = Environment(parent=self.current_env, name="RiskMitigationScope")
            catch_env.define(stmt.error_param, str(ex), is_core=False)
            self.execute_block(stmt.catch_body.statements, catch_env)

    def visit_OptOutStmt(self, stmt: OptOutStmt):
        val = "Unspecified executive opt-out"
        if stmt.value is not None:
            val = self.evaluate(stmt.value)
        raise CorpOptOutException(val, line=stmt.line, column=stmt.column)

    def visit_ExprStmt(self, stmt: ExprStmt):
        return self.evaluate(stmt.expression)

    # --- Expression Visitors ---

    def visit_LiteralExpr(self, expr: LiteralExpr) -> Any:
        return expr.value

    def visit_ArrayExpr(self, expr: ArrayExpr) -> List[Any]:
        return [self.evaluate(elem) for elem in expr.elements]

    def visit_IdentifierExpr(self, expr: IdentifierExpr) -> Any:
        return self.current_env.get(
            expr.name,
            line=expr.line,
            col=expr.column,
            source_code=self.source_code,
            file_path=self.file_path
        )

    def visit_IndexExpr(self, expr: IndexExpr) -> Any:
        target = self.evaluate(expr.target)
        idx = self.evaluate(expr.index)
        if isinstance(target, (list, tuple, str)):
            if not isinstance(idx, int):
                raise CorpTypeError(
                    f"Array index must be a numeric integer, received {type(idx).__name__}.",
                    line=expr.line,
                    column=expr.column,
                    source_code=self.source_code,
                    file_path=self.file_path
                )
            if idx < 0 or idx >= len(target):
                raise CorpRuntimeError(
                    f"Index {idx} is outside the allocated bandwidth bounds of collection (length {len(target)}).",
                    line=expr.line,
                    column=expr.column,
                    source_code=self.source_code,
                    file_path=self.file_path,
                    incident_type="OUT_OF_BOUNDS_BANDWIDTH_EXCEPTION"
                )
            return target[idx]
        elif isinstance(target, CorpModule):
            return target.environment.get(str(idx), line=expr.line, col=expr.column, source_code=self.source_code, file_path=self.file_path)
        raise CorpTypeError(
            f"Cannot index into non-collection resource of type {type(target).__name__}.",
            line=expr.line,
            column=expr.column,
            source_code=self.source_code,
            file_path=self.file_path
        )

    def visit_PleaseAdviseExpr(self, expr: PleaseAdviseExpr) -> str:
        prompt_str = ""
        if expr.prompt:
            prompt_str = str(self.evaluate(expr.prompt)) + " "
        try:
            return input(prompt_str)
        except EOFError:
            return ""

    def visit_UnaryExpr(self, expr: UnaryExpr) -> Any:
        operand = self.evaluate(expr.operand)
        op = expr.operator
        if op in ('!', 'not'):
            return not self._is_truthy(operand)
        if op == '-':
            if isinstance(operand, (int, float)):
                return -operand
            raise CorpTypeError(
                f"Unary '-' cannot be applied to non-numeric asset {type(operand).__name__}.",
                line=expr.line,
                column=expr.column,
                source_code=self.source_code,
                file_path=self.file_path
            )
        if op == '+':
            if isinstance(operand, (int, float)):
                return +operand
            return operand
        raise CorpRuntimeError(f"Unknown unary operator '{op}'", line=expr.line, column=expr.column, source_code=self.source_code, file_path=self.file_path)

    def visit_BinaryExpr(self, expr: BinaryExpr) -> Any:
        left = self.evaluate(expr.left)
        op = expr.operator

        # Short-circuit logical operators
        if op in ('||', 'or'):
            return left if self._is_truthy(left) else self.evaluate(expr.right)
        if op in ('&&', 'synergizes_with', 'and'):
            return self.evaluate(expr.right) if self._is_truthy(left) else left

        right = self.evaluate(expr.right)

        if op == '+':
            if isinstance(left, str) or isinstance(right, str):
                return corp_stringify(left) + corp_stringify(right)
            if isinstance(left, list) and isinstance(right, list):
                return left + right
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            raise CorpTypeError(
                f"Incompatible assets for addition: {type(left).__name__} + {type(right).__name__}",
                line=expr.line, column=expr.column, source_code=self.source_code, file_path=self.file_path
            )

        if op == '-':
            self._check_number_operands(op, left, right, expr)
            return left - right

        if op == '*':
            if isinstance(left, str) and isinstance(right, int):
                return left * right
            if isinstance(left, list) and isinstance(right, int):
                return left * right
            self._check_number_operands(op, left, right, expr)
            return left * right

        if op == '/':
            self._check_number_operands(op, left, right, expr)
            if right == 0:
                raise CorpRuntimeError(
                    "Division by zero is not aligned with our Q3 growth objectives.",
                    line=expr.line, column=expr.column,
                    source_code=self.source_code, file_path=self.file_path,
                    incident_type="ZERO_DIVIDEND_PERFORMANCE_ANOMALY"
                )
            res = left / right
            return int(res) if res.is_integer() else res

        if op == '%':
            self._check_number_operands(op, left, right, expr)
            if right == 0:
                raise CorpRuntimeError(
                    "Modulo by zero encountered during KPI calculation.",
                    line=expr.line, column=expr.column,
                    source_code=self.source_code, file_path=self.file_path
                )
            return left % right

        if op == '==':
            return left == right
        if op == '!=':
            return left != right
        if op == '<':
            self._check_comparable_operands(op, left, right, expr)
            return left < right
        if op == '<=':
            self._check_comparable_operands(op, left, right, expr)
            return left <= right
        if op == '>':
            self._check_comparable_operands(op, left, right, expr)
            return left > right
        if op == '>=':
            self._check_comparable_operands(op, left, right, expr)
            return left >= right

        raise CorpRuntimeError(f"Unsupported corporate operator '{op}'.", line=expr.line, column=expr.column, source_code=self.source_code, file_path=self.file_path)

    def visit_CallExpr(self, expr: CallExpr) -> Any:
        callee = self.evaluate(expr.callee)
        args = [self.evaluate(arg) for arg in expr.arguments]

        if not hasattr(callee, 'call'):
            callee_name = getattr(expr.callee, 'name', str(callee))
            raise CorpTypeError(
                f"Attempted to loop in non-callable entity '{callee_name}'. Please verify cross-functional credentials.",
                line=expr.line,
                column=expr.column,
                source_code=self.source_code,
                file_path=self.file_path
            )

        expected_arity = callee.arity()
        if expected_arity != -1 and len(args) != expected_arity:
            raise CorpRuntimeError(
                f"Delegate '{getattr(callee, 'name', 'function')}' expected {expected_arity} stakeholder deliverables, but received {len(args)}.",
                line=expr.line,
                column=expr.column,
                source_code=self.source_code,
                file_path=self.file_path,
                incident_type="STAKEHOLDER_PARAMETER_MISMATCH"
            )

        return callee.call(self, args)

    def _is_truthy(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, (str, list)):
            return len(value) > 0
        return True

    def _check_number_operands(self, op: str, left: Any, right: Any, expr: ASTNode):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise CorpTypeError(
            f"Arithmetic operator '{op}' requires numeric performance assets, received {type(left).__name__} and {type(right).__name__}.",
            line=expr.line, column=expr.column, source_code=self.source_code, file_path=self.file_path
        )

    def _check_comparable_operands(self, op: str, left: Any, right: Any, expr: ASTNode):
        if type(left) == type(right) and isinstance(left, (int, float, str)):
            return
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise CorpTypeError(
            f"Cannot evaluate comparison '{op}' across disparate business units ({type(left).__name__} vs {type(right).__name__}).",
            line=expr.line, column=expr.column, source_code=self.source_code, file_path=self.file_path
        )
