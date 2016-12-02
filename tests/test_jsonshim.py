"""Test postqa/jsonshim."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import pytest
from jsonschema.exceptions import ValidationError

from postqa.jsonshim import shim_validate_drp
from postqa.schemas import load_squash_measurements_schema, validate


@pytest.fixture()
def schema():
    return load_squash_measurements_schema()


@pytest.fixture()
def job_json(vdrp_cfht_output_r):
    return shim_validate_drp(vdrp_cfht_output_r, ('PA1', 'AM1', 'AM2'))


def test_measurements_schema(job_json, schema):
    """Validate the schema of `measurements` json sub-document."""
    validate(job_json['measurements'], schema)


def test_accepted_metrics(vdrp_cfht_output_r, schema):
    """Ensure only accepted metrics are returned."""
    accepted_metrics = ['PA1']
    job_json = shim_validate_drp(vdrp_cfht_output_r, accepted_metrics)
    for measurement in job_json['measurements']:
        assert measurement['metric'] in accepted_metrics


def test_missing_measurements(vdrp_cfht_output_r):
    """Test when input has no measurements field."""
    del vdrp_cfht_output_r['measurements']
    with pytest.raises(KeyError):
        shim_validate_drp(vdrp_cfht_output_r, ('PA1', 'AM1', 'AM2'))


def test_missing_value(vdrp_cfht_output_r):
    """Test when a measurement is missing its value field."""
    del vdrp_cfht_output_r['measurements'][0]['value']
    with pytest.raises(KeyError):
        shim_validate_drp(vdrp_cfht_output_r, ('PA1', 'AM1', 'AM2'))


def test_missing_value_validation(job_json, schema):
    """Ensure schema validation picks up on missing 'value'."""
    del job_json['measurements'][0]['value']
    with pytest.raises(ValidationError):
        validate(job_json['measurements'], schema)


def test_missing_metric_validation(job_json, schema):
    """Ensure schema validation picks up on missing 'metric'."""
    del job_json['measurements'][0]['metric']
    with pytest.raises(ValidationError):
        validate(job_json['measurements'], schema)


def test_null_value_validation(job_json, schema):
    """Ensure schema validation allows values to be null."""
    job_json['measurements'][0]['value'] = None
    validate(job_json['measurements'], schema)
