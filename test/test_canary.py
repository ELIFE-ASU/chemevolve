# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
import unittest

class TestCanary(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(3, 1+2)
