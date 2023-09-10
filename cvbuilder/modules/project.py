from dataclasses import dataclass

from .. import modules as mod
from .. import contexts


@dataclass
class Project(mod.Data):
    shortName: str = None
    name: str = None
    role: str = None
    description: mod.Description = None
    style: contexts.Style = None

    def __post_init__(self) -> None:
        if self.description is not None:
            self.description = mod.Description(self.description)

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = "\\project{\n"
        latex += context.format_variable("shortName", context.format_date(self.shortName))
        latex += context.format_variable("name", context.format_date(self.name))
        latex += context.format_variable("role", self.role)
        latex += context.format_variable("description", self.description.to_latex(context))
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

        html += context.simple_div_block("details", self.description.to_html(context))

        html += context.close_block()  # item

        return html


class ProjectModule(mod.Module):
    def __init__(self, level: int = 1, section: str = "Projects"):
        super().__init__(level, section)

    def _load(self, json_object) -> Project:
        return Project(**json_object)

    def _get_class_name(self) -> str:
        return "project"
