from django.utils.unittest import TextTestRunner, TextTestResult

from discover_runner import DiscoverRunner
from django_jenkins.runner import CITestSuiteRunner
from pygments import highlight
from pygments.lexers import PythonTracebackLexer
from pygments.formatters import TerminalFormatter


class HighlightedTextTestResult(TextTestResult):

    def _exc_info_to_string(self, err, test):
        code = super(HighlightedTextTestResult, self)._exc_info_to_string(err, test)
        return highlight(code, PythonTracebackLexer(), TerminalFormatter())


class HighlightedTextTestRunner(TextTestRunner):
    resultclass = HighlightedTextTestResult


class HighlightedDiscoverRunner(DiscoverRunner):

    def run_suite(self, suite, **kwargs):
        return HighlightedTextTestRunner(
            verbosity=self.verbosity,
            failfast=self.failfast,
        ).run(suite)


class CIDiscoverRunner(DiscoverRunner, CITestSuiteRunner):
    """
    Test runner based on unittest2 test discovery that contains
    continuous integration support.

    """
