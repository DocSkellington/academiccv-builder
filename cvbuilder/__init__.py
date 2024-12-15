"""
The CV builder reads a JSON file and uses this file to produce new documents.
"""

from dataclasses import dataclass
from pathlib import Path
import sys
import json
from . import modules, contexts


class Builder:
    """The builder orchestrates the whole process of reading JSON files to produce a CV.

    Once contexts are registered, it suffices to call the `build` function with the JSON file(s) to use.
    Each context will then load the data from the JSON file(s) before producing their output document(s).

    The builder also loads data that appear under the key `self.personal_key` (by default, `"personal"`; `see `__init__`).
    These data can then be used by the context when producing the output file(s), without needing an explicit module.
    This can be useful to define meta-properties (such as the document's author or title), for instance.

    Warning:
        A builder requires (at least) one *context*.
        Otherwise, an error message is displayed and nothing is performed.

    Warning:
        The behavior of the program when the same key appears in multiple files is undefined.

    Note:
        The contexts are treated *in the order they are passed to the builder*.
    """

    def __init__(self, personal_key: str = "personal") -> None:
        """Initializes a new builder, without any context.

        Args:
            personal_key: . Defaults to "personal".
        """
        self.contexts: list[contexts.Context] = []
        self.personal_key = personal_key

    def register_context(self, context: contexts.Context) -> None:
        """Registers a new context.

        Modules can still be added to the context after its registration.

        Args:
            context: the context to register.
        """
        self.contexts.append(context)

    def build(self, json_file_paths: Path | str | list[Path | str]) -> None:
        """Builds the documents from the JSON file(s) at the given location(s).

        The contents of the JSON file(s) are passed to each context, in the same order they were registered.

        Warning:
            Having the same key in more than one file is an undefined behavior.

        Args:
            json_file_paths: The path(s) to the JSON file(s)
        """
        if len(self.contexts) == 0:
            print("Builder: nothing to do, as there is no context", file=sys.stderr)
            return

        if not isinstance(json_file_paths, list):
            json_file_paths = [json_file_paths]

        personal = None
        for json_file_path in json_file_paths:
            if isinstance(json_file_path, str):
                json_file_path = Path(json_file_path)

            with json_file_path.open(encoding="UTF8") as file:
                content = json.load(file)

            if self.personal_key in content:
                personal = contexts.PersonalData(**content[self.personal_key])

            for context in self.contexts:
                context.load_data_from_document(content)

        for context in self.contexts:
            context.write_output(personal)
