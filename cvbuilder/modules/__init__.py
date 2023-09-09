"""
Defines default modules that can be used in the builder.
"""

from abc import ABC


class Module(ABC):
    """Base class for modules."""

    def __init__(self, level: int, section: str) -> None:
        self.level = level
        self.section = section

    def load(self, json_value) -> None:
        """Loads the data from the JSON value (usually, a dictionary).

        Arguments:
            json_value -- The JSON value to load the data from.
        """
        raise NotImplementedError("Each module must define the load method")
