import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from cvbuilder.contexts import Style
from cvbuilder.contexts.latex import LaTeXContext
from cvbuilder.modules.job import Job, JobModule


class JobTest(unittest.TestCase):
    def test_minimal(self):
        data = Job(title="Test Minimal")
        module = JobModule()
        module.jobs = [data]

        context = LaTeXContext(None)
        # pylint: disable=protected-access
        document = context._build_output([module], None)
        # pylint: enable=protected-access
        target = """\\documentclass{academiccv}

\\begin{document}
\\section{Work Experience}

\\job{
\ttitle = {Test Minimal},
}
\\end{document}"""
        self.assertEqual(document, target)

    def test_style(self):
        data = Job(
            title="Test Style",
            style=Style(
                {
                    "start": "\\bfseries",
                    "end": "\\itshape",
                    "title": "\\Large",
                    "organization": "\\color{red}",
                    "description": "\\ttshape",
                    "swap": False,
                    "margin_size": "3em",
                    "space": "2em",
                    "vspace_after": "5pt",
                }
            ),
        )
        module = JobModule()
        module.jobs = [data]

        context = LaTeXContext(None)
        # pylint: disable=protected-access
        document = context._build_output([module], None)
        # pylint: enable=protected-access
        target = """\\documentclass{academiccv}

\\begin{document}
\\section{Work Experience}

\\job{
\ttitle = {Test Style},
\tstyle = {
\t\tstart = {\\bfseries},
\t\tend = {\\itshape},
\t\ttitle = {\\Large},
\t\torganization = {\\color{red}},
\t\tdescription = {\\ttshape},
\t\tswap = false,
\t\tmargin-size = {3em},
\t\tspace = {2em},
\t\tvspace-after = {5pt},
\t},
}
\\end{document}"""
        self.assertEqual(document, target)

    def test_complete(self):
        data = Job(
            start="1970-08-01",
            end="Present",
            title="Test All Fields",
            organization="Unittest",
            description="Testing a lot of stuff",
            style=Style({"swap": True}),
        )
        module = JobModule()
        module.jobs = [data]

        context = LaTeXContext(None)
        # pylint: disable=protected-access
        document = context._build_output([module], None)
        # pylint: enable=protected-access
        target = """\\documentclass{academiccv}

\\begin{document}
\\section{Work Experience}

\\job{
\tstart = {01 Aug 1970},
\tend = {Present},
\ttitle = {Test All Fields},
\torganization = {Unittest},
\tdescription = {Testing a lot of stuff},
\tstyle = {
\t\tswap = true,
\t},
}
\\end{document}"""
        self.assertEqual(document, target)


if __name__ == "__main__":
    unittest.main()
