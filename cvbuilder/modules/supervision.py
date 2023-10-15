from __future__ import annotations
from dataclasses import dataclass

from .. import modules
from .. import contexts


@dataclass
class Supervision(modules.Data):
    year: str = None
    name: str = None
    role: str = None
    organization: str = None
    description: modules.description.Description = None
    style: contexts.latex.Style = None

    def __post_init__(self) -> None:
        if self.description is not None:
            self.description = modules.description.Description(self.description)

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = "\\supervision{\n"
        latex += context.format_variable("year", context.format_date(self.year))
        latex += context.format_variable("name", context.format_date(self.name))
        latex += context.format_variable("role", self.role)
        latex += context.format_variable("organization", self.organization)
        latex += context.format_variable("description", self.description)
        latex += context.format_style(
            self.style, before="style = ", indent=1, comma=True
        )
        latex += "}\n"

        return latex

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_div("item")

        html += context.open_div("align")

        html += context.simple_div_block("title", self.name)

        html += context.simple_div_block("role", self.role)

        html += context.close_block()  # align

        html += context.open_div("align")

        html += context.simple_div_block("organization", self.organization)

        html += context.simple_div_block("time", self.year)

        html += context.close_block()  # align

        html += context.simple_div_block("details", self.description)

        html += context.close_block()  # item

        return html


class SupervisionModule(modules.Module):
    def __init__(
        self,
        level: int = 1,
        section: str = "Supervision",
        icon: str = "iconoir-path-arrow",
        use_subsections: bool = True,
    ):
        super().__init__(level, section, icon, use_subsections)

    def _load(self, json_object) -> Supervision:
        return Supervision(**json_object)

    def _get_class_name(self) -> str:
        return "supervision"
