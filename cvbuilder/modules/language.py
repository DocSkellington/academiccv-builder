from __future__ import annotations
from dataclasses import dataclass

from .. import modules
from .. import contexts


@dataclass
class Language(modules.Data):
    """Dataclass for a single language"""

    name: modules.description.Description = modules.description.DescriptionDescriptor()
    level: modules.description.Description = modules.description.DescriptionDescriptor()

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        raise NotImplementedError("Languages module does not support the LaTeX context")

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        return context.simple_div_block(
            "language",
            context.span_block("language-name", self.name)
            + " "
            + context.span_block("language-level", f"({self.level})"),
        )


class LanguageModule(modules.Module):
    def __init__(
        self,
        level: int = 1,
        section: str = "Languages",
        introduction_text: str = "",
        icon: str = "iconoir-chat-bubble-translate",
        use_subsections: bool = True,
    ):
        super().__init__(
            level=level,
            section=section,
            section_icon=icon,
            use_subsections=use_subsections,
            introduction_text=introduction_text,
        )

    def _load(self, json_object) -> Language:
        return Language(**json_object)

    def _get_class_name(self) -> str:
        return "language"
