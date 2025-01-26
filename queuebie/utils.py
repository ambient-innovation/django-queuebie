from typing import Callable, Type

from django.apps import apps


def is_part_of_app(*, function: Callable, class_type: Type) -> bool:
    """
    Checks if a class belongs to the same Django app as the given function.
    """

    # Get the app configurations for the class and function
    class_app_config = apps.get_containing_app_config(class_type.__module__)
    function_app_config = apps.get_containing_app_config(function.__module__)

    # Check if both belong to the same app
    return class_app_config == function_app_config
