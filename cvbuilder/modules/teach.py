from dataclasses import dataclass

from .. import modules as mod
from .. import contexts


@dataclass
class Teach(mod.Data):
    year: str = None
    course: str = None
    role: str = None
    level: str = None
    organization: str = None
    description: mod.Description = None
    style: contexts.Style = None

    def __post_init__(self) -> None:
        if self.description is not None:
            self.description = mod.Description(self.description)

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = "\\teach{\n"
        latex += context.format_variable("year", context.format_date(self.year))
        latex += context.format_variable("course", context.format_date(self.course))
        latex += context.format_variable("role", self.role)
        latex += context.format_variable("level", self.level)
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

        html += context.simple_div_block("title", self.course)

        html += context.simple_div_block("role", self.role)

        html += context.close_block()  # align

        html += context.open_div("align")

        html += context.simple_div_block("level", self.level)

        html += context.simple_div_block("time", self.year)

        html += context.close_block()  # align

        html += context.simple_div_block("organization", self.organization)

        html += context.simple_div_block("details", self.description)

        html += context.close_block()  # item

        return html


class TeachModule(mod.Module):
    def __init__(self, level: int = 1, section: str = "Teaching"):
        super().__init__(level, section)

    def _load(self, json_object) -> Teach:
        return Teach(**json_object)

    def _get_class_name(self) -> str:
        return "teaching"
