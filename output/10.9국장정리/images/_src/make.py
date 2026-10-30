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
BG = "linear-gradient(145deg,#232526 0%,#3a3d40 100%)"  # 슬레이트-그레이 (보합·횡보/휴장)
ACCENT = "#e8c468"  # 휴장/쉬어가는 날 포인트 컬러 (최근 네이비·버건디·틸과 다른 톤)

# --- thumbnail: 좌상단 배지 + 중앙 타이틀, 하단 액센트 바 없음(최근 글들과 다른 조합) ---
THUMB = f"""<div class="stage" style="width:1080px;height:1080px;background:{BG}">
<div style="position:absolute;top:80px;left:80px;padding:10px 22px;border:1px solid rgba(232,196,104,.5);border-radius:6px;font-size:23px;font-weight:600;color:{ACCENT}">오늘 국장 정리 · 10/9</div>
<div style="position:absolute;top:300px;left:80px;right:80px;font-size:64px;font-weight:800;line-height:1.35;color:#ffffff">한글날 휴장<br>그래도 복기는 하고 가요</div>
<div style="position:absolute;top:620px;left:80px;right:80px;font-size:26px;line-height:1.7;color:#c7cbce">직전 거래일(10/8) 삼성전자 107조 실적 후폭풍 +<br>뉴욕증시 체크</div>
<div style="position:absolute;bottom:90px;left:80px;right:80px;display:flex;gap:18px">
  <div style="flex:1;background:rgba(255,255,255,.06);border-radius:12px;padding:22px 26px">
    <div style="font-size:20px;color:#c7cbce;margin-bottom:6px">휴장일</div>
    <div style="font-size:30px;font-weight:800;color:{ACCENT}">10/9(금)</div>
  </div>
  <div style="flex:1;background:rgba(255,255,255,.06);border-radius:12px;padding:22px 26px">
    <div style="font-size:20px;color:#c7cbce;margin-bottom:6px">다음 거래일</div>
    <div style="font-size:30px;font-weight:800;color:#ffffff">10/12(월)</div>
  </div>
</div>
</div>"""

