import unittest
import sys
import os

from . import preamble, postamble

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from cvbuilder.contexts import Style
from cvbuilder.contexts.html import HTMLContext
from cvbuilder.contexts.latex import LaTeXContext
from cvbuilder.modules.job import Job, JobModule


class JobTest(unittest.TestCase):
    def test_minimal(self):
        data = Job(title="Test Minimal")
        module = JobModule()
        module.data = [(None, [data])]

        context = HTMLContext(None)
        # pylint: disable=protected-access
        document = context._build_output([module], None)
        # pylint: enable=protected-access
        target = preamble()
        target += """\t\t\t<section class="section work">
\t\t\t\t<h2 class="work">Work Experience</h2>
\t\t\t\t<div class="item">
\t\t\t\t\t<div class="align">
\t\t\t\t\t\t<div class="title">
\t\t\t\t\t\t\tTest Minimal
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t</section>"""
        target += postamble()
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
        module.data = [("Past", [data])]

        self.maxDiff = None

        context = HTMLContext(None)
        # pylint: disable=protected-access
        document = context._build_output([module], None)
        # pylint: enable=protected-access
        target = preamble()
        target += """\t\t\t<section class="section work">
\t\t\t\t<h2 class="work">Work Experience</h2>
\t\t\t\t<section class="section past">
\t\t\t\t\t<h3 class="past">Past</h3>
\t\t\t\t\t<div class="item">
\t\t\t\t\t\t<div class="align">
\t\t\t\t\t\t\t<div class="title">
\t\t\t\t\t\t\t\tTest All Fields
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="time">
\t\t\t\t\t\t\t\t01 Aug 1970 &hyphen; Present
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="organization">
\t\t\t\t\t\t\tUnittest
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="details">
\t\t\t\t\t\t\tTesting a lot of stuff
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</section>
\t\t\t</section>"""
        target += postamble()
        self.assertEqual(document, target)


if __name__ == "__main__":
    unittest.main()
