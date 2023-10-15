"""
Text and Link modules to produce text that does not depend on the JSON document.
"""

from __future__ import annotations
from dataclasses import dataclass

from .. import contexts, modules


@dataclass
class TextData(modules.Data):
    text: modules.description.Description = modules.description.DescriptionDescriptor()

    def to_latex(self, _context: contexts.latex.LaTeXContext) -> str:
        return self.text.to_latex()

    def to_html(self, _context: contexts.html.HTMLContext) -> str:
        return self.text.to_html()

    def to_markdown(self, _context: contexts.markdown.MarkdownContext) -> str:
        return self.text.to_markdown()


class TextModule(modules.Module):
    """The text module produces a fixed text, that does not depend on the JSON document.

    Set the level to any value that is not between 1 and 6 to disable the sectioning.
    """

    def __init__(
        self,
        section: str,
        text: str | modules.description.Description,
        level: int = 2,
        icon: str = "",
    ) -> None:
        super().__init__(level, section, icon, False)
        self.text: TextData = TextData(text=text)

    def load(self, json_value) -> None:
        raise NotImplementedError(
            "Text module does not support loading data from JSON document"
        )

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        return f"\\section{{{self.section}}}\n{self.text.to_latex(context)}\n"

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_section(
            self.level,
            self.section,
            self.section.lower().replace(" ", "-"),
            self.section_icon,
        )
        html += context.paragraph_block("text", self.text.to_html(context))
        html += context.close_block()
        return html

    def to_markdown(self, context: contexts.markdown.MarkdownContext) -> str:
        return (
            context.open_section(self.level, self.section)
            + self.text.to_markdown(context)
            + context.close_block()
        )
