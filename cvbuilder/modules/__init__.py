"""
Defines default modules that can be used in the builder.
"""

from abc import ABC
from typing import Dict, Any, Tuple, Union, List


class Data(ABC):
    """Base class for data held by modules."""

    def to_latex(self, context: "contexts.latex.LaTeXContext") -> str:
        raise NotImplementedError()

    def to_html(self, context: "contexts.html.HTMLContext") -> str:
        raise NotImplementedError()

    def to_markdown(self, context: "contexts.markdown.MarkdownContext") -> str:
        return self.to_html(context)


class Description(Data):
    """A description is a type of data that can produce lists.

    More precisely, the data can be a string or a list.
    In the first case, the produce output is the string itself.
    In the second case, each string of the list is produced as-is.
    However, if the list contains a list, then that inner list is transformed into an unnumbered list.
    """

    def __init__(self, description: Union[str, List[Any]]) -> None:
        self.description = description

    def to_latex(self, context: "contexts.latex.LaTeXContext") -> str:
        if isinstance(self.description, str):
            return f"{{{self.description}}}"
        elif isinstance(self.description, list):
            latex = ""
            for part in self.description:
                if isinstance(part, str):
                    latex += f"{{{part}}}\n"
                elif isinstance(part, list):
                    latex += "\\begin{itemize}\n"
                    for line in part:
                        latex += f"\t\\item {{{line}}}\n"
                    latex += "\\end{itemize}\n"
            return latex

    def to_html(self, context: "contexts.html.HTMLContext") -> str:
        if isinstance(self.description, str):
            return self.description
        if isinstance(self.description, list):
            html = ""
            for part in self.description:
                if isinstance(part, str):
                    html += part + "\n"
                elif isinstance(part, list):
                    html += context.open_list(False, "description-list")
                    for line in part:
                        html += context.list_item("description-list-item", line)
                    html += context.close_block()
            return html

    def to_markdown(self, context: "contexts.markdown.MarkdownContext") -> str:
        if isinstance(self.description, str):
            return self.description
        if isinstance(self.description, list):
            markdown = ""
            for part in self.description:
                if isinstance(part, str):
                    markdown += part
                elif isinstance(part, list):
                    markdown += "\n\n"
                    for line in part:
                        markdown += " * " + line + "\n"
                    markdown += "\n"
            return markdown


class Module(ABC):
    """Base class for modules."""

    def __init__(self, level: int, section: str, section_icon: str = "") -> None:
        self.level = level
        self.section = section
        self.data: List[Tuple[Union[None, str], List[Data]]] = []
        self.section_icon = section_icon

    def load(self, json_value) -> None:
        """Loads the module's data from the given JSON value.

        The value can define subsections.

        Arguments:
            json_value -- The JSON value to load the data from.
        """
        for value in json_value:
            if len(value) == 1:
                key = list(value)[0]
                data_list = []
                for values in value.values():
                    for job_object in values:
                        data_list.append(self._load(job_object))
                self.data.append((key, data_list))
            else:
                data = self._load(value)
                if len(self.data) > 0 and self.data[-1][0] is None:
                    self.data[-1][1].append(data)
                else:
                    self.data.append([None, [data]])

    def _load(self, json_object) -> Data:
        """Creates a single data instance from the json_value.

        Arguments:
            json_object -- The JSON value to load the data from.
        """
        raise NotImplementedError("Each module must define the _load method")

    def to_latex(self, context: "contexts.latex.LaTeXContext") -> str:
        latex = context.open_section(self.level, self.section)
        for section, data_list in self.data:
            if section is not None:
                latex += context.open_section(self.level + 1, section)

            for data in data_list:
                latex += data.to_latex(context)

        return latex

    def to_html(self, context: "contexts.html.HTMLContext") -> str:
        class_name = self._get_class_name()
        html = context.open_section(
            self.level + 1, self.section, f"{class_name}", self.section_icon
        )
        section_level = self.level + 2

        for section, data_list in self.data:
            if section is not None:
                html += context.open_section(
                    section_level, section, section.lower().replace(" ", "-")
                )

            for data in data_list:
                html += data.to_html(context)

            if section is not None:
                html += context.close_block()

        html += context.close_block()
        return html

    def to_markdown(self, context: "contexts.markdown.MarkdownContext") -> str:
        markdown = context.open_section(1, self.section)
        for section, data_list in self.data:
            if section is not None:
                markdown += context.open_section(2, section)
            
            for data in data_list:
                markdown += data.to_markdown(context)

        return markdown

    def _get_class_name(self) -> str:
        raise NotImplementedError()
