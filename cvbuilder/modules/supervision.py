from __future__ import annotations
from dataclasses import dataclass

from .. import modules
from .. import contexts


@dataclass
class Supervision(modules.Data):
    when: modules.description.Description = modules.description.DescriptionDescriptor()
    name: modules.description.Description = modules.description.DescriptionDescriptor()
    role: modules.description.Description = modules.description.DescriptionDescriptor()
    organization: modules.description.Description = (
        modules.description.DescriptionDescriptor()
    )
    description: modules.description.Description = (
        modules.description.DescriptionDescriptor()
    )
    style: contexts.latex.Style = None

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = "\\supervision{\n"
        latex += context.format_variable("year", self.when)
        latex += context.format_variable("name", self.name)
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

        html += context.simple_div_block("time", self.when)

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
