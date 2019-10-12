import datetime
import sched
import time

import env
import logger


class Scheduler:
    _scheduler = sched.scheduler(time.time, time.sleep)

    def _next_timestamp(self, current_timestamp: float, abs_period: int) -> float:
        """
        Calculate next task execution timestamp.
        Example:
            Current timestamp: 1570869954 (11:45)
            Execution period: hourly, 3600 seconds
            Next execution timestamp: 1570870800 (12:00)

        :param current_timestamp: current unix timestamp
        :param abs_period: execution period in seconds, for example 3600 for an hour
        :return: next timestamp
        """
        return int(current_timestamp - current_timestamp % abs_period) + abs_period

    def _readable_timestamp(self, timestamp: float) -> str:
        """
        Convert timestamp in seconds to a readable date.

        :param timestamp: unix timestamp in seconds
        :return: date string
        """
        return datetime.datetime.fromtimestamp(timestamp, tz=env.get_timezone()).strftime("%Y-%m-%d %H:%M:%S")

    def _wrap_repeated_task(self, task_func, period: int):
        """
        Execute task_func and schedule next execution.

        :param task_func: task function to execute
        :param period: execution repeat period in seconds
        :return: wrapped task_func
        """
        def repeated_task():
            logger.log("---------- Executing task ({})", int(time.time()))
            try:
                task_func()
            except Exception as e:
                logger.error("Error while executing task: {}", str(e))
            self.schedule_task(task_func, period)

        return repeated_task

    def schedule_task(self, task_func, period: int = 3600):
        """
        Schedule task_func to be executed every period.
        Calls time.sleep() between executions.

        :param task_func: task function to execute
        :param period: execution repeat period in seconds
        """
        execution_time = self._next_timestamp(time.time(), period)
        logger.log("Scheduled next execution time {} ({})",
                   self._readable_timestamp(execution_time), execution_time)
        self._scheduler.enterabs(execution_time, 1, self._wrap_repeated_task(task_func, period))

    def start(self):
        """
        Start executing scheduled tasks.
        """
        try:
            self._scheduler.run()
        except KeyboardInterrupt as e:
            logger.log("Stopped scheduler {}", e)
