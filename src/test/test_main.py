import datetime
import unittest

import env
import main
import webcam


class TestMain(unittest.TestCase):

    def test_target_file_path_generation(self):
        camera = webcam.Camera("123", "any")

        date = datetime.datetime(year=2019, month=1, day=1, tzinfo=env.get_timezone())
        excepted_path = "{}/2019/01/01/{}_{}.jpg".format(camera.name, camera.name, date.timestamp())
        self.assertEqual(excepted_path, main.get_target_file_path(camera, date.timestamp()))


if __name__ == '__main__':
    unittest.main()
