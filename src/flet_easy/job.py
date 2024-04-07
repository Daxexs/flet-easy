from asyncio import sleep
from datetime import datetime, timedelta
from typing import Callable

from flet import Page


class Job:
    """Create time-definite tasks"""

    def __init__(
        self,
        func: Callable,
        key: str,
        every: timedelta,
        page: Page,
        login_done: bool,
        sleep_time: int = 1,
    ):
        self.func = func
        self.key = key
        self.every = every
        self.sleep_time = sleep_time
        self.task_running = False
        self.page = page
        self.login_done = login_done
        self.next_run_time = datetime.now() + self.every

    async def task(self):
        while self.task_running:
            await sleep(self.sleep_time)
            self.func()

    def start(self):
        if not self.task_running:
            self.task_running = True
            self.page.run_task(self.run_task)

    async def run_task(self):
        while datetime.now() <= self.next_run_time and self.login_done():
            await sleep(self.sleep_time)
        if self.login_done():
            self.func(self.key)()

    def stop(self):
        self.task_running = False
