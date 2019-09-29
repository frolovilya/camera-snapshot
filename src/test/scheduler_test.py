import unittest
from src import scheduler


class SchedulerTest(unittest.TestCase):

    def setUp(self):
        self._scheduler = scheduler.Scheduler()

    def test_timer(self):
        self.assertEqual(self._scheduler._next_timestamp(0, 3600), 3600)
        self.assertEqual(self._scheduler._next_timestamp(1, 3600), 3600)
        self.assertEqual(self._scheduler._next_timestamp(3600, 3600), 7200)
        self.assertEqual(self._scheduler._next_timestamp(3601, 3600), 7200)


if __name__ == '__main__':
    unittest.main()
