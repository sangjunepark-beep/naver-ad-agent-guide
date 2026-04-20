# Python 자동화 가이드 — 멀티모델 + 캐싱 + Batch API

하나사인몰 어드민 자동화를 Python + Playwright + Claude API로 구축하는 가이드.

---

## 1. 기본 구조

```
hanasm_admin_auto/
├── main.py              # 오케스트레이터 (Opus 호출)
├── audit.py             # 감사 전용 (Haiku 호출)
├── connector.py         # 업종 연결 (Haiku 호출)
├── executor.py          # 수정 실행 (Haiku 호출)
├── judge.py             # 판단 (Sonnet 호출)
├── report.py            # Excel 생성 (Sonnet 호출)
├── browser.py           # Playwright 세션 관리
├── prompts/
│   ├── system_opus.txt  # Opus 시스템 프롬프트 (캐시 대상)
│   ├── system_haiku.txt # Haiku 시스템 프롬프트 (캐시 대상)
│   └── system_sonnet.txt
├── scripts/
│   ├── audit.js         # (이 폴더의 scripts/ 복사)
│   ├── connect_industry.js
│   └── batch_click.js
└── data/
    ├── progress.json    # 진행 상태
    └── results/
```

---

## 2. 모델별 API 호출 함수

```python
import anthropic
import json

client = anthropic.Anthropic()

# 모델 상수
OPUS   = "claude-opus-4-6"
SONNET = "claude-sonnet-4-6"
HAIKU  = "claude-haiku-4-5-20251001"

def call_haiku(prompt: str, system: str, cache_system: bool = True) -> str:
    """반복 작업용. 캐싱 적용."""
    sys_content = [
        {
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"}  # 캐싱 핵심
        }
    ] if cache_system else [{"type": "text", "text": system}]

    resp = client.messages.create(
        model=HAIKU,
        max_tokens=2048,
        system=sys_content,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text

def call_sonnet(prompt: str, system: str, cache_system: bool = True) -> str:
    """판단 + Excel 생성용."""
    sys_content = [
        {
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"}
        }
    ] if cache_system else [{"type": "text", "text": system}]

    resp = client.messages.create(
        model=SONNET,
        max_tokens=4096,
        system=sys_content,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text

def call_opus(prompt: str, system: str) -> str:
    """전략/예외 판단 전용. 캐싱 적용."""
    resp = client.messages.create(
        model=OPUS,
        max_tokens=4096,
        system=[
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text
```

---

## 3. Prompt Caching 설정

시스템 프롬프트(스킬 내용, JS 코드 등)는 반복 호출 시 캐싱.

```python
# prompts/system_haiku.txt 로드 후 캐싱
with open("prompts/system_haiku.txt") as f:
    HAIKU_SYSTEM = f.read()

# audit.js 내용도 시스템 프롬프트에 포함 → 캐싱됨
with open("scripts/audit.js") as f:
    AUDIT_JS = f.read()

HAIKU_SYSTEM_WITH_SCRIPTS = f"""
{HAIKU_SYSTEM}

## 감사 스크립트 (그대로 실행)
```javascript
{AUDIT_JS}
```
"""

# 이 시스템 프롬프트는 288개 반복 호출 시 전부 캐시 히트
# 첫 번째 호출만 일반 요금, 이후는 캐시 요금 (1/10)
```

**캐싱 효과 (288개 기준):**

| 항목 | 캐싱 없이 | 캐싱 후 |
|------|-----------|---------|
| 시스템 프롬프트 (~2000토큰) | $0.576 | **$0.058** |
| JS 스크립트 (~500토큰) | $0.144 | **$0.014** |
| 절감 | — | **약 90%** |

---

## 4. 모델 라우팅 로직

