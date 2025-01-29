from collections.abc import Callable

from django.apps import apps


def is_part_of_app(*, function: Callable, class_type: type) -> bool:
    """
    Checks if a class belongs to the same Django app as the given function.
    """

    # Get the app configurations for the class and function
    class_app_config = apps.get_containing_app_config(class_type.__module__)
    function_app_config = apps.get_containing_app_config(function.__module__)

    # Check if both belong to the same app
    return class_app_config == function_app_config


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
