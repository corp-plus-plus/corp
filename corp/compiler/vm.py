"""
Corp++ Corporate Virtual Machine (CVM).
High-efficiency stack-based enterprise virtual machine.
"""

import sys
from typing import List, Any, Optional
from dataclasses import dataclass
from .opcodes import Opcode
from .compiler import BytecodeChunk
from corp.runtime.environment import Environment
from corp.runtime.values import CorpBuiltinFunction, corp_stringify
from corp.telemetry.corporate_error import (
    CorpRuntimeError,
    CorpTypeError,
    CorpHostileTakeoverError,
    CorpUnvettedResourceError,
    CorpOptOutException
)


@dataclass
class CallFrame:
    chunk: BytecodeChunk
    ip: int = 0
    stack_base: int = 0
    env: Optional[Environment] = None
    try_handlers: List[int] = None

    def __post_init__(self):
        if self.try_handlers is None:
            self.try_handlers = []


class CorpVM:
    def __init__(self, source_code: Optional[str] = None, file_path: Optional[str] = None):
        self.source_code = source_code
        self.file_path = file_path or "<corporate_memo.corp>"
        self.stack: List[Any] = []
        self.frames: List[CallFrame] = []
        self.global_env = Environment(name="CVM_GlobalEnterpriseScope")
        self._init_builtins()

    def _init_builtins(self):
        def _builtin_len(vm, args):
            if not args or not isinstance(args[0], (list, str)):
                return 0
            return len(args[0])

        def _builtin_range(vm, args):
            if len(args) == 1:
                return list(range(int(args[0])))
            elif len(args) >= 2:
                return list(range(int(args[0]), int(args[1])))
            return []

        self.global_env.define("headcount", CorpBuiltinFunction("headcount", _builtin_len, 1), is_core=True)
        self.global_env.define("range", CorpBuiltinFunction("range", _builtin_range, 2), is_core=True)

    def run(self, chunk: BytecodeChunk) -> Any:
        initial_frame = CallFrame(chunk=chunk, ip=0, stack_base=0, env=self.global_env)
        self.frames.append(initial_frame)

        while self.frames:
            frame = self.frames[-1]
            if frame.ip >= len(frame.chunk.code):
                self.frames.pop()
                continue

            inst = frame.chunk.code[frame.ip]
            frame.ip += 1

            op = inst.opcode
            arg = inst.arg
            line = inst.line
            col = inst.col

            if op == Opcode.OP_LOAD_CONST:
                self.stack.append(frame.chunk.constants[arg])

            elif op == Opcode.OP_POP:
                if self.stack:
                    self.stack.pop()

            elif op == Opcode.OP_DUP:
                if self.stack:
                    self.stack.append(self.stack[-1])

            elif op == Opcode.OP_DECLARE_VAR:
                val = self.stack.pop() if self.stack else None
                frame.env.define(arg, val, is_core=False)

            elif op == Opcode.OP_DECLARE_CORE:
                val = self.stack.pop() if self.stack else None
                frame.env.define(arg, val, is_core=True)

            elif op == Opcode.OP_LOAD_VAR:
                val = frame.env.get(arg, line=line, col=col, source_code=self.source_code, file_path=self.file_path)
                self.stack.append(val)

            elif op == Opcode.OP_STORE_VAR:
                val = self.stack[-1] if self.stack else None
                frame.env.assign(arg, val, line=line, col=col, source_code=self.source_code, file_path=self.file_path)

            elif op == Opcode.OP_PROMOTE:
                var_name, amount = arg
                curr = frame.env.get(var_name, line=line, col=col, source_code=self.source_code, file_path=self.file_path)
                if not isinstance(curr, (int, float)):
                    raise CorpTypeError(f"Cannot promote non-numeric variable '{var_name}'.", line=line, column=col, source_code=self.source_code, file_path=self.file_path)
                new_val = curr + amount
                frame.env.assign(var_name, new_val, line=line, col=col, source_code=self.source_code, file_path=self.file_path)

            elif op == Opcode.OP_DEMOTE:
                var_name, amount = arg
                curr = frame.env.get(var_name, line=line, col=col, source_code=self.source_code, file_path=self.file_path)
                if not isinstance(curr, (int, float)):
                    raise CorpTypeError(f"Cannot demote non-numeric variable '{var_name}'.", line=line, column=col, source_code=self.source_code, file_path=self.file_path)
                new_val = curr - amount
                frame.env.assign(var_name, new_val, line=line, col=col, source_code=self.source_code, file_path=self.file_path)

            elif op == Opcode.OP_LAYOFFS:
                frame.env.layoffs(line=line, col=col, source_code=self.source_code, file_path=self.file_path)

            elif op == Opcode.OP_BUILD_ARRAY:
                count = arg
                elems = [self.stack.pop() for _ in range(count)]
                elems.reverse()
                self.stack.append(elems)

            elif op == Opcode.OP_INDEX_GET:
                idx = self.stack.pop()
                target = self.stack.pop()
                if not isinstance(target, (list, tuple, str)) or not isinstance(idx, int):
                    raise CorpTypeError("Invalid indexing target or index value.", line=line, column=col, source_code=self.source_code, file_path=self.file_path)
                self.stack.append(target[idx])

            elif op == Opcode.OP_ADD:
                b = self.stack.pop()
                a = self.stack.pop()
                if isinstance(a, str) or isinstance(b, str):
                    self.stack.append(corp_stringify(a) + corp_stringify(b))
                elif isinstance(a, list) and isinstance(b, list):
                    self.stack.append(a + b)
                else:
                    self.stack.append(a + b)

            elif op == Opcode.OP_SUB:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)

            elif op == Opcode.OP_MUL:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)

            elif op == Opcode.OP_DIV:
                b = self.stack.pop()
                a = self.stack.pop()
                if b == 0:
                    raise CorpRuntimeError("Division by zero is not aligned with our Q3 growth objectives.", line=line, column=col, source_code=self.source_code, file_path=self.file_path)
                res = a / b
                self.stack.append(int(res) if res.is_integer() else res)

            elif op == Opcode.OP_MOD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a % b)

            elif op == Opcode.OP_NOT:
                a = self.stack.pop()
                self.stack.append(not a)

            elif op == Opcode.OP_NEG:
                a = self.stack.pop()
                self.stack.append(-a)

            elif op == Opcode.OP_EQUAL:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a == b)

            elif op == Opcode.OP_NOT_EQUAL:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a != b)

            elif op == Opcode.OP_LESS_THAN:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a < b)

            elif op == Opcode.OP_LESS_EQUAL:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a <= b)

            elif op == Opcode.OP_GREATER_THAN:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a > b)

            elif op == Opcode.OP_GREATER_EQUAL:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a >= b)

            elif op == Opcode.OP_JUMP:
                frame.ip = arg

            elif op == Opcode.OP_JUMP_IF_FALSE:
                cond = self.stack.pop()
                if not cond:
                    frame.ip = arg

            elif op == Opcode.OP_JUMP_IF_TRUE:
                cond = self.stack.pop()
                if cond:
                    frame.ip = arg

            elif op == Opcode.OP_TOUCH_BASE:
                count = arg
                args = [self.stack.pop() for _ in range(count)]
                args.reverse()
                print(" ".join(corp_stringify(x) for x in args))

            elif op == Opcode.OP_BROADCAST:
                count = arg
                args = [self.stack.pop() for _ in range(count)]
                args.reverse()
                msg = " ".join(corp_stringify(x) for x in args)
                is_tty = hasattr(sys.stderr, 'isatty') and sys.stderr.isatty()
                RED = "\033[1;31m" if is_tty else ""
                RESET = "\033[0m" if is_tty else ""
                print(f"{RED}[ALL-HANDS BROADCAST]{RESET} {msg}", file=sys.stderr)

            elif op == Opcode.OP_PLEASE_ADVISE:
                prompt_str = self.stack.pop() if self.stack else ""
                val = input(str(prompt_str) + (" " if prompt_str else ""))
                self.stack.append(val)

            elif op == Opcode.OP_MAKE_FUNCTION:
                func_chunk = self.stack.pop()
                name, params = arg
                # Pack into custom function wrapper
                class VMFunction:
                    def __init__(self, chunk, env):
                        self.chunk = chunk
                        self.closure = env
                        self.name = name

                    def arity(self):
                        return len(params)

                self.stack.append(VMFunction(func_chunk, frame.env))

            elif op == Opcode.OP_CALL:
                arg_count = arg
                callee = self.stack.pop()
                call_args = [self.stack.pop() for _ in range(arg_count)]
                call_args.reverse()

                if isinstance(callee, CorpBuiltinFunction):
                    res = callee.call(self, call_args)
                    self.stack.append(res)
                elif hasattr(callee, 'chunk'):
                    func_env = Environment(parent=callee.closure, name=f"VM_Delegate_{callee.name}")
                    for i, param_name in enumerate(callee.chunk.params):
                        param_val = call_args[i] if i < len(call_args) else None
                        func_env.define(param_name, param_val, is_core=False)
                    new_frame = CallFrame(chunk=callee.chunk, ip=0, stack_base=len(self.stack), env=func_env)
                    self.frames.append(new_frame)
                else:
                    raise CorpTypeError(f"Cannot loop in non-callable entity.", line=line, column=col, source_code=self.source_code, file_path=self.file_path)

            elif op == Opcode.OP_RETURN:
                ret_val = self.stack.pop() if self.stack else None
                popped_frame = self.frames.pop()
                if self.frames:
                    self.stack.append(ret_val)
                else:
                    return ret_val

            elif op == Opcode.OP_HARD_STOP:
                exit_code = self.stack.pop() if self.stack else 0
                return exit_code

            elif op == Opcode.OP_PUSH_TRY:
                frame.try_handlers.append(arg)

            elif op == Opcode.OP_POP_TRY:
                if frame.try_handlers:
                    frame.try_handlers.pop()

            elif op == Opcode.OP_OPT_OUT:
                val = self.stack.pop() if self.stack else "OptOut"
                if frame.try_handlers:
                    catch_ip = frame.try_handlers.pop()
                    self.stack.append(val)
                    frame.ip = catch_ip
                else:
                    raise CorpOptOutException(val, line=line, column=col)

        return 0
