import datetime
import unittest

import env
import main
import webcam


class TestMain(unittest.TestCase):

    def setUp(self):
        self._camera = webcam.Camera("123", "any")

    def _test_target_file_path_generation(self, expected_date: str, timestamp: float):
        excepted_path = "{}/{}/{}_{}.jpg".format(self._camera.name, expected_date, self._camera.name, timestamp)
        self.assertEqual(excepted_path, main.get_target_file_path(self._camera, timestamp))

    def test_today(self):
        date = datetime.datetime(year=2019, month=1, day=1,
                                 hour=23, minute=59, second=59, tzinfo=env.get_timezone())
        self._test_target_file_path_generation("2019/01/01", date.timestamp())

    def test_midnight_next_day(self):
        date = datetime.datetime(year=2019, month=1, day=2,
                                 hour=0, minute=0, second=0, tzinfo=env.get_timezone())
        self._test_target_file_path_generation("2019/01/02", date.timestamp())


if __name__ == '__main__':
    unittest.main()
