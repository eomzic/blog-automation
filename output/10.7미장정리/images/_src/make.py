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
BG = "linear-gradient(135deg,#2d0a0a 0%,#4a1414 100%)"  # 버건디-마룬 (금리 2002년 최고치 경신 분위기)
ACCENT = "#e8b4a0"

# --- thumbnail: 중앙 정렬 텍스트 + 좌상단 액센트 도형 레이아웃 ---
THUMB = f"""<div class="stage" style="width:1080px;height:1080px;background:{BG}">
<div style="position:absolute;top:-120px;left:-120px;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle,rgba(232,180,160,.18),transparent 70%)"></div>
<div style="position:absolute;top:70px;left:0;right:0;display:flex;justify-content:center">
  <div style="padding:10px 24px;border:1px solid rgba(255,255,255,.25);border-radius:6px;font-size:24px;font-weight:600;color:#e8c9bf">오늘 미장 정리 · 10/7</div>
</div>
<div style="position:absolute;top:290px;left:50%;transform:translateX(-50%);width:880px;text-align:center;font-size:66px;font-weight:800;line-height:1.35;color:#ffffff">사상최고 하루 만에 꺾이고<br>금리는 2002년來 최고</div>
<div style="position:absolute;top:620px;left:50%;transform:translateX(-50%);width:760px;text-align:center;font-size:26px;line-height:1.6;color:#e8c9bf">다우 -0.66% · S&amp;P -0.22% · 나스닥 -0.22%</div>
<div style="position:absolute;top:760px;left:50%;transform:translateX(-50%);display:flex;gap:56px">
  <div style="text-align:center">
    <div style="font-size:22px;color:#c9a89c;margin-bottom:8px">다우존스</div>
    <div style="font-size:54px;font-weight:800;color:{DOWN}">-0.66%</div>
  </div>
  <div style="text-align:center">
    <div style="font-size:22px;color:#c9a89c;margin-bottom:8px">S&amp;P 500</div>
    <div style="font-size:54px;font-weight:800;color:{DOWN}">-0.22%</div>
  </div>
  <div style="text-align:center">
    <div style="font-size:22px;color:#c9a89c;margin-bottom:8px">나스닥</div>
    <div style="font-size:54px;font-weight:800;color:{DOWN}">-0.22%</div>
  </div>
</div>
<div style="position:absolute;bottom:0;left:0;width:100%;height:10px;background:{ACCENT}"></div>
</div>"""

