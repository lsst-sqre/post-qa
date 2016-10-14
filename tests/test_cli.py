"""Test app drivers in postqa.cli module."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import jsonschema

from postqa.schemas import load_squash_job_schema
import postqa.cli
import postqa.lsstsw


def test_build_job_json(mocker, qa_json_path, lsstsw_dir):
    mocker.patch('postqa.lsstsw.git.Repo')
    postqa.lsstsw.git.Repo.return_value.active_branch.name = 'master'

    job_json = postqa.cli.build_job_json(qa_json_path, lsstsw_dir)

    schema = load_squash_job_schema()
    jsonschema.validate(job_json, schema)
