from collections.abc import Callable

SCOPE_MARKERS = ("handlers", "messages")


def message_scope(*, module_path: str) -> str:
    """
    Determines the package owning the "handlers" or "messages" directory the given module lives in.
    Falls back to the full module path for modules outside such a directory.
    """
    parts = module_path.split(".")
    markers = [index for index, part in enumerate(parts) if part in SCOPE_MARKERS]

    return ".".join(parts[: markers[-1]]) if markers else module_path


def is_same_scope(*, function: Callable, class_type: type) -> bool:
    """
    Checks if a class and the given function belong to the same scope.
    """
    return message_scope(module_path=class_type.__module__) == message_scope(module_path=function.__module__)


def unique_append_to_inner_list(*, data: dict, key: str | int, value) -> dict:
    """
    Inserts "value" in the dictionary "data" on "key".
    If "key" doesn't exist yet, it will create a new list containing "value".
    If "value" at "key" already exists, it won't be appended.
    """
    if key not in data:
        data[key] = [value]
    elif value not in data[key]:
        data[key].append(value)

    return data
