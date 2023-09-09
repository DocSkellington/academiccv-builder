from typing import List, Union, Callable
from pathlib import Path

from . import Context, Style, PersonalData
from .. import modules as mod


class HTMLContext(Context):
    def __init__(self, output_path: Union[Path, str]) -> None:
        super().__init__("html", output_path)
        self.css_files = []
        self.title_fct = None

    def add_css_file(self, css_path: Union[Path, str]) -> None:
        if isinstance(css_path, str):
            css_path = Path(css_path)
        self.css_files.append(css_path)

    def format_variable(self, name: str, value: str) -> str:
        raise NotImplementedError(
            "Contexts should implement format_variable(self, name: str, value: str)"
        )

    def format_style(self, style: Style, **kwargs) -> str:
        raise NotImplementedError(
            "Contexts should implement format_style(self, style: Style, *args, **kwargs)"
        )

    def set_title_fct(self, title_fct: Callable[[PersonalData], str]) -> None:
        self.title_fct = title_fct

    def open_section(
        self, level: int, name: str, class_name: str, indent: int = -1
    ) -> str:
        if level <= 0 or level > 6:
            return ""

        if indent == -1:
            indent = 2 + level - 1
        section = (
            "\t" * indent
            + ("<article" if level == 1 else "<section")
            + f' class="{class_name}"'
            + ">\n"
        )
        section += self.header(level, name, class_name, indent+1)
        return section

    def header(self, level: int, name: str, class_name: str, indent: int = -1) -> str:
        if level <= 0 or level > 6:
            return ""

        if indent == -1:
            indent = 2 + level - 1
        return "\t" * indent + f"<h{level} class=\"{class_name}\">{name}</h{level}>\n"

    def close_section(self, level: int, indent: int = -1) -> str:
        if indent == -1:
            indent = 2 + level - 1
        return "\t" * indent + ("</article>" if level == 1 else "</section>") + "\n\n"

    def open_div(self, class_name: str, indent: int) -> str:
        return "\t" * indent + f"<div class=\"{class_name}\">\n"

    def close_div(self, indent: int) -> str:
        return "\t" * indent + "</div>\n"

    def simple_div_block(self, class_name: str, content: str, indent: int) -> str:
        if content is None:
            return ""
        div = self.open_div(class_name, indent)
        div += "\t" * (indent + 1) + content + "\n"
        div += self.close_div(indent)
        return div

    def paragraph_block(self, class_name: str, content: str, indent: int) -> str:
        if content is None:
            return ""
        p = "\t" * indent + f"<p class=\"{class_name}\">\n"
        p += "\t" * (indent + 1) + content + "\n"
        p += "\t" * indent + "</p>\n"
        return p

    def span_block(self, class_name: str, content: str) -> str:
        if content is None:
            return ""

        return f"<span class=\"{class_name}\">{content} </span>"

    def link_block(self, class_name: str, link: str, content: str, after: str) -> str:
        if content is None:
            return ""

        return f"<a class=\"{class_name}\" href=\"{link}\">{content}</a>{after}"

    def _build_output(self, modules: List[mod.Module], personal: PersonalData) -> str:
        html = '<!DOCTYPE html>\n<html lang="en">\n'
        html += self._head(personal)
        html += "\n"
        html += self._body(modules, personal)
        html += "\n\n</html>"
        return html

    def _head(self, personal: PersonalData) -> str:
        title = ""
        if self.title_fct is None:
            title = f"{personal.name} - {personal.position}"
        else:
            title = self.title_fct(personal)

        head = f"""\t<head>
\t\t<meta charset="UTF-8">
\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">
\t\t<meta http-equiv="X-UA-Compatible" content="ie=edge">
\t\t<title>{title}</title>
\t\t<link rel="icon" href="./favicon.ico" type="image/x-icon">
"""
        for css in self.css_files:
            head += f'\t\t<link rel="stylesheet" href="{css}">\n'
        head += "\t</head>\n"
        return head

    def _body(self, modules: List[mod.Module], personal: PersonalData) -> str:
        body = "\t<body>\n"
        body += self._header(modules, personal)
        body += self._main(modules, personal)
        body += self._footer(modules, personal)
        body += "\t</body>\n"
        return body

    def _header(self, _modules: mod.Module, _personal: PersonalData) -> str:
        return ""

    def _main(self, modules: List[mod.Module], personal: PersonalData) -> str:
        main = "\t\t<main>\n"
        main += self._sidebar(modules, personal)
        main += self._run_modules(modules)
        main += "\t\t</main>\n"
        return main

    def _sidebar(self, _modules: mod.Module, personal: PersonalData) -> str:
        indent = 3
        sidebar = "\t" * indent + '<div class="sidebar">\n'
        indent += 1

        sidebar += "\t" * indent + '<div class="profile-container">\n'
        indent += 1

        if personal.photo is not None:
            sidebar += (
                "\t" * indent
                + f'<img class="profile" src="{personal.photo}" alt=""/>\n'
            )
        sidebar += "\t" * indent + f"<h1>{personal.name}</h1>\n"
        sidebar += "\t" * indent + f"<h3>{personal.position}</h3>\n"

        indent -= 1
        sidebar += "\t" * indent + "</div>\n"  # profile-container

        indent -= 1
        sidebar += "\t" * indent + "</div>\n\n"  # sidebar
        return sidebar

    def _footer(self, _modules: mod.Module, _personal: PersonalData) -> str:
        return ""
