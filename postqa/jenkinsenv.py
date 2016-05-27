"""API for scraping information from the lsstsw Jenkins CI environment."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import os
from datetime import datetime
import pytz


class JenkinsEnv(object):
    """API for Jenkins CI environment."""
    def __init__(self):
        super(JenkinsEnv, self).__init__()

    @property
    def json(self):
        """A Job json document (`dict`) with fields obtained from the
        CI environment.
        """
        return {
            'date': datetime.now(pytz.utc).isoformat(),
            'ci_name': os.getenv('DATASET', None),
            'ci_id': os.getenv('BUILD_ID', None),
            'ci_url': os.getenv('BUILD_URL', None),
            'status': 0,
        }
