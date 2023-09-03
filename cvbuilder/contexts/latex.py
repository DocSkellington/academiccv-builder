"""
LaTeX context and utilities.

The produced document relies on the academiccv package.
"""

from pathlib import Path
import sys
from abc import ABC
from typing import List, Any, Dict
from dataclasses import dataclass
import dataclasses

from . import Context, PersonalData
from .. import modules as mod


def build_variable_string(latex_name: str, value: Any) -> str:
    """Constructs a string setting a LaTeX variable in a key-value context.

    Arguments:
        latex_name -- The LaTeX name for the variable
        value -- The value of the variable

    Returns:
        Empty string if value is None, or `latex_name = value,\\n` otherwise.
    """
    if value is not None:
        string = f"\t{latex_name} = "
        if value is True:
            string += "true"
        elif value is False:
            string += "false"
        else:
            string += f"{{{value}}}"
        return string + ",\n"
    return ""


def setup_to_latex(setup, before: str, comma: bool = False) -> str:
    """Converts a setup dataclass to a succession of key-value pairs.

    Arguments:
        setup -- The setup dataclass
        before -- The string to add before the key-value pairs

    Returns:
        A string starting with `before{`, followed by the key-value pairs, and then `}`.
    """
    if setup is None:
        return ""
    latex = f"{before}{{\n"
    for field in dataclasses.fields(setup):
        name = field.name.replace("_", "-")
        latex += build_variable_string(name, getattr(setup, field.name))
    return latex + "}" + ("," if comma else "") + "\n"


class Setup(ABC):
    """Default class for all classes holding setup data."""


@dataclass
class TitleSetup(Setup):
    """Dataclass storing the setup configuration for the LaTeX title."""

    author: str = None
    position: str = None
    organization: str = None

    address: str = None
    street: str = None
    zipcode: str = None
    city: str = None
    country: str = None

    links: str = None
    email: str = None
    website: str = None
    github: str = None
    orcid: str = None
    linkedin: str = None

    date: str = None
    vertical_space: str = None
    portion_photo: float = None


@dataclass
class JobSetup(Setup):
    """Dataclass storing the setup configuration for job positions."""

    start: str = None
    end: str = None
    title: str = None
    organization: str = None
    description: str = None
    swap: bool = None
    margin_size: str = None
    space: str = None
    vspace_after: str = None


class LaTeXContext(Context):
    """The LaTeX context.

    Each used module in this context must implement the function `to_latex(self)`.

    It produces a document relying on the academiccv class.

    By default, no other package is loaded, no setup is done. That is, the document contains the
    document class, immediately followed by the document environment, the \\makecvtitle and the
    strings produced by the modules.
    """

    def __init__(self, output_path: Path) -> None:
        super().__init__("latex", output_path)
        self.packages: List[str] = []
        self.setups: Dict[str, Setup] = {}
        self.other_preamble: List[str] = []

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

    def set_setup(self, name: str, setup: Setup) -> None:
        """Sets a setup.

        The name is used to add \\{name}Setup before the key-value pairs.

        Arguments:
            name -- The name of the setup
            setup -- The new setup
        """
        self.setups[name] = setup

    def _build_output(self, modules: List[mod.Module], personal: PersonalData) -> str:
        latex = "\\documentclass{academiccv}\n\n"

        for package in self.packages:
            latex += f"\\usepackage{package}\n"

        for name, setup in self.setups.items():
            latex += setup_to_latex(setup, f"\\{name}Setup") + "\n"

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
        title += build_variable_string("author", personal.name)
        title += build_variable_string("position", personal.position)
        title += build_variable_string("organization", personal.organization)
        title += build_variable_string("photo", personal.photo)
        if isinstance(personal.email, str):
            title += build_variable_string("email", personal.email)
        elif isinstance(personal.email, list):
            for mail in personal.email:
                title += build_variable_string("email", mail)
        elif personal.email is not None:
            print("Personal data: email must be a string or a list", file=sys.stderr)
        title += build_variable_string("website", personal.website)
        title += build_variable_string("github", personal.github)
        title += build_variable_string("orcid", personal.orcid)
        title += build_variable_string("linkedIn", personal.linkedin)
        if personal.address is not None:
            title += build_variable_string("street", personal.address.street)
            title += build_variable_string("zipcode", personal.address.zipcode)
            title += build_variable_string("city", personal.address.city)
            title += build_variable_string("country", personal.address.country)
        title += "}\n\n"
        return title
