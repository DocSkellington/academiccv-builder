from __future__ import annotations
from dataclasses import dataclass

from .. import modules
from .. import contexts


@dataclass
class Award(modules.Data):
    year: str = None
    description: modules.description.Description = (
        modules.description.DescriptionDescriptor()
    )
    style: contexts.latex.Style = None

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = "\\award{\n"
        latex += context.format_variable("year", context.format_date(self.year))
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


class AwardModule(modules.Module):
    def __init__(
        self,
        level: int = 1,
        section: str = "Awards",
        icon: str = "iconoir-trophy",
        use_subsections: bool = False,
    ):
        super().__init__(level, section, icon, use_subsections)

    def _load(self, json_object) -> Award:
        return Award(**json_object)

    def _get_class_name(self) -> str:
        return "awards"
