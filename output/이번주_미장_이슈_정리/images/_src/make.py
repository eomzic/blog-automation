from playwright.sync_api import sync_playwright
import pathlib

out = pathlib.Path(__file__).parent.parent

BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#eef0fa}
</style></head><body>%s</body></html>"""

# ---- 팔레트: 네이비-퍼플 (하락·약세 마감용) ----
BG   = "linear-gradient(160deg,#1a1a2e 0%,#16213e 100%)"
TEXT = "#eef0fa"
MUTED = "#9a9dc2"
MUTED2 = "#6e7196"
ACC  = "#c4b5fd"   # 라벤더 — 최근 썸네일(peach/yellow/teal/mint)과 겹치지 않는 액센트
ACC2 = "#8b7fd6"
UP   = "#ff7373"   # 상승=빨강 (관례 고정)
DOWN = "#7aa8ff"   # 하락=파랑 (관례 고정)
NEUTRAL = "#8d90ad"

def stage(inner, h, pad="70px"):
    return (f'<div style="position:relative;width:1080px;height:{h}px;background:{BG};'
            f'padding:0 {pad};display:flex;flex-direction:column;justify-content:center;'
            f'border-left:12px solid {ACC};overflow:hidden">'
            f'<div style="position:absolute;top:0;left:0;width:100%;height:100%;'
            f'background:radial-gradient(circle at 88% 12%, rgba(196,181,253,.16), transparent 55%)"></div>'
            f'{inner}'
            f'<div style="position:absolute;bottom:22px;right:70px;font-size:18px;color:{MUTED2}">'
            f'합성 데이터 그래픽 · 10/23 기준(일부 추정치 포함)</div></div>')

def badge(text, color=ACC):
    return (f'<div style="display:inline-block;border:2px solid {color};color:{color};'
            f'font-size:23px;font-weight:800;padding:8px 22px;border-radius:40px;'
            f'margin-bottom:24px;letter-spacing:.3px">{text}</div>')

def title(t):
    return f'<div style="font-size:38px;font-weight:800;margin-bottom:26px;color:#fff;line-height:1.3">{t}</div>'

def stat_card(label, value, note="", value_color=TEXT, accent=ACC):
    note_html = (f'<div style="font-size:19px;color:{MUTED};margin-top:12px;line-height:1.55">{note}</div>'
                 if note else '')
    return (f'<div style="flex:1;background:rgba(255,255,255,.06);border-radius:18px;padding:28px 24px;'
            f'border-top:5px solid {accent}">'
            f'<div style="font-size:21px;color:{MUTED};font-weight:700">{label}</div>'
            f'<div style="font-size:36px;font-weight:800;color:{value_color};margin-top:10px;line-height:1.25">{value}</div>'
            f'{note_html}</div>')

def pt(h, b, accent=ACC):
    return (f'<div style="background:rgba(255,255,255,.06);border-radius:16px;padding:20px 26px;'
            f'margin-bottom:14px;border-left:6px solid {accent}">'
            f'<div style="font-size:26px;font-weight:800;color:#fff">{h}</div>'
            f'<div style="font-size:21px;color:{MUTED};margin-top:7px;line-height:1.55">{b}</div></div>')

def timeline_node(date, value, value_color, note, filled=True):
    dot = (f'background:{value_color};border:none' if filled
           else f'background:transparent;border:3px dashed {MUTED2}')
    val_html = (f'<div style="font-size:30px;font-weight:800;color:{value_color};margin-top:6px">{value}</div>'
                if filled else f'<div style="font-size:22px;color:{MUTED2};margin-top:6px">{value}</div>')
    return (f'<div style="display:flex;gap:22px;align-items:flex-start">'
            f'<div style="display:flex;flex-direction:column;align-items:center">'
            f'<div style="width:22px;height:22px;border-radius:50%;{dot};flex-shrink:0;margin-top:6px"></div>'
            f'<div style="width:3px;flex:1;background:rgba(255,255,255,.14);margin-top:4px"></div></div>'
            f'<div style="padding-bottom:26px">'
            f'<div style="font-size:21px;color:{MUTED};font-weight:700">{date}</div>'
            f'{val_html}'
            f'<div style="font-size:20px;color:{MUTED};margin-top:6px;line-height:1.5;max-width:720px">{note}</div>'
            f'</div></div>')

def step_item(date, label, items, hl=False):
    border = ACC if hl else "rgba(255,255,255,.18)"
    bg = "rgba(196,181,253,.10)" if hl else "rgba(255,255,255,.05)"
    return (f'<div style="display:flex;gap:24px;align-items:center;background:{bg};'
            f'border:1.5px solid {border};border-radius:16px;padding:22px 26px;margin-bottom:16px">'
            f'<div style="min-width:150px;font-size:23px;font-weight:800;color:{ACC}">{date}</div>'
            f'<div style="flex:1">'
            f'<div style="font-size:25px;font-weight:800;color:#fff">{label}</div>'
            f'<div style="font-size:19px;color:{MUTED};margin-top:5px">{items}</div></div></div>')

# =========================================================
# THUMBNAIL — 1080x1080, 주간 특집 레이아웃 (요일별 미니 바 차트 포함)
# =========================================================
days = [("월", 1.11, UP), ("화", -0.02, DOWN), ("수", 0.05, NEUTRAL), ("목", -2.60, DOWN), ("금", -1.5, DOWN)]
SCALE = 40  # px per %
ZONE = 130
bars_html = ""
for d, v, c in days:
    h = max(abs(v) * SCALE, 14)
    if v >= 0:
        bar = (f'<div style="height:{ZONE}px;display:flex;align-items:flex-end;justify-content:center">'
               f'<div style="width:50px;height:{h:.0f}px;background:{c};border-radius:8px 8px 2px 2px"></div></div>')
    else:
        bar = (f'<div style="height:{ZONE}px;display:flex;align-items:flex-start;justify-content:center">'
               f'<div style="width:50px;height:{h:.0f}px;background:{c};border-radius:2px 2px 8px 8px"></div></div>')
    label_v = f'{v:+.2f}%' if d not in ("수","금") else ("약보합" if d=="수" else "약 -1~2%")
    bars_html += (f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px;flex:1">'
                  f'<div style="font-size:15px;color:{MUTED2};height:18px;white-space:nowrap">{label_v if d=="월" or d=="목" else ""}</div>'
                  f'{bar}'
                  f'<div style="width:36px;height:2px;background:rgba(255,255,255,.25)"></div>'
                  f'<div style="font-size:20px;font-weight:700;color:{TEXT}">{d}</div></div>')

THUMB = f"""<div style="position:relative;width:1080px;height:1080px;background:{BG};padding:90px 90px 70px;display:flex;flex-direction:column">
<div style="position:absolute;top:0;left:0;width:100%;height:100%;background:radial-gradient(circle at 90% 8%, rgba(196,181,253,.18), transparent 50%)"></div>
{badge("WEEKLY RECAP · 10.19 ~ 10.23")}
<div style="font-size:30px;color:{MUTED};font-weight:700;margin-bottom:4px">나스닥 주간</div>
<div style="font-size:160px;font-weight:900;color:{DOWN};line-height:1">-4.5%</div>
<div style="margin-top:26px;font-size:50px;font-weight:900;color:#fff;line-height:1.3">6월 이후 최악의 한 주</div>
<div style="margin-top:46px;font-size:22px;color:{MUTED};font-weight:700">나스닥 요일별 등락</div>
<div style="margin-top:14px;background:rgba(255,255,255,.05);border-radius:20px;padding:26px 24px 18px;display:flex;justify-content:space-between;align-items:flex-end">
{bars_html}
</div>
<div style="margin-top:56px;display:flex;gap:16px">
<div style="flex:1;background:rgba(255,255,255,.05);border-radius:16px;padding:20px 22px"><div style="font-size:19px;color:{MUTED2};font-weight:700">S&amp;P500 주간</div><div style="font-size:30px;font-weight:800;color:{DOWN};margin-top:4px">-1.9%</div></div>
<div style="flex:1;background:rgba(255,255,255,.05);border-radius:16px;padding:20px 22px"><div style="font-size:19px;color:{MUTED2};font-weight:700">다우 주간</div><div style="font-size:30px;font-weight:800;color:{UP};margin-top:4px">+0.7%</div></div>
</div>
<div style="flex:1"></div>
<div style="font-size:21px;color:{MUTED2};font-weight:600">월~수 되돌림 랠리 → 목 메타·테슬라 실적 후 재급락</div>
<div style="position:absolute;right:0;top:0;width:14px;height:1080px;background:{ACC}"></div>
</div>"""

# =========================================================
# BODY 1 — 요일별 나스닥·S&P500·다우 등락 흐름 (꺾은선 그래픽)
# =========================================================
minV, maxV = -3.2, 1.6
plotH = 300
def yof(v):
    return 10 + (maxV - v) / (maxV - minV) * plotH
xs = [60, 255, 450, 645, 840]
nd = [1.11, -0.02, 0.05, -2.60, -1.5]
sp = [0.41, 0.28, 0.30, -1.21, -1.0]
dw = [-0.07, 1.02, 1.00, 0.02, None]
y0 = yof(0)

def poly(vals, color, dash_last=False):
    pts_solid = [(xs[i], yof(v)) for i, v in enumerate(vals) if v is not None]
    segs = ""
    n = len(pts_solid)
    for i in range(n - 1):
        x1, y1 = pts_solid[i]
        x2, y2 = pts_solid[i + 1]
        is_last = (i == n - 2)
        dash = 'stroke-dasharray="10,8"' if (is_last and dash_last) else ""
        segs += f'<line x1="{x1}" y1="{y1:.1f}" x2="{x2}" y2="{y2:.1f}" stroke="{color}" stroke-width="5" {dash} stroke-linecap="round"/>'
    dots = ""
    for i, (x, y) in enumerate(pts_solid):
        is_approx = dash_last and i == n - 1
        if is_approx:
            dots += f'<circle cx="{x}" cy="{y:.1f}" r="8" fill="{BGSOLID}" stroke="{color}" stroke-width="4" stroke-dasharray="4,3"/>'
        else:
            dots += f'<circle cx="{x}" cy="{y:.1f}" r="8" fill="{color}"/>'
    return segs + dots

BGSOLID = "#1a1a2e"
svg_lines = (
    f'<line x1="60" y1="{y0:.1f}" x2="840" y2="{y0:.1f}" stroke="rgba(255,255,255,.22)" stroke-width="2" stroke-dasharray="4,6"/>'
    + poly(nd, DOWN if False else "#ff9f7a", dash_last=True)  # 나스닥: 별도 색
)
# 색상 재정의: 나스닥=ACC(라벤더, 굵게 강조), S&P500=흰색 보조, 다우=DOWN 계열 톤 다운
NASDAQ_C = "#f6b64a"
SP_C = "#9aa0d6"
DOW_C = "#5fd6c0"
svg_lines = (
    f'<line x1="60" y1="{y0:.1f}" x2="840" y2="{y0:.1f}" stroke="rgba(255,255,255,.22)" stroke-width="2" stroke-dasharray="4,6"/>'
    + poly(sp, SP_C, dash_last=True)
    + poly(dw, DOW_C, dash_last=False)
    + poly(nd, NASDAQ_C, dash_last=True)
)
wk_labels = "".join(
    f'<text x="{x}" y="334" fill="{MUTED}" font-size="21" font-weight="700" text-anchor="middle">{d}</text>'
    for x, d in zip(xs, ["월","화","수","목","금"])
)
legend = (f'<div style="display:flex;gap:28px;margin-bottom:18px">'
          f'<div style="display:flex;align-items:center;gap:9px"><div style="width:22px;height:5px;background:{NASDAQ_C};border-radius:3px"></div><span style="font-size:20px;color:{TEXT};font-weight:700">나스닥</span></div>'
          f'<div style="display:flex;align-items:center;gap:9px"><div style="width:22px;height:5px;background:{SP_C};border-radius:3px"></div><span style="font-size:20px;color:{MUTED};font-weight:700">S&amp;P500</span></div>'
          f'<div style="display:flex;align-items:center;gap:9px"><div style="width:22px;height:5px;background:{DOW_C};border-radius:3px"></div><span style="font-size:20px;color:{MUTED};font-weight:700">다우</span></div>'
          f'</div>')

B1 = stage(
    badge("10.19 MON → 10.23 FRI") +
    title("이번 주 3대 지수, 요일별 흐름") +
    legend +
    f'<svg width="900" height="340" viewBox="0 0 900 340">{svg_lines}{wk_labels}</svg>' +
    f'<div style="margin-top:18px;font-size:19px;color:{MUTED2};line-height:1.6">점선 구간(수·금)은 "약보합/추정치" 표현을 그래프로 환산한 근사치 · 다우 금요일은 집계 전이라 표시하지 않음</div>',
    800
)

# =========================================================
# BODY 2 — 메타 vs 테슬라 capex 비교 카드
# =========================================================
def compare_card(name, pct, pct_color, rows, accent):
    rows_html = "".join(
        f'<div style="display:flex;justify-content:space-between;padding:13px 0;border-bottom:1px solid rgba(255,255,255,.12)">'
        f'<span style="font-size:19px;color:{MUTED}">{k}</span>'
        f'<span style="font-size:19px;color:{TEXT};font-weight:700;text-align:right;max-width:290px">{v}</span></div>'
        for k, v in rows
    )
    return (f'<div style="flex:1;background:rgba(255,255,255,.06);border-radius:18px;padding:26px 24px;border-top:5px solid {accent}">'
            f'<div style="font-size:25px;font-weight:800;color:#fff">{name}</div>'
            f'<div style="font-size:46px;font-weight:900;color:{pct_color};margin:8px 0 14px">{pct}</div>'
            f'{rows_html}</div>')

meta_card = compare_card("메타", "-7%대", DOWN, [
    ("3분기 매출", "646억달러 (+26.1%)"),
    ("2026 capex", "1,350~1,450억달러<br>(상향)"),
    ("장기 지출약정", "7,000억→8,250억달러"),
], "#f6b64a")

tesla_card = compare_card("테슬라", "-3~4%대", DOWN, [
    ("조정 EPS", "0.48달러 (예상 상회)"),
    ("2026 capex", '"200억달러 초과"<br>(하향)'),
    ("영업이익", "전년比 -56%"),
], "#5fd6c0")

B2 = stage(
    badge("10.21(수) 장마감 후 발표") +
    title("메타는 더 쓴다, 테슬라는 줄인다") +
    f'<div style="display:flex;gap:20px;position:relative">{meta_card}'
    f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);'
    f'background:{BGSOLID};border:2px solid {ACC};color:{ACC};font-weight:900;font-size:20px;'
    f'width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center">VS</div>'
    f'{tesla_card}</div>'
    f'<div style="margin-top:22px;font-size:19px;color:{MUTED};line-height:1.6">같은 날 밤, 정반대의 capex 메시지 — "더 쓰겠다"도 "덜 쓰겠다"도 둘 다 주가는 하락</div>',
    680
)

# =========================================================
# BODY 3 — CPI · FOMC · 브렌트유 핵심 포인트 카드
# =========================================================
B3 = stage(
    badge("겹친 변수들") +
    title("CPI 재점화 + 중동發 유가 급등") +
    f'<div style="display:flex;gap:18px">'
    + stat_card("9월 CPI (전년비)", "+3.7%", "근원 CPI +2.6% · 예상보다 뜨거운 물가", TEXT, "#f6b64a")
    + stat_card("FOMC 전망", "10월 동결", "100명 중 94명 동결 전망, 100명 전원 12월 인상 전망", TEXT, ACC)
    + stat_card("브렌트유", "113.17달러", "전일比 +4% · 5개월 최고 · 사우디 유전 드론 공격", DOWN, "#5fd6c0")
    + '</div>'
    + f'<div style="margin-top:24px;font-size:19px;color:{MUTED};line-height:1.6">"인하 기대"가 아니라 "동결 뒤 인상"이라는 낯선 조합 — 에너지엔 호재, 그 외 업종엔 물가·운송비 부담으로 해석</div>',
    560
)

# =========================================================
# BODY 4 — 코스피 종가 흐름 + 미국 이슈 연결 타임라인
# =========================================================
B4 = stage(
    badge("국내 연결") +
    title("코스피도 피하지 못한 한 주") +
    timeline_node("10/19 (일)", "+1.76%", UP, "코스피 5,768.01 — 지난주 급락분 되돌림 랠리 시작") +
    timeline_node("10/20 (화)", "-3.73%", DOWN, '코스피 5,552.74 — 키움증권 한지영 연구원 "주 후반 메타 실적 발표 경계" 경고') +
    timeline_node("10/21~23", "확인 전", "#ffffff", "이 글 작성 시점 미정리 · 목요일 밤 미국 급락을 감안하면 비슷한 영향권일 가능성", filled=False) +
    f'<div style="margin-top:4px;background:rgba(196,181,253,.10);border:1.5px solid {ACC};border-radius:14px;padding:18px 22px">'
    f'<div style="font-size:20px;color:{ACC};font-weight:800;margin-bottom:6px">💬 지난주 경고가 현실이 됐다</div>'
    f'<div style="font-size:19px;color:{MUTED};line-height:1.6">10/20 방산·조선·원전 테마 급반락이, 이번 주 미국의 "AI 테마 과열 되돌림"과 결이 비슷했어요.</div></div>',
    900
)

# =========================================================
# BODY 5 — 다음 주 일정 (FOMC·빅테크·삼성전자·SK하이닉스)
# =========================================================
B5 = stage(
    badge("다음 주 (10.26 ~ 11.2)") +
    title("이번엔 빅테크 + 국내 반도체 차례") +
    step_item("10/27~28", "FOMC 회의", "10/28(수) 오후 결과 발표") +
    step_item("10/28(수)", "알파벳 · 마이크로소프트 실적", "SK하이닉스 컨퍼런스콜 같은 날", hl=True) +
    step_item("10/29(목)", "아마존 실적", "삼성전자 실적(tentative) — 역대 최대 100조원대 영업이익 전망", hl=True) +
    step_item("11/2(월)", "애플 실적", "2026 회계연도 4분기"),
    760
)

jobs = [
    ("thumbnail", THUMB, 1080),
    ("body-1", B1, 800),
    ("body-2", B2, 680),
    ("body-3", B3, 560),
    ("body-4", B4, 900),
    ("body-5", B5, 760),
]

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, html, h in jobs:
        pg = b.new_page(viewport={"width": 1080, "height": h})
        pg.set_content(BASE % html)
        pg.screenshot(path=str(out / f"{name}.png"))
        pg.close()
    b.close()

print("done")
