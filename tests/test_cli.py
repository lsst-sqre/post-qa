"""Test app drivers in postqa.cli module."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import jsonschema
import responses

from postqa.schemas import load_schema
import postqa.cli
import postqa.lsstsw


def test_build_json_docs(mocker, qa_json_path, lsstsw_dir):
    # Mock the git repos on the file system
    mocker.patch('postqa.lsstsw.git.Repo')
    postqa.lsstsw.git.Repo.return_value.active_branch.name = 'master'

    registered_metrics = ['AM1', 'AM2', 'PA1']
    metric_json, job_json = postqa.cli.build_json_docs(qa_json_path,
                                                       lsstsw_dir,
                                                       registered_metrics)
    metric_schema = load_schema(schema='metric')
    jsonschema.validate(metric_json, metric_schema)
    job_schema = load_schema(schema='job')
    jsonschema.validate(job_json, job_schema)


@responses.activate
def test_upload_json(mocker, qa_json_path, lsstsw_dir):
    api_url = 'https://squash.lsst.codes/dashboard/api/jobs'
    api_job_endpoint = 'jobs'
    api_user = 'user'
    api_password = 'password'

    # Mock the git repos on the file system
    mocker.patch('postqa.lsstsw.git.Repo')
    postqa.lsstsw.git.Repo.return_value.active_branch.name = 'master'

    # mock requests
    responses.add(responses.POST, api_url,
                  body='{}', status=201,
                  content_type='application/json')

    registered_metrics = ['AM1', 'AM2', 'PA1']
    _, job_json = postqa.cli.build_json_docs(qa_json_path,
                                             lsstsw_dir,
                                             registered_metrics)

    postqa.cli.upload_json_doc(job_json, api_url, api_job_endpoint,
                               api_user, api_password)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == api_url
