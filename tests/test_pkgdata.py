"""Test postqa/pkgdata."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

from postqa.pkgdata import Manifest


def test_manifest(manifest):
    """Test Manifest's parsing against manually-extracted data."""
    m = Manifest(manifest)

    job_json = m.json
    assert 'packages' in job_json
    assert isinstance(job_json['packages'], list)

    # Sample data extracted from test_data/lsstsw/build/manifest/.txt
    # to ensure that the parsing is accurate.
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