```python
def route_product(audit_result: dict) -> str:
    """상품 1개의 처리 경로 결정."""
    if audit_result["e"]:
        return "industry_connector"  # 업종 미연결 → Haiku
    if audit_result["full"]:
        return "judgment_sonnet"     # 과태깅 의심 → Sonnet 판단
    if audit_result["cnt"] > 80:
        return "judgment_sonnet"     # 경계값 → Sonnet 판단
    return "normal"                  # 정상 → 건너뜀

def needs_opus_review(sonnet_result: dict) -> bool:
    """Sonnet 판단 후 Opus 검토 필요 여부."""
    # 안전/경고/법령 관련 상품
    special_keywords = ["안전", "경고", "위험", "금지", "소방", "피난", "법령", "규정"]
    name = sonnet_result.get("name", "")
    if any(kw in name for kw in special_keywords):
        return True
    # 판단 불가로 표시된 경우
    if sonnet_result.get("judgment") == "판단불가":
        return True
    return False
```

---

## 5. Batch API (감사 단계에 적용)

288개 전체 감사는 Batch API로 처리하면 비용 50% 추가 절감.

```python
def batch_audit_products(rgr_list: list[str]) -> str:
    """
    288개 감사 요청을 Batch API로 한 번에 보냄.
    비동기 처리 → 최대 24시간 내 결과 반환.
    반환값: batch_id
    """
    requests = []
    for rgr in rgr_list:
        url = f"https://ad.hanasm.kr/AdminManager/MakeGoodsTypeOneDp.php?RgrCode={rgr}&EditMode=1"
        requests.append({
            "custom_id": rgr,
            "params": {
                "model": HAIKU,
                "max_tokens": 1024,
                "system": [
                    {
                        "type": "text",
                        "text": HAIKU_SYSTEM_WITH_SCRIPTS,
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                "messages": [
                    {
                        "role": "user",
                        "content": f"아래 URL의 상품을 감사해서 JSON으로 반환:\n{url}\n\naudit.js 스크립트를 실행하고 결과를 그대로 리턴."
                    }
                ]
            }
        })

    batch = client.messages.batches.create(requests=requests)
    return batch.id

def check_batch_status(batch_id: str) -> dict:
    batch = client.messages.batches.retrieve(batch_id)
    return {
        "status": batch.processing_status,
        "completed": batch.request_counts.succeeded,
        "total": len(batch.request_counts.__dict__)
    }

def get_batch_results(batch_id: str) -> list[dict]:
    results = []
    for result in client.messages.batches.results(batch_id):
        if result.result.type == "succeeded":
            results.append({
                "rgr": result.custom_id,
                "response": result.result.message.content[0].text
            })
    return results
```

**주의:** Batch API는 Playwright(브라우저 실제 접속)와 직접 연동 불가.
브라우저 제어는 Playwright로 별도 수행하고, Claude는 "어떻게 처리할지 판단"만 담당.
실제 구조는 아래 섹션 참조.

---

## 6. Playwright + Claude 실제 연동 구조

Claude API가 브라우저를 직접 제어하지 않는다.
**Playwright가 브라우저 제어, Claude는 판단/지시만.**

