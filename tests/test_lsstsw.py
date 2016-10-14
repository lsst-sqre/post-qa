"""Test postqa/lsstsw."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import os
import pytest

from postqa.lsstsw import Lsstsw


@pytest.fixture
def lsstsw_dir():
    """A minimal mock lsstsw/ installation is in /test_data/lsstsw."""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'test_data', 'lsstsw'))


def test_manifest_path(lsstsw_dir):
    lsstsw = Lsstsw(lsstsw_dir)
    assert lsstsw.manifest_path == os.path.join(lsstsw_dir,
                                                'build/manifest.txt')


def test_package_path(lsstsw_dir):
    lsstsw = Lsstsw(lsstsw_dir)
    assert lsstsw.package_repo_path('afw') == os.path.join(lsstsw_dir,
                                                           'build/afw')


def test_package_url(lsstsw_dir):
    lsstsw = Lsstsw(lsstsw_dir)

    assert lsstsw.package_repo_url('afw') == \
        'https://github.com/lsst/afw.git'

    assert lsstsw.package_repo_url('xrootd') == \
        'https://github.com/lsst/xrootd.git'

    assert lsstsw.package_repo_url('obs_base') == \
        'https://github.com/lsst-dm/obs_base.git'
