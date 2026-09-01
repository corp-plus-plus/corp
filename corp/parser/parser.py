"""
Corp++ Recursive Descent Parser.
Builds AST from tokens with enterprise syntax error reporting.
"""

from typing import List, Optional
from corp.lexer.tokens import Token, TokenType
from corp.telemetry.corporate_error import CorpSyntaxError
from .ast import (
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


class Parser:
    def __init__(self, tokens: List[Token], source_code: Optional[str] = None, file_path: Optional[str] = None):
        self.tokens = tokens
        self.source_code = source_code
        self.file_path = file_path or "<corporate_memo.corp>"
        self.current = 0

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        token = self.peek()
        raise CorpSyntaxError(
            message=message,
            line=token.line,
            column=token.column,
            source_code=self.source_code,
            file_path=self.file_path
        )

    def match_semicolon(self):
        """Consume optional semicolon."""
        if self.check(TokenType.SEMICOLON):
            self.advance()

    def parse(self) -> Program:
        statements: List[Stmt] = []
        while not self.is_at_end():
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        return Program(statements=statements, line=1, column=1)

    # --- Declarations & Statements ---

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.SYNC_ALIGNMENT):
                return self.sync_alignment_statement()
            if self.match(TokenType.QUARTERLY_DELIVERABLES):
                return self.quarterly_deliverables_statement()
            if self.match(TokenType.ACTION_ITEM):
                return self.action_item_declaration()
            if self.match(TokenType.CORE_COMPETENCY):
                return self.core_competency_declaration()
            if self.match(TokenType.DELEGATE):
                return self.delegate_declaration()
            return self.statement()
        except CorpSyntaxError:
            self.synchronize()
            raise

    def sync_alignment_statement(self) -> SyncAlignmentStmt:
        token = self.previous()
        body = self.block()
        return SyncAlignmentStmt(body=body, line=token.line, column=token.column)

    def quarterly_deliverables_statement(self) -> QuarterlyDeliverablesStmt:
        token = self.previous()
        name = ""
        if self.check(TokenType.IDENTIFIER):
            name = self.advance().value
        body = self.block()
        return QuarterlyDeliverablesStmt(name=name, body=body, line=token.line, column=token.column)

    def action_item_declaration(self) -> ActionItemStmt:
        token = self.previous()
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name after 'action_item'.")
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.expression()
        self.match_semicolon()
        return ActionItemStmt(name=name_token.value, initializer=initializer, line=token.line, column=token.column)

    def core_competency_declaration(self) -> CoreCompetencyStmt:
        token = self.previous()
        name_token = self.consume(TokenType.IDENTIFIER, "Expected constant name after 'core_competency'.")
        self.consume(TokenType.ASSIGN, "Core competencies must be initialized with '=' immediately upon allocation.")
        initializer = self.expression()
        self.match_semicolon()
        return CoreCompetencyStmt(name=name_token.value, initializer=initializer, line=token.line, column=token.column)

    def delegate_declaration(self) -> DelegateStmt:
        token = self.previous()
        name_token = self.consume(TokenType.IDENTIFIER, "Expected function name after 'delegate'.")
        self.consume(TokenType.LPAREN, "Expected '(' after delegate name for stakeholder parameters.")
        params: List[str] = []
        if not self.check(TokenType.RPAREN):
            while True:
                param_token = self.consume(TokenType.IDENTIFIER, "Expected parameter identifier.")
                params.append(param_token.value)
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expected ')' after delegate parameter list.")
        body = self.block()
        return DelegateStmt(name=name_token.value, params=params, body=body, line=token.line, column=token.column)

    def statement(self) -> Stmt:
        if self.match(TokenType.RESTRUCTURE):
            return self.restructure_statement()
        if self.match(TokenType.PROMOTE):
            return self.promote_statement()
        if self.match(TokenType.DEMOTE):
            return self.demote_statement()
        if self.match(TokenType.LAYOFFS):
            return self.layoffs_statement()
        if self.match(TokenType.AS_PER_OUR_DISCUSSION):
            return self.as_per_our_discussion_statement()
        if self.match(TokenType.CIRCLE_BACK):
            return self.circle_back_statement()
        if self.match(TokenType.TOUCH_EVERY_BASE):
            return self.touch_every_base_statement()
        if self.match(TokenType.TABLE_THIS):
            token = self.previous()
            self.match_semicolon()
            return TableThisStmt(line=token.line, column=token.column)
        if self.match(TokenType.PUSH_TO_NEXT_SPRINT):
            token = self.previous()
            self.match_semicolon()
            return PushToNextSprintStmt(line=token.line, column=token.column)
        if self.match(TokenType.TOUCH_BASE):
            return self.touch_base_statement()
        if self.match(TokenType.BROADCAST_ALL_HANDS):
            return self.broadcast_all_hands_statement()
        if self.match(TokenType.DELIVERABLE):
            return self.deliverable_statement()
        if self.match(TokenType.LETS_TAKE_THIS_OFFLINE):
            return self.risk_mitigation_statement()
        if self.match(TokenType.OPT_OUT):
            return self.opt_out_statement()
        if self.match(TokenType.HARD_STOP):
            return self.hard_stop_statement()
        if self.check(TokenType.LBRACE):
            return self.block()

        return self.expression_statement()

    def restructure_statement(self) -> RestructureStmt:
        token = self.previous()
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name to restructure.")
        self.consume(TokenType.ASSIGN, "Expected '=' in restructure assignment.")
        val = self.expression()
        self.match_semicolon()
        return RestructureStmt(name=name_token.value, value=val, line=token.line, column=token.column)

    def promote_statement(self) -> PromoteStmt:
        token = self.previous()
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name to promote.")
        self.match_semicolon()
        return PromoteStmt(name=name_token.value, amount=1, line=token.line, column=token.column)

    def demote_statement(self) -> DemoteStmt:
        token = self.previous()
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name to demote.")
        self.match_semicolon()
        return DemoteStmt(name=name_token.value, amount=1, line=token.line, column=token.column)

    def layoffs_statement(self) -> LayoffsStmt:
        token = self.previous()
        self.match_semicolon()
        return LayoffsStmt(line=token.line, column=token.column)

    def as_per_our_discussion_statement(self) -> AsPerOurDiscussionStmt:
        token = self.previous()
        self.consume(TokenType.LPAREN, "Expected '(' after 'as_per_our_discussion'.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after discussion condition.")
        then_branch = self.statement()
        pivot_branch = None
        if self.match(TokenType.PIVOT):
            pivot_branch = self.statement()
        return AsPerOurDiscussionStmt(
            condition=condition,
            then_branch=then_branch,
            pivot_branch=pivot_branch,
            line=token.line,
            column=token.column
        )

    def circle_back_statement(self) -> CircleBackStmt:
        token = self.previous()
        self.consume(TokenType.LPAREN, "Expected '(' after 'circle_back'.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after circle back condition.")
        body = self.statement()
        return CircleBackStmt(condition=condition, body=body, line=token.line, column=token.column)

    def touch_every_base_statement(self) -> TouchEveryBaseStmt:
        token = self.previous()
        has_paren = self.match(TokenType.LPAREN)
        item_token = self.consume(TokenType.IDENTIFIER, "Expected iteration variable name in 'touch_every_base'.")
        self.consume(TokenType.IN, "Expected 'in' keyword in 'touch_every_base' loop.")
        collection = self.expression()
        if has_paren:
            self.consume(TokenType.RPAREN, "Expected ')' after 'touch_every_base' expression.")
        body = self.statement()
        return TouchEveryBaseStmt(
            item_name=item_token.value,
            collection=collection,
            body=body,
            line=token.line,
            column=token.column
        )

    def touch_base_statement(self) -> TouchBaseStmt:
        token = self.previous()
        self.consume(TokenType.LPAREN, "Expected '(' after 'touch_base'.")
        args: List[Expr] = []
        if not self.check(TokenType.RPAREN):
            while True:
                args.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expected ')' after touch_base arguments.")
        self.match_semicolon()
        return TouchBaseStmt(arguments=args, line=token.line, column=token.column)

    def broadcast_all_hands_statement(self) -> BroadcastAllHandsStmt:
        token = self.previous()
        self.consume(TokenType.LPAREN, "Expected '(' after 'broadcast_all_hands'.")
        args: List[Expr] = []
        if not self.check(TokenType.RPAREN):
            while True:
                args.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expected ')' after broadcast_all_hands arguments.")
        self.match_semicolon()
        return BroadcastAllHandsStmt(arguments=args, line=token.line, column=token.column)

    def deliverable_statement(self) -> DeliverableStmt:
        token = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON) and not self.check(TokenType.RBRACE) and not self.is_at_end():
            value = self.expression()
        self.match_semicolon()
        return DeliverableStmt(value=value, line=token.line, column=token.column)

    def risk_mitigation_statement(self) -> RiskMitigationStmt:
        token = self.previous()
        try_body = self.block()
        self.consume(TokenType.MITIGATE_RISK, "Expected 'mitigate_risk' block following 'let\'s_take_this_offline'.")
        self.consume(TokenType.LPAREN, "Expected '(' after 'mitigate_risk'.")
        err_token = self.consume(TokenType.IDENTIFIER, "Expected error parameter identifier in 'mitigate_risk'.")
        self.consume(TokenType.RPAREN, "Expected ')' after error parameter.")
        catch_body = self.block()
        return RiskMitigationStmt(
            try_body=try_body,
            error_param=err_token.value,
            catch_body=catch_body,
            line=token.line,
            column=token.column
        )

    def opt_out_statement(self) -> OptOutStmt:
        token = self.previous()
        val = None
        if self.match(TokenType.LPAREN):
            val = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after opt_out reason.")
        elif not self.check(TokenType.SEMICOLON) and not self.check(TokenType.RBRACE) and not self.is_at_end():
            val = self.expression()
        self.match_semicolon()
        return OptOutStmt(value=val, line=token.line, column=token.column)

    def hard_stop_statement(self) -> HardStopStmt:
        token = self.previous()
        code = None
        if self.match(TokenType.LPAREN):
            code = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after hard_stop exit code.")
        elif not self.check(TokenType.SEMICOLON) and not self.check(TokenType.RBRACE) and not self.is_at_end():
            code = self.expression()
        self.match_semicolon()
        return HardStopStmt(exit_code=code, line=token.line, column=token.column)

    def block(self) -> BlockStmt:
        token = self.consume(TokenType.LBRACE, "Expected '{' to start corporate scope block.")
        statements: List[Stmt] = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        self.consume(TokenType.RBRACE, "Expected '}' to close corporate scope block.")
        return BlockStmt(statements=statements, line=token.line, column=token.column)

    def expression_statement(self) -> Stmt:
        token = self.peek()
        expr = self.expression()
        self.match_semicolon()
        return ExprStmt(expression=expr, line=token.line, column=token.column)

    # --- Expressions ---

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.logical_or()

        if self.match(TokenType.ASSIGN):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, IdentifierExpr):
                # Desugar `x = y` as a restructure
                return RestructureStmt(name=expr.name, value=value, line=equals.line, column=equals.column)
            raise CorpSyntaxError(
                "Invalid assignment target in corporate memo.",
                line=equals.line, column=equals.column,
                source_code=self.source_code, file_path=self.file_path
            )

        return expr

    def logical_or(self) -> Expr:
        expr = self.logical_and()
        while self.match(TokenType.OR):
            op = self.previous()
            right = self.logical_and()
            expr = BinaryExpr(left=expr, operator=op.raw or '||', right=right, line=op.line, column=op.column)
        return expr

    def logical_and(self) -> Expr:
        expr = self.equality()
        while self.match(TokenType.AND):
            op = self.previous()
            right = self.equality()
            expr = BinaryExpr(left=expr, operator=op.raw or '&&', right=right, line=op.line, column=op.column)
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.previous()
            right = self.comparison()
            expr = BinaryExpr(left=expr, operator=op.raw, right=right, line=op.line, column=op.column)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(TokenType.GREATER_THAN, TokenType.GREATER_EQUAL, TokenType.LESS_THAN, TokenType.LESS_EQUAL):
            op = self.previous()
            right = self.term()
            expr = BinaryExpr(left=expr, operator=op.raw, right=right, line=op.line, column=op.column)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous()
            right = self.factor()
            expr = BinaryExpr(left=expr, operator=op.raw, right=right, line=op.line, column=op.column)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.previous()
            right = self.unary()
            expr = BinaryExpr(left=expr, operator=op.raw, right=right, line=op.line, column=op.column)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.NOT, TokenType.MINUS, TokenType.PLUS):
            op = self.previous()
            right = self.unary()
            return UnaryExpr(operator=op.raw, operand=right, line=op.line, column=op.column)
        return self.call()

    def call(self) -> Expr:
        if self.match(TokenType.LOOP_IN):
            token = self.previous()
            self.consume(TokenType.LPAREN, "Expected '(' after 'loop_in'.")
            
            # loop_in(func(arg1, arg2)) or loop_in(func, arg1, arg2)
            callee_ident = self.consume(TokenType.IDENTIFIER, "Expected function name in 'loop_in'.")
            callee = IdentifierExpr(name=callee_ident.value, line=callee_ident.line, column=callee_ident.column)
            
            args: List[Expr] = []
            if self.match(TokenType.LPAREN):
                # nested parens format: loop_in(func(a, b))
                if not self.check(TokenType.RPAREN):
                    while True:
                        args.append(self.expression())
                        if not self.match(TokenType.COMMA):
                            break
                self.consume(TokenType.RPAREN, "Expected ')' inside loop_in call.")
                self.consume(TokenType.RPAREN, "Expected ')' after loop_in invocation.")
            else:
                # comma separated format: loop_in(func, a, b)
                if self.match(TokenType.COMMA):
                    while True:
                        args.append(self.expression())
                        if not self.match(TokenType.COMMA):
                            break
                self.consume(TokenType.RPAREN, "Expected ')' after loop_in invocation.")

            return CallExpr(callee=callee, arguments=args, is_loop_in=True, line=token.line, column=token.column)

        if self.match(TokenType.PLEASE_ADVISE):
            token = self.previous()
            prompt = None
            if self.match(TokenType.LPAREN):
                if not self.check(TokenType.RPAREN):
                    prompt = self.expression()
                self.consume(TokenType.RPAREN, "Expected ')' after 'please_advise'.")
            return PleaseAdviseExpr(prompt=prompt, line=token.line, column=token.column)

        expr = self.primary()

        while True:
            if self.match(TokenType.LPAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.LBRACKET):
                index_expr = self.expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after array index accessor.")
                expr = IndexExpr(target=expr, index=index_expr, line=expr.line, column=expr.column)
            else:
                break

        return expr

    def finish_call(self, callee: Expr) -> CallExpr:
        token = self.previous()
        args: List[Expr] = []
        if not self.check(TokenType.RPAREN):
            while True:
                args.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expected ')' after function arguments.")
        return CallExpr(callee=callee, arguments=args, is_loop_in=False, line=token.line, column=token.column)

    def primary(self) -> Expr:
        token = self.peek()

        if self.match(TokenType.ALIGNED, TokenType.MISALIGNED, TokenType.OUT_OF_OFFICE, TokenType.UNASSIGNED):
            return LiteralExpr(value=self.previous().value, line=token.line, column=token.column)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(value=self.previous().value, line=token.line, column=token.column)

        if self.match(TokenType.IDENTIFIER):
            return IdentifierExpr(name=self.previous().value, line=token.line, column=token.column)

        if self.match(TokenType.LBRACKET):
            elements: List[Expr] = []
            if not self.check(TokenType.RBRACKET):
                while True:
                    elements.append(self.expression())
                    if not self.match(TokenType.COMMA):
                        break
            self.consume(TokenType.RBRACKET, "Expected ']' after array elements.")
            return ArrayExpr(elements=elements, line=token.line, column=token.column)

        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after group expression.")
            return expr

        raise CorpSyntaxError(
            f"Unexpected corporate token '{token.raw or token.type.name}'.",
            line=token.line, column=token.column,
            source_code=self.source_code, file_path=self.file_path
        )

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.peek().type in (
                TokenType.SYNC_ALIGNMENT,
                TokenType.QUARTERLY_DELIVERABLES,
                TokenType.ACTION_ITEM,
                TokenType.CORE_COMPETENCY,
                TokenType.DELEGATE,
                TokenType.AS_PER_OUR_DISCUSSION,
                TokenType.CIRCLE_BACK,
                TokenType.TOUCH_EVERY_BASE,
                TokenType.TOUCH_BASE,
                TokenType.BROADCAST_ALL_HANDS,
                TokenType.HARD_STOP
            ):
                return
            self.advance()
