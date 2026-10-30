#!/bin/bash
# 국장/미장 정리를 자동으로 리서치→글쓰기→이미지→조립→발행까지 진행시키는 launchd용 래퍼.
# launchd가 국장은 평일(월~금) 16:00에, 미장은 화~토 07:00에 이 스크립트를 호출한다.
# 미장이 화~토인 이유: 미국 정규장은 월~금에 열리고, 그 마감을 다음날 아침(한국시간)에
# 다루므로 월요일 마감은 화요일 아침에, ... 금요일 마감은 토요일 아침에 다룬다. 월요일
# 아침엔 다룰 새 거래일이 없다(주말엔 미국장도 안 열림 — 금요일 마감은 이미 토요일에
# 다뤘음).
#
# 사용법: auto_publish.sh gukjang|mijang

set -uo pipefail

KIND="${1:-}"
if [[ "$KIND" != "gukjang" && "$KIND" != "mijang" ]]; then
  echo "usage: auto_publish.sh gukjang|mijang" >&2
  exit 1
fi

PROJECT_DIR="/Users/eomzic/Desktop/claude"
LOG_DIR="$PROJECT_DIR/blog/logs"
mkdir -p "$LOG_DIR"

cd "$PROJECT_DIR" || exit 1

# PATH가 launchd 환경엔 최소한만 잡혀있어서 claude/node/python3 등을 못 찾는 경우가 있다.
export PATH="/usr/local/bin:/opt/homebrew/bin:$HOME/.nvm/versions/node/v24.14.0/bin:$PATH"

if [[ "$KIND" == "gukjang" ]]; then
  LABEL_DATE=$(date +%-m.%-d)
  TOPIC="${LABEL_DATE} 국장 정리"
  FOLDER="${LABEL_DATE}국장정리"
else
  # 미장은 "어제 마감한 미국 정규장"을 다룬다. 스케줄 자체가 화~토 07시로 걸려있어서
  # (launchd plist 참고) 실행되는 날은 항상 전날이 실제 미국 거래일이다 — 별도 요일
  # 분기 없이 그냥 1일 전으로 계산하면 된다.
  LABEL_DATE=$(date -v-1d +%-m.%-d)
  TOPIC="${LABEL_DATE} 미장 정리"
  FOLDER="${LABEL_DATE}미장정리"
fi

LOGFILE="$LOG_DIR/${FOLDER}_$(date +%Y%m%d_%H%M%S).log"

PROMPT="주제:
-${TOPIC}

이 요청은 launchd로 자동 실행된 무인(비대화형) 실행이다. 사람이 답할 수 없으니 확인 질문을 하지 말고, CLAUDE.md/blog/CLAUDE.md에 정의된 절차(리서치 → 글쓰기 → 이미지 → 조립 → 발행)를 판단 하에 끝까지 진행해라.

지켜야 할 것:
- 산출 폴더는 정확히 blog/output/${FOLDER}/ 로 만들어라.
- 리서치 단계에서 해당 날짜에 실제로 시장이 열렸는지(공휴일 등으로 휴장이 아니었는지) 먼저 확인해라. 만약 실제로는 더 이전 거래일 데이터를 다뤄야 하는 상황이면(예: 추석처럼 연휴로 최근 거래일이 다른 날짜인 경우), 리서치·글 내용에서 이를 명확히 밝히고 실제 거래일 기준으로 내용을 작성해라 — 폴더명/제목의 날짜 라벨은 이미 정한 대로 유지하되 본문에서 사실을 정확히 밝히면 된다.
- 발행(publisher) 단계 진입 전에 blog/.auth/chrome_profile/ 기반 세션이 실제로 유효한지 확인해라(예: headless로 blog.naver.com/eomzic_?Redirect=Write 접속 후 nid.naver.com으로 리다이렉트되는지 체크). 세션이 죽어있으면 로그인을 대신 시도하지 말고, PushNotification 도구로 사용자에게 짧게 '${TOPIC} 자동 발행 실패 - 네이버 재로그인 필요 (python3 blog/scripts/publish_naver.py --login)' 같은 메시지를 보낸 뒤 작업을 중단해라.
- 발행까지 정상적으로 끝나면 PushNotification으로 '${TOPIC} 자동 발행 완료' 같은 짧은 완료 알림을 보내라. 실패(리서치 실패, 발행 스크립트 에러 등)해도 마찬가지로 무엇이 실패했는지 짧게 PushNotification을 보내라 — 무인 실행이라 사용자가 로그를 안 볼 수도 있으니 성공이든 실패든 결과를 반드시 알려야 한다.
- 이미지 생성, Playwright 캡처, 파일 쓰기 등은 모두 판단해서 자율적으로 진행해라(승인 대기 없이)."

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') auto_publish.sh $KIND start (topic: $TOPIC) ==="
  claude -p "$PROMPT" \
    --allowedTools "Bash Read Write Edit WebSearch WebFetch Agent PushNotification" \
    --add-dir "$PROJECT_DIR"
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') auto_publish.sh $KIND end (exit=$?) ==="
} >> "$LOGFILE" 2>&1
