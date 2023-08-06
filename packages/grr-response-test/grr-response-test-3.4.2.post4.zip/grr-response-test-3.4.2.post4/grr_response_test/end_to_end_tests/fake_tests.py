#!/usr/bin/env python
# Lint as: python3
"""Dummy end-to-end test classes for testing the E2ETestRunner."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import abc

from grr_response_test.end_to_end_tests import test_base


class AbstractFakeE2ETest(test_base.EndToEndTest, metaclass=abc.ABCMeta):

  def testCommon(self):
    pass


class FakeE2ETestAll(AbstractFakeE2ETest):
  platforms = test_base.EndToEndTest.Platform.ALL


class FakeE2ETestDarwinLinux(AbstractFakeE2ETest):
  platforms = [
      test_base.EndToEndTest.Platform.DARWIN,
      test_base.EndToEndTest.Platform.LINUX
  ]

  def testDarwinLinux(self):
    pass


class FakeE2ETestLinux(AbstractFakeE2ETest):
  platforms = [test_base.EndToEndTest.Platform.LINUX]

  def testLinux(self):
    pass


class FakeE2ETestDarwin(AbstractFakeE2ETest):
  platforms = [test_base.EndToEndTest.Platform.DARWIN]


class FakeE2ETestManual(AbstractFakeE2ETest):

  platforms = test_base.EndToEndTest.Platform.ALL
  MANUAL = True
