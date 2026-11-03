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
BG = "linear-gradient(145deg,#2d0a0a 0%,#4a1414 100%)"  # 버건디-마룬 (급락·쇼크성)

# --- thumbnail: 상단 배지 + 중앙 큰 타이틀 + 하단 가로 스트립 (10/5·10/6 중앙형, 10/7 좌우분할과 모두 다른 조합) ---
THUMB = f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};text-align:center">
<div style="position:absolute;top:92px;left:50%;transform:translateX(-50%);padding:12px 30px;border:1px solid rgba(255,255,255,.28);border-radius:30px;font-size:25px;font-weight:600;color:#f3cfcf;white-space:nowrap">오늘 국장 정리 · 10/8</div>
<div style="position:absolute;top:290px;left:70px;right:70px;font-size:72px;font-weight:800;line-height:1.3;color:#ffffff">실적은 107조<br>주가는 2%대 급락</div>
<div style="position:absolute;top:660px;left:70px;right:70px;font-size:27px;line-height:1.6;color:#f3cfcf">삼성전자 호실적에도 외국인·기관 동반 매도</div>
<div style="position:absolute;bottom:0;left:0;width:100%;height:140px;background:rgba(0,0,0,.22);display:flex;align-items:center;justify-content:center;gap:90px">
  <div style="text-align:center">
    <div style="font-size:22px;color:#f3cfcf;margin-bottom:4px">코스피</div>
    <div style="font-size:46px;font-weight:800;color:{DOWN}">-2.62%</div>
  </div>
  <div style="width:1px;height:70px;background:rgba(255,255,255,.2)"></div>
  <div style="text-align:center">
    <div style="font-size:22px;color:#f3cfcf;margin-bottom:4px">코스닥</div>
    <div style="font-size:46px;font-weight:800;color:{DOWN}">-0.69%</div>
  </div>
</div>
</div>"""

# --- body-1: 비교 표 (지수) ---
def index_table():
    rows = [
        ("코스피", "6,625.93", "-177.97p", "-2.62%"),
        ("코스닥", "892.27", "-6.16p", "-0.69%"),
    ]
    trs = "".join(
        f'<tr><td style="padding:22px 20px;font-size:32px;font-weight:700;border-bottom:1px solid rgba(255,255,255,.14)">{n}</td>'
        f'<td style="padding:22px 20px;font-size:32px;text-align:right;border-bottom:1px solid rgba(255,255,255,.14)">{close}</td>'
        f'<td style="padding:22px 20px;font-size:32px;text-align:right;color:{DOWN};border-bottom:1px solid rgba(255,255,255,.14)">{pt}</td>'
        f'<td style="padding:22px 20px;font-size:32px;font-weight:800;text-align:right;color:{DOWN};border-bottom:1px solid rgba(255,255,255,.14)">{pct}</td></tr>'
        for n, close, pt, pct in rows
    )
    stat_tiles = "".join(
        f'<div style="flex:1;background:rgba(255,255,255,.06);border-radius:14px;padding:30px 26px">'
        f'<div style="font-size:22px;color:#f3cfcf;margin-bottom:12px">{label}</div>'
        f'<div style="font-size:34px;font-weight:800;color:{c}">{val}</div></div>'
        for label, val, c in [
            ("삼성전자 영업이익", "107조 4,000억원", "#f2f2f2"),
            ("전년 대비", "+783%", UP),
        ]
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:90px 80px">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">10/8 지수 마감 비교</div>
<div style="font-size:24px;color:#f3cfcf;margin-bottom:50px">전 거래일(10/7) 대비</div>
<table style="width:100%;border-collapse:collapse">
<thead><tr>
<th style="text-align:left;padding:14px 20px;font-size:22px;color:#f3cfcf;border-bottom:2px solid rgba(255,255,255,.3)">지수</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#f3cfcf;border-bottom:2px solid rgba(255,255,255,.3)">종가</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#f3cfcf;border-bottom:2px solid rgba(255,255,255,.3)">전일비</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#f3cfcf;border-bottom:2px solid rgba(255,255,255,.3)">등락률</th>
</tr></thead>
<tbody>{trs}</tbody>
</table>
<div style="margin-top:60px;font-size:24px;color:#f3cfcf;margin-bottom:24px">같은 날 발표된 삼성전자 3분기 잠정실적</div>
<div style="display:flex;gap:20px">{stat_tiles}</div>
<div style="position:absolute;bottom:60px;left:80px;font-size:20px;color:#c99">합성 데이터 그래픽 · 뉴스핌·뉴스1·글로벌이코노믹 교차 확인 기준 정리</div>
</div>"""

