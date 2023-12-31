from typing import List

from .. import modules as mod
from .. import contexts


class Logos(mod.Data):
    def __init__(
        self,
        logos: List[str],
    ):
        self.logos = logos

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        raise NotImplementedError(
            "Logos module does not support the LaTeX context"
        )

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_div("logos")

        html += context.open_div("align")

        for index, logo in enumerate(self.logos):
            html += context.img_block(f"logo{index}", logo, "")

        html += context.close_block()  # align

        html += context.close_block()  # logos

        return html


class LogosModule(mod.Module):
    def __init__(
        self,
    ):
        super().__init__(0, "", "")

    def load(self, json_value) -> None:
        self.data.append((None, [self._load(json_value)]))

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        raise NotImplementedError("Logos module is not implemented for LaTeX")

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        return self.data[0][1][0].to_html(context)

    def _load(self, json_object) -> Logos:
        return Logos(json_object)

    def _get_class_name(self) -> str:
        return "logos"
