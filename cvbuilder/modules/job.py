"""
Job module.
"""

from dataclasses import dataclass

from .. import modules as mod
from .. import contexts


@dataclass
class Job(mod.Data):
    """Dataclass for a single job"""

    start: str = None
    end: str = None
    title: str = None
    organization: str = None
    description: mod.Description = None
    style: contexts.Style = None

    def __post_init__(self) -> None:
        if self.description is not None:
            self.description = mod.Description(self.description)

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = "\\job{\n"
        latex += context.format_variable("start", context.format_date(self.start))
        latex += context.format_variable("end", context.format_date(self.end))
        latex += context.format_variable("title", self.title)
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

        html += context.simple_div_block("title", self.title)

        if self.start is not None:
            if self.end is None:
                html += context.simple_div_block(
                    "time", context.format_date(self.start) + " &hyphen; "
                )
            else:
                html += context.simple_div_block(
                    "time",
                    context.format_date(self.start)
                    + " &hyphen; "
                    + context.format_date(self.end),
                )

        html += context.close_block()  # align

        html += context.simple_div_block("organization", self.organization)

        html += context.simple_div_block("details", self.description)

        html += context.close_block()  # item

        return html


class JobModule(mod.Module):
    """Job module, holding data for the job positions defined in the JSON file."""

    def __init__(
        self,
        level: int = 1,
        section: str = "Research Experience",
        icon: str = "iconoir-brain-research",
    ):
        super().__init__(level, section, icon)

    def _load(self, json_object) -> Job:
        return Job(**json_object)

    def _get_class_name(self) -> str:
        return "work"
