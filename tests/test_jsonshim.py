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
from numpy.testing import assert_approx_equal
import jsonschema

from postqa.jsonshim import shim_vdrp_measurement, shim_validate_drp
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


@pytest.fixture()
def expected_cfht_r_job():
    """test_data/expected_chft_r_job.json as a dict."""
    json_str = load_test_data('expected_cfht_r_job.json').decode('utf-8')
    json_dict = json.loads(json_str)
    return json_dict


def test_shim_validate_drp(vdrp_cfht_output_r):
    # FIXME deprecated by test_measurements_schema()
    job_json = shim_validate_drp(vdrp_cfht_output_r)
    assert 'measurements' in job_json
    assert len(job_json['measurements']) == 3
    for measurement in job_json['measurements']:
        assert 'metric' in measurement
        assert 'value' in measurement


def test_shim_vdrp_measurement_vdrp(vdrp_cfht_output_r,
                                    expected_cfht_r_job):
    for expected_doc in expected_cfht_r_job['measurements']:
        # get matching vdrp doc
        for doc in vdrp_cfht_output_r['measurements']:
            if doc['metric']['name'] == expected_doc['metric']:
                shimmed_doc = shim_vdrp_measurement(doc)
                assert_approx_equal(
                    shimmed_doc['value'],
                    expected_doc['value'])
                assert shimmed_doc['metric'] == expected_doc['metric']
                break


def test_measurements_schema(vdrp_cfht_output_r):
    """Validate the schema of `measurements` json sub-document."""
    job_json = shim_validate_drp(vdrp_cfht_output_r)
    schema = load_squash_measurements_schema()
    jsonschema.validate(job_json['measurements'], schema)
