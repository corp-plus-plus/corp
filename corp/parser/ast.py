"""
Corp++ AST (Abstract Syntax Tree) Node Definitions.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class ASTNode:
    line: int = 1
    column: int = 1


# --- Expressions ---

@dataclass
class Expr(ASTNode):
    pass


@dataclass
class LiteralExpr(Expr):
    value: Any = None


@dataclass
class ArrayExpr(Expr):
    elements: List[Expr] = field(default_factory=list)


@dataclass
class IdentifierExpr(Expr):
    name: str = ""


@dataclass
class BinaryExpr(Expr):
    left: Expr = field(default_factory=Expr)
    operator: str = ""
    right: Expr = field(default_factory=Expr)


@dataclass
class UnaryExpr(Expr):
    operator: str = ""
    operand: Expr = field(default_factory=Expr)


@dataclass
class CallExpr(Expr):
    callee: Expr = field(default_factory=Expr)
    arguments: List[Expr] = field(default_factory=list)
    is_loop_in: bool = False


@dataclass
class PleaseAdviseExpr(Expr):
    prompt: Optional[Expr] = None


@dataclass
class IndexExpr(Expr):
    target: Expr = field(default_factory=Expr)
    index: Expr = field(default_factory=Expr)


# --- Statements ---

@dataclass
class Stmt(ASTNode):
    pass


@dataclass
class BlockStmt(Stmt):
    statements: List[Stmt] = field(default_factory=list)


@dataclass
class Program(Stmt):
    statements: List[Stmt] = field(default_factory=list)


@dataclass
class QuarterlyDeliverablesStmt(Stmt):
    name: str = ""
    body: BlockStmt = field(default_factory=BlockStmt)


@dataclass
class SyncAlignmentStmt(Stmt):
    body: BlockStmt = field(default_factory=BlockStmt)


@dataclass
class HardStopStmt(Stmt):
    exit_code: Optional[Expr] = None


@dataclass
class ActionItemStmt(Stmt):
    name: str = ""
    initializer: Optional[Expr] = None


@dataclass
class CoreCompetencyStmt(Stmt):
    name: str = ""
    initializer: Expr = field(default_factory=Expr)


@dataclass
class RestructureStmt(Stmt):
    name: str = ""
    value: Expr = field(default_factory=Expr)


@dataclass
class PromoteStmt(Stmt):
    name: str = ""
    amount: int = 1


@dataclass
class DemoteStmt(Stmt):
    name: str = ""
    amount: int = 1


@dataclass
class LayoffsStmt(Stmt):
    pass


@dataclass
class AsPerOurDiscussionStmt(Stmt):
    condition: Expr = field(default_factory=Expr)
    then_branch: Stmt = field(default_factory=Stmt)
    pivot_branch: Optional[Stmt] = None


@dataclass
class CircleBackStmt(Stmt):
    condition: Expr = field(default_factory=Expr)
    body: Stmt = field(default_factory=Stmt)


@dataclass
class TouchEveryBaseStmt(Stmt):
    item_name: str = ""
    collection: Expr = field(default_factory=Expr)
    body: Stmt = field(default_factory=Stmt)


@dataclass
class TableThisStmt(Stmt):
    pass


@dataclass
class PushToNextSprintStmt(Stmt):
    pass


@dataclass
class TouchBaseStmt(Stmt):
    arguments: List[Expr] = field(default_factory=list)


@dataclass
class BroadcastAllHandsStmt(Stmt):
    arguments: List[Expr] = field(default_factory=list)


@dataclass
class DelegateStmt(Stmt):
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: BlockStmt = field(default_factory=BlockStmt)


@dataclass
class DeliverableStmt(Stmt):
    value: Optional[Expr] = None


@dataclass
class RiskMitigationStmt(Stmt):
    try_body: BlockStmt = field(default_factory=BlockStmt)
    error_param: str = "err"
    catch_body: BlockStmt = field(default_factory=BlockStmt)


@dataclass
class OptOutStmt(Stmt):
    value: Optional[Expr] = None


@dataclass
class ExprStmt(Stmt):
    expression: Expr = field(default_factory=Expr)
