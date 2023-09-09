"""
Module for publications.
"""

from dataclasses import dataclass
from typing import Union

from .. import contexts
from .. import modules as mod


@dataclass
class Publication(mod.Data):
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

    def to_latex(self, context: contexts.latex.LaTeXContext, indent: int) -> str:
        latex = "\\job{\n"
        latex += context.format_variable("title", self.title)
        latex += context.format_variable("authors", self.authors)
        latex += context.format_variable("year", self.year)
        latex += context.format_variable("reference", self.reference)
        latex += context.format_variable("where", self.where)
        latex += context.format_variable("shortWhere", self.shortWhere)
        latex += context.format_variable("doi", self.doi)
        latex += context.format_variable("arxiv", self.arxiv)
        latex += context.format_style(
            self.style, before="style = ", indent=1, comma=True
        )
        latex += "}\n"

        return latex

    def to_html(self, context: contexts.html.HTMLContext, indent: int) -> str:
        html = context.open_div("item", indent)
        indent += 1

        html += context.open_div("upper", indent)
        indent += 1

        if self.reference is not None:
            html += context.header(
                3,
                context.span_block("reference", self.reference) + " " + self.title,
                "title",
                indent,
            )
        else:
            html += context.header(3, self.title, "title", indent)

        html += context.simple_div_block("time", self.year, indent)

        indent -= 1
        html += context.close_div(indent)  # upper

        details = context.span_block("authors", self.authors + ".")
        if self.where is not None:
            details += context.span_block("where", self.where + ".")
        if self.shortWhere is not None:
            details += context.span_block("shortWhere", self.shortWhere + ".")
        if self.doi is not None:
            details += context.link_block(
                "doi",
                "https://doi.org/" + self.doi,
                "DOI: " + self.doi,
                ". ",
            )
        if self.arxiv is not None:
            details += context.link_block(
                "doi arxiv",
                "https://doi.org/" + self.arxiv,
                "arXiv: " + self.arxiv,
                ". ",
            )

        html += context.paragraph_block("details", details, indent)

        indent -= 1
        html += context.close_div(indent)  # item

        return html


class PublicationModule(mod.Module):
    """Publication module, holding data for the job positions defined in the JSON file."""

    def __init__(self, level: int = 1, section: str = "Publications"):
        super().__init__(level, section)

    def _load(self, json_object):
        return Publication(**json_object)

    def _get_class_name(self) -> str:
        return "publications"
