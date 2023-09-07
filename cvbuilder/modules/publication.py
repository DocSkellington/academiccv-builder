"""
Module for publications.
"""

from dataclasses import dataclass
from typing import Union, List

from .. import setup
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
    style: setup.Setup = None


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
        for publication in self.publications:
            latex += "\\job{\n"
            latex += contexts.latex.build_variable_string("title", publication.title)
            latex += contexts.latex.build_variable_string(
                "authors", publication.authors
            )
            latex += contexts.latex.build_variable_string("year", publication.year)
            latex += contexts.latex.build_variable_string(
                "reference", publication.reference
            )
            latex += contexts.latex.build_variable_string("where", publication.where)
            latex += contexts.latex.build_variable_string(
                "shortWhere", publication.shortWhere
            )
            latex += contexts.latex.build_variable_string("doi", publication.doi)
            latex += contexts.latex.build_variable_string("arxiv", publication.arxiv)
            if publication.style is not None:
                latex += publication.style.to_latex("style = ", indent=1, comma=True)
            latex += "}\n"
        return latex