# --- body-1: 비교 표 (3대 지수) ---
def index_table():
    rows = [
        ("다우존스", "51,179.87", "-341.41p", "-0.66%"),
        ("S&P 500", "7,801.77", "-17.16p", "-0.22%"),
        ("나스닥 종합", "27,538.69", "-61.20p", "-0.22%"),
    ]
    trs = "".join(
        f'<tr><td style="padding:22px 20px;font-size:32px;font-weight:700;border-bottom:1px solid rgba(255,255,255,.12)">{n}</td>'
        f'<td style="padding:22px 20px;font-size:32px;text-align:right;border-bottom:1px solid rgba(255,255,255,.12)">{close}</td>'
        f'<td style="padding:22px 20px;font-size:32px;text-align:right;color:{DOWN};border-bottom:1px solid rgba(255,255,255,.12)">{pt}</td>'
        f'<td style="padding:22px 20px;font-size:32px;font-weight:800;text-align:right;color:{DOWN};border-bottom:1px solid rgba(255,255,255,.12)">{pct}</td></tr>'
        for n, close, pt, pct in rows
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:0 80px">
<div style="position:absolute;top:50%;left:80px;right:80px;transform:translateY(-58%)">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">10/7 미국 3대 지수 마감</div>
<div style="font-size:24px;color:#e8c9bf;margin-bottom:50px">전 거래일(10/6, 사상 최고치) 대비</div>
<table style="width:100%;border-collapse:collapse">
<thead><tr>
<th style="text-align:left;padding:14px 20px;font-size:22px;color:#e8c9bf;border-bottom:2px solid rgba(255,255,255,.3)">지수</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#e8c9bf;border-bottom:2px solid rgba(255,255,255,.3)">종가</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#e8c9bf;border-bottom:2px solid rgba(255,255,255,.3)">전일비</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#e8c9bf;border-bottom:2px solid rgba(255,255,255,.3)">등락률</th>
</tr></thead>
<tbody>{trs}</tbody>
</table>
<div style="margin-top:50px;background:rgba(255,255,255,.06);border-radius:16px;padding:32px 34px;font-size:24px;line-height:1.7;color:#f2e4df">세 지수 모두 하락 — 다우가 가장 크게 밀렸고, 나스닥·S&amp;P는 상대적으로 선방</div>
</div>
<div style="position:absolute;bottom:50px;left:80px;font-size:20px;color:#b08478">합성 데이터 그래픽 · Yahoo Finance·CNBC·TheStreet 교차 확인 기준</div>
</div>"""

# --- body-2: 단계별 다이어그램 (금리 흐름 10/6 -> 10/7) ---
def yield_flow():
    steps = [
        ("10/6 마감", "10년물 5.275%", "전일 소폭 하락 마감"),
        ("10/7 장중", "30년물 5.73%", "2002년 5월 이후 최고"),
        ("10/7 마감", "10년물 5.3%대", "다시 상승 전환"),
    ]
    step_html = "".join(
        f'<div style="flex:1;background:rgba(255,255,255,.06);border-radius:16px;padding:30px 24px;text-align:center">'
        f'<div style="font-size:20px;color:#e8c9bf;margin-bottom:14px">{label}</div>'
        f'<div style="font-size:34px;font-weight:800;color:#ffffff;margin-bottom:10px">{val}</div>'
        f'<div style="font-size:19px;color:#c9a89c;line-height:1.5">{desc}</div></div>'
        for label, val, desc in steps
    )
    arrow = f'<div style="font-size:40px;color:{ACCENT};display:flex;align-items:center;padding:0 10px">&#8594;</div>'
    items = arrow.join(step_html.split("</div></div>")[i] + "</div></div>" for i in range(len(steps)))
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:0 80px">
<div style="position:absolute;top:50%;left:80px;right:80px;transform:translateY(-55%)">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">국채 금리, 또 2002년 수준으로</div>
<div style="font-size:24px;color:#e8c9bf;margin-bottom:60px">하루 사이 방향이 다시 위로 꺾였어요</div>
<div style="display:flex;align-items:stretch">{items}</div>
<div style="margin-top:50px;background:rgba(255,255,255,.06);border-radius:16px;padding:32px 34px;font-size:24px;line-height:1.7;color:#f2e4df">정확한 종가는 소스마다 10년물 5.31%~5.36%로 소폭 엇갈려요 — 방향 전환이 핵심 포인트</div>
</div>
<div style="position:absolute;bottom:50px;left:80px;font-size:20px;color:#b08478">합성 데이터 그래픽 · 복수 소스 교차 확인 기준</div>
</div>"""

# --- body-3: 핵심 포인트 카드 ---
def key_points():
    points = [
        ("📉", "전일 기록은 하루짜리", "3대 지수 10/6 사상 최고 → 10/7 동반 하락"),
        ("🏦", "금리 2002년래 최고 재경신", "30년물 장중 5.73%, 2002년 5월 이후 최고"),
        ("📋", "9월 FOMC 의사록 공개", "시장이 하루 종일 주시, 구체 톤은 소스 간 엇갈려 보류"),
        ("💻", "반도체 대형주는 선방", "엔비디아·AMD 사상 최고가 대비 1% 미만 하락"),
    ]
    cards = "".join(
        f'<div style="background:rgba(255,255,255,.06);border-radius:16px;padding:32px 30px;display:flex;gap:20px;align-items:flex-start">'
        f'<div style="font-size:40px;line-height:1">{emoji}</div>'
        f'<div><div style="font-size:27px;font-weight:800;color:#ffffff;margin-bottom:8px">{title}</div>'
        f'<div style="font-size:21px;color:#e8c9bf;line-height:1.6">{desc}</div></div></div>'
        for emoji, title, desc in points
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:0 80px">
<div style="position:absolute;top:50%;left:80px;right:80px;transform:translateY(-52%)">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">오늘 미장 핵심 포인트</div>
<div style="font-size:24px;color:#e8c9bf;margin-bottom:46px">10/7(수) 마감 기준</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:22px">{cards}</div>
</div>
<div style="position:absolute;bottom:50px;left:80px;font-size:20px;color:#b08478">합성 데이터 그래픽 · 10/7 마감 기준 정리</div>
</div>"""

pages = {
    "thumbnail.png": THUMB,
    "body-1.png": index_table(),
    "body-2.png": yield_flow(),
    "body-3.png": key_points(),
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1080})
    for name, html in pages.items():
        page.set_content(BASE % html)
        page.screenshot(path=str(here.parent / name))
    browser.close()

print("done")
