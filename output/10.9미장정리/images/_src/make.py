from playwright.sync_api import sync_playwright
import pathlib

here = pathlib.Path(__file__).parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#f2f2f2}
.stage{position:relative;overflow:hidden}
</style></head><body>%s</body></html>"""

DOWN = "#5b8def"  # 하락(파랑) - house convention
UP = "#e05252"    # 상승(빨강) - house convention
BG = "linear-gradient(145deg,#0f2027 0%,#134e4a 100%)"  # 딥그린-틸 (상승·반등 마감)
ACCENT = "#5eead4"  # 틸 계열 포인트 컬러 (최근 슬레이트그레이·버건디와 다른 톤)

# --- thumbnail: 좌측 정렬 타이틀 + 우측 대형 퍼센트 숫자 강조 (최근 '중앙형'/'좌텍스트+원형글로우' 조합과 다른 레이아웃) ---
THUMB = f"""<div class="stage" style="width:1080px;height:1080px;background:{BG}">
<div style="position:absolute;top:80px;left:80px;padding:10px 24px;border:1px solid rgba(94,234,212,.4);border-radius:6px;font-size:23px;font-weight:600;color:{ACCENT}">오늘 미장 정리 · 10/9</div>
<div style="position:absolute;top:260px;left:80px;right:440px;font-size:62px;font-weight:800;line-height:1.35;color:#ffffff">오픈AI 쇼크<br>하루 만에 싹 반등</div>
<div style="position:absolute;top:600px;left:80px;right:440px;font-size:25px;line-height:1.7;color:#aee6da">이란 리스크 완화 + 실적시즌 기대감<br>반도체·통신주는 오히려 약세</div>
<div style="position:absolute;top:330px;right:70px;text-align:right">
  <div style="font-size:22px;color:{ACCENT};margin-bottom:4px">다우존스</div>
  <div style="font-size:88px;font-weight:800;color:{UP}">+0.83%</div>
</div>
<div style="position:absolute;bottom:90px;left:80px;right:80px;display:flex;gap:18px">
  <div style="flex:1;background:rgba(255,255,255,.07);border-radius:12px;padding:22px 26px">
    <div style="font-size:19px;color:#aee6da;margin-bottom:6px">S&amp;P500</div>
    <div style="font-size:28px;font-weight:800;color:{UP}">+0.59%</div>
  </div>
  <div style="flex:1;background:rgba(255,255,255,.07);border-radius:12px;padding:22px 26px">
    <div style="font-size:19px;color:#aee6da;margin-bottom:6px">나스닥</div>
    <div style="font-size:28px;font-weight:800;color:{UP}">+0.64%</div>
  </div>
</div>
</div>"""

# --- body-1: 비교 표 (3대 지수 10/9 마감) ---
def index_table():
    rows = [
        ("다우존스30", "51,654.95", "+423.31p", "+0.83%", UP),
        ("S&P500", "7,811.51", "+46.15p", "+0.59%", UP),
        ("나스닥종합", "27,366.17", "+172.83p", "+0.64%", UP),
    ]
    trs = "".join(
        f'<tr><td style="padding:22px 20px;font-size:30px;font-weight:700;border-bottom:1px solid rgba(255,255,255,.14)">{n}</td>'
        f'<td style="padding:22px 20px;font-size:30px;text-align:right;border-bottom:1px solid rgba(255,255,255,.14)">{close}</td>'
        f'<td style="padding:22px 20px;font-size:30px;text-align:right;color:{c};border-bottom:1px solid rgba(255,255,255,.14)">{pt}</td>'
        f'<td style="padding:22px 20px;font-size:30px;font-weight:800;text-align:right;color:{c};border-bottom:1px solid rgba(255,255,255,.14)">{pct}</td></tr>'
        for n, close, pt, pct, c in rows
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:0 80px;display:flex;flex-direction:column;justify-content:center">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">3대 지수 동반 상승 — 10/9 마감</div>
<div style="font-size:24px;color:#aee6da;margin-bottom:58px">주간 기준으로도 세 지수 모두 상승 마감</div>
<table style="width:100%;border-collapse:collapse">
<thead><tr>
<th style="text-align:left;padding:18px 20px;font-size:22px;color:#aee6da;border-bottom:2px solid rgba(255,255,255,.3)">지수</th>
<th style="text-align:right;padding:18px 20px;font-size:22px;color:#aee6da;border-bottom:2px solid rgba(255,255,255,.3)">종가</th>
<th style="text-align:right;padding:18px 20px;font-size:22px;color:#aee6da;border-bottom:2px solid rgba(255,255,255,.3)">전일비</th>
<th style="text-align:right;padding:18px 20px;font-size:22px;color:#aee6da;border-bottom:2px solid rgba(255,255,255,.3)">등락률</th>
</tr></thead>
<tbody>{trs}</tbody>
</table>
<div style="margin-top:56px;border-left:6px solid {ACCENT};background:rgba(94,234,212,.1);border-radius:0 16px 16px 0;padding:30px 36px">
<div style="font-size:24px;line-height:1.6;color:#f2f2f2">"트럼프, 중간선거 전 이란 공격 미실시 언급<br>VIX 3.70%↓ 14.84, 중동 리스크 완화가 상승 견인"</div>
</div>
<div style="position:absolute;bottom:60px;left:80px;font-size:19px;color:#aee6da">합성 데이터 그래픽 · 10/9(현지시각) 뉴욕증시 마감 기준</div>
</div>"""

