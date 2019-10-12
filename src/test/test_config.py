import unittest
import os

import config


class TestConfig(unittest.TestCase):

    _config_file_path = "config.yml"

    _secret_placeholder = "(secret)"

    def setUp(self):
        os.environ['TIME_PERIOD_SEC'] = str(100)
        os.environ['FFMPEG_BIN'] = "/usr/local/bin/ffmpeg"

    def test_properties_override(self):
        props = config.get_properties(self._config_file_path)

        self.assertEqual(props['time_period_sec'], os.environ['TIME_PERIOD_SEC'])
        self.assertEqual(props['ffmpeg']['bin'], os.environ['FFMPEG_BIN'])

        self.assertEqual(props['s3']['bucket_name'], self._secret_placeholder)
        self.assertEqual(props['s3']['access_key'], self._secret_placeholder)
        self.assertEqual(props['s3']['secret_key'], self._secret_placeholder)


if __name__ == '__main__':
    unittest.main()
