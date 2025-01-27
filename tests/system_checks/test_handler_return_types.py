import ast

from queuebie.system_checks.handler_return_types import CommandReturnVisitor


def test_handler_returns_single_command():
#     code = """@register_command
# def another_method():
#     return Command()
#     """

    code = """
from some_module import register_command
from queuebie.messages import Command

@register_command
def some_method():
    return [Command(), Command()]

@register_command
def another_method():
    return Command()

@register_command
def none_method():
    return None

@register_command
def invalid_method():
    return "invalid"

@register_command
def wrong_command_method():
    from another_module import Command
    return Command()
"""

    tree = ast.parse(code)

    visitor = CommandReturnVisitor()
    visitor.visit(tree)
