"""
Job module.
"""

from __future__ import annotations
from dataclasses import dataclass

from .. import modules
from .. import contexts


@dataclass
class Job(modules.Data):
    """Dataclass for a single job"""

    start: str = None
    end: str = None
    title: modules.description.Description = modules.description.DescriptionDescriptor()
    organization: modules.description.Description = (
        modules.description.DescriptionDescriptor()
    )
    description: modules.description.Description = (
        modules.description.DescriptionDescriptor()
    )
    style: contexts.latex.Style = None

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


class JobModule(modules.Module):
    """Job module, holding data for the job positions defined in the JSON file."""

    def __init__(
        self,
        level: int = 1,
        section: str = "Research Experience",
        introduction_text: str = "",
        icon: str = "iconoir-brain-research",
        use_subsections: bool = True,
    ):
        super().__init__(
            level=level,
            section=section,
            section_icon=icon,
            use_subsections=use_subsections,
            introduction_text=introduction_text,
        )

    def _load(self, json_object) -> Job:
        return Job(**json_object)

    def _get_class_name(self) -> str:
        return "work"