# --- body-2: 핵심 포인트 카드 (다음 주 실적시즌 기대감) ---
def earnings_cards():
    cards = [
        ("S&P500 3분기 순이익 전망", "전년 대비", "+30.6%", UP),
        ("에너지 업종 이익 전망", "전년 대비", "+123%", UP),
        ("기술 업종 이익 전망", "전년 대비", "+66.5%", UP),
        ("실적 시즌 개막", "웰스파고·골드만삭스", "JP모간체이스 (다음 주)", ACCENT),
    ]
    grid = "".join(
        f'<div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:16px;padding:46px 32px">'
        f'<div style="font-size:23px;color:#aee6da;margin-bottom:12px">{name}</div>'
        f'<div style="font-size:18px;color:#8fc7ba;margin-bottom:20px">{sub}</div>'
        f'<div style="font-size:36px;font-weight:800;color:{color}">{val}</div></div>'
        for name, sub, val, color in cards
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:0 80px;display:flex;flex-direction:column;justify-content:center">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">다음 주부터 3분기 실적 시즌</div>
<div style="font-size:24px;color:#aee6da;margin-bottom:54px">은행株가 먼저 깃발 들어요 — 핵심 전망 네 가지</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:26px">{grid}</div>
<div style="position:absolute;bottom:60px;left:80px;font-size:19px;color:#aee6da">합성 데이터 그래픽 · 애널리스트 전망치 종합 기준</div>
</div>"""

# --- body-3: 비교 표 (AI 업종 내 디커플링 — 반도체 약세 vs 비반도체 AI주 강세) ---
def decoupling_table():
    rows = [
        ("필라델피아 반도체지수", "-0.41%", DOWN),
        ("엔비디아", "-0.52%", DOWN),
        ("마이크론", "-0.66%", DOWN),
        ("SK하이닉스 ADR", "-0.86%", DOWN),
        ("팔란티어", "+5.17%", UP),
        ("아마존", "+3.29%", UP),
        ("마이크로소프트", "+2.38%", UP),
    ]
    trs = "".join(
        f'<tr><td style="padding:18px 20px;font-size:27px;font-weight:700;border-bottom:1px solid rgba(255,255,255,.14)">{n}</td>'
        f'<td style="padding:18px 20px;font-size:27px;font-weight:800;text-align:right;color:{c};border-bottom:1px solid rgba(255,255,255,.14)">{pct}</td></tr>'
        for n, pct, c in rows
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:0 80px;display:flex;flex-direction:column;justify-content:center">
<div style="font-size:40px;font-weight:800;margin-bottom:12px">AI주 안에서도 갈렸어요</div>
<div style="font-size:24px;color:#aee6da;margin-bottom:46px">반도체는 약세, 비반도체 AI주는 강세</div>
<table style="width:100%;border-collapse:collapse">
<tbody>{trs}</tbody>
</table>
<div style="position:absolute;bottom:60px;left:80px;font-size:19px;color:#aee6da">합성 데이터 그래픽 · 10/9(현지시각) 뉴욕증시 마감 기준</div>
</div>"""

jobs = {
    "thumbnail.png": THUMB,
    "body-1.png": index_table(),
    "body-2.png": earnings_cards(),
    "body-3.png": decoupling_table(),
}

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1080})
    for name, html in jobs.items():
        pg.set_content(BASE % html)
        pg.screenshot(path=str(here.parent / name), full_page=False)
        print("saved", name)
    b.close()
