from playwright.sync_api import sync_playwright
import pathlib

here = pathlib.Path(__file__).parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#f2f2f2}
.stage{position:relative;overflow:hidden}
</style></head><body>%s</body></html>"""

# 슬레이트-그레이 팔레트 (최근 썸네일과 겹치지 않도록 선택)
THUMB = """<div class="stage" style="width:1080px;height:1080px;background:linear-gradient(160deg,#232526 0%,#3a3d40 100%);text-align:left">
<div style="position:absolute;top:96px;left:90px;padding:12px 28px;border:1px solid rgba(255,255,255,.25);border-radius:6px;font-size:26px;font-weight:600">오늘 미장 정리 · 10/6</div>
<div style="position:absolute;top:300px;left:90px;right:90px;font-size:80px;font-weight:800;line-height:1.25">3대 지수 상승<br>S&amp;P 500 사상 최고</div>
<div style="position:absolute;top:660px;left:90px;right:90px;font-size:30px;color:#cfd3d6;line-height:1.5">10년물 금리 5.275%, 장중 5.3% 돌파 후 하락 마감</div>
<div style="position:absolute;bottom:0;right:0;width:260px;height:14px;background:#9fb3c8"></div>
</div>"""

def bar_card(title, rows, note):
    items = "".join(
        f'<div style="display:flex;align-items:center;margin:18px 0"><div style="width:230px;font-size:28px;color:#dfe3e6">{n}</div>'
        f'<div style="flex:1;height:44px;background:rgba(255,255,255,.08);border-radius:4px;position:relative">'
        f'<div style="position:absolute;left:{0 if v>=0 else 50 + v*0.4}%;width:{abs(v)*0.4}%;top:0;bottom:0;background:{c};border-radius:4px"></div></div>'
        f'<div style="width:190px;text-align:right;font-size:28px;font-weight:700;color:{c}">{t}</div></div>'
        for n, v, c, t in rows)
    return f"""<div class="stage" style="width:1080px;height:1080px;background:#1c1f21;padding:90px 80px">
<div style="font-size:44px;font-weight:800;margin-bottom:40px">{title}</div>{items}
<div style="position:absolute;bottom:60px;left:80px;font-size:22px;color:#8d969c">합성 데이터 그래픽 · 출처 기사 기준 정리 · {note}</div></div>"""

def index_card():
    rows = [("S&P 500", 0.58, "#ff6b6b", "+0.58%"),
            ("나스닥 종합", 0.45, "#ff6b6b", "+0.45%"),
            ("다우 산업평균", 0.49, "#ff6b6b", "+0.49%")]
    return bar_card("미국 3대 지수 등락률 (10/6 마감)", rows, "상승=빨강 (국장 표기 관례)")

def yield_card():
    return """<div class="stage" style="width:1080px;height:1080px;background:#1c1f21;padding:110px 90px">
<div style="font-size:44px;font-weight:800;margin-bottom:60px">미 10년물 국채금리 (10/6)</div>
<div style="border-left:6px solid #9fb3c8;background:rgba(159,179,200,.10);padding:48px 56px;border-radius:6px">
<div style="font-size:30px;color:#cfd3d6;margin-bottom:18px">마감</div>
<div style="font-size:120px;font-weight:800;line-height:1">5.275%</div>
<div style="font-size:30px;color:#9fb3c8;margin-top:16px">전일 대비 -3.6bp</div></div>
<div style="margin-top:56px;font-size:34px;line-height:1.6;color:#dfe3e6">장중에는 5.3%를 넘어 2002년 이후 최고 수준 근처까지 올랐어요.</div>
<div style="position:absolute;bottom:60px;left:90px;font-size:22px;color:#8d969c">합성 데이터 그래픽 · 출처 기사 기준 정리</div></div>"""

def point_card():
    pts = [("1", "S&P 500 종가 7,818.93", "전일 대비 +0.58%, 종가 기준 사상 최고"),
           ("2", "기술주 강세가 지수 견인", "반도체 종목 강세 보도 다수"),
           ("3", "유가 숫자는 제외", "출처 날짜가 섞여 확정 불가")]
    items = "".join(
        f'<div style="display:flex;gap:30px;margin:34px 0;padding:34px 36px;background:rgba(255,255,255,.05);border-radius:8px">'
        f'<div style="font-size:60px;font-weight:800;color:#9fb3c8;width:60px">{n}</div>'
        f'<div><div style="font-size:38px;font-weight:700;margin-bottom:10px">{h}</div>'
        f'<div style="font-size:26px;color:#aab3b9">{d}</div></div></div>'
        for n, h, d in pts)
    return f"""<div class="stage" style="width:1080px;height:1080px;background:#1c1f21;padding:90px 80px">
<div style="font-size:44px;font-weight:800">오늘 핵심 포인트 3가지</div>{items}
<div style="position:absolute;bottom:60px;left:80px;font-size:22px;color:#8d969c">합성 데이터 그래픽 · 출처 기사 기준 정리</div></div>"""

jobs = {"thumbnail.png": THUMB, "body-1.png": index_card(), "body-2.png": yield_card(), "body-3.png": point_card()}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1080})
    for name, html in jobs.items():
        pg.set_content(BASE % html)
        pg.screenshot(path=str(here.parent / name), full_page=False)
        print("saved", name)
    b.close()
