# Building an academic curriculum vitae from a JSON document

This project aims at providing an easy-to-configure tool to output academic CV files from a JSON document.

## Installation

### From release

Download the `.whl` file of the latest release and run `pip install academiccv_builder-2.0.0-py3-none-any.whl`.

### From source

Inside the root folder of this repository, run `pip install -e .`

## Usage

The files are produced following a specific pipeline:

  1. Create a **Builder** which orchestrates the execution.
  2. Add a **Context** which produced a unique output file.
    Multiple contexts can be added to the same builder.
  3. For each context, add **modules** to produce the contents of the file(s).
    You can add as many modules as you wish.
  4. Call `builder.build('pathToFile.json')` to produce, for each context, the output file, using the defined modules.

It is possible to provide multiple JSON files to `builder.build` (passing them as a list).
In that case, every module receives every file and retrieves the required data when it is available.
If the **same key appears in multiple documents**, the implementation may do anything (i.e., it is an undefined behavior).

See [the example file](example.py) for a demonstration of the commands, and [the JSON files](json_example/).

We highly recommend that all dates are written under the ISO format `YYYY-mm-dd`.
Without changing the function `format_date` of the `Context` class, failing to follow this format may produce unexpected results.

### Builder

The main purpose of the builder is to orchestrate the loaded contexts.
That is, it opens the JSON file(s), passes the contents to each context, before producing the output file(s).
Its main functions are:

  - `builder.add_context(context)` to add a new context.
  - `builder.build(json_file_paths)` where `json_file_paths` is either a path to a single JSON file, or a list of paths.
  The function loads the files and transfers the contents to each context.
  Finally, the output file(s) are produced.

### Context

