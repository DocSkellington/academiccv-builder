from __future__ import annotations
from dataclasses import dataclass

from .. import modules
from .. import contexts


@dataclass
class Service(modules.Data):
    year: str = None
    description: modules.description.Description = (
        modules.description.DescriptionDescriptor()
    )
    style: contexts.latex.Style = None

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = "\\service{\n"
        latex += context.format_variable("year", self.year)
        latex += context.format_variable("description", self.description)
        latex += context.format_style(
            self.style, before="style = ", indent=1, comma=True
        )
        latex += "}\n"

        return latex

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_div("item")

        html += context.open_div("align")

        html += context.simple_div_block("title", self.description)

        html += context.simple_div_block("details", self.year)

        html += context.close_block()  # align

        html += context.close_block()  # item

        return html


class ServiceModule(modules.Module):
    def __init__(
        self,
        level: int = 1,
        section: str = "Collective and administrative responsibilities",
        introduction_text: str = "",
        icon: str = "iconoir-stats-report",
        use_subsections: bool = True,
    ):
        super().__init__(
            level=level,
            section=section,
            section_icon=icon,
            use_subsections=use_subsections,
            introduction_text=introduction_text,
        )

    def _load(self, json_object) -> Service:
        return Service(**json_object)

    def _get_class_name(self) -> str:
        return "services"
