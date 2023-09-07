import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from cvbuilder.contexts import Style
from cvbuilder.contexts.latex import LaTeXContext
from cvbuilder.modules.publication import Publication, PublicationModule


class PublicationTest(unittest.TestCase):
    def test_style(self):
        data = Publication(
            title="Test Style",
            authors="Authors",
            year=2023,
            style=Style(
                {
                    "title": "\\bfseries",
                    "authors": "\\itshape",
                    "year": "\\Large",
                    "reference": "\\color{red}",
                    "where": "\\ttshape",
                    "shortWhere": "\\color{green}",
                    "doi": "\\color{white}",
                    "doi_prefix": "DOI:",
                    "arxiv": "\\color{blue}",
                    "arxiv_prefix": "ARXIV:",
                }
            ),
        )
        module = PublicationModule()
        module.publications = [data]

        context = LaTeXContext(None)
        # pylint: disable=protected-access
        document = context._build_output([module], None)
        # pylint: enable=protected-access
        self.maxDiff = None
        target = """\\documentclass{academiccv}

\\begin{document}
\\section{Work Experience}

\\job{
\ttitle = {Test Style},
\tauthors = {Authors},
\tyear = {2023},
\tstyle = {
\t\ttitle = {\\bfseries},
\t\tauthors = {\\itshape},
\t\tyear = {\\Large},
\t\treference = {\\color{red}},
\t\twhere = {\\ttshape},
\t\tshortWhere = {\\color{green}},
\t\tdoi = {\\color{white}},
\t\tdoi-prefix = {DOI:},
\t\tarxiv = {\\color{blue}},
\t\tarxiv-prefix = {ARXIV:},
\t},
}
\\end{document}"""
        self.assertEqual(document, target)

    def test_complete(self):
        data = Publication(
            title="Publication Test",
            authors="Authors",
            year=2023,
            reference="REFERENCE",
            where="Somewhere",
            shortWhere="Sw",
            doi="0000",
            arxiv="0001",
            style=Style({"title": "\\bfseries"}),
        )
        module = PublicationModule()
        module.publications = [data]

        context = LaTeXContext(None)
        # pylint: disable=protected-access
        document = context._build_output([module], None)
        # pylint: enable=protected-access
        target = """\\documentclass{academiccv}

\\begin{document}
\\section{Work Experience}

\\job{
\ttitle = {Publication Test},
\tauthors = {Authors},
\tyear = {2023},
\treference = {REFERENCE},
\twhere = {Somewhere},
\tshortWhere = {Sw},
\tdoi = {0000},
\tarxiv = {0001},
\tstyle = {
\t\ttitle = {\\bfseries},
\t},
}
\\end{document}"""
        self.assertEqual(document, target)


if __name__ == "__main__":
    unittest.main()
