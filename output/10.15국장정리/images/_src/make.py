from playwright.sync_api import sync_playwright
import pathlib
out = pathlib.Path(__file__).parent.parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#eef0f6}
.stage{position:relative;overflow:hidden}
table{border-collapse:collapse;width:100%%}
td,th{padding:20px 16px;font-size:30px;text-align:right}
td:first-child,th:first-child{text-align:left}
</style></head><body>%s</body></html>"""
DOWN="#6fa0ff"; UP="#ff6b6b"; MUTED="#b8bbd6"; ACC="#b79cff"
BG="linear-gradient(135deg,#1a1a2e 0%,#16213e 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.14)"
TH=f"border-bottom:2px solid rgba(255,255,255,.3);color:{MUTED}"
def stage(inner,h,pad="0 70px"):
    return f'<div class="stage" style="width:1080px;height:{h}px;background:{BG};padding:{pad};display:flex;flex-direction:column;justify-content:center">{inner}<div style="position:absolute;bottom:30px;left:70px;font-size:19px;color:#8b8fb0">합성 데이터 그래픽 · 10/15 마감 기준 정리</div></div>'
def title(t): return f'<div style="font-size:42px;font-weight:800;margin-bottom:30px;color:#fff">{t}</div>'
THUMB=f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};text-align:center">
<div style="margin-top:100px"><span style="background:{ACC};color:#1a1a2e;font-size:30px;font-weight:800;padding:10px 28px;border-radius:30px">국장 정리 · 10/15</span></div>
<div style="margin-top:80px;font-size:84px;font-weight:900;color:#fff;line-height:1.25">서킷브레이커<br>발동</div>
<div style="margin-top:50px;font-size:230px;font-weight:900;color:{DOWN};line-height:1">-7.57%</div>
<div style="margin-top:50px;font-size:44px;font-weight:700;color:{MUTED};line-height:1.5">코스피 5,554.22 · 코스닥 760.82(-7.65%)</div>
<div style="margin-top:14px;font-size:36px;color:{MUTED}">외국인 코스피 3조 6,243억원 순매도</div></div>"""
def row(cells,th=False):
    st=TH if th else LINE; tag="th" if th else "td"
    return "<tr>"+"".join(f'<{tag} style="{st};{c[1] if isinstance(c,tuple) else ""}">{c[0] if isinstance(c,tuple) else c}</{tag}>' for c in cells)+"</tr>"
def n(v):
    c=UP if v.startswith("+") else DOWN
    return (v,f"color:{c};font-weight:700")
def step(i,t,s):
    return f'<div style="display:flex;align-items:center;gap:24px;background:rgba(255,255,255,.07);border-radius:16px;padding:22px 28px;margin-bottom:16px"><div style="min-width:104px;font-size:30px;font-weight:900;color:{ACC}">{i}</div><div><div style="font-size:33px;font-weight:800;color:#fff">{t}</div><div style="font-size:24px;color:{MUTED};margin-top:4px">{s}</div></div></div>'
B1=stage(title("10/15 장 중단 타임라인")+
 step("09:07","코스피 매도 사이드카","개장 5,673.01 (-5.59%)")+
 step("09:12","코스닥 매도 사이드카","프로그램 매도호가 5분 효력정지")+
 step("12:23","코스닥 1단계 서킷브레이커","-8.01%, 20분 거래 중단")+
 step("12:38","코스피 1단계 서킷브레이커","5,528.05 (-8.00%), 7/29 이후 78일 만")+
 step("마감","코스피 5,554.22 (-7.57%)","장중 저점 5,506.23 (-8.36%)"),980)
def card(l,v,c="#fff"):
    return f'<div style="background:rgba(255,255,255,.07);border-radius:16px;padding:24px 28px"><div style="font-size:25px;color:{MUTED}">{l}</div><div style="font-size:48px;font-weight:800;color:{c};margin-top:6px">{v}</div></div>'
B2=stage(title("간밤 미국 (10/14 현지)")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">'+
 card("9월 CPI (전년비)","3.7%",UP)+card("시장 예상 / 8월","3.6% / 3.4%")+
 card("나스닥","-1.88%",DOWN)+card("필라델피아 반도체","-4.30%",DOWN)+
 card("S&P500","-1.11%",DOWN)+card("코어위브","-15.46%",DOWN)+'</div>'+
 f'<div style="margin-top:26px;font-size:26px;line-height:1.6;color:{MUTED}">10월 금리 인상 확률 22.1% → 51.5% → 30%대<br>마이크론 -3.88% · 샌디스크 -5.97% · 하이닉스 ADR -4.02%</div>',860)
B3=stage(title("주요 종목 등락 (10/15 종가)")+'<table>'+row(["종목","종가","등락률"],True)+
 row(["삼성전자","210,000원",n("-9.48%")])+row(["SK하이닉스","1,262,000원",n("-11.06%")])+
 row(["삼성전기","1,163,000원",n("-15.36%")])+row(["삼성바이오로직스","1,247,000원",n("+5.50%")])+
 row(["주성엔지니어링(코스닥)","204,500원",n("-14.97%")])+row(["LG에너지솔루션","—",n("-4.62%")])+'</table>',920)
B4=stage(title("투자자별 순매수(+)·순매도(-)")+'<table>'+row(["구분","코스피","코스닥"],True)+
 row(["외국인",n("-3조 6,243억"),n("+2,158억")])+row(["기관",n("+1조 6,932억"),n("-1,631억")])+
 row(["개인",n("+1조 2,887억"),n("-669억")])+'</table>'+
 f'<div style="margin-top:26px;font-size:26px;color:{MUTED}">코스피 외국인 7거래일 연속 순매도</div>',780)
jobs=[("thumbnail",THUMB,1080),("body-1",B1,980),("body-2",B2,860),("body-3",B3,920),("body-4",B4,780)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,html,h in jobs:
        pg=b.new_page(viewport={"width":1080,"height":h}); pg.set_content(BASE%html); pg.screenshot(path=str(out/f"{name}.png")); pg.close()
    b.close()
