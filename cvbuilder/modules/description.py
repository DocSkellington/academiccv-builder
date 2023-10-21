from __future__ import annotations
from typing import TYPE_CHECKING
import re
import markdown

from ..modules.utils import etree_to_latex

if TYPE_CHECKING:
    from ..modules import Data

markdown.Markdown.output_formats["latex"] = etree_to_latex.to_latex_string


class Description:
    """A descriptive string written in Markdown.

    The Markdown is converted to LaTeX, HTML, or kept as-is, depending on the output format.
    """

    def __init__(self, text: str) -> None:
        self.description = text

    def __str__(self) -> str:
        return self.description

    def is_empty(self) -> bool:
        return self.description is None

    def to_latex(self) -> str:
        if self.is_empty():
            return ""
        return markdown.markdown(self.description, output_format="latex")

    def to_html(self) -> str:
        if self.is_empty():
            return ""
        html = markdown.markdown(self.description, output_format="html")
        # To obtain a better output, we remove all the p tags.
        # This allows text to flow more naturally, without line breaks.
        return re.sub("(<p>|</p>)", "", html)

    def to_markdown(self) -> str:
        if self.is_empty():
            return ""
        return self.description


# Taken from https://docs.python.org/3/library/dataclasses.html#descriptor-typed-fields
class DescriptionDescriptor:
    """Utility class to be used in dataclasses to automatically call the Descriptor's constructor.

    See, for instance, cvbuilder.modules.award.Award.
    """

    def __init__(self, default: Description = Description(None)) -> None:
        self._default = default

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = "_" + name  # pylint: disable = attribute-defined-outside-init

    def __get__(self, obj: None | Data, _type: type):
        if obj is None:
            return self._default
        return getattr(obj, self._name, self._default)

    def __set__(self, obj: Data, value: str | int | Description):
        if isinstance(value, str):
            value = Description(value)
        elif isinstance(value, (int, float, bool)):
            value = Description(str(value))
        elif not isinstance(value, Description):
            raise TypeError(
                "Can not construct a Description from "
                + repr(value)
                + f"({type(value)})"
            )
        setattr(obj, self._name, value)
