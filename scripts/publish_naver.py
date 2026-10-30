#!/usr/bin/env python3
"""
네이버 블로그 자동 발행 스크립트.

publisher 에이전트(agents/publisher.md)가 이 스크립트를 호출한다.
직접 실행할 때는 아래 순서로 사용한다.

1) 최초 1회, 로그인 세션 생성 (브라우저 창에서 직접 로그인 후 터미널에서 Enter):
     python3 publish_naver.py --login

2) 에디터 화면 구조 진단 (발행하지 않음 — 선택자 보정용):
     python3 publish_naver.py --inspect

3) 실제 글 작성 (기본은 입력만 하고 발행 버튼은 누르지 않음):
     python3 publish_naver.py output/9.9국장정리

4) 실제 발행까지:
     python3 publish_naver.py output/9.9국장정리 --publish

5) 예약 발행 시각을 직접 지정 (기본 "다음 정시로 올림" 대신):
     python3 publish_naver.py output/9.9국장정리 --publish --at "2026-09-19 10:00"

**주의 (2026-10-30 추가)**: 짧은 기간에 --login을 반복하면 네이버가 "ID 안전 조치"
(비정상 로그인 탐지)로 계정을 잠근 사고가 실제로 있었다. --login은 하루 한 번 정도로만
쓰고, 세션이 아직 살아있을 가능성이 있으면(예: 몇 시간 전에 썼다면) 먼저 --publish를
그냥 시도해보고 "세션 만료" 에러가 날 때만 --login을 하는 식으로 아껴 쓸 것. (CDP로
사용자의 실제 Chrome에 붙는 방식을 시도했었지만, Chrome이 2025년부터 기본 로그인 프로필에
대한 원격 디버깅을 보안상 차단해서 되돌렸다 — 자세한 경위는 blog/CLAUDE.md 참고.)

입력: output/[주제]/final.html 안의 <div id="post-title">, <div id="post-body">
(assembler.md 스펙 — 이 두 id가 없으면 실행되지 않는다)

카테고리는 주제 폴더 이름(국장/미장/실적발표/포트폴리오 키워드)에서 자동 판별하고,
발행 시간은 --at이 없으면 항상 "다음 정시로 올림"으로 예약 발행한다 (정시에 이미 걸쳐 있으면 즉시 발행).
"""
import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

BLOG_ID = "eomzic_"
ROOT = Path(__file__).resolve().parent.parent
AUTH_DIR = ROOT / ".auth"
PROFILE_DIR = AUTH_DIR / "chrome_profile"
SCRIPTS_DIR = Path(__file__).resolve().parent
SELECTORS_PATH = SCRIPTS_DIR / "naver_selectors.json"

# 주제 폴더 이름에 이 키워드가 있으면 해당 네이버 블로그 카테고리로 자동 분류한다.
# 순서대로 검사하며 먼저 매치되는 규칙을 사용한다.
CATEGORY_RULES = [
    (re.compile("국장|미장"), "시황"),
    (re.compile("실적발표"), "실적발표"),
    (re.compile("포트폴리오"), "주식"),
]

DEFAULT_SELECTORS = {
    "editor_iframe": "iframe#mainFrame",
    "title": None,
    "body": None,
    "photo_button": None,
    "publish_open_button": None,
    "publish_confirm_button": None,
    "category_dropdown_button": None,
    "category_option_item": None,
    "schedule_radio_label": None,
    "schedule_date_input": None,
    "schedule_hour_select": None,
    "schedule_minute_select": None,
    "calendar_next_month_button": None,
    "calendar_day_cell": None,
}


def load_selectors() -> dict:
    if SELECTORS_PATH.exists():
        return json.loads(SELECTORS_PATH.read_text(encoding="utf-8"))
    return dict(DEFAULT_SELECTORS)