# --- body-2: 핵심 포인트 카드 (종목별 등락) ---
def stock_cards():
    cards = [
        ("삼성전자", "262,000원", "-2.42%", DOWN),
        ("SK하이닉스", "1,681,000원", "-2.44%", DOWN),
        ("주성엔지니어링", "코스닥", "+8.89%", UP),
        ("원익IPS", "코스닥", "+4.88%", UP),
        ("리노공업", "코스닥", "+4.46%", UP),
        ("이오테크닉스", "코스닥", "+2.51%", UP),
    ]
    grid = "".join(
        f'<div style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:34px 30px">'
        f'<div style="font-size:26px;color:#f3d6d6;margin-bottom:14px">{name}</div>'
        f'<div style="font-size:22px;color:#c99;margin-bottom:18px">{price}</div>'
        f'<div style="font-size:40px;font-weight:800;color:{color}">{pct}</div></div>'
        for name, price, pct, color in cards
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:90px 80px">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">반도체 대형주 vs 코스닥 장비주 (10/8)</div>
<div style="font-size:24px;color:#f3cfcf;margin-bottom:46px">대형 반도체주 약세, 소부장은 CAPEX 기대에 강세</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:22px">{grid}</div>
<div style="position:absolute;bottom:60px;left:80px;font-size:20px;color:#c99">합성 데이터 그래픽 · 10/8 마감가 기준</div>
</div>"""

# --- body-3: 인용/강조 박스 (수급) ---
def flow_quote():
    tiles = "".join(
        f'<div style="background:rgba(255,255,255,.06);border-radius:14px;padding:26px 28px">'
        f'<div style="font-size:21px;color:#f3cfcf;margin-bottom:10px">{label}</div>'
        f'<div style="font-size:30px;font-weight:800;color:{c}">{val}</div></div>'
        for label, val, c in [
            ("외국인 (코스피)", "-1조 9,885억원", DOWN),
            ("기관 (코스피)", "-1조 6,657억원", DOWN),
            ("개인 (코스피)", "+2조 9,008억원", UP),
            ("외국인+기관 합산", "약 -3조 6,500억원", DOWN),
        ]
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:90px 80px">
<div style="font-size:42px;font-weight:800;margin-bottom:46px">호실적에도 외국인은 돌아서지 않았다</div>
<div style="border-left:6px solid {DOWN};background:rgba(91,141,239,.1);border-radius:0 16px 16px 0;padding:36px 44px;margin-bottom:44px">
<div style="font-size:28px;line-height:1.7;color:#f2f2f2">"외국인·기관 동반 매도가<br>삼성전자 실적 서프라이즈를 눌렀다"</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">{tiles}</div>
<div style="position:absolute;bottom:60px;left:80px;font-size:20px;color:#c99">합성 데이터 그래픽 · 코스피 투자자별 순매수 기준, 소스 간 소폭 차이 있음</div>
</div>"""

jobs = {
    "thumbnail.png": THUMB,
    "body-1.png": index_table(),
    "body-2.png": stock_cards(),
    "body-3.png": flow_quote(),
}

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1080})
    for name, html in jobs.items():
        pg.set_content(BASE % html)
        pg.screenshot(path=str(here.parent / name), full_page=False)
        print("saved", name)
    b.close()
