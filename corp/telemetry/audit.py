"""
Corp++ Enterprise Static Compliance & KPI Auditor.
Performs compliance audits against corporate best practices.
"""

from typing import Dict, Any
from corp.lexer.lexer import Lexer
from corp.lexer.tokens import TokenType
from corp.parser.parser import Parser
from corp.parser.ast import Program, SyncAlignmentStmt, CoreCompetencyStmt, ActionItemStmt, RiskMitigationStmt


def audit_source(source_code: str, file_path: str = "<audit.corp>") -> Dict[str, Any]:
    lexer = Lexer(source_code, file_path=file_path)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=source_code, file_path=file_path)
    program = parser.parse()

    total_tokens = len(tokens)
    action_items = sum(1 for t in tokens if t.type == TokenType.ACTION_ITEM)
    core_competencies = sum(1 for t in tokens if t.type == TokenType.CORE_COMPETENCY)
    risk_mitigations = sum(1 for t in tokens if t.type == TokenType.LETS_TAKE_THIS_OFFLINE)
    layoffs_count = sum(1 for t in tokens if t.type == TokenType.LAYOFFS)
    has_sync = any(isinstance(s, SyncAlignmentStmt) for s in program.statements)

    synergy_score = min(100, 50 + (core_competencies * 10) + (risk_mitigations * 15) - (layoffs_count * 5))
    esg_rating = "AAA (Executive Grade)" if synergy_score >= 80 else "BBB (Action Required)"

    return {
        "file_path": file_path,
        "total_tokens": total_tokens,
        "action_items": action_items,
        "core_competencies": core_competencies,
        "risk_mitigations": risk_mitigations,
        "layoffs_count": layoffs_count,
        "has_sync_alignment": has_sync,
        "synergy_score": synergy_score,
        "esg_compliance_rating": esg_rating
    }
