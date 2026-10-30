#!/bin/bash
# 2026-10-15에 시작한 "AI 브리핑 인용 감소" 2주 관찰 기간이 끝난 뒤, 사용자에게 묻지 않고
# 알아서 점검하고 필요하면 바로 고치라는 지시(2026-10-15)에 따라 1회성으로 실행되는 스크립트.
# launchd가 2026-10-29 저녁에 한 번만 호출한다.

set -uo pipefail

PROJECT_DIR="/Users/eomzic/Desktop/claude"
LOG_DIR="$PROJECT_DIR/blog/logs"
mkdir -p "$LOG_DIR"
cd "$PROJECT_DIR" || exit 1

export PATH="/usr/local/bin:/opt/homebrew/bin:$HOME/.nvm/versions/node/v24.14.0/bin:$PATH"

LOGFILE="$LOG_DIR/review_citation_fix_$(date +%Y%m%d_%H%M%S).log"

PROMPT='2026-10-15에 "블로그 게시물이 네이버 AI 브리핑에 인용되는 횟수가 줄었다"는 문제를 조사해서 원인 2가지를 찾아 고쳤다: (1) 하루 2회(국장+미장)였던 자동 발행을 하루 1회(국장만)로 줄임, (2) blog/guides/style-guide.md를 v5로 갱신해서 인사말/마무리의 숨은 반복 공식(예상→반전 구조, "솔직히 ~한데요 저는 일단 ~하려고요" 구조, 마무리 이모지 100% 고정)을 금지함. 사용자가 "2주간 이대로 발행해보고, 점검해서 문제 있으면 그때 수정하자. 묻지 말고 알아서 점검하고 수정할 부분 있으면 알아서 수정해"라고 명시적으로 지시했다 (2026-10-15).

오늘이 그 2주 관찰 기간이 끝나는 시점이다. 사람에게 묻지 말고 아래를 스스로 수행해라:

1. blog/output/ 아래 2026-10-15 이후 발행된 글들(주로 국장정리)을 전부 열어서 다음을 점검해라:
   - 인사말/마무리가 여전히 특정 틀을 반복하고 있는지 (3편 이상 연속으로 비슷한 구조면 문제)
   - 마무리 이모지가 여전히 특정 이모지 하나로 고정돼있는지
   - 섹션 순서/개수가 매번 똑같이 고정돼있는지
   - 이미지 썸네일 팔레트/레이아웃이 실제로 로테이션되고 있는지 (images/thumbnail.png들을 비교)
   - 발행 빈도가 실제로 하루 1회로 유지됐는지 (blog/logs/, launchd 상태 확인)
2. 문제를 발견하면, 사람에게 승인을 구하지 말고 바로 고쳐라 — style-guide.md/image-guide.md 추가 수정, 필요하면 발행 빈도/스케줄 재조정(launchctl, plist 파일) 등. blog/CLAUDE.md에 이번 점검 결과와 조치 내용을 날짜와 함께 기록해라.
3. 문제가 없었다면 "문제 없음, 현재 설정 유지"라고 blog/CLAUDE.md에 짧게 기록해라.
4. 마지막에 PushNotification으로 점검 결과를 한 줄로 요약해서 보내라 (문제 발견+수정 여부, 또는 이상 없음).

이 실행은 launchd로 자동 실행된 무인(비대화형) 실행이니 확인 질문을 하지 말고 판단해서 끝까지 진행해라.'

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') review_citation_fix.sh start ==="
  claude -p "$PROMPT" \
    --allowedTools "Bash Read Write Edit WebSearch WebFetch Agent PushNotification" \
    --add-dir "$PROJECT_DIR"
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') review_citation_fix.sh end (exit=$?) ==="
} >> "$LOGFILE" 2>&1