def parse_final_html(topic_dir: Path):
    """final.html을 읽어 (제목 텍스트, 본문 세그먼트 리스트)를 반환한다.

    본문 세그먼트는 ("html", html_string) 또는 ("image", 로컬 절대경로) 튜플의 순서 있는 리스트.
    네이버 에디터는 클립보드로 붙여넣은 HTML 안의 data: URI 이미지를
    "허용되지 않는 형식"으로 거부하므로, 이미지는 별도로 실제 파일 업로드(사진 추가 버튼 +
    파일 선택창)로 삽입해야 한다 — 그래서 텍스트/이미지를 문서 순서대로 분리해둔다."""
    final_html_path = topic_dir / "final.html"
    if not final_html_path.exists():
        sys.exit(f"final.html이 없습니다: {final_html_path}")

    soup = BeautifulSoup(final_html_path.read_text(encoding="utf-8"), "html.parser")

    title_el = soup.find(id="post-title")
    body_el = soup.find(id="post-body")
    if title_el is None:
        sys.exit('final.html에서 id="post-title"을 찾지 못했습니다. assembler.md 스펙을 확인하세요.')
    if body_el is None:
        sys.exit('final.html에서 id="post-body"를 찾지 못했습니다. assembler.md 스펙을 확인하세요.')

    title_text = title_el.get_text(strip=True)

    segments = []
    buffer = []

    def flush():
        html = "".join(str(c) for c in buffer)
        if html.strip():
            segments.append(("html", html))
        buffer.clear()

    for child in body_el.contents:
        if getattr(child, "name", None) == "img":
            flush()
            src = child.get("src", "")
            if re.match(r"^https?:", src):
                sys.exit(
                    f"외부 URL 이미지는 아직 지원하지 않습니다 (자동 업로드 대상이 아님): {src}\n"
                    "assembler가 만든 이미지를 output/[주제]/images/에 로컬 파일로 넣고 상대경로로 참조해야 합니다."
                )
            abs_path = (topic_dir / src).resolve()
            if not abs_path.exists():
                sys.exit(f"이미지 파일을 찾을 수 없습니다: {abs_path}")
            segments.append(("image", str(abs_path)))
        else:
            buffer.append(child)
    flush()

    return title_text, segments


def infer_category(topic_name: str):
    """주제 폴더 이름에서 CATEGORY_RULES에 맞는 네이버 블로그 카테고리를 판별한다.
    매치되는 규칙이 없으면 None을 반환 (이 경우 에디터의 기본/마지막 사용 카테고리가 유지된다)."""
    for pattern, category in CATEGORY_RULES:
        if pattern.search(topic_name):
            return category
    return None


def compute_target_time(now: datetime) -> datetime:
    """발행 예약 시각을 계산한다: 다음 정시로 올림 (정각이면 그 시각 그대로)."""
    floor_hour = now.replace(minute=0, second=0, microsecond=0)
    if now == floor_hour:
        return floor_hour
    return floor_hour + timedelta(hours=1)


