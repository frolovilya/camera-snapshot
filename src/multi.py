import multiprocessing as mp
import time
import random

import logger


def capture_camera_worker(camera):
    time.sleep(random.randint(0, 2))
    logger.log("cam" + str(camera))


def run_multi():
    logger.log("start")

    workers = mp.Pool(3)
    for i in range(3):
        workers.apply_async(capture_camera_worker, args=(i,))

    workers.close()
    workers.join()

    logger.log("end")


if __name__ == "__main__":
    logger.start()
    run_multi()
