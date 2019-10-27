import datetime
import sched
import time
import multiprocessing as mp

import env
import logger


class Scheduler:
    def __init__(self, workers_count: int):
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._tasks = []
        self._workers_count = workers_count

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

    def _repeat_tasks(self, period: int):
        """
        Execute task_func and schedule next execution.

        :param period: execution repeat period in seconds
        :return: wrapped task_func
        """
        logger.log("---------- Executing task ({})", int(time.time()))
        try:
            workers = mp.Pool(self._workers_count)
            try:
                for task_func, task_args in self._tasks:
                    workers.apply_async(task_func, args=task_args)

                workers.close()
                workers.join()
                logger.log("Finished tasks")
            except KeyboardInterrupt as e:
                workers.terminate()
                logger.log("Interrupted task execution")
                raise e
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            logger.error("Error while executing task: {}", str(e))

        self._schedule_next_invocation(period)

    def _schedule_next_invocation(self, period: int):
        """
        Schedule tasks to be executed every specified time period.
        Calls time.sleep() between executions.

        :param period: execution repeat period in seconds
        """
        execution_time = self._next_timestamp(time.time(), period)
        logger.log("Scheduled next execution time {} ({})",
                   self._readable_timestamp(execution_time), execution_time)
        self._scheduler.enterabs(execution_time, 1, self._repeat_tasks, argument=(period,))

    def add_task(self, task_func, *task_args):
        self._tasks.append((task_func, task_args))

    def start(self, period: int):
        """
        Start executing scheduled tasks at every time period.
        """
        try:
            self._schedule_next_invocation(period)
            self._scheduler.run()
        except KeyboardInterrupt as e:
            # all KeyboardInterrupt exceptions are raised up to this block
            logger.log("Stopped scheduler {}", e)
