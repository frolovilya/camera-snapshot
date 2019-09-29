import datetime
import sched
import time

import env
import logger


class Scheduler:
    _scheduler = sched.scheduler(time.time, time.sleep)

    def _next_timestamp(self, current_timestamp, abs_period):
        return int(current_timestamp - current_timestamp % abs_period) + abs_period

    def _readable_timestamp(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp, tz=env.get_timezone()).strftime("%Y-%m-%d %H:%M:%S")

    def _wrap_repeated_task(self, task_func, period):
        def repeated_task():
            logger.log("---------- Executing task ({})", int(time.time()))
            try:
                task_func()
            except Exception as e:
                logger.error("Error while executing task: {}", str(e))
            self.schedule_task(task_func, period)

        return repeated_task

    def schedule_task(self, task_func, period=3600):
        execution_time = self._next_timestamp(time.time(), int(period))
        logger.log("Scheduled next execution time {} ({})",
                   self._readable_timestamp(execution_time), execution_time)
        self._scheduler.enterabs(execution_time, 1, self._wrap_repeated_task(task_func, int(period)))

    def start(self):
        try:
            self._scheduler.run()
        except KeyboardInterrupt as e:
            logger.log("Stopped scheduler {}", e)
