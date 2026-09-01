"""
Corp++ Bytecode Compiler.
Translates Corp++ AST into enterprise bytecode chunks.
"""

from typing import List, Any, Dict, Optional
from dataclasses import dataclass, field
from .opcodes import Opcode
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


@dataclass
class Instruction:
    opcode: Opcode
    arg: Any = None
    line: int = 1
    col: int = 1


@dataclass
class BytecodeChunk:
    name: str = "<main>"
    code: List[Instruction] = field(default_factory=list)
    constants: List[Any] = field(default_factory=list)
    params: List[str] = field(default_factory=list)

    def add_constant(self, val: Any) -> int:
        for idx, c in enumerate(self.constants):
            if c == val and type(c) == type(val):
                return idx
        self.constants.append(val)
        return len(self.constants) - 1

    def emit(self, opcode: Opcode, arg: Any = None, line: int = 1, col: int = 1) -> int:
        self.code.append(Instruction(opcode, arg, line, col))
        return len(self.code) - 1

    def disassemble(self) -> str:
        lines = [f"=== Strategic Bytecode Chunk: {self.name} ==="]
        for idx, inst in enumerate(self.code):
            arg_str = f" {inst.arg!r}" if inst.arg is not None else ""
            lines.append(f"{idx:04d}  {inst.opcode.name:<22}{arg_str}")
        return "\n".join(lines)


