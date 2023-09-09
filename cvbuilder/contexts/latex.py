"""
LaTeX context and utilities.

The produced document relies on the academiccv package.
"""

from pathlib import Path
import sys
from typing import List, Union

from . import Context, PersonalData, Style
from .. import modules as mod


class LaTeXContext(Context):
    """The LaTeX context.

    Each used module in this context must implement the function `to_latex(self)`.

    It produces a document relying on the academiccv class.

    By default, no other package is loaded, and no style configuration is done.
    That is, the document contains the document class, immediately followed by the document
    environment, the \\makecvtitle and the strings produced by the modules.

    For styles, the name is used to add \\{name}Setup before the key-value pairs in the preamble.
    """

    def __init__(self, output_path: Union[Path, str]) -> None:
        super().__init__("latex", output_path)
        self.packages: List[str] = []
        self.other_preamble: List[str] = []

    def format_variable(self, name: str, value: str) -> str:
        if value is not None:
            string = f"\t{name} = "
            if value is True:
                string += "true"
            elif value is False:
                string += "false"
            else:
                string += f"{{{value}}}"
            return string + ",\n"
        return ""

    def format_style(self, style: Style, **kwargs) -> str:
        """Converts a style instance to a succession of key-value pairs for a LaTeX output.

        Arguments:
            style -- The style
        Keyword arguments:
            before -- The string to add before the key-value pairs
            indent -- The indentation level
            comma -- Whether to put a comma after the closing curly brace

        Any other keyword argument is ignored.

        Returns:
            A string starting with `before{`, followed by the key-value pairs, and then `}`.
        """
        if style is None:
            return ""

        before = kwargs.get("before", "")
        indent = kwargs.get("indent", 0)
        comma = kwargs.get("comma", False)

        latex = "\t" * indent
        latex += f"{before}{{\n"
        for field, value in vars(style).items():
            name = field.replace("_", "-")
            var = self.format_variable(name, value)
            if var != "":
                latex += "\t" * indent
                latex += var
        return latex + "\t" * indent + "}" + ("," if comma else "") + "\n"

    def add_package(self, package: str) -> None:
        """Adds a new package that must be loaded in the preamble.

        Arguments:
            package -- The package name
        """
        self.packages.append(package)

    def add_to_preamble(self, other: str) -> None:
        """Adds something to the preamble.

        Arguments:
            other -- The thing to add to the preamble.
                    It must be a valid LaTeX command for the document to compile.
        """
        self.other_preamble.append(other)

    def open_section(self, level: int, name: str) -> str:
        if level == 0:
            return ""
        if level == 1:
            return f"\\section{{{name}}}\n"
        if level == 2:
            return f"\\subsection{{{name}}}\n"
        if level == 3:
            return f"\\subsubsection{{{name}}}\n"
        if level == 4:
            return f"\\paragraph{{{name}}}\n"
        if level == 5:
            return f"\\subparagraph{{{name}}}\n"
        raise ValueError(f"LaTeX context: heading of level {level} is invalid.")

    def _build_output(self, modules: List[mod.Module], personal: PersonalData) -> str:
        latex = "\\documentclass{academiccv}\n\n"

        for package in self.packages:
            latex += f"\\usepackage{package}\n"

        for name, style in self.styles.items():
            latex += self.format_style(style, before=f"\\{name}Setup") + "\n"

        for other in self.other_preamble:
            latex += other + "\n"

        latex += "\\begin{document}\n"
        if personal is not None:
            latex += self._cv_title(personal)
        latex += self._run_modules(modules)
        latex += "\\end{document}"

        return latex

    def _cv_title(self, personal: PersonalData) -> str:
        title = "\\makecvtitle{\n"
        title += self.format_variable("author", personal.name)
        title += self.format_variable("position", personal.position)
        title += self.format_variable("organization", personal.organization)
        title += self.format_variable("photo", personal.photo)
        if isinstance(personal.email, str):
            title += self.format_variable("email", personal.email)
        elif isinstance(personal.email, list):
            for mail in personal.email:
                title += self.format_variable("email", mail)
        elif personal.email is not None:
            print("Personal data: email must be a string or a list", file=sys.stderr)
        title += self.format_variable("website", personal.website)
        title += self.format_variable("github", personal.github)
        title += self.format_variable("orcid", personal.orcid)
        title += self.format_variable("linkedIn", personal.linkedin)
        if personal.address is not None:
            title += self.format_variable("street", personal.address.street)
            title += self.format_variable("zipcode", personal.address.zipcode)
            title += self.format_variable("city", personal.address.city)
            title += self.format_variable("country", personal.address.country)
        title += "}\n\n"
        return title
