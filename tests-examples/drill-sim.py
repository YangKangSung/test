import asyncio
import random
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

console = Console()

async def simulate_test_case(progress, task_id, tc):
    """개별 테스트 케이스의 생명주기를 시뮬레이션합니다."""
    tc_id = tc['id']
    tc_type = tc['type'].upper()

    # 1. 트리거 단계 (Queue 대기 상황 시뮬레이션)
    progress.update(task_id, description=f"[bold white][{tc_type}][/bold white] {tc_id} - [지연] 대기 중...")
    await asyncio.sleep(random.uniform(1, 3))

    # 2. 실행 단계
    progress.update(task_id, description=f"[bold blue][{tc_type}][/bold blue] {tc_id} - [실행] 진행 중...")

    total_steps = 100
    current_step = 0

    while current_step < total_steps:
        # 작업 속도가 제각각인 것을 표현
        step_increment = random.randint(5, 15)
        current_step += step_increment
        if current_step > total_steps: current_step = total_steps

        await asyncio.sleep(random.uniform(0.3, 0.8))
        progress.update(task_id, completed=current_step)

        # 중간에 상태 메시지 변경
        if current_step > 50:
            progress.update(task_id, description=f"[bold yellow][{tc_type}][/bold yellow] {tc_id} - [검증] 결과 확인 중...")

    # 3. 최종 결과 결정 (80% 확률로 성공, 20% 확률로 실패 시뮬레이션)
    is_success = random.random() > 0.2

    if is_success:
        progress.update(task_id, description=f"[bold green][{tc_type}][/bold green] {tc_id} - [PASS] 성공")
        return True
    else:
        progress.update(task_id, description=f"[bold red][{tc_type}][/bold red] {tc_id} - [FAIL] 에러 발생")
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
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:

        # 모든 테스트 케이스를 Task로 등록
        tasks = []
        for tc in test_set:
            task_id = progress.add_task(description="", total=100)
            tasks.append(simulate_test_case(progress, task_id, tc))

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