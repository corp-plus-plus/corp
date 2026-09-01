"""
Corp++ Runtime Values & Corporate Callable Types.
"""

from typing import List, Any, Optional, Callable


class CorpValue:
    """Base class for Corp++ runtime values."""
    pass


class CorpCallable:
    """Callable interface for Corp++ functions and delegates."""
    def arity(self) -> int:
        raise NotImplementedError

    def call(self, interpreter, arguments: List[Any]):
        raise NotImplementedError


class CorpFunction(CorpCallable):
    def __init__(self, declaration, closure, is_delegate: bool = True):
        self.declaration = declaration
        self.closure = closure
        self.is_delegate = is_delegate

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter, arguments: List[Any]):
        from .environment import Environment
        from corp.telemetry.corporate_error import CorpReturn

        local_env = Environment(parent=self.closure, name=f"Delegate_{self.declaration.name}")
        for i, param_name in enumerate(self.declaration.params):
            arg_val = arguments[i] if i < len(arguments) else None
            local_env.define(param_name, arg_val, is_core=False)

        try:
            interpreter.execute_block(self.declaration.body.statements, local_env)
        except CorpReturn as ret:
            return ret.value
        return None

    def __repr__(self) -> str:
        return f"<CorporateDelegate {self.declaration.name}({', '.join(self.declaration.params)})>"


class CorpBuiltinFunction(CorpCallable):
    def __init__(self, name: str, fn: Callable, num_args: int = -1):
        self.name = name
        self.fn = fn
        self.num_args = num_args

    def arity(self) -> int:
        return self.num_args

    def call(self, interpreter, arguments: List[Any]):
        return self.fn(interpreter, arguments)

    def __repr__(self) -> str:
        return f"<CorporateBuiltin {self.name}>"


class CorpModule:
    def __init__(self, name: str, environment):
        self.name = name
        self.environment = environment

    def __repr__(self) -> str:
        return f"<QuarterlyDeliverablesModule {self.name}>"


def corp_stringify(value: Any) -> str:
    """Format runtime values in corporate nomenclature."""
    if value is None:
        return "out_of_office"
    if isinstance(value, bool):
        return "aligned" if value else "misaligned"
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return str(value)
    if isinstance(value, list):
        items = ", ".join(corp_stringify(v) for v in value)
        return f"[{items}]"
    return str(value)
