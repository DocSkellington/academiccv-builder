from typing import List, Union, Callable, Tuple
from pathlib import Path

from . import Context, Style, PersonalData
from .. import modules as mod


class HTMLContext(Context):
    def __init__(self, output_path: Union[Path, str]) -> None:
        super().__init__("html", output_path)
        self.css_files = []
        self.title_fct = None
        self.stack: List[Tuple[str, int]] = []

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

    def close_block(self) -> str:
        if len(self.stack) > 0:
            tag, indent = self.stack.pop()
            return "\t" * indent + f"</{tag}>\n"
        return ""

    def _get_indent(self) -> int:
        if len(self.stack) > 0:
            return self.stack[-1][1] + 1
        else:
            return 3

    def open_section(self, level: int, name: str, class_name: str) -> str:
        if level <= 0 or level > 6:
            return ""

        indent = self._get_indent()
        tag = "article" if level == 1 else "section"
        self.stack.append((tag, indent))

        section = "\t" * indent + f'<{tag} class="section {class_name}">\n'
        section += self.header(level, name, class_name)
        return section

    def header(self, level: int, name: str, class_name: str) -> str:
        if level <= 0 or level > 6:
            return ""

        return (
            "\t" * self._get_indent()
            + f'<h{level} class="{class_name}">{name}</h{level}>\n'
        )

    def open_div(self, class_name: str) -> str:
        indent = self._get_indent()
        self.stack.append(("div", indent))
        return "\t" * indent + f'<div class="{class_name}">\n'

    def simple_div_block(self, class_name: str, content: str) -> str:
        if content is None:
            return ""
        div = self.open_div(class_name)
        div += "\t" * self._get_indent() + content + "\n"
        div += self.close_block()
        return div

    def paragraph_block(self, class_name: str, content: str) -> str:
        if content is None:
            return ""
        indent = self._get_indent()
        p = "\t" * indent + f'<p class="{class_name}">\n'
        p += "\t" * (indent + 1) + content + "\n"
        p += "\t" * indent + "</p>\n"
        return p

    def span_block(self, class_name: str, content: str) -> str:
        if content is None:
            return ""

        return f'<span class="{class_name}">{content}</span>'

    def link_block(self, class_name: str, link: str, content: str, after: str) -> str:
        if content is None:
            return ""

        return f'<a class="{class_name}" href="{link}">{content}</a>{after}'

    def open_list(self, numbered: bool, class_name: str) -> str:
        tag = "ol" if numbered else "ul"
        indent = self._get_indent()
        self.stack.append((tag, indent))
        return "\t" * indent + f'<{tag} class="{class_name}">\n'

    def list_item(self, class_name: str, content: str) -> str:
        if content is None:
            return ""
        return "\t" * self._get_indent() + f'<li class="{class_name}">{content}</li>\n'

    def img_block(self, class_name: str, img: str, alt: str) -> str:
        return (
            "\t" * self._get_indent()
            + f'<img class="{class_name}" src="{img}" alt="{alt}"/>\n'
        )

    def _build_output(self, modules: List[mod.Module], personal: PersonalData) -> str:
        html = '<!DOCTYPE html>\n<html lang="en">\n'
        html += self._head(personal)
        html += "\n"
        html += self._body(modules, personal)
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

        sidebar += self.open_section(2, "CONTACT", "contact")

        sidebar += self.open_list(False, "contact-list")

        if isinstance(personal.email, list):
            for email in personal.email:
                sidebar += self.list_item(
                    "mail", self.link_block("mail-link", f"mailto:{email}", email, "")
                )
        else:
            sidebar += self.list_item(
                "mail",
                self.link_block(
                    "mail-link", f"mailto:{personal.email}", personal.email, ""
                ),
            )

        if personal.address is not None:
            sidebar += self.list_item(
                "address",
                self.link_block(
                    "address-link",
                    personal.address.link,
                    personal.address.street
                    + ", "
                    + str(personal.address.zipcode)
                    + ", "
                    + personal.address.city
                    + ", "
                    + personal.address.country,
                    "",
                ),
            )

        if personal.pdf is not None:
            sidebar += self.list_item(
                "pdf",
                self.link_block("pdf-link", personal.pdf, "Curriculum vitae", ""),
            )

        if personal.github is not None:
            sidebar += self.list_item(
                "github",
                self.link_block(
                    "github-link",
                    f"https://github.com/{personal.github}",
                    personal.github,
                    "",
                ),
            )

        if personal.orcid is not None:
            sidebar += self.list_item(
                "orcid",
                self.link_block(
                    "orcid-link",
                    f"https://orcid.org/{personal.orcid}",
                    personal.orcid,
                    "",
                ),
            )

        if personal.linkedin is not None:
            sidebar += self.list_item(
                "linkedin",
                self.link_block(
                    "linkedin-link",
                    f"https://linkedin.com/in/{personal.linkedin}",
                    personal.linkedin,
                    "",
                ),
            )

        sidebar += self.close_block()  # list

        sidebar += self.close_block()  # contact

        if len(personal.languages) > 0:
            sidebar += self.open_section(2, "LANGUAGES", "languages")

            sidebar += self.open_list(False, "languages-list")

            for language in personal.languages:
                sidebar += self.list_item(
                    "language",
                    self.span_block("language-name", language.name)
                    + " "
                    + self.span_block("language-level", f"({language.level})"),
                )

            sidebar += self.close_block()  # list

            sidebar += self.close_block()  # languages

        sidebar += self.close_block() + "\n"  # sidebar
        return sidebar

    def _footer(self, _modules: mod.Module, _personal: PersonalData) -> str:
        return ""
