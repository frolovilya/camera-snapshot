import sched
import time
from src import logger


class Scheduler:
    s = sched.scheduler(time.time, time.sleep)

    def __next_timestamp(self, current_timestamp, abs_period):
        return int(current_timestamp - current_timestamp % abs_period) + abs_period

    def __wrap_repeated_task(self, task_func, period):
        def repeated_task():
            logger.log("Executing task at {}", int(time.time()))
            task_func()
            self.schedule_task(task_func, period)

        return repeated_task

    def schedule_task(self, task_func, period=3600):
        execution_time = self.__next_timestamp(time.time(), period)
        logger.log("Scheduled next execution time {}", execution_time)
        self.s.enterabs(execution_time, 1, self.__wrap_repeated_task(task_func, period))

    def start(self):
        self.s.run()
