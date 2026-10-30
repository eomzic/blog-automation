from playwright.sync_api import sync_playwright
import pathlib

here = pathlib.Path(__file__).parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#f2f2f2}
.stage{position:relative;overflow:hidden}
</style></head><body>%s</body></html>"""

DOWN = "#5b8def"  # 하락(파랑) - house convention, 절대 안 바꿈
UP = "#e05252"    # 상승(빨강) - house convention, 절대 안 바꿈
ACCENT = "#d9b872"  # 슬레이트 팔레트 보조 포인트컬러(앰버) - 장식용으로만 사용
BG = "linear-gradient(135deg,#232526 0%,#3a3d40 100%)"  # 슬레이트-그레이 (보합·방향성 불분명한 날)

# --- thumbnail: 좌상단 배지 + 좌측 정렬 타이틀 + 우상단 원형 글로우 + 중앙 가로 스탯 pill (직전 글들의 '중앙정렬+하단 풀폭 바' / '좌텍스트+우측 큰 숫자' 조합과 다른 레이아웃) ---
THUMB = f"""<div class="stage" style="width:1080px;height:1080px;background:{BG}">
<div style="position:absolute;top:-180px;right:-180px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(217,184,114,.22) 0%,rgba(217,184,114,0) 70%)"></div>
<div style="position:absolute;top:88px;left:80px;padding:12px 28px;border:1px solid rgba(255,255,255,.3);border-radius:30px;font-size:24px;font-weight:600;color:#e8c98a">오늘 미장 정리 · 10/8</div>
<div style="position:absolute;top:270px;left:80px;right:80px;font-size:70px;font-weight:800;line-height:1.32;color:#ffffff">오픈AI 매출 쇼크<br>나스닥 1.25%↓</div>
<div style="position:absolute;top:610px;left:80px;right:140px;font-size:27px;line-height:1.6;color:#cfd3d4">반도체 급락 + 유가 4%대 급등, AI 거품론 재점화</div>
<div style="position:absolute;top:760px;left:80px;display:flex;gap:16px">
  <div style="background:rgba(255,255,255,.08);border-radius:16px;padding:22px 30px">
    <div style="font-size:20px;color:#cfd3d4;margin-bottom:6px">다우</div>
    <div style="font-size:34px;font-weight:800;color:{UP}">+0.10%</div>
  </div>
  <div style="background:rgba(255,255,255,.08);border-radius:16px;padding:22px 30px">
    <div style="font-size:20px;color:#cfd3d4;margin-bottom:6px">S&amp;P500</div>
    <div style="font-size:34px;font-weight:800;color:{DOWN}">-0.47%</div>
  </div>
  <div style="background:rgba(255,255,255,.08);border-radius:16px;padding:22px 30px">
    <div style="font-size:20px;color:#cfd3d4;margin-bottom:6px">나스닥</div>
    <div style="font-size:34px;font-weight:800;color:{DOWN}">-1.25%</div>
  </div>
</div>
</div>"""

# --- body-1: 비교 표 (다우/S&P/나스닥) ---
def index_table():
    rows = [
        ("다우존스", "51,231.64", "+51.77p", "+0.10%", UP),
        ("S&P 500", "7,765.36", "-36.41p", "-0.47%", DOWN),
        ("나스닥 종합", "27,193.34", "-345.35p", "-1.25%", DOWN),
    ]
    trs = "".join(
        f'<tr><td style="padding:22px 20px;font-size:32px;font-weight:700;border-bottom:1px solid rgba(255,255,255,.14)">{n}</td>'
        f'<td style="padding:22px 20px;font-size:32px;text-align:right;border-bottom:1px solid rgba(255,255,255,.14)">{close}</td>'
        f'<td style="padding:22px 20px;font-size:30px;text-align:right;color:{c};border-bottom:1px solid rgba(255,255,255,.14)">{pt}</td>'
        f'<td style="padding:22px 20px;font-size:32px;font-weight:800;text-align:right;color:{c};border-bottom:1px solid rgba(255,255,255,.14)">{pct}</td></tr>'
        for n, close, pt, pct, c in rows
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:90px 80px">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">10/8 뉴욕증시 마감 비교</div>
<div style="font-size:24px;color:#cfd3d4;margin-bottom:50px">전일(10/7) 대비</div>
<table style="width:100%;border-collapse:collapse">
<thead><tr>
<th style="text-align:left;padding:14px 20px;font-size:22px;color:#cfd3d4;border-bottom:2px solid rgba(255,255,255,.3)">지수</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#cfd3d4;border-bottom:2px solid rgba(255,255,255,.3)">종가</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#cfd3d4;border-bottom:2px solid rgba(255,255,255,.3)">전일비</th>
<th style="text-align:right;padding:14px 20px;font-size:22px;color:#cfd3d4;border-bottom:2px solid rgba(255,255,255,.3)">등락률</th>
</tr></thead>
<tbody>{trs}</tbody>
</table>
<div style="margin-top:60px;background:rgba(217,184,114,.1);border-left:6px solid {ACCENT};border-radius:0 14px 14px 0;padding:26px 30px;font-size:24px;line-height:1.6;color:#f2f2f2">다우만 소폭 상승, S&amp;P·나스닥은 이틀 연속 약세 — AI·반도체 쪽만 집중적으로 눌린 하루</div>
<div style="position:absolute;bottom:50px;left:80px;font-size:20px;color:#9aa0a3">합성 데이터 그래픽 · 뉴스핌·머니투데이·야후파이낸스 교차 확인 기준 정리</div>
</div>"""

