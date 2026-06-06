from asyncio import sleep
from datetime import datetime, timedelta
from typing import Callable

from flet import Page


class Job:
    """Create time-definite tasks"""

    def __init__(
        self,
        func: Callable[..., None],
        key: str,
        every: timedelta,
        page: Page,
        login_done: Callable[[], bool],
        sleep_time: int = 1,
    ) -> None:
        self.func = func
        self.key = key
        self.every = every
        self.sleep_time = sleep_time
        self.task_running = False
        self.page = page
        self.login_done = login_done
        self.next_run_time = datetime.now() + self.every

    def start(self) -> None:
        if not self.task_running:
            self.task_running = True
            self.page.run_task(self.run_task)

    async def run_task(self) -> None:
        while datetime.now() <= self.next_run_time and self.login_done():
            await sleep(self.sleep_time)
        if self.login_done():
            self.func(self.key)

    def stop(self) -> None:
        self.task_running = False
