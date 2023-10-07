from dataclasses import dataclass
from typing import List, Dict, Any, Union

from .. import modules as mod
from .. import contexts


@dataclass
class Event(mod.Data):
    year: Union[str, int] = None
    name: str = None
    where: str = None

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


class EventModule(mod.Module):
    """Event module.

    Events are automatically sorted and grouped by year.
    Within a year, the order of the JSON document is followed.
    """

    def __init__(
        self,
        level: int = 0,
        section: str = "Attended events",
        icon: str = "iconoir-calendar",
    ):
        super().__init__(level, section, icon)

    def load(self, json_value: List[Dict[str, Any]]) -> None:
        events = list(map(self._load, json_value))

        # If you wish to disable the subsections, replace the rest of this function by
        # talks.sort(lambda talk: talk.date.year)
        # self.data.append((None, talks))

        years = sorted(
            list(set(map(lambda event: str(event.year), events))), reverse=True
        )

        for year in years:
            data = []
            for event in events:
                if str(event.year) == str(year):
                    data.append(event)
            self.data.append((str(year), data))

    def _load(self, json_object) -> Event:
        # year = (
        #     dateutil.parser.parse(json_object["year"])
        #     if "year" in json_object
        #     else Event.year
        # )
        # name = json_object["name"] if "name" in json_object else Event.name
        # where = json_object["where"] if "where" in json_object else Event.where
        # return Event(year=year, name=name, where=where)
        return Event(**json_object)

    def _get_class_name(self) -> str:
        return "event"
