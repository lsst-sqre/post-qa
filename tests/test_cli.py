"""Test app drivers in postqa.cli module."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import jsonschema
import responses

from postqa.schemas import load_squash_job_schema
import postqa.cli
import postqa.lsstsw


def test_build_job_json(mocker, qa_json_path, lsstsw_dir):
    # Mock the git repos on the file system
    mocker.patch('postqa.lsstsw.git.Repo')
    postqa.lsstsw.git.Repo.return_value.active_branch.name = 'master'

    job_json = postqa.cli.build_job_json(qa_json_path, lsstsw_dir)

    schema = load_squash_job_schema()
    jsonschema.validate(job_json, schema)


@responses.activate
def test_upload_json(mocker, qa_json_path, lsstsw_dir):
    api_url = 'https://squash.lsst.codes/api/jobs'
    api_user = 'user'
    api_password = 'password'

    # Mock the git repos on the file system
    mocker.patch('postqa.lsstsw.git.Repo')
    postqa.lsstsw.git.Repo.return_value.active_branch.name = 'master'

    # mock requests
    responses.add(responses.POST, api_url,
                  body='{}', status=201,
                  content_type='application/json')

    job_json = postqa.cli.build_job_json(qa_json_path, lsstsw_dir)

    postqa.cli.upload_json(job_json, api_url, api_user, api_password)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == api_url
