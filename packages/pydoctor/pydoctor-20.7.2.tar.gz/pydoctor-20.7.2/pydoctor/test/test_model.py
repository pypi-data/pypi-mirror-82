"""
Unit tests for model.
"""
from __future__ import print_function

import sys
import zlib

from pydoctor import model, sphinx
from pydoctor.driver import parse_args
from pydoctor.test.test_astbuilder import fromText


class FakeOptions(object):
    """
    A fake options object as if it came from that stupid optparse thing.
    """
    sourcehref = None



class FakeDocumentable(object):
    """
    A fake of pydoctor.model.Documentable that provides a system and
    sourceHref attribute.
    """
    system = None
    sourceHref = None



def test_setSourceHrefOption():
    """
    Test that the projectbasedirectory option sets the model.sourceHref
    properly.
    """
    viewSourceBase = "http://example.org/trac/browser/trunk"
    projectBaseDir = "/foo/bar/ProjectName"
    moduleRelativePart = "/package/module.py"

    mod = FakeDocumentable()
    mod.filepath = projectBaseDir + moduleRelativePart

    options = FakeOptions()
    options.projectbasedirectory = projectBaseDir

    system = model.System()
    system.sourcebase = viewSourceBase
    system.options = options
    mod.system = system
    system.setSourceHref(mod)

    expected = viewSourceBase + moduleRelativePart
    assert mod.sourceHref == expected


def test_initialization_default():
    """
    When initialized without options, will use default options and default
    verbosity.
    """
    sut = model.System()

    assert None is sut.options.projectname
    assert 3 == sut.options.verbosity


def test_initialization_options():
    """
    Can be initialized with options.
    """
    options = object()

    sut = model.System(options=options)

    assert options is sut.options


def test_fetchIntersphinxInventories_empty():
    """
    Convert option to empty dict.
    """
    options, _ = parse_args([])
    options.intersphinx = []
    sut = model.System(options=options)

    sut.fetchIntersphinxInventories(sphinx.StubCache({}))

    # Use internal state since I don't know how else to
    # check for SphinxInventory state.
    assert {} == sut.intersphinx._links


def test_fetchIntersphinxInventories_content():
    """
    Download and parse intersphinx inventories for each configured
    intersphix.
    """
    options, _ = parse_args([])
    options.intersphinx = [
        'http://sphinx/objects.inv',
        'file:///twisted/index.inv',
        ]
    url_content = {
        'http://sphinx/objects.inv': zlib.compress(
            b'sphinx.module py:module -1 sp.html -'),
        'file:///twisted/index.inv': zlib.compress(
            b'twisted.package py:module -1 tm.html -'),
        }
    sut = model.System(options=options)
    log = []
    sut.msg = lambda part, msg: log.append((part, msg))
    # Patch url getter to avoid touching the network.
    sut.intersphinx._getURL = lambda url: url_content[url]

    sut.fetchIntersphinxInventories(sphinx.StubCache(url_content))

    assert [] == log
    assert (
        'http://sphinx/sp.html' ==
        sut.intersphinx.getLink('sphinx.module')
        )
    assert (
        'file:///twisted/tm.html' ==
        sut.intersphinx.getLink('twisted.package')
        )


def test_docsources_class_attribute():
    src = '''
    class Base:
        attr = False
        """documentation"""
    class Sub(Base):
        attr = True
    '''
    mod = fromText(src)
    base_attr = mod.contents['Base'].contents['attr']
    sub_attr = mod.contents['Sub'].contents['attr']
    assert base_attr in list(sub_attr.docsources())


def test_docstring_lineno():
    src = '''
    def f():
        """
        This is a long docstring.

        Somewhat long, anyway.
        This should be enough.
        """
    '''
    mod = fromText(src)
    func = mod.contents['f']
    assert func.linenumber == 2
    assert func.docstring_lineno == 4 # first non-blank line


class Dummy(object):
    def crash(self):
        """Mmm"""

def test_introspection():
    """Find docstrings from this test using introspection."""
    system = model.System()
    py_mod = sys.modules[__name__]
    system.introspectModule(py_mod, __name__)

    module = system.objForFullName(__name__)
    assert module.docstring == __doc__

    func = module.contents['test_introspection']
    assert func.docstring == "Find docstrings from this test using introspection."

    method = system.objForFullName(__name__ + '.Dummy.crash')
    assert method.docstring == "Mmm"
