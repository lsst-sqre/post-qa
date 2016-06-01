"""Test postqa/pkgdata."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import os
import io
import pkg_resources
import pytest

from postqa.pkgdata import Manifest


def load_test_data(filename):
    resource_args = (__name__, os.path.join('../test_data/', filename))
    assert pkg_resources.resource_exists(*resource_args)
    data_str = pkg_resources.resource_string(*resource_args).decode('utf-8')
    return data_str


@pytest.fixture()
def manifest():
    """test_data/manifest.txt"""
    manifest_data = load_test_data('manifest.txt')
    return io.StringIO(manifest_data)


def test_manifest(manifest):
    m = Manifest(manifest)

    job_json = m.json
    assert 'packages' in job_json
    assert isinstance(job_json['packages'], list)

    known_packages = [
        ('afw',
         'fc355a99abe3425003b0e5fbe1e13a39644b1e95',
         '2.2016.10-22-gfc355a9')
    ]

    for (known_name, known_commit, known_version) in known_packages:
        for p in job_json['packages']:
            if p['name'] == known_name:
                assert p['git_commit'] == known_commit
                assert p['build_version'] == known_version
