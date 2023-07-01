from typing import Optional, Any, List

from interpreter.error_handler import ErrorHandler
from interpreter.interpreter import GlobalScope, Var, Param, Function, Value, DataType
from interpreter.interpreter.builtins import Builtins, BUILTINS
from interpreter.interpreter.builtins.input import Input
from interpreter.interpreter.builtins.str import ToStr
from interpreter.interpreter.builtins.print import Print
from interpreter.position import Position
from interpreter.program import (
    IdentifierExpression,
    Literal,
    FunctionCallStatement,
    FunctionDefinitionStatement,
    MatchStatement,
    CaseDefaultStatement,
    CaseStatement,
    CaseIdentifier,
    LoopStatement,
    ConditionalStatement,
    Assignment,
    Block,
    Parameter,
    NegatedFactor,
    MultiplicativeExpression,
    AdditiveExpression,
    RelationalExpression,
    AndExpression,
    OrExpression,
    VarDefinition,
    ReturnStatement,
    RelationalOperator,
    AdditiveOperator,
    MultiplicativeOperator,
    UnaryOperator,
    LiteralType,
)
from interpreter.program.operator import CaseOperator
from interpreter.program.program import Program
from interpreter.program.statement import BreakStatement, ContinueStatement
from interpreter.visitor.visitor import Visitor

num = int | float

MAXIMUM_RECURSION_DEPTH = 900


