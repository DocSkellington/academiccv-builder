from typing import List

from .. import modules as mod
from .. import contexts


class Summary(mod.Data):
    def __init__(
        self,
        logos: List[str],
        text: mod.Description,
        level: int,
        section: str,
        icon: str,
    ):
        self.logos = logos
        if text is not None:
            self.text = mod.Description(text)
        else:
            self.text = None
        self.level = level
        self.section = section
        self.icon = icon

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        raise NotImplementedError(
            "The summary module does not support the LaTeX context"
        )

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_div("logos")

        html += context.open_div("align")

        for index, logo in enumerate(self.logos):
            html += context.img_block(f"logo{index}", logo, "")

        html += context.close_block()  # align

        html += context.close_block()  # logos

        html += context.open_section(self.level, self.section, "summary", self.icon)

        html += context.simple_div_block("details", self.text)

        html += context.close_block()

        return html


class SummaryModule(mod.Module):
    def __init__(
        self,
        level: int = 0,
        section: str = "Summary",
        icon: str = "iconoir-chat-bubble",
    ):
        super().__init__(level, section, icon)

    def load(self, json_value) -> None:
        self.data.append((None, [self._load(json_value)]))

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        raise NotImplementedError("Summary module is not implemented for LaTeX")

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        return self.data[0][1][0].to_html(context)

    def _load(self, json_object) -> Summary:
        logos = json_object["logos"] if "logos" in json_object else []
        text = json_object["text"] if "text" in json_object else None
        return Summary(logos, text, self.level + 1, self.section, self.section_icon)

    def _get_class_name(self) -> str:
        return "summary"
