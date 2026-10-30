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
BG = "linear-gradient(135deg,#1a1a2e 0%,#16213e 100%)"

# --- thumbnail: 좌측 정렬 텍스트 + 우측 큰 퍼센트 강조 레이아웃 ---
THUMB = f"""<div class="stage" style="width:1080px;height:1080px;background:{BG}">
<div style="position:absolute;top:88px;left:80px;padding:10px 24px;border:1px solid rgba(255,255,255,.25);border-radius:6px;font-size:24px;font-weight:600;color:#cfd3e6">오늘 국장 정리 · 10/7</div>
<div style="position:absolute;top:300px;left:80px;width:560px;font-size:70px;font-weight:800;line-height:1.3;color:#ffffff">코스피·코스닥<br>동반 2%대 하락</div>
<div style="position:absolute;top:660px;left:80px;width:560px;font-size:28px;line-height:1.6;color:#9aa3c7">삼성전자 실적 발표 하루 앞두고<br>다 같이 몸사리기</div>
<div style="position:absolute;top:0;bottom:0;right:0;width:360px;display:flex;flex-direction:column;align-items:flex-end;justify-content:center;padding-right:70px">
  <div style="font-size:26px;color:#9aa3c7;margin-bottom:6px">코스피</div>
  <div style="font-size:88px;font-weight:800;color:{DOWN};line-height:1.0;margin-bottom:46px">-1.98%</div>
  <div style="font-size:26px;color:#9aa3c7;margin-bottom:6px">코스닥</div>
  <div style="font-size:88px;font-weight:800;color:{DOWN};line-height:1.0">-2.34%</div>
</div>
<div style="position:absolute;bottom:0;left:0;width:100%;height:10px;background:{DOWN}"></div>
</div>"""

# --- body-1: 비교 표 (지수) ---
def index_table():
    rows = [
        ("코스피", "6,803.90", "-137.49p", "-1.98%"),
        ("코스닥", "898.43", "-21.49p", "-2.34%"),
    ]
    trs = "".join(
        f'<tr><td style="padding:22px 20px;font-size:32px;font-weight:700;border-bottom:1px solid rgba(255,255,255,.12)">{n}</td>'
        f'<td style="padding:22px 20px;font-size:32px;text-align:right;border-bottom:1px solid rgba(255,255,255,.12)">{close}</td>'
        f'<td style="padding:22px 20px;font-size:32px;text-align:right;color:{DOWN};border-bottom:1px solid rgba(255,255,255,.12)">{pt}</td>'
        f'<td style="padding:22px 20px;font-size:32px;font-weight:800;text-align:right;color:{DOWN};border-bottom:1px solid rgba(255,255,255,.12)">{pct}</td></tr>'
        for n, close, pt, pct in rows
    )
    stat_tiles = "".join(
        f'<div style="flex:1;background:rgba(255,255,255,.05);border-radius:14px;padding:30px 26px">'
        f'<div style="font-size:22px;color:#9aa3c7;margin-bottom:12px">{label}</div>'
        f'<div style="font-size:36px;font-weight:800;color:{c}">{val}</div></div>'
        for label, val, c in [
            ("상승 종목", "333개", UP),
            ("하락 종목", "527개", DOWN),
            ("거래대금", "19조 6,993억원", "#e8eaf5"),
        ]
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:90px 80px">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">10/7 지수 마감 비교</div>
<div style="font-size:24px;color:#9aa3c7;margin-bottom:50px">전 거래일(10/6) 대비</div>
<table style="width:100%;border-collapse:collapse">
<thead><tr>
<th style="text-align:left;padding:14px 20px;font-size:22px;color:#9aa3c7;border-bottom:2px solid rgba(255,255,255,.3)">지수</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#9aa3c7;border-bottom:2px solid rgba(255,255,255,.3)">종가</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#9aa3c7;border-bottom:2px solid rgba(255,255,255,.3)">전일비</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#9aa3c7;border-bottom:2px solid rgba(255,255,255,.3)">등락률</th>
</tr></thead>
<tbody>{trs}</tbody>
</table>
<div style="margin-top:60px;font-size:24px;color:#9aa3c7;margin-bottom:24px">시장 전반 현황</div>
<div style="display:flex;gap:20px">{stat_tiles}</div>
<div style="position:absolute;bottom:60px;left:80px;font-size:20px;color:#6b7399">합성 데이터 그래픽 · 뉴스핌·서울신문 교차 확인 기준 정리</div>
</div>"""

# --- body-2: 핵심 포인트 카드 (종목별 등락) ---
def stock_cards():
    cards = [
        ("삼성전자", "268,500원", "-1.29%", DOWN),
        ("SK하이닉스", "1,723,000원", "-2.82%", DOWN),
        ("삼성전기", "-", "-4.24%", DOWN),
        ("현대차", "-", "-3.45%", DOWN),
        ("LG에너지솔루션", "-", "+0.26%", UP),
        ("KB금융", "-", "+0.96%", UP),
    ]
    grid = "".join(
        f'<div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:34px 30px">'
        f'<div style="font-size:26px;color:#cfd3e6;margin-bottom:14px">{name}</div>'
        f'<div style="font-size:24px;color:#6b7399;margin-bottom:18px">{price}</div>'
        f'<div style="font-size:42px;font-weight:800;color:{color}">{pct}</div></div>'
        for name, price, pct, color in cards
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:90px 80px">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">주요 종목 등락 (10/7)</div>
<div style="font-size:24px;color:#9aa3c7;margin-bottom:46px">반도체·자동차 약세, 2차전지·금융 선방</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:22px">{grid}</div>
<div style="position:absolute;bottom:60px;left:80px;font-size:20px;color:#6b7399">합성 데이터 그래픽 · 10/7 마감가 기준</div>
</div>"""

# --- body-3: 인용/강조 박스 (수급, 소스별 차이 투명 공개) ---
def flow_quote():
    tiles = "".join(
        f'<div style="background:rgba(255,255,255,.05);border-radius:14px;padding:26px 28px">'
        f'<div style="font-size:21px;color:#9aa3c7;margin-bottom:10px">{label}</div>'
        f'<div style="font-size:30px;font-weight:800;color:{c}">{val}</div></div>'
        for label, val, c in [
            ("외국인 (코스피, 뉴스핌)", "-3조 1,095억원", DOWN),
            ("외국인 (코스피, 서울신문)", "-2조 5,976억원", DOWN),
            ("개인 (코스피, 뉴스핌)", "+3조 2,616억원", UP),
            ("외국인 (코스닥)", "-3,259억원", DOWN),
            ("개인 (코스닥)", "+5,771억원", UP),
            ("기관 (코스피, 뉴스핌)", "-8,598억원", DOWN),
        ]
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:90px 80px">
<div style="font-size:42px;font-weight:800;margin-bottom:46px">외국인, 오늘도 팔았다</div>
<div style="border-left:6px solid {DOWN};background:rgba(91,141,239,.08);border-radius:0 16px 16px 0;padding:36px 44px;margin-bottom:44px">
<div style="font-size:28px;line-height:1.7;color:#e8eaf5">"외국인의 대규모 순매도가<br>코스피·코스닥 하락을 주도했다"</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">{tiles}</div>
<div style="position:absolute;bottom:60px;left:80px;font-size:20px;color:#6b7399">합성 데이터 그래픽 · 코스피 외국인·기관 금액은 소스 간 차이 있어 병기</div>
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
