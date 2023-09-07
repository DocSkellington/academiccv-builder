"""
Utilities to handle setups (style configurations) for modules.
"""

from typing import Dict, Any

from . import contexts


class Setup:
    """Default class for all classes holding setup data."""

    def __init__(self, key_values: Dict[str, Any]) -> None:
        for key, value in key_values.items():
            setattr(self, key, value)

    def to_latex(self, before: str, indent: int = 0, comma: bool = False) -> str:
        """Converts a setup instance to a succession of key-value pairs for a LaTeX output.

        Arguments:
            before -- The string to add before the key-value pairs
            indent -- The indentation level
            comma -- Whether to put a comma after the closing curly brace

        Returns:
            A string starting with `before{`, followed by the key-value pairs, and then `}`.
        """
        latex = "\t" * indent
        latex += f"{before}{{\n"
        for field, value in vars(self).items():
            name = field.replace("_", "-")
            var = contexts.latex.build_variable_string(name, value)
            if var != "":
                latex += "\t" * indent
                latex += var
        return latex + "\t" * indent + "}" + ("," if comma else "") + "\n"
