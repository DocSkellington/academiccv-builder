import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from cvbuilder.contexts import PersonalData, Address, Style
from cvbuilder.contexts.latex import LaTeXContext


class TitleTest(unittest.TestCase):
    def test_minimal(self):
        data = PersonalData(
            name="Testy", position="Testing", organization="Tests, Inc."
        )
        context = LaTeXContext(None)
        # pylint: disable=protected-access
        document = context._build_output([], data)
        # pylint: enable=protected-access

        target = """\\documentclass{academiccv}

\\begin{document}
\\makecvtitle{
\tauthor = {Testy},
\tposition = {Testing},
\torganization = {Tests, Inc.},
}

\\end{document}"""
        self.assertEqual(document, target)

    def test_complete(self):
        data = PersonalData(
            name="Testy",
            position="Testing",
            organization="Tests, Inc.",
            photo="path.png",
            email=["a@mail.com", "b@mail.com"],
            website="https://website.com",
            github="Test@Github",
            orcid="ORCID",
            linkedin="LinkedIn",
            address=Address(
                street="1, Street Street",
                zipcode="0000",
                city="City",
                country="Country",
            ),
        )
        context = LaTeXContext(None)
        # pylint: disable=protected-access
        document = context._build_output([], data)
        # pylint: enable=protected-access

        target = """\\documentclass{academiccv}

\\begin{document}
\\makecvtitle{
\tauthor = {Testy},
\tposition = {Testing},
\torganization = {Tests, Inc.},
\tphoto = {path.png},
\temail = {a@mail.com},
\temail = {b@mail.com},
\twebsite = {https://website.com},
\tgithub = {Test@Github},
\torcid = {ORCID},
\tlinkedIn = {LinkedIn},
\tstreet = {1, Street Street},
\tzipcode = {0000},
\tcity = {City},
\tcountry = {Country},
}

\\end{document}"""
        self.assertEqual(document, target)

    def test_style(self):
        data = PersonalData(
            name="Testy", position="Testing", organization="Tests, Inc."
        )
        style = Style(
            {"author": "\\normalfont", "vertical_space": "3em", "portion_photo": 0.2}
        )
        context = LaTeXContext(None)
        context.set_style("title", style)
        # pylint: disable=protected-access
        document = context._build_output([], data)
        # pylint: enable=protected-access
        print(document)

        target = """\\documentclass{academiccv}

\\titleSetup{
\tauthor = {\\normalfont},
\tvertical-space = {3em},
\tportion-photo = {0.2},
}

\\begin{document}
\\makecvtitle{
\tauthor = {Testy},
\tposition = {Testing},
\torganization = {Tests, Inc.},
}

\\end{document}"""
        self.assertEqual(document, target)


if __name__ == "__main__":
    unittest.main()
