import subprocess
import os
import threading
import time
from collections import deque
from prefect import task, flow
from prefect.task_runners import ConcurrentTaskRunner
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text

# --- 전역 상태 및 로그 관리 (메모리 공유) ---
task_states = {}
# 화면 아래쪽에 표시할 로그를 최근 30줄만 기억하도록 세팅 (자동 밀어내기)
log_messages = deque(maxlen=30)

def add_log(msg):
    """실시간 로그 패널에 메시지를 추가합니다."""
    log_messages.append(msg)

def update_state(name, status, msg=""):
    """대시보드 표의 상태를 업데이트합니다."""
    task_states[name] = {"status": status, "msg": msg}

# --- 1. 실시간 로그 캡처 Task ---
@task
def run_pytest(step_name, test_func, node_id=None):
    update_state(step_name, "Running", "테스트 실행 중...")
    add_log(f"▶️ [START] {step_name} 가동 시작")

    env = os.environ.copy()
    if node_id: env["NODE_ID"] = str(node_id)

    cmd = ["pytest", f"test_engine.py::{test_func}", "-v", "--tb=short"]

    # [핵심] subprocess.run 대신 Popen을 사용하여 출력을 한 줄씩 실시간으로 낚아챕니다.
    process = subprocess.Popen(
        cmd, env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # pytest가 뱉어내는 로그를 실시간으로 큐에 넣습니다.
    for line in process.stdout:
        stripped = line.strip()
        if stripped: # 빈 줄 제외
            add_log(f"  [{step_name}] {stripped}")

    process.wait() # 작업이 끝날 때까지 대기

    if process.returncode != 0:
        update_state(step_name, "Failed", "❌ 에러 발생")
        add_log(f"❌ [FAIL] {step_name} 실패!")
        raise Exception(f"{step_name} 실패")

    update_state(step_name, "Success", "✅ 완료")
    add_log(f"✅ [SUCCESS] {step_name} 정상 완료")
    return True

# --- 2. 파이프라인 Flow ---
@flow(task_runner=ConcurrentTaskRunner())
def run_infrastructure_pipeline():
    add_log("🚀 [SYSTEM] 인프라 파이프라인 가동을 시작합니다.")

    # [Depth 1] 셋업
    setup = run_pytest.submit("1. Global_Setup", "test_global_setup").result()

    all_health_checks = []

    # [Depth 2~4] 병렬 노드 처리
    for i in range(1, 4):
        config = run_pytest.submit(f"2. Node_{i}_Config", "test_node_config", node_id=i)

        if i == 1: # 분기
            security = run_pytest.submit(f"3. Node_{i}_Security", "test_node_security", node_id=i, wait_for=[config])
            health = run_pytest.submit(f"4. Node_{i}_Health", "test_node_health", node_id=i, wait_for=[security])
        else:
            health = run_pytest.submit(f"4. Node_{i}_Health", "test_node_health", node_id=i, wait_for=[config])

        all_health_checks.append(health)

    # [Depth 5] 대기 및 종료
    for h in all_health_checks:
        h.result()

    run_pytest.submit("5. Final_Report", "test_final_report").result()
    add_log("🎉 [SYSTEM] 모든 파이프라인이 성공적으로 종료되었습니다.")

# --- 3. Rich 화면 레이아웃 렌더링 ---
def generate_layout():
    # 화면을 위(대시보드) / 아래(로그)로 나눕니다.
    layout = Layout()
    layout.split_column(
        Layout(name="dashboard", ratio=1),  # 위쪽 50%
        Layout(name="logs", ratio=1)        # 아래쪽 50%
    )

    # 1) 대시보드 표 생성
    table = Table(expand=True, show_header=True, header_style="bold magenta")
    table.add_column("Task Name", ratio=2); table.add_column("Status", ratio=1, justify="center"); table.add_column("Message", ratio=3)

    for name, data in sorted(task_states.items()):
        status = data["status"]
        if status == "Running": color, icon = "cyan", "🔄"
        elif status == "Success": color, icon = "green", "✅"
        elif status == "Failed": color, icon = "red", "❌"
        else: color, icon = "white", "⏳"

        table.add_row(f"[bold]{name}", f"[{color}]{icon} {status}", f"[dim]{data['msg']}")

    layout["dashboard"].update(Panel(table, title="[bold blue]🚀 파이프라인 대시보드[/bold blue]", border_style="blue"))

    # 2) 실시간 로그 화면 생성
    log_text = Text("\n".join(log_messages))
    layout["logs"].update(Panel(log_text, title="[bold yellow]📜 실시간 실행 로그 (stdout/stderr)[/bold yellow]", border_style="yellow"))

    return layout

# --- 메인 실행부 ---
if __name__ == "__main__":
    # 터미널 화면 정리
    os.system('cls' if os.name == 'nt' else 'clear')

    # 파이프라인을 백그라운드 스레드에서 시작
    flow_thread = threading.Thread(target=run_infrastructure_pipeline, daemon=True)
    flow_thread.start()

    # 메인 스레드는 화면 그리기에 전념
    with Live(generate_layout(), refresh_per_second=10, screen=True) as live:
        while flow_thread.is_alive():
            time.sleep(0.1)
            live.update(generate_layout())

        # 끝난 후 마지막 화면 렌더링 유지 (2초)
        live.update(generate_layout())
        time.sleep(2)