A context produces a single file from the JSON documents, using the defined modules.
The implementation provides three different contexts:

  - `LaTeXContext` which produces a file meant to be used with the [academiccv](https://github.com/DocSkellington/academic-cv) class.
    If the `ContactModule` is used, it is **required that its category is `title`**.
    Otherwise, the output will not be correct.
  - `HTMLContext` which produces an HTML file.
    Paths to CSS files can be added via the `add_css_file(css_path)` function.
    While a default style is provided in the [`resources`](resources/) folder, we highly recommend you design your own.
    The generated webpage has a sidebar and a main content.
    The sidebar always contains the identification information.
    Any module with the category `sidebar` will be added to the sidebar.
  - `MarkdownContext` which produces a Markdown file.
    Note that the file contains many explicit HTML tags, in order to have a very flexible style.
    That is, the Markdown context produces something close to the HTML context.
    Still, it may be interesting to produce Markdown files and then converting them into HTML files, if the website contains other pages.
    See my project [WebsiteBuilder](https://github.com/DocSkellington/WebsiteBuilder) for a way to do so.

Each context is responsible for maintaining its own sequence of modules and has
the following function:

  - `context.add_module(in_json, module, category)` to add a new module `module` to the context `context`.
    The value of `in_json` is used as a key in the JSON document to extract the data.
    For instance, if `in_json` is `contact`, then the module's data will be constructed from the value of the key `contact` **at the root of the JSON document**.
    The `category` (by default, `default`) allows a context to filter which module to execute.
    Typically, every `default` module will be used to create the main content.
    See the documentation of each context to know the available categories.

### Modules

A module holds data loaded from the JSON file and uses it to produce a part of the output document.
The default implementation of the `load(self, json_value)` function assumes that `json_value` is a list.
Each item of this list is then passed to the function `_load(self, json_object)` which is expected to be implemented by a loaded module.

The following modules are implemented.
Except if mentioned otherwise, all data values are optional and each module can describe multiple instances of the described data (i.e., the value in the JSON document is a list, except if stated otherwise).
The (`key`) indicates the corresponding key in the JSON document.

  - `AwardModule` lists the received awards:
    - year (`year`), and
    - a description (`description`).
  - `ContactModule` lists the **unique** (i.e., the value in the JSON document must be an object) collection of contact information:
    - email address(es) (`email`),
    - website (`website`),
    - GitHub username (`github`),
    - ORCID number (`orcid`),
    - LinkedIn username (`linkedin`),
    - a postal address (`address`) comprised of the **mandatory keys** `street`, `zipcode`, `city`, `country`, and `link` (to OpenStreetMaps, for instance; this one is **not** mandatory), and
    - the link to the PDF (`pdf`).
  - `EventModule` lists the events the researcher attended:
    - the year (`year`),
    - the name (`name`), and
    - the location (`where`).
  - `JobModule` lists the positions held by the researched:
    - the start and end dates (`start`, `end`),
    - the position's title (`title`),
    - the organization (`organization`), and
    - a description (`description`).
  - `LanguageModule` lists the known languages:
    - the name of the language (`name`), and
    - the fluency level, typically something like B1 (`level`).
    The LaTeX context is not supported.
  - `LogosModule` lists the logos.
    The value in the JSON document must be a list of strings.
    The LaTeX context is not supported.
  - `ProjectModule` lists the main projects:
    - a short name, typically an acronym (`shortName`),
    - the name of the project (`name`),
    - the role within the project (`role`), and
    - a description (`description`).
  - `PublicationModule` lists the publications:
    - the **mandatory** title (`title`),
    - the **mandatory** authors (`authors`),
    - the **mandatory** year (`year`),
    - a reference, typically something like `[BRV23]` (`reference`),
    - the journal/conference (`where`),
    - a short name for the journal/conference (`shortWhere`),
    - the DOI (`doi`),
    - the arxiv DOI (`arxiv`), and
    - a note/remark on the paper (`note`).
  - `SupervisionModule` lists the supervised students/projects:
    - the year (`year`),
    - the name(s) of the student(s)/project (`name`),
    - the role within the supervision (`role`),
    - the organization the supervision took place in (`organization`),
    - a description (`description`).
  - `SummaryModule` which displays a text about the researcher.
    It must be a list containing strings or lists.
    Each list is converted into a list in the appropriate format (so, `itemize` for LaTeX, `ul` for HTML, and so on).
  - `TeachModule` lists the courses given by the researcher:
    - the year(s) (`year`),
    - the course's name (`course`),
    - the role within the course (`role`),
    - the level at which the course is given (`level`),
    - the organization (`organization`),
    - a description (`description`).
  - `TalkModule` lists the given talks:
    - the date (`date`),
    - the title (`title`),
    - the conference/context (`conference`),
    - the location (`where`).
  - `TextModule` which prints an arbitrary text.
    The text is displayed as-is.
    It must be set within the Python code, i.e., it is not loaded from the JSON file.
  - `LinkModule` which prints an arbitrary text containing a link, typically to another generated document.
    The text is displayed as-is (except the link that is formatted to match the context).
    It must be set within the Python code, i.e., it is not loaded from the JSON file.

Almost every module produces a section header when invoked.
The text displayed (and the icon for the HTML context) can be changed when instancing the class.
Leave the text empty (and the icon for the HTML context) to not produce the section header.

Finally, each data class also stores a `style` containing styling commands, meant to be used for the LaTeX context.
That is, it is possible to define a specific style but only for LaTeX.

### The JSON file

The JSON file is expected to be structured as an object where each key corresponds to a module.
The only key that is fixed is `personal` (which holds the identification data of the researcher) which must be an object with the following keys:

  - `name`: the name of the researcher (**mandatory**),
  - `position`: the current position of the researcher (**mandatory**),
  - `organization`: the current organization(s)/affiliation(s) (**mandatory**), and
  - `photo`: the path to a picture.

Everything else in the document can be named as you wish.
That being said, a [JSON Schema](schema.json) is provided with reasonable key names.

Many values in the JSON document can be used to encode subsections (`h3` for HTML, `##` for Markdown).
For instance,
```json
"jobs": [
  { "Current positions": [ { ... } ] },
  { "Past positions": [ { ... } ] }
]
```
will produce two subsections: *Current positions*, and *Past positions*.

Observe that you can split the file into multiple smaller files, if you use multiple instances of the builder.

## Development

Run `pipenv install --dev` at the root of the repository to install all (developing) dependencies.

Pull requests are welcome!

## Acknowledgments

This project is inspired by the [`JSON Resume`](https://jsonresume.org/) project.

## License
This project is licensed under [MIT License](LICENSE).
