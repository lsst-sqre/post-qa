"""Test postqa/jsonshim."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import jsonschema

from postqa.jsonshim import shim_validate_drp
from postqa.schemas import load_squash_measurements_schema


def test_measurements_schema(vdrp_cfht_output_r):
    """Validate the schema of `measurements` json sub-document."""
    job_json = shim_validate_drp(vdrp_cfht_output_r)
    schema = load_squash_measurements_schema()
    jsonschema.validate(job_json['measurements'], schema)
