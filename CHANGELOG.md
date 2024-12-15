# v2.0.0 (dev)

## Features
  - Each context uses its own list of modules (#1).
  - Multiple JSON files can be loaded at the same time (#2).
  - The key holding the personal data can be changed (#5).
  - Simplification of subsections in JSON files (#6).
  - `modules.description.Description` now expects a Markdown string, allowing for a more flexible output (#8).
    - Most of the fields are now instances of `modules.description.Description`
  - Most modules allow an introductory text, put between the section header and the data's output (#7).
  - Links to PDF and video for talks, and to homepage and artifact for projects (#4).
  - Award: only the year is displayed.
  - Added Services.
  - Talks and events are now grouped per year, and sorted by date within each year.
  - LaTeX: possibility to add class options.

## Bug fixes
  - Type annotations do not cause missing imports errors (#3).
  - HTML: an `a` tag (link block) is not constructed when the link is empty.
  - Fixed an error produced by Hatch(ling) when building the wheel file.
  - Fixed an error when calling `markdown` (ModuleNotFoundError: No module named 's').
  - Replaced `iconoir-pin-alt` (not defined anymore) by `iconoir-map-pin`.

## Code details
  - Use Python 3.9+ syntax for type annotations
