from abc import ABC
from dataclasses import dataclass

from ..modules import description


class Data(ABC):
    """Base class for data held by modules."""

    def to_latex(self, context: "contexts.latex.LaTeXContext") -> str:
        raise NotImplementedError()

    def to_html(self, context: "contexts.html.HTMLContext") -> str:
        raise NotImplementedError()

    def to_markdown(self, context: "contexts.markdown.MarkdownContext") -> str:
        return self.to_html(context)


@dataclass
class SimpleText:
    text: description.Description = description.DescriptionDescriptor()

    def to_latex(self) -> str:
        return self.text.to_latex()

    def to_html(self) -> str:
        return self.text.to_html()

    def to_markdown(self) -> str:
        return self.text.to_markdown()


class Module(ABC):
    """Base class for modules."""

    def __init__(
        self,
        *,
        level: int,
        section: str,
        introduction_text: str,
        section_icon: str,
        use_subsections: bool,
    ) -> None:
        self.level = level
        self.section = section
        self.data: list[tuple[None | str, list[Data]]] = []
        self.introduction_text = SimpleText(introduction_text)
        self.section_icon = section_icon
        self.use_subsections = use_subsections

    def load(self, json_value) -> None:
        """Loads the module's data from the given JSON value.

        If the module is set to use subsections, the loading function assumes that the value looks like
        ```
        {
            "order": ["sub1", "sub2", ..., "subn"],
            "sub1": [ ... ],
            "sub2": [ ... ],
            ...,
            "subn": [ ... ],
        }
        ```
        (the order of the "subi" keys do not matter).
        The value of each "subi" must be an array containing objects, which follow the module-specific data format.

        If the module is set to not use subsections, the loading function assumes that the value is simply a list of objects, following the module-specific data format.

        Arguments:
            json_value -- The JSON value to load the data from.
        """
        if self.use_subsections:
            if "order" not in json_value:
                raise ValueError(
                    f"A module ({self.__class__}) is configured to use subsections but the 'order' field is missing"
                )
            order = json_value["order"]
            for subsection in order:
                data_list = []
                for data_object in json_value[subsection]:
                    data_list.append(self._load(data_object))
                if subsection == "None":
                    subsection = None
                self.data.append((subsection, data_list))
        else:
            data_list = []
            for data_object in json_value:
                data_list.append(self._load(data_object))
            self.data.append((None, data_list))

    def _load(self, json_object) -> Data:
        """Creates a single data instance from the json_value.

        Arguments:
            json_object -- The JSON value to load the data from.
        """
        raise NotImplementedError("Each module must define the _load method")

    def to_latex(self, context: "contexts.latex.LaTeXContext") -> str:
        latex = context.open_section(self.level, self.section)
        latex += self.introduction_text.to_latex()
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

        html += self.introduction_text.to_html()
        for section, data_list in self.data:
            if section is not None:
                html += context.open_section(
                    self.level + 2, section, section.lower().replace(" ", "-")
                )

            for data in data_list:
                html += data.to_html(context)

            if section is not None:
                html += context.close_block()

        html += context.close_block()
        return html

    def to_markdown(self, context: "contexts.markdown.MarkdownContext") -> str:
        markdown = context.open_section(1, self.section)
        markdown += self.introduction_text.to_markdown()
        for section, data_list in self.data:
            if section is not None:
                markdown += context.open_section(2, section)

            for data in data_list:
                markdown += data.to_markdown(context)

        return markdown

    def _get_class_name(self) -> str:
        raise NotImplementedError()
