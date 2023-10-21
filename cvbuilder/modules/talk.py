from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import datetime
import dateutil.parser

from .. import modules
from .. import contexts


@dataclass
class Talk(modules.Data):
    date: datetime.datetime = None
    title: modules.description.Description = modules.description.DescriptionDescriptor()
    conference: modules.description.Description = (
        modules.description.DescriptionDescriptor()
    )
    where: modules.description.Description = modules.description.DescriptionDescriptor()
    pdf: str = None
    video: str = None
    style: contexts.latex.Style = None

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = "\\talk{\n"
        latex += context.format_variable("date", context.format_date(self.date))
        latex += context.format_variable("title", self.title)
        latex += context.format_variable("conference", self.conference)
        latex += context.format_variable("where", self.where)
        latex += context.format_style(
            self.style, before="style = ", indent=1, comma=True
        )
        latex += "}\n"
        return latex

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_div("item")

        html += context.open_div("align")

        html += context.simple_div_block("title", self.title)

        html += context.simple_div_block("time", context.format_date(self.date))

        html += context.close_block()  # align

        details = ""
        if not self.conference.is_empty():
            details += context.span_block(
                "conference", self.conference.to_html() + ". "
            )
        if not self.where.is_empty():
            details += context.span_block("where", self.where.to_html() + ". ")
        if self.pdf is not None:
            details += context.link_block(
                "pdf", link=self.pdf, content="Link to PDF", after=". "
            )
        if self.video is not None:
            details += context.link_block(
                "pdf", link=self.video, content="Link to video", after=". "
            )

        if details != "":
            html += context.paragraph_block("details", details)

        html += context.close_block()  # item
        return html


class TalkModule(modules.Module):
    """Talk module.

    Talks are automatically sorted by their date, and grouped together by year.
    """

    def __init__(
        self,
        level: int = 1,
        section: str = "Talks",
        introduction_text: str = "",
        icon: str = "iconoir-sound-high",
        use_subsections: bool = True,
    ) -> None:
        super().__init__(
            level=level,
            section=section,
            section_icon=icon,
            use_subsections=use_subsections,
            introduction_text=introduction_text,
        )

    def load(self, json_value: list[dict[str, Any]]) -> None:
        talks = list(map(self._load, json_value))

        if self.use_subsections:
            years = sorted(
                list(set(map(lambda talk: talk.date.year, talks))), reverse=True
            )

            for year in years:
                data = []
                for talk in talks:
                    if talk.date.year == year:
                        data.append(talk)
                self.data.append((str(year), data))
        else:
            talks.sort(lambda talk: talk.date.year)
            self.data.append((None, talks))

    def _load(self, json_object) -> Talk:
        date = (
            dateutil.parser.parse(json_object["date"])
            if "date" in json_object
            else Talk.date
        )
        title = json_object.get("title", Talk.title)
        conference = json_object.get("conference", Talk.conference)
        where = json_object.get("where", Talk.where)
        pdf = json_object.get("pdf", Talk.pdf)
        video = json_object.get("video", Talk.video)
        style = (
            contexts.latex.Style(**json_object["style"])
            if "style" in json_object
            else Talk.style
        )
        return Talk(
            date=date,
            title=title,
            conference=conference,
            where=where,
            pdf=pdf,
            video=video,
            style=style,
        )

    def _get_class_name(self) -> str:
        return "talks"
