"""
Module for publications.
"""

from __future__ import annotations
from dataclasses import dataclass

from .. import contexts
from .. import modules


@dataclass
class Publication(modules.Data):
    """A publication must have a title, authors, and a publication year."""

    title: str
    authors: str
    year: str | int
    reference: modules.description.Description = (
        modules.description.DescriptionDescriptor()
    )
    where: modules.description.Description = modules.description.DescriptionDescriptor()
    shortWhere: modules.description.Description = (
        modules.description.DescriptionDescriptor()
    )
    doi: str = None
    arxiv: str = None
    note: modules.description.Description = modules.description.DescriptionDescriptor()
    style: contexts.latex.Style = None

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = "\\publication{\n"
        latex += context.format_variable("title", self.title)
        latex += context.format_variable("authors", self.authors)
        latex += context.format_variable("year", self.year)
        latex += context.format_variable("reference", self.reference)
        latex += context.format_variable("where", self.where)
        latex += context.format_variable("shortWhere", self.shortWhere)
        latex += context.format_variable("doi", self.doi)
        latex += context.format_variable("arxiv", self.arxiv)
        latex += context.format_variable("note", self.note)
        latex += context.format_style(
            self.style, before="style = ", indent=1, comma=True
        )
        latex += "}\n"

        return latex

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_div("item")

        html += context.open_div("align")

        if not self.reference.is_empty():
            html += context.simple_div_block(
                "title",
                context.span_block("reference", f"[{self.reference.to_html()}]")
                + " "
                + self.title,
            )
        else:
            html += context.simple_div_block("title", self.title)

        html += context.simple_div_block("time", self.year)

        html += context.close_block()  # align

        details = context.span_block("authors", self.authors + ". ")
        if not self.where.is_empty():
            details += context.span_block("where", self.where.to_html() + ". ")
        if not self.shortWhere.is_empty():
            details += context.span_block(
                "shortWhere", self.shortWhere.to_html() + ". "
            )
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
        if not self.note.is_empty():
            details += context.span_block("note", self.note.to_html() + ". ")

        html += context.paragraph_block("details", details)

        html += context.close_block()  # item

        return html


class PublicationModule(modules.Module):
    """Publication module, holding data for the job positions defined in the JSON file."""

    def __init__(
        self,
        level: int = 1,
        section: str = "Publications",
        introduction_text: str = "",
        icon: str = "iconoir-journal",
        use_subsections: bool = True,
    ):
        super().__init__(
            level=level,
            section=section,
            section_icon=icon,
            use_subsections=use_subsections,
            introduction_text=introduction_text,
        )

    def _load(self, json_object):
        return Publication(**json_object)

    def _get_class_name(self) -> str:
        return "publications"
