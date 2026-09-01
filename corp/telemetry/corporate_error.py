"""
Enterprise Corporate Error & Telemetry System for Corp++.
Produces passive-aggressive corporate incident reports and PIP notices.
"""

import sys
import random
from typing import Optional, List


PASSIVE_AGGRESSIVE_PREFIXES = [
    "Per my last email,",
    "As previously aligned during our standup,",
    "Re: Re: Re: Urgent deliverables -",
    "To loop back on our prior discussion,",
    "With all due respect to the leadership team,",
    "Just gently bumping this thread,",
    "Per our Q3 strategic alignment memorandum,",
    "Friendly reminder from Corporate HR:",
    "Per the Employee Handbook Section 4.2.1,",
    "Circling back on this unresolved blocker,"
]

ACTION_ITEMS = [
    "Action Item: Please upskill before the next sprint planning session.",
    "Action Item: Submit an IT ticket to request additional mental bandwidth.",
    "Action Item: A Performance Improvement Plan (PIP) has been automatically scheduled with HR.",
    "Action Item: Escalate to your Level 2 Managing Director immediately.",
    "Action Item: Please attend mandatory cross-functional synergy retraining.",
    "Action Item: Review the slide deck on non-breaking business logic.",
    "Action Item: Align with stakeholders before attempting this operation again."
]


class CorpError(Exception):
    """Base exception for all Corp++ enterprise incidents."""
    def __init__(
        self,
        message: str,
        line: int = 1,
        column: int = 1,
        incident_type: str = "PERFORMANCE_DEFICIENCY",
        source_code: Optional[str] = None,
        file_path: Optional[str] = None
    ):
        self.message = message
        self.line = line
        self.column = column
        self.incident_type = incident_type
        self.source_code = source_code
        self.file_path = file_path or "<corporate_memo.corp>"
        self.incident_id = f"CORP-INC-{random.randint(10000, 99999)}"
        super().__init__(self.format_report())

    def format_report(self) -> str:
        prefix = random.choice(PASSIVE_AGGRESSIVE_PREFIXES)
        action_item = random.choice(ACTION_ITEMS)
        
        # Color codes (graceful fallback if not a TTY)
        is_tty = hasattr(sys.stderr, 'isatty') and sys.stderr.isatty()
        RED = "\033[1;31m" if is_tty else ""
        YELLOW = "\033[1;33m" if is_tty else ""
        CYAN = "\033[1;36m" if is_tty else ""
        BOLD = "\033[1m" if is_tty else ""
        RESET = "\033[0m" if is_tty else ""
        GRAY = "\033[90m" if is_tty else ""

        banner = f"{RED}╔══════════════════════════════════════════════════════════════════════════╗{RESET}\n"
        banner += f"{RED}║  [CORP++ ENTERPRISE INCIDENT REPORT] ID: {self.incident_id:<30} ║{RESET}\n"
        banner += f"{RED}║  ESCALATION LEVEL: {self.incident_type:<49} ║{RESET}\n"
        banner += f"{RED}╚══════════════════════════════════════════════════════════════════════════╝{RESET}\n"

        body = f"{YELLOW}{BOLD}{prefix}{RESET} {self.message}\n\n"
        body += f"{GRAY}Location:{RESET} {CYAN}{self.file_path}:{self.line}:{self.column}{RESET}\n"

        if self.source_code:
            lines = self.source_code.splitlines()
            if 1 <= self.line <= len(lines):
                target_line = lines[self.line - 1]
                body += f"\n  {GRAY}{self.line:4d} |{RESET} {target_line}\n"
                pointer_col = max(1, self.column)
                pointer = " " * (pointer_col - 1) + "^"
                body += f"       | {RED}{BOLD}{pointer}{RESET}\n"

        body += f"\n{YELLOW}{BOLD}Next Steps:{RESET} {action_item}\n"
        return f"\n{banner}{body}"


class CorpSyntaxError(CorpError):
    def __init__(self, message: str, line: int = 1, column: int = 1, source_code: Optional[str] = None, file_path: Optional[str] = None):
        super().__init__(
            message=f"Grammar misalignment detected: {message}",
            line=line,
            column=column,
            incident_type="UNSCHEDULED_SYNTAX_ALIGNMENT_DEBACLE",
            source_code=source_code,
            file_path=file_path
        )


class CorpRuntimeError(CorpError):
    def __init__(self, message: str, line: int = 1, column: int = 1, source_code: Optional[str] = None, file_path: Optional[str] = None, incident_type: str = "RUNTIME_BANDWIDTH_EXHAUSTION"):
        super().__init__(
            message=message,
            line=line,
            column=column,
            incident_type=incident_type,
            source_code=source_code,
            file_path=file_path
        )


class CorpTypeError(CorpRuntimeError):
    def __init__(self, message: str, line: int = 1, column: int = 1, source_code: Optional[str] = None, file_path: Optional[str] = None):
        super().__init__(
            message=f"Sub-optimal data synergy: {message}",
            line=line,
            column=column,
            incident_type="CROSS_FUNCTIONAL_TYPE_MISALIGNMENT",
            source_code=source_code,
            file_path=file_path
        )


class CorpHostileTakeoverError(CorpRuntimeError):
    def __init__(self, var_name: str, line: int = 1, column: int = 1, source_code: Optional[str] = None, file_path: Optional[str] = None):
        super().__init__(
            message=f"Hostile takeover attempt rejected! Cannot restructure '{var_name}' as it is declared as a non-negotiable 'core_competency'.",
            line=line,
            column=column,
            incident_type="HOSTILE_TAKEOVER_VIOLATION",
            source_code=source_code,
            file_path=file_path
        )


class CorpUnvettedResourceError(CorpRuntimeError):
    def __init__(self, var_name: str, line: int = 1, column: int = 1, source_code: Optional[str] = None, file_path: Optional[str] = None):
        super().__init__(
            message=f"Unvetted resource allocation: Variable '{var_name}' has not completed corporate onboarding or was eliminated during recent layoffs.",
            line=line,
            column=column,
            incident_type="UNVETTED_RESOURCE_ALLOCATION",
            source_code=source_code,
            file_path=file_path
        )


class CorpOptOutException(Exception):
    """Represents an intentional 'opt_out' (throw) in Corp++."""
    def __init__(self, value: any, line: int = 1, column: int = 1):
        self.value = value
        self.line = line
        self.column = column
        super().__init__(str(value))


class CorpHardStop(Exception):
    """Represents a clean program exit triggered by 'hard_stop'."""
    def __init__(self, code: int = 0):
        self.code = code
        super().__init__(f"Program reached a clean hard stop with exit code {code}.")


class CorpReturn(Exception):
    """Represents a function return value ('deliverable')."""
    def __init__(self, value: any):
        self.value = value
        super().__init__("Corporate deliverable ready.")


class CorpBreak(Exception):
    """Represents 'table_this'."""
    pass


class CorpContinue(Exception):
    """Represents 'push_to_next_sprint'."""
    pass
