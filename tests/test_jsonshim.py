"""Test postqa/jsonshim."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import os
import json
import pkg_resources
import pytest
import jsonschema

from postqa.jsonshim import shim_validate_drp
from postqa.schemas import load_squash_measurements_schema


def load_test_data(filename):
    resource_args = (__name__, os.path.join('../test_data/', filename))
    assert pkg_resources.resource_exists(*resource_args)
    data_str = pkg_resources.resource_string(*resource_args)
    return data_str


@pytest.fixture()
def vdrp_cfht_output_r():
    """test_data/Cfht_output_r.json from validate_drp as a dict."""
    json_str = load_test_data('Cfht_output_r.json').decode('utf-8')
    json_dict = json.loads(json_str)
    return json_dict


def test_measurements_schema(vdrp_cfht_output_r):
    """Validate the schema of `measurements` json sub-document."""
    job_json = shim_validate_drp(vdrp_cfht_output_r)
    schema = load_squash_measurements_schema()
    jsonschema.validate(job_json['measurements'], schema)