# --- body-1: 단계별 다이어그램 (10월 캘린더 - 휴장/거래일 흐름) ---
def calendar_diagram():
    days = [
        ("10/6", "월", "거래일", False),
        ("10/7", "화", "거래일", False),
        ("10/8", "수", "거래일 · 삼전 실적", False),
        ("10/9", "목", "한글날 휴장", True),
        ("10/10", "금", "주말", True),
        ("10/11", "토", "주말", True),
        ("10/12", "일", "다음 거래일", False),
    ]
    cells = "".join(
        f'<div style="background:{"rgba(232,196,104,.14)" if off else "rgba(255,255,255,.06)"};'
        f'border:1px solid {"rgba(232,196,104,.45)" if off else "rgba(255,255,255,.12)"};'
        f'border-radius:14px;padding:26px 16px;text-align:center">'
        f'<div style="font-size:24px;font-weight:800;color:{"%s" % ACCENT if off else "#ffffff"};margin-bottom:6px">{d}</div>'
        f'<div style="font-size:18px;color:#c7cbce;margin-bottom:10px">{w}요일</div>'
        f'<div style="font-size:16px;color:{ACCENT if off else "#9aa0a6"}">{label}</div></div>'
        for d, w, label, off in days
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:0 70px;display:flex;flex-direction:column;justify-content:center">
<div style="font-size:40px;font-weight:800;margin-bottom:10px">10월 둘째 주, 거래일은 언제?</div>
<div style="font-size:23px;color:#c7cbce;margin-bottom:54px">10/9 한글날 휴장 → 주말 포함 사흘 연휴 → 10/12(월) 재개장</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px">{cells}</div>
<div style="position:absolute;bottom:60px;left:70px;font-size:19px;color:#9aa0a6">합성 데이터 그래픽 · 한국거래소 휴장일 기준 정리</div>
</div>"""

# --- body-2: 핵심 포인트 카드 (10/8 복기) ---
def recap_cards():
    cards = [
        ("코스피", "6,625.93", "-2.62%", DOWN),
        ("코스닥", "892.27", "-0.69%", DOWN),
        ("삼성전자 영업이익", "107조 4,000억원", "+783%", UP),
        ("외국인+기관 순매도", "약 -3조 6,500억원", DOWN, DOWN),
    ]
    # normalize 4th tuple length issue
    cards = [
        ("코스피", "6,625.93", "-2.62%", DOWN),
        ("코스닥", "892.27", "-0.69%", DOWN),
        ("삼성전자 영업이익", "107조 4,000억원", "전년 대비 +783%", UP),
        ("외국인+기관 순매도", "코스피 기준", "약 -3조 6,500억원", DOWN),
    ]
    grid = "".join(
        f'<div style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:46px 32px">'
        f'<div style="font-size:24px;color:#c7cbce;margin-bottom:12px">{name}</div>'
        f'<div style="font-size:19px;color:#9aa0a6;margin-bottom:20px">{sub}</div>'
        f'<div style="font-size:40px;font-weight:800;color:{color}">{val}</div></div>'
        for name, sub, val, color in cards
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:0 80px;display:flex;flex-direction:column;justify-content:center">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">직전 거래일(10/8) 한눈에 복기</div>
<div style="font-size:24px;color:#c7cbce;margin-bottom:54px">실적은 역대급, 주가는 하락 — 그날의 핵심 네 가지</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:26px">{grid}</div>
<div style="position:absolute;bottom:60px;left:80px;font-size:19px;color:#9aa0a6">합성 데이터 그래픽 · 10/8 마감 기준 복기 정리</div>
</div>"""

# --- body-3: 비교 표 (뉴욕증시 10/8 마감) ---
def ny_table():
    rows = [
        ("S&P500", "6,753.72", "+39.13p", "+0.58%", UP),
        ("나스닥종합", "23,043.38", "+255.01p", "+1.12%", UP),
        ("다우존스30", "46,601.78", "-1.20p", "보합", "#c7cbce"),
    ]
    trs = "".join(
        f'<tr><td style="padding:22px 20px;font-size:30px;font-weight:700;border-bottom:1px solid rgba(255,255,255,.14)">{n}</td>'
        f'<td style="padding:22px 20px;font-size:30px;text-align:right;border-bottom:1px solid rgba(255,255,255,.14)">{close}</td>'
        f'<td style="padding:22px 20px;font-size:30px;text-align:right;color:{c};border-bottom:1px solid rgba(255,255,255,.14)">{pt}</td>'
        f'<td style="padding:22px 20px;font-size:30px;font-weight:800;text-align:right;color:{c};border-bottom:1px solid rgba(255,255,255,.14)">{pct}</td></tr>'
        for n, close, pt, pct, c in rows
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:0 80px;display:flex;flex-direction:column;justify-content:center">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">연휴 중 체크 — 뉴욕증시 10/8 마감</div>
<div style="font-size:24px;color:#c7cbce;margin-bottom:58px">국내 휴장 사이, 나스닥은 1%대 강세</div>
<table style="width:100%;border-collapse:collapse">
<thead><tr>
<th style="text-align:left;padding:18px 20px;font-size:22px;color:#c7cbce;border-bottom:2px solid rgba(255,255,255,.3)">지수</th>
<th style="text-align:right;padding:18px 20px;font-size:22px;color:#c7cbce;border-bottom:2px solid rgba(255,255,255,.3)">종가</th>
<th style="text-align:right;padding:18px 20px;font-size:22px;color:#c7cbce;border-bottom:2px solid rgba(255,255,255,.3)">전일비</th>
<th style="text-align:right;padding:18px 20px;font-size:22px;color:#c7cbce;border-bottom:2px solid rgba(255,255,255,.3)">등락률</th>
</tr></thead>
<tbody>{trs}</tbody>
</table>
<div style="margin-top:56px;border-left:6px solid {UP};background:rgba(224,82,82,.1);border-radius:0 16px 16px 0;padding:30px 36px">
<div style="font-size:24px;line-height:1.6;color:#f2f2f2">"기술주 중심 강세가 이어지며<br>다음 거래일 국내 반도체 분위기에도 참고될 변수"</div>
</div>
<div style="position:absolute;bottom:60px;left:80px;font-size:19px;color:#9aa0a6">합성 데이터 그래픽 · 10/8(현지시각) 뉴욕증시 마감 기준</div>
</div>"""

jobs = {
    "thumbnail.png": THUMB,
    "body-1.png": calendar_diagram(),
    "body-2.png": recap_cards(),
    "body-3.png": ny_table(),
}

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1080})
    for name, html in jobs.items():
        pg.set_content(BASE % html)
        pg.screenshot(path=str(here.parent / name), full_page=False)
        print("saved", name)
    b.close()
