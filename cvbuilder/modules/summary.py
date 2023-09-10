from typing import List

from .. import modules as mod
from .. import contexts


class Summary(mod.Data):
    def __init__(self, logos: List[str], text: mod.Description):
        self.logos = logos
        if text is not None:
            self.text = mod.Description(text)
        else:
            self.text = None

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        raise NotImplementedError(
            "The summary module does not support the LaTeX context"
        )

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_div("logos")

        html += context.open_div("align")

        for index, logo in enumerate(self.logos):
            html += context.img_block(f"logo{index}", logo, "")

        html += context.close_block() # align

        html += context.close_block() # logos

        html += context.simple_div_block("details", self.text)

        return html


class SummaryModule(mod.Module):
    def __init__(self, level: int = 0, section: str = ""):
        super().__init__(level, section)

    def load(self, json_value) -> None:
        self.data.append((None, [self._load(json_value)]))

    def _load(self, json_object) -> Summary:
        logos = json_object["logos"] if "logos" in json_object else []
        text = json_object["text"] if "text" in json_object else None
        return Summary(logos, text)

    def _get_class_name(self) -> str:
        return "summary"
