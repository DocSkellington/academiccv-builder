from __future__ import annotations
import markdown

from ..modules.utils import etree_to_latex

class Description():
    """A descriptive string written in Markdown.

    The Markdown is converted to LaTeX, HTML, or kept as-is, depending on the output format.
    """

    def __init__(self, description: str) -> None:
        self.description = description

    def to_latex(self) -> str:
        markdown.Markdown.output_formats["latex"] = etree_to_latex.to_latex_string
        return markdown.markdown(self.description, output_format="latex")

    def to_html(self) -> str:
        return markdown.markdown(self.description, output_format="html")

    def to_markdown(self) -> str:
        return self.description
