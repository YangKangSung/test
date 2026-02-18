"""Pytest plugin: Rich progress integration for test run visualization.

- Adds a Suite progress bar (total = number of collected tests).
- Adds one progress task per test and updates it on start/finish.

Usage:
  - Drop this file into your test directory and run `pytest tests-examples`.
  - Set environment variable `RICH_PROGRESS=0` to disable.
"""
import os
import threading
import time
import random
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
    Column,
)
from rich.text import Text

console = Console()
_progress = None
_suite_task = None
_test_tasks = {}
_running = set()
_lock = threading.Lock()
_stop_event = threading.Event()
_bg_thread = None
_last_update = {}


class FieldColumn(TextColumn):
    """TextColumn wrapper that safely reads from task.fields and handles missing keys.

    It builds a format string like "{task.fields[test_name]:<50}" and delegates to
    TextColumn, but catches KeyError during render to avoid crashing when a field
    hasn't been set yet.
    """

    def __init__(self, field: str, fmt: str = "{:<50}", style: str | None = None):
        # fmt e.g. "{:<50}" -> inner ":<50"
        inner = fmt[1:-1]
        text = f"{{task.fields[{field}]{inner}}}"
        super().__init__(text, style=style)
        self.field = field

    def render(self, task):
        try:
            return super().render(task)
        except KeyError:
            # Field not set yet; return empty text so rendering continues safely
            return Text("", style=self.style)




def _enabled():
    return os.environ.get("RICH_PROGRESS", "1") != "0"


def _bg_updater():
    """Background thread that advances running tasks to simulate byte transfer speed."""
    interval = 0.1
    while not _stop_event.is_set():
        with _lock:
            now = time.time()
            for nodeid in list(_running):
                task_id = _test_tasks.get(nodeid)
                if task_id is None or _progress is None:
                    continue
                try:
                    task = _progress.tasks[task_id]
                except Exception:
                    continue
                total = task.total or 1
                if task.completed >= total:
                    continue
                # simulate speed between 0.3MB/s and 6MB/s
                speed = random.uniform(0.3e6, 6e6)
                chunk = speed * interval
                new_completed = min(total, task.completed + chunk)
                _progress.update(task_id, completed=new_completed)
        time.sleep(interval)


def pytest_sessionstart(session):
    global _progress, _bg_thread, _stop_event
    if not _enabled():
        return
    # Start the Progress context manager with Docker-pull style columns
    _progress = Progress(
        SpinnerColumn(),
        # Fixed-width test name column so statuses align vertically
        FieldColumn("test_name", fmt="{:<50}", style="white"),
        # Fixed-width status column (e.g., queued/running/PASS/FAIL)
        FieldColumn("status", fmt="{:>14}", style="bold"),
        BarColumn(bar_width=None),
        DownloadColumn(binary_units=True),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    )
    _progress.__enter__()

    # Start background updater
    _stop_event.clear()
    _bg_thread = threading.Thread(target=_bg_updater, name="pytest-progress-updater", daemon=True)
    _bg_thread.start()



def pytest_collection_modifyitems(session, config, items):
    """Called after collection; create suite task with total number of tests."""
    global _suite_task
    if not _enabled() or _progress is None:
        return
    total = len(items)
    _suite_task = _progress.add_task("[cyan]Suite[/cyan]", total=total)
    # ensure the suite task exposes the expected fields so columns render safely
    _progress.update(_suite_task, test_name="[cyan]Suite[/cyan]", status="")


def pytest_runtest_logstart(nodeid, location):
    """Create a per-test task when a test starts (bytes-based for docker-like display)."""
    if not _enabled() or _progress is None:
        return
    size = random.randint(1_000_000, 8_000_000)
    # create task with empty description; we use fields to populate name/status in fixed columns
    task_id = _progress.add_task(description="", total=size)
    _test_tasks[nodeid] = task_id
    with _lock:
        _running.add(nodeid)
        # warm initial progress so the speed column isn't empty and set fields
        warm = random.randint(int(size * 0.02), int(size * 0.05))
        _progress.update(task_id, completed=warm, test_name=nodeid, status="[blue]running[/blue]")


def pytest_runtest_logreport(report):
    """Update per-test task based on report. Only act on the main call phase."""
    if not _enabled() or _progress is None:
        return
    nodeid = report.nodeid
    task_id = _test_tasks.get(nodeid)
    if task_id is None:
        return

    # Only finalize on the call phase (the actual test function)
    if report.when == "call":
        try:
            total = _progress.tasks[task_id].total or 0
        except Exception:
            total = 0
        if report.passed:
            _progress.update(task_id, completed=total, status=f"[green]PASS[/green]")
        elif report.failed:
            _progress.update(task_id, completed=total, status=f"[bold red]FAIL[/bold red]")
        else:
            _progress.update(task_id, status=f"[yellow]{report.outcome}[/yellow]")

        with _lock:
            _running.discard(nodeid)

        # advance the suite bar
        global _suite_task
        if _suite_task is not None:
            _progress.update(_suite_task, advance=1)


def pytest_sessionfinish(session, exitstatus):
    """Stop and cleanup the progress context."""
    global _progress, _bg_thread
    if not _enabled() or _progress is None:
        return
    try:
        # stop background updater
        _stop_event.set()
        if _bg_thread is not None:
            _bg_thread.join(timeout=2.0)
        # Keep the final display for a short moment then exit
        _progress.stop()
    finally:
        _progress.__exit__(None, None, None)
        _progress = None
        _test_tasks.clear()
        _running.clear()
        _stop_event.clear()
        _bg_thread = None

