#!/usr/bin/env python
# Lint as: python3
"""Load all cron flows in order to populate the registry."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

# pylint: disable=unused-import
# These imports populate the Flow registry
from grr_response_server.flows.cron import system
