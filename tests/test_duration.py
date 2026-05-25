import unittest

from video_tools.duration import check_duration


class TestDuration(unittest.TestCase):
    def test_duration(self):
        self.assertTrue(check_duration(90, 100), 'Shorter, within tolerance')
        self.assertTrue(check_duration(105, 90), 'Longer, within tolerance')
        self.assertFalse(check_duration(80, 100, 5), 'Shorter, outside tolerance')
        self.assertFalse(check_duration(150, 90, 5), 'Longer, outside tolerance')
