"""Test postqa/lsstsw."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import os
import pytest
import jsonschema

import postqa.lsstsw
from postqa.lsstsw import Lsstsw
from postqa.schemas import load_squash_packages_schema


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


def test_packages_json_schema(mocker, lsstsw_dir):
    """Validate the schema of the 'packages' json sub-document."""
    # mock git.Repo in postqa.lsstsw so that a repo's active branch is master
    # and doesn't attempt to actually query the repo in the filesystem.
    mocker.patch('postqa.lsstsw.git.Repo')
    postqa.lsstsw.git.Repo.return_value.active_branch.name = 'master'

    lsstsw = Lsstsw(lsstsw_dir)
    job_json = lsstsw.json

    schema = load_squash_packages_schema()

    jsonschema.validate(job_json['packages'], schema)
