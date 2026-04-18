#!/usr/bin/env bash
# ============================================================================
# sync_memory.sh — 하나사인몰 auto-memory ↔ GitHub 양방향 동기화
# ----------------------------------------------------------------------------
# 리포:   https://github.com/sangjunepark-beep/naver-ad-agent-guide
# 경로:   memory/*.md (GitHub) ↔ .auto-memory/*.md (Cowork 세션)
#
# 사용법:
#   PULL (GitHub → 로컬):   bash sync_memory.sh pull
#   PUSH (로컬 → GitHub):   GH_TOKEN=ghp_xxx bash sync_memory.sh push
#   CHECK (상태 비교):      bash sync_memory.sh check
#
# 주의:
#   - PULL은 리포가 Public 상태이거나 PAT가 있을 때만 동작
#   - PUSH는 반드시 PAT 필요 (GH_TOKEN 환경변수로 주입)
#   - PAT를 스크립트에 하드코딩 금지 (노출 리스크)
# ============================================================================

set -euo pipefail

REPO_OWNER="sangjunepark-beep"
REPO_NAME="naver-ad-agent-guide"
BRANCH="main"
REMOTE_DIR="memory"

# 로컬 .auto-memory 경로 자동 탐색 (세션명 가변 대응)
LOCAL_DIR=""
for candidate in /sessions/*/mnt/.auto-memory; do
  if [ -d "$candidate" ]; then
    LOCAL_DIR="$candidate"
    break
  fi
done

if [ -z "$LOCAL_DIR" ]; then
  echo "[ERROR] .auto-memory 폴더를 찾을 수 없습니다." >&2
  exit 1
fi

# 관리 대상 파일 15개
FILES=(
  MEMORY.md
  feedback_decision_and_token_confirmation.md
  feedback_gsheet_query_date_fix.md
  feedback_hanasignmall_cs_offline_conversion.md
  feedback_model_mix_and_context.md
  feedback_n8n_json_import.md
  project_01sheet_structure_change.md
  project_name_change.md
  project_naver_ad_conversion_inflation.md
  project_naver_shopping_ad_api_quirks.md
  project_overall_progress.md
  project_phase35_done.md
  project_phase3_import_done.md
  project_phase4_done.md
  reference_n8n_workflows.md
  project_home_pc_migration.md
  reference_n8n_api_key.md
  project_phase5_done.md
  project_product_mapping_done.md
)

CMD="${1:-}"

# ----------------------------------------------------------------------------
# PULL: GitHub → 로컬
# ----------------------------------------------------------------------------
pull_files() {
  echo "[PULL] GitHub → $LOCAL_DIR"
  local base="https://raw.githubusercontent.com/$REPO_OWNER/$REPO_NAME/$BRANCH/$REMOTE_DIR"
  local ok=0 fail=0

  for f in "${FILES[@]}"; do
    local tmp="$LOCAL_DIR/.tmp_$f"
    local code
    code=$(curl -s -o "$tmp" -w "%{http_code}" \
      ${GH_TOKEN:+-H "Authorization: token $GH_TOKEN"} \
      "$base/$f")

    if [ "$code" = "200" ] && [ -s "$tmp" ]; then
      mv "$tmp" "$LOCAL_DIR/$f"
      printf "  [OK]   %s\n" "$f"
      ok=$((ok+1))
    else
      rm -f "$tmp"
      printf "  [FAIL] %s (HTTP %s)\n" "$f" "$code"
      fail=$((fail+1))
    fi
  done

  echo "---"
  echo "완료: 성공 $ok / 실패 $fail"
}

# ----------------------------------------------------------------------------
# PUSH: 로컬 → GitHub (PAT 필수)
# ----------------------------------------------------------------------------
push_files() {
  if [ -z "${GH_TOKEN:-}" ]; then
    echo "[ERROR] GH_TOKEN 환경변수가 필요합니다." >&2
    echo "        예: GH_TOKEN=ghp_xxx bash sync_memory.sh push" >&2
    exit 1
  fi

  echo "[PUSH] $LOCAL_DIR → GitHub"
  local api="https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/contents/$REMOTE_DIR"
  local ok=0 fail=0 skip=0
  local ts
  ts=$(date +"%Y-%m-%d %H:%M")

  for f in "${FILES[@]}"; do
    local local_file="$LOCAL_DIR/$f"
    if [ ! -f "$local_file" ]; then
      printf "  [SKIP] %s (로컬 없음)\n" "$f"
      skip=$((skip+1))
      continue
    fi

    # 현재 SHA 조회 (업데이트용)
    local sha
    sha=$(curl -s -H "Authorization: token $GH_TOKEN" \
      "$api/$f?ref=$BRANCH" | grep -o '"sha":"[^"]*"' | head -1 | cut -d'"' -f4)

    # 로컬 파일 base64 인코딩
    local content_b64
    content_b64=$(base64 -w 0 "$local_file")

    # PUT 요청 페이로드
    local payload
    if [ -n "$sha" ]; then
      payload=$(printf '{"message":"sync: %s (%s)","content":"%s","branch":"%s","sha":"%s"}' \
        "$f" "$ts" "$content_b64" "$BRANCH" "$sha")
    else
      payload=$(printf '{"message":"add: %s (%s)","content":"%s","branch":"%s"}' \
        "$f" "$ts" "$content_b64" "$BRANCH")
    fi

    local http_code
    http_code=$(curl -s -o /tmp/gh_resp.json -w "%{http_code}" \
      -X PUT \
      -H "Authorization: token $GH_TOKEN" \
      -H "Content-Type: application/json" \
      -d "$payload" \
      "$api/$f")

    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
      printf "  [OK]   %s\n" "$f"
      ok=$((ok+1))
    else
      printf "  [FAIL] %s (HTTP %s)\n" "$f" "$http_code"
      fail=$((fail+1))
    fi
  done

  echo "---"
  echo "완료: 성공 $ok / 실패 $fail / 스킵 $skip"
}

# ----------------------------------------------------------------------------
# CHECK: 로컬 vs 리모트 상태 비교 (수정시각/사이즈만 대강)
# ----------------------------------------------------------------------------
check_status() {
  echo "[CHECK] 로컬 파일 현황: $LOCAL_DIR"
  local count=0 total_size=0
  for f in "${FILES[@]}"; do
    if [ -f "$LOCAL_DIR/$f" ]; then
      local size
      size=$(wc -c < "$LOCAL_DIR/$f")
      total_size=$((total_size + size))
      count=$((count + 1))
      printf "  [OK]   %-55s %6d bytes\n" "$f" "$size"
    else
      printf "  [MISS] %s\n" "$f"
    fi
  done
  echo "---"
  echo "파일: $count / 15    총 $total_size bytes"
}

# ----------------------------------------------------------------------------
# 디스패치
# ----------------------------------------------------------------------------
case "$CMD" in
  pull)  pull_files ;;
  push)  push_files ;;
  check) check_status ;;
  *)
    cat <<EOF
사용법:
  bash sync_memory.sh pull              # GitHub → 로컬 (15개 덮어쓰기)
  GH_TOKEN=ghp_xxx sync_memory.sh push  # 로컬 → GitHub (PAT 필수)
  bash sync_memory.sh check             # 로컬 파일 상태 점검

리포:   https://github.com/$REPO_OWNER/$REPO_NAME
로컬:   $LOCAL_DIR
대상:   ${#FILES[@]}개 파일
EOF
    exit 1
    ;;
esac
