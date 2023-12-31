"""
Defines default contexts that can be used in the builder.
"""

from abc import ABC
from typing import List, Union, Dict, Any
from dataclasses import dataclass, field
from pathlib import Path
import dateutil.parser
import datetime

from .. import modules as mod


@dataclass
class PersonalData:
    """Dataclass for data identifying the CV author"""

    name: str
    position: str
    organization: str
    photo: str = None


class Context(ABC):
    """A context used to produce one file from the JSON file.

    The exact behavior depends on the subclass.

    The context is also responsible for the header/title definition, using an instance of PersonalData
    """

    def __init__(
        self,
        name: str,
        output_path: Union[Path, str],
        date_output_format: str = "%d %b %Y",
    ) -> None:
        if isinstance(output_path, str):
            self.output_path = Path(output_path)
        else:
            self.output_path = output_path
        self.name = name
        self.date_output_format = date_output_format

    def format_variable(self, name: str, value: str) -> str:
        """Constructs a string to set the variable named "name" to the given value, in the appropriate manner for the context.

        Arguments:
            name -- The context appropriate name for the variable
            value -- The value of the variable

        Returns:
            Empty string if value is None, or a context appropriate string
        """
        raise NotImplementedError(
            "Contexts should implement format_variable(self, name: str, value: str)"
        )

    def format_date(
        self, date_input: Union[datetime.datetime, str], date_output_format: str = None
    ) -> str:
        """Format a date to the requested format.

        If the format is None (the default value), the format set for in the class' constructor is used.

        If the input is a string that can not be converted to a date, the function returns the string as is.
        For instance, if the string is "Present", then "Present" is returned.

        If the input string is None, the function returns None.

        Arguments:
            date_input -- The input date
            date_output_format -- The format for the output string

        Returns:
            The date formatted, or the input string as is, or None
        """
        if date_input is None:
            return None
        if isinstance(date_input, datetime.datetime):
            if date_output_format is None:
                return date_input.strftime(self.date_output_format)
            return date_input.strftime(date_output_format)
        try:
            date = dateutil.parser.parse(date_input)
            if date_output_format is None:
                return date.strftime(self.date_output_format)
            return date.strftime(date_output_format)
        except dateutil.parser.ParserError:
            return date_input

    def write_output(
        self, modules: List["ModuleDescriptor"], personal: PersonalData
    ) -> None:
        """Writes the output of this context into a single file.

        Arguments:
            modules -- The modules to use
            personal -- The personal data to use
        """
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with self.output_path.open(mode="w", encoding="UTF8") as file:
            file.write(self._build_output(modules, personal))

    def _run_modules(
        self, modules: List["ModuleDescriptor"], category: str = "default"
    ) -> str:
        output = ""
        for module in modules:
            if module.category != category:
                continue

            method = None
            try:
                method = getattr(module.module, f"to_{self.name}")
            except AttributeError as exc:
                raise NotImplementedError(
                    f"Each used module must implement the function to_{self.name}"
                ) from exc

            output += method(self)
        return output

    def _build_output(self, modules: List[mod.Module], personal: PersonalData) -> str:
        raise NotImplementedError("Context classes must implement build_output")
