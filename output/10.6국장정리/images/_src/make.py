from playwright.sync_api import sync_playwright
import pathlib

here = pathlib.Path(__file__).parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#f2f2f2}
.stage{position:relative;overflow:hidden}
</style></head><body>%s</body></html>"""

THUMB = """<div class="stage" style="width:1080px;height:1080px;background:linear-gradient(160deg,#0f2027 0%,#134e4a 100%);text-align:center">
<div style="position:absolute;top:96px;left:50%;transform:translateX(-50%);padding:12px 28px;border:1px solid rgba(255,255,255,.25);border-radius:6px;font-size:26px;font-weight:600">오늘 국장 정리 · 10/6</div>
<div style="position:absolute;top:330px;left:90px;right:90px;font-size:84px;font-weight:800;line-height:1.25">코스피 7,000선 아래<br>코스닥은 3% 급등</div>
<div style="position:absolute;top:700px;left:90px;right:90px;font-size:30px;color:#bfe6df;line-height:1.5">연휴 끝 첫 거래일 · 외국인 1.7조 순매도</div>
<div style="position:absolute;bottom:0;left:0;right:0;height:14px;background:#5fd1b8"></div>
</div>"""

def bar_card(title, rows):
    items = "".join(
        f'<div style="display:flex;align-items:center;margin:18px 0"><div style="width:230px;font-size:28px;color:#dfe9e7">{n}</div>'
        f'<div style="flex:1;height:44px;background:rgba(255,255,255,.08);border-radius:4px;position:relative">'
        f'<div style="position:absolute;left:{0 if v>=0 else 50 + v*0.4}%;width:{abs(v)*0.4 if v>=0 else abs(v)*0.4}%;top:0;bottom:0;background:{c};border-radius:4px"></div></div>'
        f'<div style="width:150px;text-align:right;font-size:28px;font-weight:700;color:{c}">{t}</div></div>'
        for n, v, c, t in rows)
    return f"""<div class="stage" style="width:1080px;height:1080px;background:#0b1d22;padding:90px 80px">
<div style="font-size:44px;font-weight:800;margin-bottom:40px">{title}</div>{items}
<div style="position:absolute;bottom:60px;left:80px;font-size:22px;color:#7fa6a0">합성 데이터 그래픽 · 출처 기사 기준 정리</div></div>"""

def index_card():
    rows = [("코스피", -0.89, "#6fa8ff", "-0.89%"), ("코스닥", 2.98, "#ff6b6b", "+2.98%")]
    return bar_card("지수 등락률 (10/6 마감)", rows)

def flow_card():
    rows = [("외국인", -17.5, "#6fa8ff", "-1.75조"), ("기관", 10.1, "#ff6b6b", "+1조대*"), ("개인", 7.4, "#ff6b6b", "+7,000억대")]
    return bar_card("투자자별 순매수 (코스피)", rows) + "<!-- *소스별 차이 있음 -->"

def sector_card():
    rows = [("의료·정밀기기", 6.5, "#ff6b6b", "+6.53%"), ("화학", 1.6, "#ff6b6b", "+1.59%"),
            ("제약", -1.1, "#6fa8ff", "-1.09%"), ("전기전자", -1.3, "#6fa8ff", "-1.31%"),
            ("운수장비·부품", -1.4, "#6fa8ff", "-1.43%")]
    return bar_card("업종 등락률 (코스피, 10/6)", rows)

jobs = {"thumbnail.png": THUMB, "body-1.png": index_card(), "body-2.png": flow_card(), "body-3.png": sector_card()}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1080})
    for name, html in jobs.items():
        pg.set_content(BASE % html)
        pg.screenshot(path=str(here.parent / name), full_page=False)
        print("saved", name)
    b.close()
