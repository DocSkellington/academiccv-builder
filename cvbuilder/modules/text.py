"""
Text and Link modules to produce text that does not depend on the JSON document.
"""

from __future__ import annotations

from .. import contexts, modules


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
        super().__init__(
            level=level,
            section=section,
            section_icon=icon,
            use_subsections=False,
            introduction_text=text,
        )

    def load(self, json_value) -> None:
        raise NotImplementedError(
            "Text module does not support loading data from JSON document"
        )

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_section(
            self.level,
            self.section,
            self.section.lower().replace(" ", "-"),
            self.section_icon,
        )
        html += context.paragraph_block("text", self.introduction_text.to_html())
        html += context.close_block()
        return html
