import unittest
import os
from src import config


class ConfigTest(unittest.TestCase):

    config_file_path = "../../config.yml"

    def setUp(self):
        os.environ['TIME_PERIOD'] = str(100)
        os.environ['FFMPEG_BIN'] = "/usr/local/bin/ffmpeg"

    def test_properties_override(self):
        props = config.get_properties(self.config_file_path)

        self.assertEqual(props['time_period'], os.environ['TIME_PERIOD'])
        self.assertEqual(props['ffmpeg']['bin'], os.environ['FFMPEG_BIN'])


if __name__ == '__main__':
    unittest.main()
