from dataclasses import dataclass

from .. import modules as mod
from .. import contexts


@dataclass
class Award(mod.Data):
    year: str = None
    description: mod.Description = None
    style: contexts.Style = None

    def __post_init__(self) -> None:
        if self.description is not None:
            self.description = mod.Description(self.description)

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


class AwardModule(mod.Module):
    def __init__(
        self,
        level: int = 1,
        section: str = "Awards",
        icon: str = "iconoir-trophy",
    ):
        super().__init__(level, section, icon)

    def _load(self, json_object) -> Award:
        return Award(**json_object)

    def _get_class_name(self) -> str:
        return "awards"
