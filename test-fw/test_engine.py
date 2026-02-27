import os
import json
import time
import pytest

STATUS_DIR = "task_status"

def update_status(task_name, status, msg):
    os.makedirs(STATUS_DIR, exist_ok=True)
    with open(os.path.join(STATUS_DIR, f"{task_name}.json"), "w", encoding='utf-8') as f:
        json.dump({"name": task_name, "status": status, "msg": msg}, f)

# [Depth 1] 글로벌 셋업
def test_global_setup():
    update_status("1. Global_Setup", "Running", "공통 인프라 세팅 중...")
    time.sleep(2)
    assert True # 실제 검증 로직
    update_status("1. Global_Setup", "Success", "완료")

# [Depth 2] 노드 기본 설정 (병렬)
def test_node_config():
    node_id = os.getenv("NODE_ID", "0")
    update_status(f"2. Node_{node_id}_Config", "Running", "설정 적용 중...")
    time.sleep(1.5)
    assert True
    update_status(f"2. Node_{node_id}_Config", "Success", "완료")

# [Depth 3] 조건부 보안 스캔 (분기 - 특정 노드만 실행)
def test_node_security():
    node_id = os.getenv("NODE_ID", "0")
    update_status(f"3. Node_{node_id}_Security", "Running", "정밀 보안 스캔 중...")
    time.sleep(3) # 보안 스캔은 좀 더 오래 걸림
    assert True
    update_status(f"3. Node_{node_id}_Security", "Success", "완료")

# [Depth 4] 노드 헬스 체크 (병렬)
def test_node_health():
    node_id = os.getenv("NODE_ID", "0")
    update_status(f"4. Node_{node_id}_Health", "Running", "서비스 기동 확인 중...")
    time.sleep(1)
    assert True
    update_status(f"4. Node_{node_id}_Health", "Success", "완료")

# [Depth 5] 최종 리포트 (순차)
def test_final_report():
    update_status("5. Final_Report", "Running", "결과 취합 및 리포트 생성 중...")
    time.sleep(1.5)
    assert True
    update_status("5. Final_Report", "Success", "완료")