def ensure_login(playwright, interactive: bool):
    """로그인 세션을 준비한다.

    예전엔 쿠키만 storage_state JSON으로 저장했다가 매번 새 브라우저에 주입하는
    방식이었는데, 세션이 거의 매일(길어야 10시간 정도) 끊기는 문제가 계속 반복됐다.
    쿠키 값 자체는 남아있어도 서버 쪽에서 무효화된 상태였다 — 매번 "새 브라우저에
    쿠키만 이식받는" 형태라 네이버 쪽에서 낯선 기기로 봤을 가능성, 그리고 정상 사용
    중 네이버가 세션을 갱신해도 그 갱신분이 스냅샷 방식이라 다음 실행에 반영이 안 됐을
    가능성이 있다. 그래서 쿠키만 따로 관리하지 않고, 브라우저 프로필 전체(쿠키+로컬
    스토리지+캐시 등)를 디스크에 그대로 유지하는 영속 프로필(persistent context)로
    바꿨다 — 매번 같은 브라우저로 돌아오는 것처럼 보이게 하고, 실행 중 발생하는 세션
    갱신도 프로필에 자동으로 반영되게 하기 위함이다.

    (2026-10-30: 사용자의 실제 Chrome에 CDP로 접속하는 방식을 시도했었지만, Chrome이
    기본 로그인 프로필에 대한 원격 디버깅을 보안상 차단해서 이 방식으로 되돌렸다. 대신
    --login을 짧은 기간에 반복하면 네이버 "ID 안전 조치"에 걸릴 수 있으니 아껴 써야
    한다 — 위 모듈 docstring의 "주의" 참고.)

    interactive=False (기본 실행/--inspect)일 때는 세션이 없거나 무효해도
    절대 자동으로 로그인 흐름에 들어가지 않는다 — 비대화형(Bash 자동 실행 등) 환경에서
    input()이 즉시 통과되어 빈 세션으로 기존 로그인 상태를 덮어쓰는 사고를 막기 위함.
    이 경우 사용자가 `--login`을 직접 실행하도록 안내하고 종료한다.

    interactive=True (--login 플래그)일 때만 실제 로그인 흐름을 탄다."""
    AUTH_DIR.mkdir(exist_ok=True)
    profile_existed = PROFILE_DIR.exists()

    # 2026-10-30: "ID 안전 조치"가 반복되다가 로그인마다 비밀번호 변경을 요구하는
    # 수준으로 악화됐다 — Playwright 기본 Chromium이 navigator.webdriver=true를
    # 그대로 노출하고, 버전도 사용자의 실제 Chrome(156)보다 한참 뒤(148, "for Testing"
    # 빌드)라서 네이버가 "자동화된 낯선 브라우저"로 더 강하게 의심했을 가능성이 있다.
    # 자동화 흔적(navigator.webdriver)을 지우고, 실제 쓰는 Chrome과 비슷한 User-Agent를
    # 줘서 최대한 평범한 브라우저처럼 보이게 한다. (CDP로 실제 Chrome에 붙는 방식은
    # Chrome 자체의 보안 정책으로 막혀서 이미 시도 후 되돌렸다 — 위 docstring 참고.)
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"
        ),
    )
    context.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
    )

    if profile_existed:
        # NID_AUT/NID_SES(실제 접근 권한 쿠키)는 "로그인 상태 유지"를 체크해도
        # session-only라서, 브라우저를 완전히 새 프로세스로 재시작하면(=매번 CLI를
        # 새로 실행하는 이 스크립트의 구조) 거의 바로 사라진다. 대신 NID_SAUTO(자동
        # 재로그인 토큰)는 살아남는데, 이게 NID_AUT/NID_SES를 조용히 재발급하는 건
        # nid.naver.com 로그인 엔드포인트를 거칠 때뿐이다 — 에디터 URL로 바로 들어가면
        # 그 재발급 기회 자체가 없어서 "세션 만료"로 오판하고 매번 재로그인을 요구하는
        # 문제가 있었다. 그래서 바로 에디터로 가지 않고 로그인 엔드포인트를 먼저 들러
        # NID_SAUTO로 조용한 재인증이 일어날 기회를 준 다음, 실제로 발행 때 쓰는 것과
        # 동일한 진입점(에디터 리다이렉트 URL)으로 이동해서 로그인 페이지로 튕기는지를
        # 확인한다. (쿠키 존재 여부나 "로그인" 링크 유무로 판단하는 방식은 전부 오탐이
        # 확인된 바 있다 — 죽은 세션을 "재사용 가능"으로 오판해서 실제 로그인을 건너뛰는
        # 사고가 반복됨.)
        probe = context.new_page()
        probe.goto("https://nid.naver.com/nidlogin.login", wait_until="domcontentloaded")
        probe.wait_for_timeout(1500)
        probe.goto(f"https://blog.naver.com/{BLOG_ID}?Redirect=Write", wait_until="domcontentloaded")
        probe.wait_for_timeout(2000)
        session_alive = "nid.naver.com" not in probe.url
        probe.close()
        if session_alive:
            print("기존 로그인 세션을 재사용합니다.")
            return context
        print("저장된 프로필이 있지만 네이버 서버에서 세션이 만료된 상태입니다.")

    if not interactive:
        context.close()
        sys.exit(
            "로그인 세션이 없거나 유효하지 않습니다.\n"
            "터미널에서 아래 명령을 직접 실행해서 로그인해주세요 (자동화 스크립트가 대신 로그인하지 않습니다):\n"
            "  python3 blog/scripts/publish_naver.py --login"
        )

    page = context.new_page()
    page.goto("https://nid.naver.com/nidlogin.login", wait_until="domcontentloaded")

    # "로그인 상태 유지" 체크박스를 미리 켜둔다. 자격증명은 전혀 건드리지 않는
    # 순수 UI 옵션이라 자동으로 체크해도 안전하다.
    try:
        stay_checkbox = page.locator("#loginStay")
        if stay_checkbox.count() > 0 and not stay_checkbox.is_checked():
            stay_checkbox.check(timeout=2000)
    except PWTimeout:
        pass

    print("\n열린 브라우저 창에서 네이버에 직접 로그인해주세요 (2단계 인증 포함).")
    print("(\"로그인 상태 유지\"는 세션을 오래 유지하기 위해 미리 체크해뒀습니다.)")
    input("로그인을 완료했으면 이 터미널에서 Enter를 누르세요...")

    live_cookies = {c["name"] for c in context.cookies() if "naver.com" in c.get("domain", "")}
    if "NID_AUT" not in live_cookies or "NID_SES" not in live_cookies:
        page.close()
        context.close()
        sys.exit(
            "로그인이 확인되지 않았습니다 (NID_AUT/NID_SES 쿠키 없음). "
            "종료합니다. 로그인을 완료한 뒤 다시 실행해주세요."
        )

    # 쿠키 체크 직후엔 분명히 NID_AUT/NID_SES가 있었는데도, 바로 이어서 context.close()하면
    # 디스크(영속 프로필의 쿠키 DB)에 다 안 쓰인 채로 날아가는 걸 실제로 겪었다 — 로그인
    # 직후 재확인하면 쿠키가 통째로 사라져 있었다. 닫기 전에 flush될 시간을 좀 준다.
    page.wait_for_timeout(2000)
    print(f"로그인 세션을 저장했습니다: {PROFILE_DIR}")
    page.close()
    return context


