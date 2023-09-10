"""
Text and Link modules to produce text that does not depend on the JSON document.
"""

from . import Module
from .. import contexts


class TextModule(Module):
    """The text module produces a fixed text, that does not depend on the JSON document.

    Set the level to any value that is not between 1 and 6 to disable the sectioning.
    """

    def __init__(self, section: str, text: str, level: int = 2, icon: str = "") -> None:
        super().__init__(level, section, icon)
        self.text = text

    def to_latex(self, _context: contexts.latex.LaTeXContext) -> None:
        return f"\\section{{{self.section}}}\n{self.text}\n"

    def to_html(self, context: contexts.html.HTMLContext) -> None:
        html = context.open_section(
            self.level,
            self.section,
            self.section.lower().replace(" ", "-"),
            self.section_icon,
        )
        html += context.paragraph_block("text", self.text)
        html += context.close_block()
        return html


class LinkModule(Module):
    """The link module produces a fixed text including a link to some other resource.

    Set the level to any value that is not between 1 and 6 to disable the sectioning.
    """

    def __init__(
        self,
        section: str,
        before: str,
        link: str,
        text: str,
        after: str,
        level: int = 2,
        icon: str = "",
    ) -> None:
        if section == "":
            super().__init__(0, "", icon)
        else:
            super().__init__(level, section, icon)

        self.section = section
        self.before = before
        self.link = link
        self.text = text
        self.after = after

    def to_latex(self, context: contexts.latex.LaTeXContext) -> None:
        section = context.open_section(self.level, self.section)

        url = ""
        if self.text != "":
            url = f"\\href{{{self.link}}}{{{self.text}}}"
        else:
            url = f"\\url{{{self.link}}}"

        return f"{section}{self.before}{url}{self.after}\n"

    def to_html(self, context: contexts.html.HTMLContext) -> None:
        content = self.before + context.link_block("", self.link, self.text, self.after)

        link = context.open_section(
            self.level,
            self.section,
            self.section.lower().replace(" ", "-"),
            self.section_icon,
        )
        link += context.paragraph_block("text", content)
        link += context.close_block()
        return link
