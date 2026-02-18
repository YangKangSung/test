import asyncio
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
    TextColumn,
)
from rich.text import Text

console = Console()


class FieldColumn(TextColumn):
    """Column that reads a named field from task.fields and supports middle
    ellipsizing and returning Rich Text objects directly."""

    def __init__(self, field: str, fmt: str = "{:<30}", style: str | None = None, ellipsize_middle: bool = False):
        # extract width
        width = None
        try:
            inner = fmt[1:-1]
            digits = ''.join(ch for ch in inner if ch.isdigit())
            if digits:
                width = int(digits)
        except Exception:
            width = None
        text = f"{{task.fields[{field}]}}"
        super().__init__(text, style=style)
        self.field = field
        self.width = width
        self.ellipsize_middle = ellipsize_middle

    def render(self, task):
        val = task.fields.get(self.field, "")
        if isinstance(val, Text):
            return val
        s = str(val)
        if self.ellipsize_middle and self.width and len(s) > self.width:
            keep = self.width - 3
            left = keep // 2
            right = keep - left
            s = s[:left] + "..." + s[-right:]
        return Text(s, style=self.style)


async def simulate_test_case(progress, task_id, tc, suite_id=None):
    """개별 테스트 케이스의 생명주기를 바이트 단위로 시뮬레이션합니다."""
    tc_id = tc['id']
    tc_type = tc['type'].upper()
    total_bytes = tc.get('size', 10_000_000)

    # 1. 트리거 단계 (Queue 대기 상황 시뮬레이션)
    progress.update(task_id, status=Text("대기", style="yellow"))
    await asyncio.sleep(random.uniform(0.5, 2.0))

    # 2. 실행 단계 (docker pull 스타일: bytes, speed, ETA 표시)
    progress.update(task_id, status=Text("다운로드", style="blue"))

    downloaded = 0

    while downloaded < total_bytes:
        # 작업 속도가 제각각인 것을 표현 (bytes 단위)
        chunk = random.randint(50_000, 2_000_000)
        downloaded += chunk
        if downloaded > total_bytes:
            downloaded = total_bytes

        await asyncio.sleep(random.uniform(0.05, 0.3))
        progress.update(task_id, completed=downloaded)

        # 중간 상태 메시지 변경
        if downloaded > total_bytes * 0.5:
            progress.update(task_id, status=Text("검증", style="yellow"))

    # 3. 최종 결과 결정 (80% 확률로 성공, 20% 확률로 실패 시뮬레이션)
    is_success = random.random() > 0.2

    if is_success:
        progress.update(task_id, completed=total_bytes, status=Text("PASS", style="black on green"))
        if suite_id:
            progress.update(suite_id, advance=1)
        return True
    else:
        progress.update(task_id, completed=downloaded, status=Text("FAIL", style="white on red"))
        # move failed test to top for visibility
        try:
            progress.move_task(task_id, 0)
        except Exception:
            pass
        if suite_id:
            progress.update(suite_id, advance=1)
        return False

async def run_orchestrator():
    test_set = [
        {"id": "TC-WEB-01", "type": "jenkins"},
        {"id": "TC-API-02", "type": "airflow"},
        {"id": "TC-DB-03", "type": "jenkins"},
        {"id": "TC-DATA-04", "type": "airflow"},
        {"id": "TC-SEC-05", "type": "jenkins"},
    ]

    console.print("[bold cyan]🚀 비동기 테스트 오케스트레이터 시뮬레이션을 시작합니다...[/bold cyan]\n")

    with Progress(
        SpinnerColumn(),
        # Fixed-width TC name column and status column so output aligns like docker pull
        FieldColumn("test_name", fmt="{:<30}", style="white", ellipsize_middle=True),
        FieldColumn("status", fmt="{:>18}", style="bold"),
        BarColumn(bar_width=40),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        TimeElapsedColumn(),
        console=console
    ) as progress:

        # Suite 진행바 추가
        suite_id = progress.add_task("[cyan]Suite[/cyan]", total=len(test_set), test_name="[cyan]Suite[/cyan]", status="")

        # 모든 테스트 케이스를 Task로 등록 (크기: 1MB ~ 20MB)
        tasks = []
        for tc in test_set:
            size = random.randint(1_000_000, 20_000_000)
            tc['size'] = size
            # create task with fields for fixed columns
            task_id = progress.add_task(description="", total=size, test_name=f"[{tc['type'].upper()}] {tc['id']}", status="[yellow]대기[/yellow]")
            tasks.append(simulate_test_case(progress, task_id, tc, suite_id))

        # 모든 비동기 작업 실행 및 결과 수합
        results = await asyncio.gather(*tasks)

    # 최종 요약 출력
    console.print("\n[bold white]" + "="*50 + "[/bold white]")
    passed = sum(results)
    failed = len(results) - passed

    summary_color = "green" if failed == 0 else "red"
    console.print(f"[{summary_color}]최종 결과: {passed} 성공 / {failed} 실패[/{summary_color}]")
    console.print("[bold white]" + "="*50 + "[/bold white]")

if __name__ == "__main__":
    asyncio.run(run_orchestrator())