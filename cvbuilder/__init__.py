"""
The CV builder reads a JSON file and uses this file to produce new documents.
"""

from dataclasses import dataclass
from pathlib import Path
import json
from . import modules, contexts


# Modules are processed in the order they are added
class Builder:
    """The builder reads a JSON file to create documents in other formats, dictated by 'contexts'.

    For each loaded context, it produces one (or multiple, depending on the context) documents.
    These documents are built from modules. Each one processes a specific part of the JSON file.
    The contexts are treated *in the order they are passed to the builder*.
    """

    def __init__(self, personal_key: str = "personal") -> None:
        """Initializes a new builder.

        Keyword Arguments:
            personal_key -- The name of the key whose value contains the "personal" date such as the name, current job position, and so on
                    (default: {"personal"})
        """
        self.contexts: list[contexts.Context] = []
        self.personal_key = personal_key

    def add_context(self, context: contexts.Context) -> None:
        """Adds a new context to the builder.

        Arguments:
            context -- The context
        """
        self.contexts.append(context)

    def build(self, json_file_paths: Path | str | list[Path | str]) -> None:
        """Builds the documents from the JSON file(s) at the given location(s).

        Contexts are treated in the same order they were added.

        Having the same key in more than one file is an undefined behavior.

        Arguments:
            json_file_paths -- The path(s) to the JSON file(s)
        """
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
