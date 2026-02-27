import subprocess
import os
from prefect import task, flow, get_run_logger
from prefect.task_runners import ConcurrentTaskRunner

# --- 1. [핵심] 견고한 Task 정의 (재시도 및 장애 격리) ---
# 일시적인 오류를 대비해 최대 2번, 5초 간격으로 자동 재시도합니다.
@task(retries=2, retry_delay_seconds=5)
def run_pytest(step_name, test_func, node_id=None):
    logger = get_run_logger() # Prefect 공식 로거 사용
    logger.info(f"▶️ [시작] {step_name}")

    env = os.environ.copy()
    if node_id:
        env["NODE_ID"] = str(node_id)

    cmd = ["pytest", f"test_engine.py::{test_func}", "-q", "--tb=short"]
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)

    # 실패하더라도 Exception을 발생시켜 Flow를 죽이지 않고, 상태 딕셔너리를 반환합니다. (장애 격리)
    if result.returncode != 0:
        logger.error(f"❌ [실패] {step_name}\n{result.stdout}")
        return {"step": step_name, "node_id": node_id, "status": "FAILED"}

    logger.info(f"✅ [성공] {step_name}")
    return {"step": step_name, "node_id": node_id, "status": "SUCCESS"}

# --- 2. 파이프라인 Flow 정의 ---
@flow(task_runner=ConcurrentTaskRunner())
def robust_infrastructure_pipeline():
    logger = get_run_logger()
    logger.info("🚀 운영 환경용 인프라 파이프라인 가동")

    # [Depth 1] 글로벌 셋업 (이게 실패하면 전체 중단해야 하므로 엄격하게 체크)
    setup_result = run_pytest.submit("Global_Setup", "test_global_setup").result()
    if setup_result["status"] == "FAILED":
        logger.error("🚨 인프라 초기화 실패로 전체 파이프라인을 비상 중단합니다.")
        return

    node_futures = []

    # [Depth 2~4] 병렬 노드 작업 (3개)
    for i in range(1, 4):
        # Setup 완료 후 병렬 실행
        config = run_pytest.submit(f"Node_{i}_Config", "test_node_config", node_id=i)

        if i == 1:
            # Node 1: 보안 스캔 (분기)
            security = run_pytest.submit(f"Node_{i}_Security", "test_node_security", node_id=i, wait_for=[config])
            health = run_pytest.submit(f"Node_{i}_Health", "test_node_health", node_id=i, wait_for=[security])
        else:
            # Node 2, 3: 바로 헬스 체크
            health = run_pytest.submit(f"Node_{i}_Health", "test_node_health", node_id=i, wait_for=[config])

        node_futures.append(health)

    # [Depth 5] 상태 취합 및 최종 리포트 (모든 병렬 작업 대기)
    logger.info("⏳ 모든 노드의 작업이 끝날 때까지 대기합니다...")

    # .result()를 호출하여 백그라운드 작업들이 완료될 때까지 Blocking
    health_results = [future.result() for future in node_futures]

    # 성공/실패 통계 계산
    success_count = sum(1 for r in health_results if r["status"] == "SUCCESS")
    failed_count = len(health_results) - success_count

    logger.info(f"📊 [결과 요약] 성공: {success_count}대 / 실패: {failed_count}대")

    # 최종 리포트 생성
    final_report = run_pytest.submit("Final_Report", "test_final_report")
    final_report.result() # Flow가 종료되기 전 마지막으로 한 번 더 대기

    logger.info("🎉 파이프라인 전체 프로세스 종료")

if __name__ == "__main__":
    robust_infrastructure_pipeline()