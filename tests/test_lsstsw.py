"""Test postqa/lsstsw."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

from postqa.lsstsw import Lsstsw


def test_manifest_path():
    lsstsw = Lsstsw('foo')
    assert lsstsw.manifest_path == 'foo/build/manifest.txt'


def test_package_path():
    lsstsw = Lsstsw('foo')
    assert lsstsw.package_repo_path('afw') == 'foo/build/afw'
