from __future__ import annotations
from dataclasses import dataclass

from .. import modules
from .. import contexts


@dataclass
class Project(modules.Data):
    shortName: modules.description.Description = (
        modules.description.DescriptionDescriptor()
    )
    name: modules.description.Description = modules.description.DescriptionDescriptor()
    role: modules.description.Description = modules.description.DescriptionDescriptor()
    description: modules.description.Description = (
        modules.description.DescriptionDescriptor()
    )
    style: contexts.latex.Style = None

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = "\\project{\n"
        latex += context.format_variable("shortName", self.shortName)
        latex += context.format_variable("name", self.name)
        latex += context.format_variable("role", self.role)
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

        html += context.simple_div_block("shortName", self.shortName)

        html += context.close_block()  # align

        html += context.simple_div_block("role", self.role)

        html += context.simple_div_block("details", self.description)

        html += context.close_block()  # item

        return html


class ProjectModule(modules.Module):
    def __init__(
        self,
        level: int = 1,
        section: str = "Projects",
        introduction_text: str = "",
        icon: str = "iconoir-light-bulb",
        use_subsections: bool = False,
    ):
        super().__init__(
            level=level,
            section=section,
            introduction_text=introduction_text,
            section_icon=icon,
            use_subsections=use_subsections,
        )

    def _load(self, json_object) -> Project:
        return Project(**json_object)

    def _get_class_name(self) -> str:
        return "project"
