import ast
import logging

from queuebie.logger import get_logger


class CommandReturnVisitor(ast.NodeVisitor):
    """
    AST visitor to find methods with the `register_command` decorator
    """

    logger: logging.Logger

    def __init__(self):
        super().__init__()

        self.logger = get_logger()

    def visit_FunctionDef(self, node): # noqa: N802
        # Check if the `register_command` decorator is used
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "register_command":
                # Check the method's return value
                if isinstance(node.body[-1], ast.Return):
                    return_value = node.body[-1].value
                    # If the return value is a list
                    if isinstance(return_value, ast.List):
                        # Verify all elements in the list are of type `queuebie.messages.Command`
                        if all(
                            isinstance(elm, ast.Call)
                            and isinstance(elm.func, ast.Attribute)
                            and elm.func.attr == "Command"
                            and isinstance(elm.func.value, ast.Name)
                            and elm.func.value.id == "queuebie"
                            for elm in return_value.elts
                        ):
                            self.logger.debug(f"{node.name} returns a List[queuebie.messages.Command].")
                        else:
                            raise RuntimeError(f"{node.name} returns invalid elements in the list.")
                    # If the return value is a single `queuebie.messages.Command`
                    elif isinstance(return_value, ast.Call):
                        if (
                            isinstance(return_value.func, ast.Attribute)
                            and return_value.func.attr == "Command"
                            and isinstance(return_value.func.value, ast.Name)
                            and return_value.func.value.id == "queuebie"
                        ):
                            self.logger.debug(f"{node.name} returns a single queuebie.messages.Command.")
                        else:
                            raise RuntimeError(f"{node.name} returns an invalid Command type.")
                    # If the return value is None
                    elif isinstance(return_value, ast.NameConstant) and return_value.value is None:
                        self.logger.debug(f"{node.name} returns None.")
                    else:
                        raise RuntimeError(f"{node.name} returns an invalid Command type.")
        self.generic_visit(node)