def dismiss_recovery_popup(page, frame, attempts: int = 8, interval_ms: int = 400):
    """"작성 중인 글이 있습니다. 이어서 작성하시겠습니까?" 임시저장 복구 팝업을 닫는다.
    렌더링이 비동기라 즉시 count()==0이어도 잠시 후 뜰 수 있으므로(실제로 겪음 —
    팝업의 se-popup-dim 오버레이가 화면 전체를 덮어 제목/본문/사진 버튼 클릭을 전부
    가로막았다), 짧은 간격으로 여러 번 재확인한다. 항상 "취소"를 눌러 새 글로 시작한다."""
    recovery_cancel = frame.locator(".se-popup-alert-confirm .se-popup-button-cancel")
    for _ in range(attempts):
        try:
            if recovery_cancel.count() > 0:
                recovery_cancel.first.click(timeout=2000)
                page.wait_for_timeout(400)
                return True
        except PWTimeout:
            pass
        page.wait_for_timeout(interval_ms)
    return False


def open_editor(context):
    page = context.new_page()
    page.goto(f"https://blog.naver.com/{BLOG_ID}", wait_until="domcontentloaded")

    try:
        page.get_by_role("link", name=re.compile("글쓰기")).first.click(timeout=5000)
    except PWTimeout:
        page.goto(f"https://blog.naver.com/{BLOG_ID}?Redirect=Write", wait_until="domcontentloaded")

    # 새 창으로 뜨는 경우 대응
    if len(context.pages) > 1:
        page = context.pages[-1]

    page.wait_for_selector("iframe#mainFrame", timeout=20000)
    frame = page.frame_locator("iframe#mainFrame")
    page.wait_for_timeout(1500)

    dismiss_recovery_popup(page, frame)

    # 도움말 패널이 열려 있으면 닫기 (열려있으면 발행 버튼 클릭 등을 가로챔)
    help_close = frame.locator(".se-help-panel-close-button")
    try:
        if help_close.count() > 0:
            help_close.first.click(timeout=3000)
            page.wait_for_timeout(300)
    except PWTimeout:
        pass

    return page, frame


