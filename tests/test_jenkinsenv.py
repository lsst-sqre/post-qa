"""Test postqa.jenkinsenv."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA


import postqa.jenkinsenv


def test_jenkinsenv(mocker):
    # environment vars that JenkinsEnv uses, and mock responses
    env_vars = {
        'BUILD_ID': 'b1234',
        'PRODUCT': 'job_name',
        'dataset': 'cfht',
        'label': 'label',
        'BUILD_URL': 'https://example.org'
    }
    json_envvar_map = {
        'ci_id': 'BUILD_ID',
        'ci_name': 'PRODUCT',
        'ci_dataset': 'dataset',
        'ci_label': 'label',
        'ci_url': 'BUILD_URL'
    }

    def env_side_effects(*args, **kwargs):
        return env_vars[args[0]]

    # Mock os.getenv to isolate this test
    mocker.patch('postqa.jenkinsenv.os')
    postqa.jenkinsenv.os.getenv.side_effect = env_side_effects

    jenkinsenv = postqa.jenkinsenv.JenkinsEnv()
    job_json = jenkinsenv.json

    for json_key, envvar in json_envvar_map.items():
        assert job_json[json_key] == env_vars[envvar]
