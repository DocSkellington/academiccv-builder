from .. import modules as mod
from .. import contexts


class Summary(mod.Data):
    def __init__(
        self,
        text: mod.Description,
    ):
        if text is not None:
            self.text = mod.Description(text)
        else:
            self.text = None

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        raise NotImplementedError(
            "The summary module does not support the LaTeX context"
        )

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        return context.simple_div_block("details", self.text)

    def to_markdown(self, context: contexts.markdown.MarkdownContext) -> str:
        return context.paragraph(self.text)


class SummaryModule(mod.Module):
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
