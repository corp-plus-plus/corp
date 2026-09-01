"""
Token definitions and Corporate Lexicon for Corp++.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    # Program Lifecycle & Entry Point
    SYNC_ALIGNMENT = auto()          # sync_alignment
    QUARTERLY_DELIVERABLES = auto()  # quarterly_deliverables
    HARD_STOP = auto()              # hard_stop

    # State & Memory Management
    ACTION_ITEM = auto()            # action_item (let / mutable)
    CORE_COMPETENCY = auto()        # core_competency (const / immutable)
    RESTRUCTURE = auto()            # restructure (reassignment)
    PROMOTE = auto()                # promote (++ / increment)
    DEMOTE = auto()                 # demote (-- / decrement)
    LAYOFFS = auto()                # layoffs (scope memory flush / GC)

    # Control Flow & Branching
    AS_PER_OUR_DISCUSSION = auto()  # as_per_our_discussion (if)
    PIVOT = auto()                  # pivot (else)
    CIRCLE_BACK = auto()            # circle_back (while)
    TOUCH_EVERY_BASE = auto()       # touch_every_base (for...in)
    IN = auto()                     # in
    TABLE_THIS = auto()             # table_this (break)
    PUSH_TO_NEXT_SPRINT = auto()    # push_to_next_sprint (continue)

    # Standard I/O & Telemetry
    TOUCH_BASE = auto()             # touch_base (print/stdout)
    PLEASE_ADVISE = auto()          # please_advise (input/stdin)
    BROADCAST_ALL_HANDS = auto()    # broadcast_all_hands (stderr)

    # Procedures & Cross-Functional Collaboration
    DELEGATE = auto()               # delegate (function declaration)
    LOOP_IN = auto()                # loop_in (function invocation)
    DELIVERABLE = auto()            # deliverable (return)

    # Enterprise Risk Management (Exceptions)
    LETS_TAKE_THIS_OFFLINE = auto() # let's_take_this_offline (try)
    MITIGATE_RISK = auto()          # mitigate_risk (catch)
    OPT_OUT = auto()                # opt_out (throw)

    # Primitives & Literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    ALIGNED = auto()                # aligned (true)
    MISALIGNED = auto()             # misaligned (false)
    OUT_OF_OFFICE = auto()          # out_of_office (null / None)
    UNASSIGNED = auto()             # unassigned (undefined)

    # Operators & Delimiters
    ASSIGN = auto()                 # =
    PLUS = auto()                   # +
    MINUS = auto()                  # -
    MULTIPLY = auto()               # *
    DIVIDE = auto()                 # /
    MODULO = auto()                 # %
    EQUAL = auto()                  # ==
    NOT_EQUAL = auto()              # !=
    LESS_THAN = auto()              # <
    LESS_EQUAL = auto()             # <=
    GREATER_THAN = auto()           # >
    GREATER_EQUAL = auto()          # >=
    AND = auto()                    # && / synergizes_with / and
    OR = auto()                     # || / or
    NOT = auto()                    # ! / not

    LPAREN = auto()                 # (
    RPAREN = auto()                 # )
    LBRACE = auto()                 # {
    RBRACE = auto()                 # }
    LBRACKET = auto()               # [
    RBRACKET = auto()               # ]
    COMMA = auto()                  # ,
    DOT = auto()                    # .
    COLON = auto()                  # :
    SEMICOLON = auto()              # ;

    EOF = auto()


KEYWORDS = {
    'sync_alignment': TokenType.SYNC_ALIGNMENT,
    'quarterly_deliverables': TokenType.QUARTERLY_DELIVERABLES,
    'hard_stop': TokenType.HARD_STOP,

    'action_item': TokenType.ACTION_ITEM,
    'core_competency': TokenType.CORE_COMPETENCY,
    'restructure': TokenType.RESTRUCTURE,
    'promote': TokenType.PROMOTE,
    'demote': TokenType.DEMOTE,
    'layoffs': TokenType.LAYOFFS,

    'as_per_our_discussion': TokenType.AS_PER_OUR_DISCUSSION,
    'pivot': TokenType.PIVOT,
    'circle_back': TokenType.CIRCLE_BACK,
    'touch_every_base': TokenType.TOUCH_EVERY_BASE,
    'in': TokenType.IN,
    'table_this': TokenType.TABLE_THIS,
    'push_to_next_sprint': TokenType.PUSH_TO_NEXT_SPRINT,

    'touch_base': TokenType.TOUCH_BASE,
    'please_advise': TokenType.PLEASE_ADVISE,
    'broadcast_all_hands': TokenType.BROADCAST_ALL_HANDS,

    'delegate': TokenType.DELEGATE,
    'loop_in': TokenType.LOOP_IN,
    'deliverable': TokenType.DELIVERABLE,

    "let's_take_this_offline": TokenType.LETS_TAKE_THIS_OFFLINE,
    'lets_take_this_offline': TokenType.LETS_TAKE_THIS_OFFLINE,
    'mitigate_risk': TokenType.MITIGATE_RISK,
    'opt_out': TokenType.OPT_OUT,

    'aligned': TokenType.ALIGNED,
    'true': TokenType.ALIGNED,
    'misaligned': TokenType.MISALIGNED,
    'false': TokenType.MISALIGNED,
    'out_of_office': TokenType.OUT_OF_OFFICE,
    'null': TokenType.OUT_OF_OFFICE,
    'unassigned': TokenType.UNASSIGNED,
    'undefined': TokenType.UNASSIGNED,

    'synergizes_with': TokenType.AND,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'not': TokenType.NOT
}


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
    raw: str = ""

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"
