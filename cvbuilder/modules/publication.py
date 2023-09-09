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
    style: contexts.Style = None


class PublicationModule(mod.Module):
    """Publication module, holding data for the job positions defined in the JSON file."""

    def __init__(self, level: int = 1, section: str = "Publications"):
        super().__init__(level, section)
        self.publications: List[Publication] = []

    def load(self, json_value):
        for value in json_value:
            publication = Publication(**value)
            self.publications.append(publication)

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = context.open_section(self.level, self.section)
        for publication in self.publications:
            latex += "\\job{\n"
            latex += context.format_variable("title", publication.title)
            latex += context.format_variable("authors", publication.authors)
            latex += context.format_variable("year", publication.year)
            latex += context.format_variable("reference", publication.reference)
            latex += context.format_variable("where", publication.where)
            latex += context.format_variable("shortWhere", publication.shortWhere)
            latex += context.format_variable("doi", publication.doi)
            latex += context.format_variable("arxiv", publication.arxiv)
            latex += context.format_style(
                publication.style, before="style = ", indent=1, comma=True
            )
            latex += "}\n"
        return latex