class Compiler:
    def __init__(self, source_code: Optional[str] = None, file_path: Optional[str] = None):
        self.source_code = source_code
        self.file_path = file_path or "<corporate_memo.corp>"
        self.chunk = BytecodeChunk()
        self.loop_starts: List[int] = []
        self.loop_break_jumps: List[List[int]] = []

    def compile(self, program: Program) -> BytecodeChunk:
        # Separate sync_alignment from declarations
        sync_stmts = []
        for stmt in program.statements:
            if isinstance(stmt, SyncAlignmentStmt):
                sync_stmts.append(stmt)
            else:
                self.compile_stmt(stmt)

        for sync in sync_stmts:
            for s in sync.body.statements:
                self.compile_stmt(s)

        self.chunk.emit(Opcode.OP_LOAD_CONST, self.chunk.add_constant(0))
        self.chunk.emit(Opcode.OP_RETURN)
        return self.chunk

    def compile_stmt(self, stmt: Stmt):
        method = getattr(self, f"compile_{stmt.__class__.__name__}", None)
        if method:
            method(stmt)
        else:
            raise NotImplementedError(f"Compiler missing handler for {stmt.__class__.__name__}")

    def compile_ActionItemStmt(self, stmt: ActionItemStmt):
        if stmt.initializer:
            self.compile_expr(stmt.initializer)
        else:
            self.chunk.emit(Opcode.OP_LOAD_CONST, self.chunk.add_constant(None), stmt.line, stmt.column)
        self.chunk.emit(Opcode.OP_DECLARE_VAR, stmt.name, stmt.line, stmt.column)

    def compile_CoreCompetencyStmt(self, stmt: CoreCompetencyStmt):
        self.compile_expr(stmt.initializer)
        self.chunk.emit(Opcode.OP_DECLARE_CORE, stmt.name, stmt.line, stmt.column)

    def compile_RestructureStmt(self, stmt: RestructureStmt):
        self.compile_expr(stmt.value)
        self.chunk.emit(Opcode.OP_STORE_VAR, stmt.name, stmt.line, stmt.column)

    def compile_PromoteStmt(self, stmt: PromoteStmt):
        self.chunk.emit(Opcode.OP_PROMOTE, (stmt.name, stmt.amount), stmt.line, stmt.column)

    def compile_DemoteStmt(self, stmt: DemoteStmt):
        self.chunk.emit(Opcode.OP_DEMOTE, (stmt.name, stmt.amount), stmt.line, stmt.column)

    def compile_LayoffsStmt(self, stmt: LayoffsStmt):
        self.chunk.emit(Opcode.OP_LAYOFFS, None, stmt.line, stmt.column)

    def compile_BlockStmt(self, stmt: BlockStmt):
        for s in stmt.statements:
            self.compile_stmt(s)

    def compile_AsPerOurDiscussionStmt(self, stmt: AsPerOurDiscussionStmt):
        self.compile_expr(stmt.condition)
        jump_false_idx = self.chunk.emit(Opcode.OP_JUMP_IF_FALSE, None, stmt.line, stmt.column)

        self.compile_stmt(stmt.then_branch)

        if stmt.pivot_branch:
            jump_end_idx = self.chunk.emit(Opcode.OP_JUMP, None)
            self.chunk.code[jump_false_idx].arg = len(self.chunk.code)
            self.compile_stmt(stmt.pivot_branch)
            self.chunk.code[jump_end_idx].arg = len(self.chunk.code)
        else:
            self.chunk.code[jump_false_idx].arg = len(self.chunk.code)

    def compile_CircleBackStmt(self, stmt: CircleBackStmt):
        loop_start = len(self.chunk.code)
        self.loop_starts.append(loop_start)
        self.loop_break_jumps.append([])

        self.compile_expr(stmt.condition)
        exit_jump = self.chunk.emit(Opcode.OP_JUMP_IF_FALSE, None, stmt.line, stmt.column)

        self.compile_stmt(stmt.body)
        self.chunk.emit(Opcode.OP_JUMP, loop_start)

        loop_end = len(self.chunk.code)
        self.chunk.code[exit_jump].arg = loop_end
        for break_idx in self.loop_break_jumps.pop():
            self.chunk.code[break_idx].arg = loop_end
        self.loop_starts.pop()

    def compile_TouchEveryBaseStmt(self, stmt: TouchEveryBaseStmt):
        # Desugar into while loop over array
        # 1. Load collection
        self.compile_expr(stmt.collection)
        coll_const = f"__coll_{stmt.line}_{stmt.column}"
        idx_const = f"__idx_{stmt.line}_{stmt.column}"

        self.chunk.emit(Opcode.OP_DECLARE_VAR, coll_const)
        self.chunk.emit(Opcode.OP_LOAD_CONST, self.chunk.add_constant(0))
        self.chunk.emit(Opcode.OP_DECLARE_VAR, idx_const)

        loop_start = len(self.chunk.code)
        self.loop_starts.append(loop_start)
        self.loop_break_jumps.append([])

        # Condition: idx < len(coll)
        self.chunk.emit(Opcode.OP_LOAD_VAR, idx_const)
        self.chunk.emit(Opcode.OP_LOAD_VAR, coll_const)
        self.chunk.emit(Opcode.OP_LOAD_VAR, "headcount")
        self.chunk.emit(Opcode.OP_CALL, 1)
        self.chunk.emit(Opcode.OP_LESS_THAN)
        exit_jump = self.chunk.emit(Opcode.OP_JUMP_IF_FALSE, None)

        # Body: item = coll[idx]
        self.chunk.emit(Opcode.OP_LOAD_VAR, coll_const)
        self.chunk.emit(Opcode.OP_LOAD_VAR, idx_const)
        self.chunk.emit(Opcode.OP_INDEX_GET)
        self.chunk.emit(Opcode.OP_DECLARE_VAR, stmt.item_name)

        self.compile_stmt(stmt.body)

        # Increment idx
        self.chunk.emit(Opcode.OP_PROMOTE, (idx_const, 1))
        self.chunk.emit(Opcode.OP_JUMP, loop_start)

        loop_end = len(self.chunk.code)
        self.chunk.code[exit_jump].arg = loop_end
        for break_idx in self.loop_break_jumps.pop():
            self.chunk.code[break_idx].arg = loop_end
        self.loop_starts.pop()

    def compile_TableThisStmt(self, stmt: TableThisStmt):
        if not self.loop_break_jumps:
            raise Exception("Cannot 'table_this' outside of an active circular alignment sprint.")
        idx = self.chunk.emit(Opcode.OP_JUMP, None, stmt.line, stmt.column)
        self.loop_break_jumps[-1].append(idx)

    def compile_PushToNextSprintStmt(self, stmt: PushToNextSprintStmt):
        if not self.loop_starts:
            raise Exception("Cannot 'push_to_next_sprint' outside of an active circular alignment sprint.")
        self.chunk.emit(Opcode.OP_JUMP, self.loop_starts[-1], stmt.line, stmt.column)

    def compile_TouchBaseStmt(self, stmt: TouchBaseStmt):
        for arg in stmt.arguments:
            self.compile_expr(arg)
        self.chunk.emit(Opcode.OP_TOUCH_BASE, len(stmt.arguments), stmt.line, stmt.column)

    def compile_BroadcastAllHandsStmt(self, stmt: BroadcastAllHandsStmt):
        for arg in stmt.arguments:
            self.compile_expr(arg)
        self.chunk.emit(Opcode.OP_BROADCAST, len(stmt.arguments), stmt.line, stmt.column)

    def compile_DelegateStmt(self, stmt: DelegateStmt):
        child_compiler = Compiler(source_code=self.source_code, file_path=self.file_path)
        child_compiler.chunk.name = stmt.name
        child_compiler.chunk.params = stmt.params
        for s in stmt.body.statements:
            child_compiler.compile_stmt(s)
        child_compiler.chunk.emit(Opcode.OP_LOAD_CONST, child_compiler.chunk.add_constant(None))
        child_compiler.chunk.emit(Opcode.OP_RETURN)

        func_chunk_idx = self.chunk.add_constant(child_compiler.chunk)
        self.chunk.emit(Opcode.OP_LOAD_CONST, func_chunk_idx, stmt.line, stmt.column)
        self.chunk.emit(Opcode.OP_MAKE_FUNCTION, (stmt.name, stmt.params), stmt.line, stmt.column)
        self.chunk.emit(Opcode.OP_DECLARE_VAR, stmt.name, stmt.line, stmt.column)

    def compile_DeliverableStmt(self, stmt: DeliverableStmt):
        if stmt.value:
            self.compile_expr(stmt.value)
        else:
            self.chunk.emit(Opcode.OP_LOAD_CONST, self.chunk.add_constant(None), stmt.line, stmt.column)
        self.chunk.emit(Opcode.OP_RETURN, None, stmt.line, stmt.column)

    def compile_HardStopStmt(self, stmt: HardStopStmt):
        if stmt.exit_code:
            self.compile_expr(stmt.exit_code)
        else:
            self.chunk.emit(Opcode.OP_LOAD_CONST, self.chunk.add_constant(0), stmt.line, stmt.column)
        self.chunk.emit(Opcode.OP_HARD_STOP, None, stmt.line, stmt.column)

    def compile_RiskMitigationStmt(self, stmt: RiskMitigationStmt):
        try_jump = self.chunk.emit(Opcode.OP_PUSH_TRY, None, stmt.line, stmt.column)
        self.compile_stmt(stmt.try_body)
        self.chunk.emit(Opcode.OP_POP_TRY)
        skip_catch_jump = self.chunk.emit(Opcode.OP_JUMP, None)

        catch_start = len(self.chunk.code)
        self.chunk.code[try_jump].arg = catch_start
        self.chunk.emit(Opcode.OP_DECLARE_VAR, stmt.error_param)
        self.compile_stmt(stmt.catch_body)
        self.chunk.code[skip_catch_jump].arg = len(self.chunk.code)

    def compile_OptOutStmt(self, stmt: OptOutStmt):
        if stmt.value:
            self.compile_expr(stmt.value)
        else:
            self.chunk.emit(Opcode.OP_LOAD_CONST, self.chunk.add_constant("OptOut"), stmt.line, stmt.column)
        self.chunk.emit(Opcode.OP_OPT_OUT, None, stmt.line, stmt.column)

    def compile_ExprStmt(self, stmt: ExprStmt):
        self.compile_expr(stmt.expression)
        self.chunk.emit(Opcode.OP_POP, None, stmt.line, stmt.column)

    # --- Expressions ---

    def compile_expr(self, expr: Expr):
        method = getattr(self, f"compile_{expr.__class__.__name__}", None)
        if method:
            method(expr)
        else:
            raise NotImplementedError(f"Compiler missing handler for expr {expr.__class__.__name__}")

    def compile_LiteralExpr(self, expr: LiteralExpr):
        idx = self.chunk.add_constant(expr.value)
        self.chunk.emit(Opcode.OP_LOAD_CONST, idx, expr.line, expr.column)

    def compile_ArrayExpr(self, expr: ArrayExpr):
        for elem in expr.elements:
            self.compile_expr(elem)
        self.chunk.emit(Opcode.OP_BUILD_ARRAY, len(expr.elements), expr.line, expr.column)

    def compile_IdentifierExpr(self, expr: IdentifierExpr):
        self.chunk.emit(Opcode.OP_LOAD_VAR, expr.name, expr.line, expr.column)

    def compile_IndexExpr(self, expr: IndexExpr):
        self.compile_expr(expr.target)
        self.compile_expr(expr.index)
        self.chunk.emit(Opcode.OP_INDEX_GET, None, expr.line, expr.column)

    def compile_PleaseAdviseExpr(self, expr: PleaseAdviseExpr):
        if expr.prompt:
            self.compile_expr(expr.prompt)
        else:
            self.chunk.emit(Opcode.OP_LOAD_CONST, self.chunk.add_constant(""), expr.line, expr.column)
        self.chunk.emit(Opcode.OP_PLEASE_ADVISE, None, expr.line, expr.column)

    def compile_UnaryExpr(self, expr: UnaryExpr):
        self.compile_expr(expr.operand)
        if expr.operator in ('!', 'not'):
            self.chunk.emit(Opcode.OP_NOT, None, expr.line, expr.column)
        elif expr.operator == '-':
            self.chunk.emit(Opcode.OP_NEG, None, expr.line, expr.column)

    def compile_BinaryExpr(self, expr: BinaryExpr):
        self.compile_expr(expr.left)
        self.compile_expr(expr.right)
        op = expr.operator
        if op == '+':
            self.chunk.emit(Opcode.OP_ADD, None, expr.line, expr.column)
        elif op == '-':
            self.chunk.emit(Opcode.OP_SUB, None, expr.line, expr.column)
        elif op == '*':
            self.chunk.emit(Opcode.OP_MUL, None, expr.line, expr.column)
        elif op == '/':
            self.chunk.emit(Opcode.OP_DIV, None, expr.line, expr.column)
        elif op == '%':
            self.chunk.emit(Opcode.OP_MOD, None, expr.line, expr.column)
        elif op == '==':
            self.chunk.emit(Opcode.OP_EQUAL, None, expr.line, expr.column)
        elif op == '!=':
            self.chunk.emit(Opcode.OP_NOT_EQUAL, None, expr.line, expr.column)
        elif op == '<':
            self.chunk.emit(Opcode.OP_LESS_THAN, None, expr.line, expr.column)
        elif op == '<=':
            self.chunk.emit(Opcode.OP_LESS_EQUAL, None, expr.line, expr.column)
        elif op == '>':
            self.chunk.emit(Opcode.OP_GREATER_THAN, None, expr.line, expr.column)
        elif op == '>=':
            self.chunk.emit(Opcode.OP_GREATER_EQUAL, None, expr.line, expr.column)

    def compile_CallExpr(self, expr: CallExpr):
        for arg in expr.arguments:
            self.compile_expr(arg)
        self.compile_expr(expr.callee)
        self.chunk.emit(Opcode.OP_CALL, len(expr.arguments), expr.line, expr.column)
