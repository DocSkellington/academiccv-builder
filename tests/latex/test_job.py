import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from cvbuilder.contexts.latex import LaTeXContext, JobSetup
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
            style=JobSetup(
                start="\\bfseries",
                end="\\itshape",
                title="\\Large",
                organization="\\color{red}",
                description="\\ttshape",
                swap=False,
                margin_size="3em",
                space="2em",
                vspace_after="5pt",
            ),
        )
        module = JobModule()
        module.jobs = [data]

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
\tstyle = {
\tstart = {\\bfseries},
\tend = {\\itshape},
\ttitle = {\\Large},
\torganization = {\\color{red}},
\tdescription = {\\ttshape},
\tswap = false,
\tmargin-size = {3em},
\tspace = {2em},
\tvspace-after = {5pt},
},
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
            style=JobSetup(swap=True),
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
\tswap = true,
},
}
\\end{document}"""
        self.assertEqual(document, target)


if __name__ == "__main__":
    unittest.main()
