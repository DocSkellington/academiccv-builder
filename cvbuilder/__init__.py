"""
The CV builder reads a JSON file and uses this file to produce new documents.
"""

from dataclasses import dataclass
from typing import List, Union
from pathlib import Path
import json
from . import modules, contexts

@dataclass
class ModuleDescriptor:
    in_json: str
    module: modules.Module
    category: str

# Modules are processed in the order they are added
class Builder:
    """The builder reads a JSON file to create documents in other formats, dictated by 'contexts'.

    For each loaded context, it produces one (or multiple, depending on the context) documents.
    These documents are built from modules. Each one processes a specific part of the JSON file.
    The modules and contexts are treated *in the order they are passed to the builder*.
    """

    def __init__(self) -> None:
        self.modules: List[ModuleDescriptor] = []
        self.contexts: List[contexts.Context] = []

    def add_context(self, context: contexts.Context) -> None:
        """Adds a new context to the builder.

        Arguments:
            context -- The context
        """
        self.contexts.append(context)

    def add_module(self, in_json: str, module: modules.Module, category: str = "default") -> None:
        """Adds a new module.

        Each module is filled from data stored in the JSON file.
        The 'in_json' argument defines which key contains the data to be used for this module.
        If None, no value is read.

        Arguments:
            in_json -- The JSON key
            module -- The module
        """
        self.modules.append(ModuleDescriptor(in_json, module, category))

    def build(self, json_file_path: Union[Path, str]) -> None:
        """Builds the documents from the JSON file at the given location.

        Modules and contexts are treated in the same order they were added.

        Arguments:
            json_file -- The path to the JSON file
        """
        if isinstance(json_file_path, str):
            json_file_path = Path(json_file_path)

        with json_file_path.open(encoding="UTF8") as file:
            content = json.load(file)

        personal = contexts.PersonalData(**content["personal"])

        for module in self.modules:
            if module.in_json is not None:
                module.module.load(content[module.in_json])

        for context in self.contexts:
            context.write_output(self.modules, personal)