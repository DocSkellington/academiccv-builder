from __future__ import annotations
from dataclasses import dataclass

from .. import modules
from .. import contexts


@dataclass
class Summary(modules.Data):
    text: modules.description.Description = modules.description.DescriptionDescriptor()

    def to_latex(self, _context: contexts.latex.LaTeXContext) -> str:
        return self.text.to_latex()

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        return context.simple_div_block("details", self.text)

    def to_markdown(self, context: contexts.markdown.MarkdownContext) -> str:
        return context.paragraph(self.text)


class SummaryModule(modules.Module):
    def __init__(
        self,
        level: int = 0,
        section: str = "Summary",
        icon: str = "iconoir-chat-bubble",
        use_subsections: bool = True,
    ):
        super().__init__(level, section, icon, use_subsections)

    def load(self, json_value) -> None:
        self.data.append((None, [self._load(json_value)]))

    def _load(self, json_object) -> Summary:
        return Summary(json_object)

    def _get_class_name(self) -> str:
        return "summary"