```python
from playwright.sync_api import sync_playwright
import json

def audit_product(page, rgr: str) -> dict:
    """Playwright로 페이지 접속 → JS 실행 → 결과 반환. Claude 불필요."""
    url = f"https://ad.hanasm.kr/AdminManager/MakeGoodsTypeOneDp.php?RgrCode={rgr}&EditMode=1"
    page.goto(url)
    page.wait_for_load_state("networkidle")
    
    with open("scripts/audit.js") as f:
        js = f.read()
    
    result_str = page.evaluate(js)
    return json.loads(result_str)

def connect_industry(page, rgr: str, code: str):
    """업종 1개 연결. Claude 불필요 — 고정 패턴."""
    url = f"https://ad.hanasm.kr/AdminManager/MakeGoodsTypeOneDp.php?RgrCode={rgr}&EditMode=1"
    page.goto(url)
    page.wait_for_load_state("networkidle")
    
    with open("scripts/connect_industry.js") as f:
        js = f.read().replace("'__CODE__'", f"'{code}'")
    
    page.evaluate(js)
    page.wait_for_load_state("networkidle")  # 리로드 대기

def judge_product_with_claude(audit_result: dict) -> dict:
    """Sonnet으로 판단. 브라우저 접속 없음."""
    prompt = f"""
상품명: {audit_result['n']}
체크수: {audit_result['cnt']}
업종미연결: {audit_result['e']}
업종별 공간 상세: {json.dumps(audit_result.get('detail', {}), ensure_ascii=False)}

이 상품의 공간 체크 상태가 정상인지 과태깅인지 판단해서 JSON으로만 반환.
형식: {{"judgment": "정상|과태깅(수정필요)|업종미연결|판단불가", "reason": "한 줄 이유"}}
"""
    result = call_sonnet(prompt, SONNET_JUDGMENT_SYSTEM)
    return json.loads(result)

# 메인 플로우
def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # 기존 세션 재사용 (로그인 유지)
        ctx = browser.new_context(storage_state="session.json")
        page = ctx.new_page()

        rgr_list = load_rgr_list("data/rgr_list.json")
        results = []

        for rgr in rgr_list:
            # 1단계: 감사 (Playwright 직접 실행, Claude 불필요)
            audit = audit_product(page, rgr)
            
            # 2단계: 라우팅
            route = route_product(audit)
            
            if route == "industry_connector":
                # Playwright로 9업종 연결 (Claude 불필요)
                for code in ["01","02","03","04","05","06","07","08","09"]:
                    connect_industry(page, rgr, code)
            
            elif route == "judgment_sonnet":
                # Claude Sonnet으로 판단
                judgment = judge_product_with_claude(audit)
                if needs_opus_review(judgment):
                    # Opus에 에스컬레이션
                    judgment = escalate_to_opus(audit, judgment)
                results.append({**audit, "rgr": rgr, **judgment})
            
            save_progress(rgr, results)

        generate_excel_report(results, "data/results/report.xlsx")

if __name__ == "__main__":
    main()
```

---

## 7. 비용 시뮬레이션 (288개 기준)

| 단계 | 모델 | 예상 토큰 | 캐싱 적용 | 예상 비용 |
|------|------|-----------|-----------|-----------|
| 감사 288개 | Haiku | 1M input | 90% 캐시 | ~$0.13 |
| 판단 ~100개 | Sonnet | 300K input | 80% 캐시 | ~$0.18 |
| Excel 생성 1회 | Sonnet | 50K input | — | ~$0.02 |
| Opus 예외 ~10개 | Opus | 100K input | — | ~$1.50 |
| **합계** | | | | **~$1.83** |

Opus 단일로 돌렸을 때의 $50~100 대비 **약 1/30 수준**.

---

## 8. 세션 관리 (로그인 유지)

```python
# 최초 1회: 수동 로그인 후 세션 저장
def save_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto("https://ad.hanasm.kr/")
        input("로그인 완료 후 엔터 누르세요...")  # 수동 로그인
        ctx.storage_state(path="session.json")
        print("세션 저장 완료")

# 이후: session.json 재사용
ctx = browser.new_context(storage_state="session.json")
```

---

## 9. 진행 상태 관리 (중단/재시작)

```python
# 체크포인트 저장
def save_progress(last_rgr: str, results: list):
    with open("data/progress.json", "w") as f:
        json.dump({"last": last_rgr, "done": len(results)}, f)

# 재시작 시 이어서
def load_checkpoint(rgr_list: list) -> list:
    try:
        with open("data/progress.json") as f:
            prog = json.load(f)
        last_idx = next((i for i,r in enumerate(rgr_list) if r == prog["last"]), 0)
        return rgr_list[last_idx+1:]
    except FileNotFoundError:
        return rgr_list
```
