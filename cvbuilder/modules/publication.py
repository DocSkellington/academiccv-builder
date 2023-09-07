"""
Module for publications.
"""

from dataclasses import dataclass
from typing import Union, List

from .. import contexts
from .. import modules as mod


@dataclass
class Publication:
    """A publication must have a title, authors, and a publication year."""

    title: str
    authors: str
    year: Union[str, int]
    reference: str = None
    where: str = None
    shortWhere: str = None
    doi: str = None
    arxiv: str = None
    style: contexts.latex.PublicationSetup = None


class PublicationModule(mod.Module):
    """Publication module, holding data for the job positions defined in the JSON file."""

    def __init__(self):
        self.publications: List[Publication] = []

    def load(self, json_value):
        for value in json_value:
            publication = Publication(**value)
            self.publications.append(publication)

    def to_latex(self, _context: contexts.Context) -> str:
        latex = "\\section{Work Experience}\n\n"
        for job in self.publications:
            latex += "\\job{\n"
            latex += contexts.latex.build_variable_string("title", job.title)
            latex += contexts.latex.build_variable_string("authors", job.authors)
            latex += contexts.latex.build_variable_string("year", job.year)
            latex += contexts.latex.build_variable_string("reference", job.reference)
            latex += contexts.latex.build_variable_string("where", job.where)
            latex += contexts.latex.build_variable_string("shortWhere", job.shortWhere)
            latex += contexts.latex.build_variable_string("doi", job.doi)
            latex += contexts.latex.build_variable_string("arxiv", job.arxiv)
            latex += contexts.latex.setup_to_latex(
                job.style, "style = ", indent=1, comma=True
            )
            latex += "}\n"
        return latex
