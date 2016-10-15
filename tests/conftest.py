"""Common pytest fixtures."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import os
import json
import pytest


pytest_plugins = "pytest_mock", "pytest_cov",


@pytest.fixture
def lsstsw_dir():
    """A minimal mock lsstsw/ installation is in /test_data/lsstsw."""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'test_data', 'lsstsw'))


@pytest.fixture()
def vdrp_cfht_output_r(qa_json_path):
    """test_data/Cfht_output_r.json from validate_drp as a dict."""
    with open(qa_json_path, encoding='utf-8') as f:
        json_dict = json.load(f)
    return json_dict


@pytest.fixture()
def qa_json_path():
    return pkg_resources.resource_filename(
        __name__, '../test_data/Cfht_output_r.json')
