#!/bin/bash
# 대형기업 실적발표 자동 감지 + 블로그 작성/발행 래퍼.
# launchd가 평일 08:00에 이 스크립트를 호출한다.
#
# 완벽한 실시간 감지가 아니라(정확한 실적 캘린더 API는 대부분 유료), 매일 아침
# WebSearch로 "최근 1~2일 내 실적발표했는지"를 워치리스트 종목마다 확인하는 방식이다.
# 발표~감지 사이 최대 하루 정도 지연이 있을 수 있다는 한계가 있다.

set -uo pipefail

PROJECT_DIR="/Users/eomzic/Desktop/claude"
LOG_DIR="$PROJECT_DIR/blog/logs"
mkdir -p "$LOG_DIR"
cd "$PROJECT_DIR" || exit 1

export PATH="/usr/local/bin:/opt/homebrew/bin:$HOME/.nvm/versions/node/v24.14.0/bin:$PATH"

TODAY=$(date +%Y%m%d_%H%M%S)
LOGFILE="$LOG_DIR/auto_earnings_${TODAY}.log"

WATCHLIST="삼성전자, SK하이닉스, 두산로보틱스, 오라클(ORCL), 마이크론(MU), 엔비디아(NVDA), TSMC(TSM), 애플(AAPL), 마이크로소프트(MSFT), 아마존(AMZN), 알파벳/구글(GOOGL), 메타(META), 테슬라(TSLA)"

PROMPT="이 요청은 launchd로 자동 실행된 무인(비대화형) 실행이다. 사람이 답할 수 없으니 확인 질문을 하지 말고 판단해서 끝까지 진행해라.

목적: 아래 워치리스트 종목 중 최근 1~2일 내(오늘 또는 어제) 분기/연간 실적을 발표한 곳이 있으면, 블로그에 실적발표 정리 글을 자동으로 작성·발행한다.

워치리스트: ${WATCHLIST}

절차:
1. 워치리스트 종목 각각에 대해 WebSearch로 '[종목명] 실적발표 [오늘 날짜 근처]' 식으로 검색해서, 최근 1~2일 내에 분기/연간 실적을 실제로 발표했는지 확인해라. 예정(미래) 발표는 대상이 아니다 — 이미 발표된 것만 다룬다.
2. 발표를 확인했으면, blog/output/ 아래 그 종목·분기를 이미 다룬 폴더가 있는지 먼저 확인해라(예: 폴더명에 종목명+분기 정보가 들어간 기존 폴더). 이미 있으면 중복 작성하지 말고 건너뛴다.
3. 새로 다뤄야 할 실적발표가 있으면, CLAUDE.md/blog/CLAUDE.md에 정의된 절차(리서치 → 글쓰기 → 이미지 → 조립 → 발행)를 그대로 따라 진행해라. 과거 실적발표 글 사례(예: blog/output/3분기_마이크론_실적발표/, blog/output/2분기_구글_실적발표/ 등이 있으면)를 참고해서 톤/구성을 맞춰라.
   - 산출 폴더명에 반드시 '실적발표'라는 단어를 포함시켜라(예: 'SK하이닉스_3분기_실적발표') — publish_naver.py가 이 키워드로 카테고리를 '실적발표'로 자동 분류한다.
   - 회계분기 표기(예: FY vs 캘린더 분기)가 실제 기업 발표와 다를 수 있으니 리서치 단계에서 정확한 표기를 직접 확인해라(마이크론 케이스에서 '3분기'로 요청했지만 실제로는 FY2026 4분기였던 사례가 있었다).
   - 보유 종목(삼성전자·두산로보틱스·오라클)의 실적이면 실제 보유 사실과 자연스럽게 연결해라. 다른 종목(SK하이닉스·엔비디아 등) 실적이어도 그게 보유 종목(삼성전자 등)에 미치는 영향이 있으면 언급해라(과거 마이크론 실적 글에서 삼성전자·SK하이닉스 반응을 다룬 선례 참고).
   - 발행 전 blog/.auth/chrome_profile/ 기반 네이버 세션이 유효한지 headless로 확인해라(blog.naver.com/eomzic_?Redirect=Write 접속 후 nid.naver.com으로 리다이렉트되는지). 세션이 죽어있으면 로그인을 대신 시도하지 말고 PushNotification으로 '[종목명] 실적발표 글 자동 작성 완료, 발행만 세션 만료로 대기 중 - 재로그인 필요'라고 알린 뒤 그 종목은 건너뛰고 다음 종목 확인으로 넘어가라(발행 안 된 글의 산출물은 그대로 남겨둔다).
   - 같은 날 여러 종목이 발표됐으면 종목별로 각각 별도 글을 순서대로 작성·발행해라.
4. 발표된 종목이 하나도 없으면(흔한 경우일 것이다) 아무 글도 쓰지 말고, 조용히 종료해라 — 매일 '없음' 알림을 보내면 피로감만 준다. 단, 확인 과정에서 에러(WebSearch 실패 등)가 있었으면 그건 알려라.
5. 실제로 글을 작성·발행했으면 PushNotification으로 어떤 종목의 실적발표 글이 발행(또는 세션 문제로 대기 중)됐는지 짧게 알려라."

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') auto_earnings.sh start ==="
  claude -p "$PROMPT" \
    --allowedTools "Bash Read Write Edit WebSearch WebFetch Agent PushNotification" \
    --add-dir "$PROJECT_DIR"
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') auto_earnings.sh end (exit=$?) ==="
} >> "$LOGFILE" 2>&1