def dump_editor_structure(page, frame):
    """진단용: 에디터 화면의 상호작용 가능 요소를 텍스트로 덤프 + 스크린샷."""
    js = """
    () => {
      const pick = el => ({
        tag: el.tagName,
        id: el.id || null,
        cls: (el.className && typeof el.className === 'string') ? el.className : null,
        role: el.getAttribute('role'),
        placeholder: el.getAttribute('placeholder') || el.getAttribute('data-placeholder'),
        text: (el.innerText || '').slice(0, 40),
        contentEditable: el.isContentEditable
      });
      const els = Array.from(document.querySelectorAll('[contenteditable], button, [role="button"], input, textarea, a'));
      return els.map(pick).filter(x => x.text || x.placeholder || x.contentEditable);
    }
    """
    frame_dump = frame.locator("body").evaluate(js)
    top_dump = page.evaluate(js)

    out = SCRIPTS_DIR / "editor_dump.json"
    out.write_text(
        json.dumps({"top_page": top_dump, "editor_iframe": frame_dump}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    shot = SCRIPTS_DIR / "editor_screenshot.png"
    page.screenshot(path=str(shot), full_page=True)
    return out, shot


def set_clipboard(page, html: str, text: str):
    page.evaluate(
        """
        async ([html, text]) => {
          const item = new ClipboardItem({
            'text/html': new Blob([html], {type: 'text/html'}),
            'text/plain': new Blob([text], {type: 'text/plain'})
          });
          await navigator.clipboard.write([item]);
        }
        """,
        [html, text],
    )


def paste_html(page, html: str):
    plain_text = re.sub(r"<[^>]+>", " ", html)
    set_clipboard(page, html, plain_text)
    page.keyboard.press("Meta+V")


def insert_image(page, frame, sel, image_path: str):
    """현재 커서 위치에 로컬 이미지 파일을 실제로 업로드해서 삽입한다.
    클립보드로 붙여넣은 HTML 안의 data: URI 이미지는 네이버 에디터가
    "허용되지 않는 형식"이라며 거부하므로, 반드시 '사진 추가' 버튼의
    네이티브 파일 선택창을 통해야 한다 (--inspect 보정 단계에서 확인됨)."""
    photo_btn = frame.locator(sel["photo_button"]).first
    photo_btn.wait_for(state="visible", timeout=5000)
    page.wait_for_timeout(300)

    # 클릭 자체는 성공해도 filechooser 이벤트가 안 뜨는 간헐적 타이밍 이슈가
    # 실제로 있었다(같은 셀렉터, 같은 흐름인데도 재현이 안 될 때가 있었음).
    # 좌표 클릭 등 다른 방식으로 우회하지 않고, 같은 문서화된 셀렉터로만 몇 번 더
    # 재시도한다.
    last_error = None
    for attempt in range(3):
        try:
            with page.expect_file_chooser(timeout=8000) as fc_info:
                photo_btn.click()
            fc_info.value.set_files(image_path)
            page.wait_for_timeout(1500)
            return
        except PWTimeout as e:
            last_error = e
            page.wait_for_timeout(800)
    raise last_error


def select_category(frame, sel, category_name: str):
    frame.locator(sel["category_dropdown_button"]).first.click()
    option = frame.locator(sel["category_option_item"], has_text=category_name)
    if option.count() == 0:
        sys.exit(f"카테고리 '{category_name}'을(를) 드롭다운에서 찾지 못했습니다. naver_selectors.json을 다시 보정해주세요.")
    option.first.click()


def select_schedule(page, frame, sel, target_dt: datetime, now: datetime):
    """발행 시간을 '예약'으로 전환하고 target_dt(항상 정시)로 설정한다."""
    frame.locator(sel["schedule_radio_label"]).click()

    if target_dt.date() != now.date():
        date_input = frame.locator(sel["schedule_date_input"])
        date_input.click()
        page.wait_for_timeout(400)
        if (target_dt.year, target_dt.month) != (now.year, now.month):
            frame.locator(sel["calendar_next_month_button"]).click()
            page.wait_for_timeout(300)
        day_cell = frame.locator(sel["calendar_day_cell"], has_text=re.compile(rf"^{target_dt.day}$"))
        day_cell.first.click()
        page.wait_for_timeout(300)

    frame.locator(sel["schedule_hour_select"]).select_option(f"{target_dt.hour:02d}")
    frame.locator(sel["schedule_minute_select"]).select_option("00")


def fill_and_publish(page, frame, sel, title_text, body_segments, topic_name, do_publish: bool, target_override=None):
    page.context.grant_permissions(["clipboard-read", "clipboard-write"], origin="https://blog.naver.com")

    # open_editor()에서 이미 한 번 처리하지만, 팝업이 그보다 늦게 떠서 여기서
    # 처음 마주치는 경우가 실제로 있었다 — 제목 입력 직전에 한 번 더 확인한다.
    dismiss_recovery_popup(page, frame, attempts=3)

    title_el = frame.locator(sel["title"]).first
    title_el.click()
    page.wait_for_timeout(400)
    paste_html(page, title_text)
    page.wait_for_timeout(300)

    body_el = frame.locator(sel["body"]).first
    body_el.click()
    page.wait_for_timeout(400)
    for kind, value in body_segments:
        if kind == "html":
            paste_html(page, value)
            page.wait_for_timeout(300)
        else:
            insert_image(page, frame, sel, value)

    if not do_publish:
        print("`--publish` 없이 실행되어 발행하지 않았습니다. 브라우저에서 직접 확인 후 필요하면 발행 버튼을 눌러주세요.")
        return None

    # 도움말 패널이 그 사이에 (다시) 떠서 발행 버튼 클릭을 가로챌 수 있다 —
    # open_editor()에서 한 번 닫아도 비동기로 나중에 뜨는 경우가 있었다(실제로 겪음).
    help_close = frame.locator(".se-help-panel-close-button")
    try:
        if help_close.count() > 0:
            help_close.first.click(timeout=3000)
            page.wait_for_timeout(300)
    except PWTimeout:
        pass

    frame.locator(sel["publish_open_button"]).first.click()
    page.wait_for_timeout(1000)

    category = infer_category(topic_name)
    if category:
        select_category(frame, sel, category)
        page.wait_for_timeout(300)
        print(f"카테고리: {category}")
    else:
        print(f"경고: '{topic_name}'에서 카테고리를 자동 판별하지 못했습니다 (국장/미장/실적발표/포트폴리오 키워드 없음) — 기본(마지막 사용) 카테고리로 발행됩니다.")

    now = datetime.now()
    target = target_override if target_override is not None else compute_target_time(now)
    # 값 설정 + 클릭에 걸리는 시간을 감안해, target이 "지금과 사실상 같은 시점"이면
    # 예약 대신 즉시 발행으로 처리한다 (그렇지 않으면 폼 제출 시점엔 이미 과거가 되어
    # 네이버 쪽 "현재 시간 이후로 설정해주세요" 검증에 걸릴 수 있다).
    if target - now > timedelta(seconds=45):
        select_schedule(page, frame, sel, target, now)
        page.wait_for_timeout(300)
        print(f"예약 발행 시각: {target.strftime('%Y-%m-%d %H:%M')}")
    else:
        print("정시에 걸려 있어 예약 대신 즉시 발행으로 진행합니다.")

    frame.locator(sel["publish_confirm_button"]).first.click()
    page.wait_for_timeout(2000)
    return page.url


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("topic_dir", nargs="?", help="output/[주제] 폴더 경로")
    parser.add_argument("--login", action="store_true", help="로그인 세션만 새로 만든다")
    parser.add_argument("--inspect", action="store_true", help="에디터 화면 구조를 덤프한다 (발행 안 함)")
    parser.add_argument("--publish", action="store_true", help="실제로 발행 버튼까지 클릭한다")
    parser.add_argument(
        "--at",
        metavar="YYYY-MM-DD HH:MM",
        help="예약 발행 시각을 직접 지정한다 (기본값인 '다음 정시로 올림' 대신 사용). --publish와 함께 써야 의미가 있다. 분 단위는 네이버 에디터가 10분 단위 select만 지원하므로 10의 배수(00/10/20/30/40/50)여야 한다.",
    )
    args = parser.parse_args()

    target_override = None
    if args.at:
        try:
            target_override = datetime.strptime(args.at, "%Y-%m-%d %H:%M")
        except ValueError:
            sys.exit(f"--at 형식이 올바르지 않습니다: '{args.at}' (예: '2026-09-19 10:00')")
        if target_override.minute % 10 != 0:
            sys.exit(f"--at의 분(minute)은 10의 배수여야 합니다 (네이버 에디터 제약): '{args.at}'")
        if target_override <= datetime.now():
            sys.exit(f"--at은 현재 시각 이후여야 합니다: '{args.at}'")

    with sync_playwright() as p:
        context = ensure_login(p, interactive=args.login)

        if args.login:
            print("로그인 세션 준비 완료.")
            context.close()
            return

        page, frame = open_editor(context)

        if args.inspect:
            page.wait_for_timeout(2000)
            dump_path, shot_path = dump_editor_structure(page, frame)
            print(f"덤프 저장: {dump_path}")
            print(f"스크린샷 저장: {shot_path}")
            input("확인 후 Enter를 누르면 브라우저를 닫습니다...")
            context.close()
            return

        if not args.topic_dir:
            sys.exit("주제 폴더 경로를 입력하세요. 예: python3 publish_naver.py output/9.9국장정리")

        topic_dir = Path(args.topic_dir).resolve()
        title_text, body_segments = parse_final_html(topic_dir)

        sel = load_selectors()
        required = ["title", "body", "photo_button", "publish_open_button", "publish_confirm_button"]
        if args.publish:
            # 카테고리 선택 / 예약 발행 단계는 --publish일 때만 실행되므로 그때만 필수로 검사한다.
            required += [
                "category_dropdown_button", "category_option_item",
                "schedule_radio_label", "schedule_date_input",
                "schedule_hour_select", "schedule_minute_select",
                "calendar_next_month_button", "calendar_day_cell",
            ]
        missing = [k for k in required if not sel.get(k)]
        if missing:
            sys.exit(
                f"아직 보정되지 않은 선택자가 있습니다: {missing}\n"
                f"먼저 `python3 publish_naver.py --inspect`로 화면 구조를 확인하고 "
                f"{SELECTORS_PATH}를 채워주세요."
            )

        result_url = fill_and_publish(
            page, frame, sel, title_text, body_segments, topic_dir.name, args.publish,
            target_override=target_override,
        )
        if result_url:
            # --publish 완료 시에는 사람 개입 없이 바로 종료한다 (publisher 에이전트가
            # 비대화형으로 이 스크립트를 실행하므로, 여기서 input()으로 멈추면 영원히 행에 걸린다).
            print(f"발행 완료: {result_url}")
            context.close()
            return

        shot = SCRIPTS_DIR / "last_fill_screenshot.png"
        page.screenshot(path=str(shot), full_page=True)
        print(f"입력 결과 스크린샷: {shot}")
        input("Enter를 누르면 브라우저를 닫습니다...")
        context.close()


if __name__ == "__main__":
    main()
