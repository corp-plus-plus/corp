"""
Corp++ Bytecode Instruction Set (Corporate Opcodes).
"""

from enum import Enum, auto


class Opcode(Enum):
    # Constants & Stack
    OP_LOAD_CONST = auto()       # Push constant from constants pool
    OP_POP = auto()              # Discard top of stack
    OP_DUP = auto()              # Duplicate top of stack

    # Variables & Environment
    OP_DECLARE_VAR = auto()      # Declare mutable action_item
    OP_DECLARE_CORE = auto()     # Declare immutable core_competency
    OP_LOAD_VAR = auto()         # Load variable value
    OP_STORE_VAR = auto()        # Reassign mutable variable
    OP_PROMOTE = auto()          # Increment variable by 1
    OP_DEMOTE = auto()           # Decrement variable by 1
    OP_LAYOFFS = auto()          # Scope memory flush

    # Collections
    OP_BUILD_ARRAY = auto()      # Build array from N stack items
    OP_INDEX_GET = auto()        # target[index]

    # Arithmetic & Logic
    OP_ADD = auto()              # +
    OP_SUB = auto()              # -
    OP_MUL = auto()              # *
    OP_DIV = auto()              # /
    OP_MOD = auto()              # %
    OP_NOT = auto()              # !
    OP_NEG = auto()              # - (unary)
    OP_EQUAL = auto()            # ==
    OP_NOT_EQUAL = auto()        # !=
    OP_LESS_THAN = auto()        # <
    OP_LESS_EQUAL = auto()       # <=
    OP_GREATER_THAN = auto()     # >
    OP_GREATER_EQUAL = auto()    # >=

    # Control Flow
    OP_JUMP = auto()             # Unconditional jump
    OP_JUMP_IF_FALSE = auto()    # Jump if falsy
    OP_JUMP_IF_TRUE = auto()     # Jump if truthy

    # I/O & Telemetry
    OP_TOUCH_BASE = auto()       # Print N arguments
    OP_BROADCAST = auto()        # Broadcast all-hands
    OP_PLEASE_ADVISE = auto()    # Prompt stdin input

    # Procedures & Calls
    OP_MAKE_FUNCTION = auto()    # Create closure / function object
    OP_CALL = auto()             # Invoke function with N args
    OP_RETURN = auto()           # Return from function

    # Exceptions & Halts
    OP_PUSH_TRY = auto()         # Push exception handler offset
    OP_POP_TRY = auto()          # Pop exception handler
    OP_OPT_OUT = auto()          # Throw exception
    OP_HARD_STOP = auto()        # Clean exit 0
