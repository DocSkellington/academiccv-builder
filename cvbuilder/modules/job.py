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
    style: contexts.latex.JobSetup = None


class JobModule(mod.Module):
    """Job module, holding data for the job positions defined in the JSON file."""

    def __init__(self):
        self.jobs: List[Job] = []

    def load(self, json_value):
        for value in json_value:
            job = Job(**value)
            self.jobs.append(job)

    def to_latex(self, context: contexts.Context) -> str:
        latex = "\\section{Work Experience}\n\n"
        for job in self.jobs:
            latex += "\\job{\n"
            latex += contexts.latex.build_variable_string(
                "start", context.format_date(job.start)
            )
            latex += contexts.latex.build_variable_string(
                "end", context.format_date(job.end)
            )
            latex += contexts.latex.build_variable_string("title", job.title)
            latex += contexts.latex.build_variable_string(
                "organization", job.organization
            )
            latex += contexts.latex.build_variable_string(
                "description", job.description
            )
            latex += contexts.latex.setup_to_latex(
                job.style, "style = ", indent=1, comma=True
            )
            latex += "}\n"
        return latex
