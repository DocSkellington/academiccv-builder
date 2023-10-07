from typing import List, Union
from pathlib import Path

from . import Context, PersonalData, html
from .. import modules as mod


class MarkdownContext(Context, html.HTMLStack):
    def __init__(self, output_path: Union[Path, str], title: str) -> None:
        Context.__init__(self, "markdown", output_path)
        html.HTMLStack.__init__(self)
        self.title = title

    def _get_indent(self) -> int:
        if len(self.stack) > 0:
            return self.stack[-1][1] + 1
        return 0

    def open_section(
        self, level: int, name: str, _class_name: str = None, _icon: str = None
    ) -> str:
        self.stack.append((None, self._get_indent() - 1))

        if name != "":
            return "\n" + "#" * level + " " + name + "\n\n"
        return ""

    def paragraph(self, contents: str | mod.Description) -> str:
        if contents is None:
            return ""

        if isinstance(contents, mod.Description):
            return contents.to_markdown(self)
        return contents

    def link(self, url: str, text: str) -> str:
        return f"[{text}]({url})"

    def _build_output(self, modules: List[mod.Module], personal: PersonalData) -> str:
        markdown = f"title: {self.title}\n\n{self._run_modules(modules)}"
        return markdown
