"""Common pytest fixtures."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import os
import io
import json
import pytest


@pytest.fixture
def lsstsw_dir():
    """A minimal mock lsstsw/ installation is in /test_data/lsstsw."""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(test_dir, 'data', 'lsstsw')


@pytest.fixture()
def manifest(lsstsw_dir):
    """Sample manifest file object.."""
    manifest_path = os.path.join(lsstsw_dir, 'build', 'manifest.txt')
    with open(manifest_path, encoding='utf-8') as f:
        manifest_data = f.read()
    return io.StringIO(manifest_data)


@pytest.fixture()
def vdrp_cfht_output_r(qa_json_path):
    """data/Cfht_output_r.json from validate_drp as a dict."""
    with open(qa_json_path, encoding='utf-8') as f:
        json_dict = json.load(f)
    return json_dict


@pytest.fixture()
def qa_json_path():
    """Path to the sample validate_drp dataset."""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(test_dir, 'data', 'Cfht_output_r.json')