# --- body-2: 핵심 포인트 카드 (반도체 대형주) ---
def chip_cards():
    cards = [
        ("필라델피아 반도체지수", "-3.39% ~ -4%", DOWN),
        ("엔비디아", "-2.24% ~ -2.94%", DOWN),
        ("TSMC", "약 -3%", DOWN),
        ("브로드컴", "약 -4%", DOWN),
        ("AMD", "-3.90% ~ -4%", DOWN),
        ("마이크론", "-5% 이상", DOWN),
        ("인텔", "-5.34%", DOWN),
        ("SK하이닉스 ADR", "-4.34%", DOWN),
    ]
    grid = "".join(
        f'<div style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:30px 26px">'
        f'<div style="font-size:23px;color:#e4d3b2;margin-bottom:16px">{name}</div>'
        f'<div style="font-size:36px;font-weight:800;color:{color}">{pct}</div></div>'
        for name, pct, color in cards
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:90px 80px">
<div style="font-size:42px;font-weight:800;margin-bottom:12px">반도체 대형주 일제히 급락 (10/8)</div>
<div style="font-size:24px;color:#cfd3d4;margin-bottom:44px">오픈AI 매출 쇼크 여파 · 소스별 수치 차이는 범위로 표기</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">{grid}</div>
<div style="position:absolute;bottom:50px;left:80px;font-size:20px;color:#9aa0a3">합성 데이터 그래픽 · 10/8 마감 기준, 소스 간 소수점 차이 있음</div>
</div>"""

# --- body-3: 인용/강조 박스 (유가) ---
def oil_quote():
    tiles = "".join(
        f'<div style="background:rgba(255,255,255,.06);border-radius:14px;padding:28px 30px">'
        f'<div style="font-size:21px;color:#cfd3d4;margin-bottom:10px">{label}</div>'
        f'<div style="font-size:32px;font-weight:800;color:{UP}">{val}</div></div>'
        for label, val in [
            ("브렌트유", "104.28달러 (+4.1%)"),
            ("WTI유", "91.49달러 (+3.6%)"),
        ]
    )
    return f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:90px 80px">
<div style="font-size:42px;font-weight:800;margin-bottom:46px">유가, 하루 만에 4%대 급등</div>
<div style="border-left:6px solid {ACCENT};background:rgba(217,184,114,.1);border-radius:0 16px 16px 0;padding:36px 44px;margin-bottom:44px">
<div style="font-size:28px;line-height:1.7;color:#f2f2f2">"호르무즈 해협 긴장과 허리케인발<br>공급 차질이 겹쳤다"</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:40px">{tiles}</div>
<div style="font-size:24px;line-height:1.6;color:#cfd3d4">10년물 국채금리 5.23%(-0.05%p) · 30년물 5.61%</div>
<div style="position:absolute;bottom:50px;left:80px;font-size:20px;color:#9aa0a3">합성 데이터 그래픽 · 10/8 마감 기준</div>
</div>"""

jobs = {
    "thumbnail.png": THUMB,
    "body-1.png": index_table(),
    "body-2.png": chip_cards(),
    "body-3.png": oil_quote(),
}

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1080})
    for name, html in jobs.items():
        pg.set_content(BASE % html)
        pg.screenshot(path=str(here.parent / name), full_page=False)
        print("saved", name)
    b.close()
