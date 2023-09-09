"""
Job module.
"""

from typing import List
from dataclasses import dataclass

from .. import modules as mod
from .. import contexts


@dataclass
class Job:
    """Dataclass for a single job"""

    start: str = None
    end: str = None
    title: str = None
    organization: str = None
    description: str = None
    style: contexts.Style = None


class JobModule(mod.Module):
    """Job module, holding data for the job positions defined in the JSON file."""

    def __init__(self, level: int = 2, section: str = "Work Experience"):
        super().__init__(level, section)
        self.jobs: List[Job] = []

    def load(self, json_value):
        for value in json_value:
            job = Job(**value)
            self.jobs.append(job)

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = context.open_section(self.level, self.section) + "\n"
        for job in self.jobs:
            latex += "\\job{\n"
            latex += context.format_variable("start", context.format_date(job.start))
            latex += context.format_variable("end", context.format_date(job.end))
            latex += context.format_variable("title", job.title)
            latex += context.format_variable("organization", job.organization)
            latex += context.format_variable("description", job.description)
            latex += context.format_style(
                job.style, before="style = ", indent=1, comma=True
            )
            latex += "}\n"
        return latex

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_section(self.level, self.section, "section work-section")
        indent = 4

        for job in self.jobs:
            html += context.open_div("item", indent)
            indent += 1

            html += context.open_div("upper", indent)
            indent += 1

            html += context.header(3, job.title, "job", indent)

            html += context.simple_div_block(
                "time",
                context.format_date(job.start)
                + " &hyphen; "
                + context.format_date(job.end),
                indent,
            )

            indent -= 1
            html += context.close_div(indent) # upper

            html += context.simple_div_block("organization", job.organization, indent)

            html += context.simple_div_block("details", job.description, indent)

            indent -= 1
            html += context.close_div(indent) # item

        html += context.close_section(self.level)
        return html
