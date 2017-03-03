"""Test app drivers in postqa.cli module."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import jsonschema
import responses
import pytest

from postqa.schemas import load_schema
import postqa.cli
import postqa.lsstsw


def test_build_json_docs(mocker, qa_json_path, lsstsw_dir):
    # Mock the git repos on the file system
    mocker.patch('postqa.lsstsw.git.Repo')
    postqa.lsstsw.git.Repo.return_value.active_branch.name = 'master'

    metric_json, job_json = postqa.cli.build_json_docs(qa_json_path,
                                                       lsstsw_dir)
    metric_schema = load_schema(schema='metric')
    jsonschema.validate(metric_json, metric_schema)
    job_schema = load_schema(schema='job')
    jsonschema.validate(job_json, job_schema)


@responses.activate
def test_load_registered_metrics():
    api_url = 'http://squash.lsst.codes/dashboard/api/'
    metric_endpoint_url = 'http://squash.lsst.codes/dashboard/api/metrics/'

    # Mock requests
    with open("tests/data/api_response.json") as f:
        api_response = f.read()

    responses.add(responses.GET, api_url,
                  body=api_response, status=200,
                  content_type='application/json')

    with open("tests/data/metric_endpoint_response.json") as f:
        metric_endpoint_response = f.read()

    responses.add(responses.GET, metric_endpoint_url,
                  body=metric_endpoint_response, status=200,
                  content_type='application/json')

    postqa.cli.load_registered_metrics(api_url)

    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == api_url
    assert responses.calls[0].response.text == api_response
    assert responses.calls[1].request.url == metric_endpoint_url
    assert responses.calls[1].response.text == metric_endpoint_response


@responses.activate
def test_upload_json_doc(mocker, qa_json_path, lsstsw_dir):
    api_url = 'http://squash.lsst.codes/dashboard/api/'
    metric_endpoint_url = 'http://squash.lsst.codes/dashboard/api/metrics/'
    job_endpoint_url = 'http://squash.lsst.codes/dashboard/api/jobs/'

    # Mock the git repos on the file system
    mocker.patch('postqa.lsstsw.git.Repo')
    postqa.lsstsw.git.Repo.return_value.active_branch.name = 'master'

    # Mock requests
    with open("tests/data/api_response.json") as f:
        api_response = f.read()

    responses.add(responses.GET, api_url,
                  body=api_response, status=200,
                  content_type='application/json')

    responses.add(responses.POST, metric_endpoint_url,
                  body='{}', status=201,
                  content_type='application/json')

    responses.add(responses.POST, job_endpoint_url,
                  body='{}', status=201,
                  content_type='application/json')

    metric_json, job_json = postqa.cli.build_json_docs(qa_json_path,
                                                       lsstsw_dir)

    postqa.cli.upload_json_doc(metric_json, api_url, 'metrics')
    postqa.cli.upload_json_doc(job_json, api_url, 'jobs')

    assert len(responses.calls) == 4
    assert responses.calls[0].request.url == api_url
    assert responses.calls[0].response.status_code == 200
    assert responses.calls[0].response.text == api_response
    assert responses.calls[1].request.url == metric_endpoint_url
    assert responses.calls[1].response.status_code == 201
    assert responses.calls[2].request.url == api_url
    assert responses.calls[2].response.status_code == 200
    assert responses.calls[2].response.text == api_response
    assert responses.calls[3].request.url == job_endpoint_url
    assert responses.calls[3].response.status_code == 201


@responses.activate
def test_upload_json_doc_bad_api_http_status():
    api_url = 'http://squash.lsst.codes/dashboard/api/'

    responses.add(responses.GET, api_url,
                  body=None, status=500,
                  content_type='application/json')

    with pytest.raises(SystemExit):
        postqa.cli.upload_json_doc(None, api_url, 'metrics')

    with pytest.raises(SystemExit):
        postqa.cli.upload_json_doc(None, api_url, 'jobs')

    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == api_url
    assert responses.calls[0].response.status_code == 500
    assert responses.calls[1].request.url == api_url
    assert responses.calls[1].response.status_code == 500


@responses.activate
def test_upload_json_doc_bad_endpoint_http_status(mocker, qa_json_path,
                                                  lsstsw_dir):
    api_url = 'http://squash.lsst.codes/dashboard/api/'
    metric_endpoint_url = 'http://squash.lsst.codes/dashboard/api/metrics/'
    job_endpoint_url = 'http://squash.lsst.codes/dashboard/api/jobs/'

    # Mock the git repos on the file system
    mocker.patch('postqa.lsstsw.git.Repo')
    postqa.lsstsw.git.Repo.return_value.active_branch.name = 'master'

    # Mock requests
    with open("tests/data/api_response.json") as f:
        api_response = f.read()

    responses.add(responses.GET, api_url,
                  body=api_response, status=200,
                  content_type='application/json')

    responses.add(responses.POST, metric_endpoint_url,
                  body='{}', status=301,
                  content_type='application/json')

    responses.add(responses.POST, job_endpoint_url,
                  body='{}', status=301,
                  content_type='application/json')

    metric_json, job_json = postqa.cli.build_json_docs(qa_json_path,
                                                       lsstsw_dir)

    with pytest.raises(SystemExit):
        postqa.cli.upload_json_doc(metric_json, api_url, 'metrics')

    with pytest.raises(SystemExit):
        postqa.cli.upload_json_doc(job_json, api_url, 'jobs')

    assert len(responses.calls) == 4
    assert responses.calls[0].request.url == api_url
    assert responses.calls[0].response.status_code == 200
    assert responses.calls[0].response.text == api_response
    assert responses.calls[1].request.url == metric_endpoint_url
    assert responses.calls[1].response.status_code == 301
    assert responses.calls[2].request.url == api_url
    assert responses.calls[2].response.status_code == 200
    assert responses.calls[2].response.text == api_response
    assert responses.calls[3].request.url == job_endpoint_url
    assert responses.calls[3].response.status_code == 301