class Interpreter(Visitor, Builtins):
    def __init__(self, error_handler: ErrorHandler):
        self._scope = GlobalScope()
        self._error_handler = error_handler
        self._last_value: Optional[Value] = None
        [self._scope.update(b()) for b in BUILTINS]
        self._last_position: Optional[Position] = None
        self._return: bool = False
        self._break: bool = False
        self._continue: bool = False
        self._recursion_depth: int = 0

    def visit_program(self, program: Program):
        for stmt in program.statements:
            stmt.accept(self)

    def visit_identifier_expression(self, expression: IdentifierExpression) -> Any:
        var = self._scope.look_up(expression.name)
        if var is None:
            self._error_handler.not_defined(expression.position, expression.name)
        self._last_value = var.value

    def visit_literal(self, expression: Literal):
        self._last_value = Value.from_literal(expression)

    def visit_or_expression(self, expression: OrExpression):
        expression.left.accept(self)
        left = self._last_value
        self._check_type(expression.position, left, DataType.BOOL)

        if left.value is True:
            self._last_value = Value(DataType.BOOL, True)
            return

        if expression.right is None:
            self._last_value = Value(DataType.BOOL, left.value)
            return

        expression.right.accept(self)
        right = self._last_value
        self._check_type(expression.position, right, DataType.BOOL)

        if right.value is True:
            self._last_value = Value(DataType.BOOL, True)
            return
        self._last_value = Value(DataType.BOOL, False)

    def visit_and_expression(self, expression: AndExpression):
        expression.left.accept(self)
        left = self._last_value
        self._check_type(expression.position, left, DataType.BOOL)

        if left.value is False:
            self._last_value = Value(DataType.BOOL, False)
            return

        if expression.right is None:
            self._last_value = Value(DataType.BOOL, left.value)
            return

        expression.right.accept(self)
        right = self._last_value
        self._check_type(expression.position, right, DataType.BOOL)

        if right.value is False:
            self._last_value = Value(DataType.BOOL, False)
            return
        self._last_value = Value(DataType.BOOL, True)

    def visit_relational_expression(self, expression: RelationalExpression):
        expression.left.accept(self)
        left = self._last_value
        expression.right.accept(self)
        right = self._last_value

        if left.type != right.type:
            self._error_handler.operation_bad_types(expression.position)
            return
        match expression.operator:
            case RelationalOperator.LESS:
                self._last_value = Value(DataType.BOOL, left.value < right.value)
                return
            case RelationalOperator.LESS_OR_EQ:
                self._last_value = Value(DataType.BOOL, left.value <= right.value)
                return
            case RelationalOperator.EQ:
                self._last_value = Value(DataType.BOOL, left.value == right.value)
                return
            case RelationalOperator.NOT_EQ:
                self._last_value = Value(DataType.BOOL, left.value != right.value)
                return
            case RelationalOperator.GREATER:
                self._last_value = Value(DataType.BOOL, left.value > right.value)
                return
            case RelationalOperator.GREATER_OR_EQ:
                self._last_value = Value(DataType.BOOL, left.value >= right.value)
                return
        self._last_value = Value(DataType.BOOL, False)

    def visit_additive_expression(self, expression: AdditiveExpression):
        expression.left.accept(self)
        left = self._last_value
        expression.right.accept(self)
        right = self._last_value

        if left.type != right.type:
            self._error_handler.operation_bad_types(expression.position)
            return
        match expression.operator:
            case AdditiveOperator.ADDITION:
                self._last_value = Value(DataType.NUM, left.value + right.value)
                return

            case AdditiveOperator.SUBTRACTION:
                self._last_value = Value(DataType.NUM, left.value - right.value)
                return

    def visit_multiplicative_expression(self, expression: MultiplicativeExpression):
        expression.left.accept(self)
        left = self._last_value
        expression.right.accept(self)
        right = self._last_value

        if left.type != right.type:
            self._error_handler.operation_bad_types(expression.position)
            return
        match expression.operator:
            case MultiplicativeOperator.MULTIPLICATION:
                self._last_value = Value(DataType.NUM, left.value * right.value)
                return
            case MultiplicativeOperator.DIVISION:
                if right.value == 0:
                    self._error_handler.zero_division(expression.position)
                    return
                self._last_value = Value(DataType.NUM, left.value / right.value)
            case MultiplicativeOperator.MODULO:
                if right.value == 0:
                    self._error_handler.zero_division(expression.position)
                    return
                self._last_value = Value(DataType.NUM, left.value % right.value)
                return

    def visit_negated_expression(self, expression: NegatedFactor):
        expression.factor.accept(self)
        operand = self._last_value
        match expression.operator:
            case UnaryOperator.NEGATION:
                if not operand.type == DataType.BOOL:
                    self._error_handler.operation_bad_types(expression.position)
                    return
                self._last_value = Value(DataType.BOOL, not operand.value)
                return
            case UnaryOperator.MINUS:
                if not operand.type == DataType.NUM:
                    self._error_handler.operation_bad_types(expression.position)
                    return
                self._last_value = Value(DataType.NUM, -operand.value)
                return

    def visit_parameter(self, parameter: Parameter):
        self._last_value = Param(parameter.name, parameter.mut)

    def visit_block(self, statements: Block) -> Any:
        for stmt in statements.statements:
            if self._return is True or self._break is True or self._continue is True:
                return
            if isinstance(stmt, (ReturnStatement, ContinueStatement, BreakStatement)):
                stmt.accept(self)
                return
            stmt.accept(self)

    def visit_conditional_statement(self, statement: ConditionalStatement):
        statement.condition.accept(self)
        if self._last_value.value:
            statement.if_block.accept(self)
        if statement.else_block is not None:
            statement.else_block.accept(self)

    def visit_loop_statement(self, statement: LoopStatement):
        statement.condition.accept(self)
        condition = self._last_value

        self._break = False

        while condition.value:
            self._continue = False
            statement.body.accept(self)
            if self._break is True:
                break

            statement.condition.accept(self)
            condition = self._last_value

    def visit_case_identifier(self, identifier: CaseIdentifier):
        pass

    def visit_data_type(self, statement: DataType):
        pass

    def visit_case_statement(self, statement: CaseStatement):
        for stmt in statement.body.statements:
            stmt.accept(self)

    def visit_case_default_statement(self, statement: CaseDefaultStatement):
        for stmt in statement.body.statements:
            stmt.accept(self)

    def visit_match_statement(self, statement: MatchStatement):
        match_args = []
        for arg in statement.args:
            arg.accept(self)
            match_args.append(self._last_value)
        if len(match_args) < 1:
            self._error_handler.missing_parameter(statement.position, "")

        case_stmt = (
            self._pick_case(match_args, statement.case_stmts) or statement.default_stmt
        )
        if case_stmt is None:
            return None

        if len(case_stmt.params) > len(match_args):
            self._error_handler.unexpected_argument(case_stmt.identifier.position)

        for arg, param in zip(match_args, case_stmt.params):
            var = Var(param.name, arg, param.mut)
            self._scope.update(var)
        case_stmt.accept(self)

    def _pick_case(
        self, args: List[Value], cases: List[CaseStatement]
    ) -> Optional[CaseStatement]:
        for case in cases:
            if (
                self._if_matches_parity(args, case.identifier)
                or self._if_matches_quarter(args, case.identifier)
                or self._if_matches_types(args, case.identifier)
                or self._if_matches_literal(args, case.identifier)
            ):
                return case
        return None

    def _if_matches_parity(self, args: List[Value], identifier: CaseIdentifier) -> bool:
        if not isinstance(identifier.identifier, CaseOperator):
            return False
        if identifier.identifier not in [CaseOperator.IS_ODD, CaseOperator.IS_EVEN]:
            return False

        self._check_type(identifier.position, args[0], DataType.NUM)
        match identifier.identifier:
            case CaseOperator.IS_ODD:
                return args[0].value % 2 != 0
            case CaseOperator.IS_EVEN:
                return args[0].value % 2 == 0

    def _if_matches_quarter(
        self, args: List[Value], identifier: CaseIdentifier
    ) -> bool:
        if not isinstance(identifier.identifier, CaseOperator):
            return False
        if identifier.identifier not in [
            CaseOperator.IS_QUARTERO,
            CaseOperator.IS_QUARTERTW,
            CaseOperator.IS_QUARTERTH,
            CaseOperator.IS_QUARTERF,
        ]:
            return False

        if len(args) < 2:
            self._error_handler.missing_parameter(
                identifier.position, "for Quarter operator"
            )
            pass
        self._check_type(identifier.position, args[0], DataType.NUM)
        self._check_type(identifier.position, args[1], DataType.NUM)

        match identifier.identifier:
            case CaseOperator.IS_QUARTERO:
                return (args[0].value > 0) and (args[1].value > 0)
            case CaseOperator.IS_QUARTERTW:
                return (args[0].value < 0) and (args[1].value > 0)
            case CaseOperator.IS_QUARTERTH:
                return (args[0].value < 0) and (args[1].value < 0)
            case CaseOperator.IS_QUARTERF:
                return (args[0].value > 0) and (args[1].value < 0)

    def _if_matches_types(self, args: List[Value], identifier: CaseIdentifier) -> bool:
        if not isinstance(identifier.identifier, LiteralType):
            return False
        return args[0].type == DataType.from_literal_type(identifier.identifier)

    def _if_matches_literal(
        self, args: List[Value], identifier: CaseIdentifier
    ) -> bool:
        if not isinstance(identifier.identifier, Literal):
            return False
        self._check_type(
            identifier.position,
            args[0],
            DataType.from_literal_type(identifier.identifier.type),
        )
        return args[0].value == identifier.identifier.value

    def visit_function_definition_statement(
        self, statement: FunctionDefinitionStatement
    ):
        name = statement.name
        params = []
        for p in statement.params:
            p.accept(self)
            params.append(self._last_value)
        fn = Function(name, params, statement.body)
        self._scope.update(fn)

    def visit_function_call_statement(self, statement: FunctionCallStatement):
        fn = self._scope.look_up(statement.name)
        if fn is None:
            self._error_handler.not_defined(statement.position, statement.name)
            return
        if not isinstance(fn, Function):
            self._error_handler.not_callable(statement.position, statement.name)
            return
        if (args_len := len(statement.arguments)) != (params_len := fn.params_len):
            if args_len < params_len:
                self._error_handler.missing_parameter(
                    statement.r_position, fn.params[args_len].name
                )
                return
            elif args_len > params_len:
                self._error_handler.unexpected_argument(statement.r_position)
                return
        args = []
        for arg, param in zip(statement.arguments, fn.params):
            arg.accept(self)
            args.append(Var(param.name, self._last_value, param.mut))

        self._recursion_depth += 1
        if self._recursion_depth > MAXIMUM_RECURSION_DEPTH:
            self._error_handler.max_recursion_depth(statement.position)
            return

        self._scope.fn_call(fn, *args)
        self._last_value = Value(DataType.NULL, None)
        if type(fn) != Function:
            self._last_position = statement.position
            fn.accept(self)
            self._scope.fn_return()
            return

        fn.body.accept(self)
        self._scope.fn_return()
        self._return = False
        self._recursion_depth -= 1

    def visit_return_statement(self, statement: ReturnStatement):
        statement.expression.accept(self)
        self._return = True

    def visit_var_definition(self, statement: VarDefinition):
        name = statement.name
        if self._scope.look_up(name):
            self._error_handler.already_defined(statement.position, name)
            return

        statement.expression.accept(self)
        expr = self._last_value
        mutable = statement.mut
        self._scope.update(Var(name, expr, mutable))

    def visit_assignment(self, statement: Assignment):
        name = statement.name

        if not (var := self._scope.look_up(name)):
            self._error_handler.not_defined(statement.position, name)
            return
        if not var.mutable:
            self._error_handler.assign_mut(statement.position, name)
            return
        statement.expression.accept(self)
        expr = self._last_value
        self._scope.update(Var(name, expr, var.mutable))

    def _check_type(self, position: Position, value: Value, expected: DataType) -> bool:
        if value.type != expected:
            self._error_handler.unexpected_type(position, value.type, expected)
            return False
        return True

    def visit_continue_statement(self, statement: ContinueStatement):
        self._continue = True

    def visit_break_statement(self, statement: BreakStatement):
        self._break = True

    def visit_print(self, fn: Print):
        value = self._scope.look_up("arg").value
        self._check_type(self._last_position, value, DataType.STR)
        print(value.value, end="")

    def visit_to_str(self, fn: ToStr):
        arg = self._scope.look_up("arg")
        match arg.value.type:
            case DataType.STR:
                self._last_value = arg
            case DataType.NUM:
                arg_val = arg.value.value
                value = int(arg_val) if arg_val // 1 == arg_val else arg_val
                value = str(value)
                self._last_value = Value(DataType.STR, value)
            case DataType.BOOL:
                value = "true" if arg.value.value else "false"
                self._last_value = Value(DataType.STR, value)
            case DataType.NULL:
                value = "null"
                self._last_value = Value(DataType.STR, value)

    def visit_input(self, fn: Input):
        res = input()
        self._last_value = Value(DataType.STR, res)
