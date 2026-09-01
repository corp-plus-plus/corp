"""
Corp++ Lexical Environment & Corporate Resource Allocation.
Implements corporate scoping, core competency immutability, and layoffs memory flush.
"""

import sys
from typing import Dict, Set, Any, Optional
from corp.telemetry.corporate_error import (
    CorpHostileTakeoverError,
    CorpUnvettedResourceError
)


class Environment:
    def __init__(self, parent: Optional['Environment'] = None, name: str = "CorporateGlobalScope"):
        self.parent = parent
        self.name = name
        self.values: Dict[str, Any] = {}
        self.core_competencies: Set[str] = set()
        self.is_verbose_telemetry = False

    def define(self, name: str, value: Any, is_core: bool = False):
        self.values[name] = value
        if is_core:
            self.core_competencies.add(name)
        elif name in self.core_competencies:
            self.core_competencies.remove(name)

    def get(self, name: str, line: int = 1, col: int = 1, source_code: Optional[str] = None, file_path: Optional[str] = None) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get(name, line, col, source_code, file_path)
        raise CorpUnvettedResourceError(
            var_name=name,
            line=line,
            column=col,
            source_code=source_code,
            file_path=file_path
        )

    def assign(self, name: str, value: Any, line: int = 1, col: int = 1, source_code: Optional[str] = None, file_path: Optional[str] = None):
        if name in self.values:
            if name in self.core_competencies:
                raise CorpHostileTakeoverError(
                    var_name=name,
                    line=line,
                    column=col,
                    source_code=source_code,
                    file_path=file_path
                )
            self.values[name] = value
            return
        if self.parent is not None:
            self.parent.assign(name, value, line, col, source_code, file_path)
            return
        raise CorpUnvettedResourceError(
            var_name=name,
            line=line,
            column=col,
            source_code=source_code,
            file_path=file_path
        )

    def layoffs(self, line: int = 1, col: int = 1, source_code: Optional[str] = None, file_path: Optional[str] = None) -> int:
        """
        Scope memory flush / garbage collection trigger.
        Terminates all mutable action_items in the current scope to optimize enterprise headcount.
        Retains only immutable core_competencies.
        """
        initial_count = len(self.values)
        non_core_keys = [k for k in self.values.keys() if k not in self.core_competencies]
        for key in non_core_keys:
            del self.values[key]
        severed_count = len(non_core_keys)

        is_tty = hasattr(sys.stderr, 'atty') and sys.stderr.isatty()
        GRAY = "\033[90m" if is_tty else ""
        YELLOW = "\033[33m" if is_tty else ""
        RESET = "\033[0m" if is_tty else ""

        print(
            f"{GRAY}[CORP++ HR MEMO - SCOPE FLUSH]{RESET} {YELLOW}Restructuring executed in '{self.name}'. "
            f"{severed_count} non-core action items eliminated to streamline Q3 operational efficiency.{RESET}",
            file=sys.stderr
        )
        return severed_count
