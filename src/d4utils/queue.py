"""This module provides a functionality to initilize and maintain a MaxQueuePool."""

import concurrent.futures
import logging
from threading import BoundedSemaphore
from typing import Any
from typing import Callable
from typing import Union


class MaxQueuePool:
    """MaxQueuePool class.

    This Class wraps a concurrent.futures.Executor limiting the size
    of its task queue.

    If `max_queue_size` tasks are submitted, the next call to submit
    will block until a previously submitted one is completed.

    cf https://gist.github.com/noxdafox/4150eff0059ea43f6adbdd66e5d5e87e

    """

    def __init__(
        self,
        executor: type[concurrent.futures.ProcessPoolExecutor],
        *,
        max_queue_size: int,
        max_workers: Union[int, Any] = None
    ):
        """Initialize the pool with a maximum number of workers."""
        logging.info(
            "Initializing queue with %i queue slots, %i workers",
            max_queue_size,
            max_workers,
        )
        self.pool = executor(max_workers=max_workers)
        self.pool_queue = BoundedSemaphore(max_queue_size)

    def submit(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Submit a new task to the pool.

        This will block if the queue is full.
        """
        self.pool_queue.acquire()  # pylint: disable=consider-using-with
        future = self.pool.submit(func, *args, **kwargs)
        future.add_done_callback(self.pool_queue_callback)

        return future

    def pool_queue_callback(self, _: Any) -> None:
        """Called when a future is done. Releases one queue slot."""
        self.pool_queue.release()


def init_pool(cores: int = 1) -> MaxQueuePool:
    """Initialize a process pool with a maximum number of workers."""
    return MaxQueuePool(
        concurrent.futures.ProcessPoolExecutor,
        max_workers=cores,
        max_queue_size=int(2 * cores),
    )
