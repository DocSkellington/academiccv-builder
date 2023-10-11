from dataclasses import dataclass
from typing import Any
import datetime
import dateutil.parser

from .. import modules as mod
from .. import contexts


@dataclass
class Talk(mod.Data):
    date: datetime.datetime = None
    title: str = None
    conference: str = None
    where: str = None
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
        if self.conference is not None:
            details += context.span_block("conference", self.conference + ". ")
        if self.where is not None:
            details += context.span_block("where", self.where + ".")

        html += context.paragraph_block("details", details)

        html += context.close_block()  # item
        return html


class TalkModule(mod.Module):
    """Talk module.

    Talks are automatically sorted by their date, and grouped together by year.
    """

    def __init__(
        self, level: int = 1, section: str = "Talks", icon: str = "iconoir-sound-high"
    ) -> None:
        super().__init__(level, section, icon)

    def load(self, json_value: list[dict[str, Any]]) -> None:
        talks = list(map(self._load, json_value))

        # If you wish to disable the subsections, replace the rest of this function by
        # talks.sort(lambda talk: talk.date.year)
        # self.data.append((None, talks))

        years = sorted(list(set(map(lambda talk: talk.date.year, talks))), reverse=True)

        for year in years:
            data = []
            for talk in talks:
                if talk.date.year == year:
                    data.append(talk)
            self.data.append((str(year), data))

    def _load(self, json_object) -> Talk:
        date = (
            dateutil.parser.parse(json_object["date"])
            if "date" in json_object
            else Talk.date
        )
        title = json_object["title"] if "title" in json_object else Talk.title
        conference = (
            json_object["conference"]
            if "conference" in json_object
            else Talk.conference
        )
        where = json_object["where"] if "where" in json_object else Talk.where
        style = (
            contexts.latex.Style(**json_object["style"])
            if "style" in json_object
            else Talk.style
        )
        return Talk(
            date=date, title=title, conference=conference, where=where, style=style
        )

    def _get_class_name(self) -> str:
        return "talks"
