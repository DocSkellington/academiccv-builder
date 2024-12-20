from __future__ import annotations
from typing import Callable
from pathlib import Path

from . import Context, PersonalData
from .. import modules


class HTMLStack:
    """A stack for an HTML context.

    It provides utilities to open and close headers, div blocks, paragraphs, and so on.
    """

    def __init__(self) -> None:
        self.stack: list[tuple[str, int]] = []

    def close_block(self) -> str:
        if len(self.stack) > 0:
            tag, indent = self.stack.pop()
            if tag is not None:
                return "\t" * indent + f"</{tag}>\n"
        return ""

    def _get_indent(self) -> int:
        if len(self.stack) > 0:
            return self.stack[-1][1] + 1
        return 3

    def open_section(
        self, level: int, name: str, class_name: str, icon: str = None
    ) -> str:
        if level <= 0 or level > 6:
            return ""

        indent = self._get_indent()
        tag = "section"
        self.stack.append((tag, indent))

        section = "\t" * indent + f'<{tag} class="section {class_name}">\n'
        section += self.header(level, name, class_name, icon)
        return section

    def header(self, level: int, name: str, class_name: str, icon: str = None) -> str:
        if level <= 0 or level > 6:
            return ""

        if icon is None or icon == "":
            icon = ""
        else:
            icon = self.idiomatic_block("section-icon " + icon, "")

        if name == "" and icon == "":
            return ""

        return (
            "\t" * self._get_indent()
            + f'<h{level} class="{class_name}">{icon}{name}</h{level}>\n'
        )

    def open_div(self, class_name: str) -> str:
        indent = self._get_indent()
        self.stack.append(("div", indent))
        return "\t" * indent + f'<div class="{class_name}">\n'

    def simple_div_block(
        self, class_name: str, content: str | modules.description.Description
    ) -> str:
        if content is None:
            return ""
        if isinstance(content, modules.description.Description):
            if content.is_empty():
                return ""
            content = content.to_html()
        div = self.open_div(class_name)
        div += "\t" * self._get_indent() + content + "\n"
        div += self.close_block()
        return div

    def paragraph_block(
        self, class_name: str, content: str | modules.description.Description
    ) -> str:
        if content is None:
            return ""
        if isinstance(content, modules.description.Description):
            if content.is_empty():
                return ""
            content = content.to_html()
        indent = self._get_indent()
        p = "\t" * indent + f'<p class="{class_name}">\n'
        p += "\t" * (indent + 1) + content + "\n"
        p += "\t" * indent + "</p>\n"
        return p

    def span_block(
        self, class_name: str, content: str | modules.description.Description
    ) -> str:
        if content is None:
            return ""
        if isinstance(content, modules.description.Description):
            if content.is_empty():
                return ""
            content = content.to_html()

        return f'<span class="{class_name}">{content}</span>'

    def link_block(self, class_name: str, link: str, content: str, after: str) -> str:
        if content is None or link == "":
            return ""

        return f'<a class="{class_name}" href="{link}">{content}</a>{after}'

    def open_list(self, numbered: bool, class_name: str) -> str:
        tag = "ol" if numbered else "ul"
        indent = self._get_indent()
        self.stack.append((tag, indent))
        return "\t" * indent + f'<{tag} class="{class_name}">\n'

    def list_item(
        self, class_name: str, content: str | modules.description.Description
    ) -> str:
        if content is None:
            return ""
        if isinstance(content, modules.description.Description):
            if content.is_empty():
                return ""
            content = content.to_html()
        return "\t" * self._get_indent() + f'<li class="{class_name}">{content}</li>\n'

    def img_block(self, class_name: str, img: str, alt: str) -> str:
        return (
            "\t" * self._get_indent()
            + f'<img class="{class_name}" src="{img}" alt="{alt}"/>\n'
        )

    def idiomatic_block(self, class_name: str, content: str) -> str:
        return "\t" * self._get_indent() + f'<i class="{class_name}">{content}</i>'


class HTMLContext(Context, HTMLStack):
    def __init__(self, output_path: Path | str) -> None:
        Context.__init__(self, "html", output_path)
        HTMLStack.__init__(self)
        self.css_files = []
        self.title_fct = None

    def add_css_file(self, css_path: Path | str) -> None:
        if isinstance(css_path, str):
            css_path = Path(css_path)
        self.css_files.append(css_path)

    def format_variable(self, name: str, value: str) -> str:
        raise NotImplementedError(
            "Contexts should implement format_variable(self, name: str, value: str)"
        )

    def set_title_fct(self, title_fct: Callable[[PersonalData], str]) -> None:
        self.title_fct = title_fct

    def _build_output(self, personal: PersonalData) -> str:
        html = '<!DOCTYPE html>\n<html lang="en">\n'
        html += self._head(personal)
        html += "\n"
        html += self._body(personal)
        html += "</html>"
        return html

    def _head(self, personal: PersonalData) -> str:
        if personal is None:
            return '\t<head>\n\t\t<meta charset="UTF-8">\n\t</head>\n'

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
\t\t<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/iconoir-icons/iconoir@main/css/iconoir.css">
"""
        for css in self.css_files:
            head += f'\t\t<link rel="stylesheet" href="{css}">\n'
        head += "\t</head>\n"
        return head

    def _body(self, personal: PersonalData) -> str:
        body = "\t<body>\n"
        body += self._header(personal)
        body += self._main(personal)
        body += self._footer(personal)
        body += "\t</body>\n"
        return body

    def _header(self, _personal: PersonalData) -> str:
        return ""

    def _main(self, personal: PersonalData) -> str:
        main = "\t\t<main>\n"
        main += self._sidebar(personal)
        main += self._run_modules()
        main += "\t\t</main>\n"
        return main

    def _sidebar(self, personal: PersonalData) -> str:
        if personal is None:
            return ""

        sidebar = self.open_div("sidebar")

        sidebar += self.open_div("profile-container")

        if personal.photo is not None:
            sidebar += self.img_block("profile", personal.photo, "")
        sidebar += self.simple_div_block("name", personal.name)
        sidebar += self.simple_div_block("position", personal.position)
        sidebar += self.simple_div_block("organization", personal.organization)

        sidebar += self.close_block()  # profile-container

        sidebar += self._run_modules("sidebar")

        sidebar += self.close_block() + "\n"  # sidebar
        return sidebar

    def _footer(self, _personal: PersonalData) -> str:
        return ""
