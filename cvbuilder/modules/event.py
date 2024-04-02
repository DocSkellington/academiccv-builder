from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import datetime
import dateutil.parser

from .. import modules
from .. import contexts


@dataclass
class Event(modules.Data):
    year: datetime.datetime = None
    name: modules.description.Description = modules.description.DescriptionDescriptor()
    where: modules.description.Description = modules.description.DescriptionDescriptor()

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        raise NotImplementedError(
            "The events module does not support the LaTeX context"
        )

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_div("item")

        html += context.open_div("align")

        html += context.simple_div_block("title", self.name)
        html += context.simple_div_block("where", self.where)

        html += context.close_block()

        html += context.close_block()

        return html


class EventModule(modules.Module):
    """Event module.

    Events are automatically sorted and grouped by year.
    Within a year, the order of the JSON document is followed.
    """

    def __init__(
        self,
        level: int = 1,
        section: str = "Attended events",
        introduction_text: str = "",
        icon: str = "iconoir-calendar",
        use_subsections: bool = True,
    ):
        super().__init__(
            level=level,
            section=section,
            section_icon=icon,
            use_subsections=use_subsections,
            introduction_text=introduction_text,
        )

    def load(self, json_value: list[dict[str, Any]]) -> None:
        events = list(map(self._load, json_value))

        if self.use_subsections:
            self.data = modules.sort_by_date(
                modules.group_per_year(events, lambda event: event.year),
                lambda event: event.year,
            )
        else:
            events.sort(lambda event: event.year)
            self.data.append((None, events))

    def _load(self, json_object) -> Event:
        year = (
            dateutil.parser.parse(str(json_object["year"]))
            if "year" in json_object
            else Event.year
        )
        name = json_object["name"] if "name" in json_object else Event.name
        where = json_object["where"] if "where" in json_object else Event.where
        return Event(year=year, name=name, where=where)

    def _get_class_name(self) -> str:
        return "event"
