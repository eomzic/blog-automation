from playwright.sync_api import sync_playwright
import pathlib
out = pathlib.Path(__file__).parent.parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#f1f1ef}
table{border-collapse:collapse;width:100%%}
td,th{padding:20px 16px;font-size:29px;text-align:right}
td:first-child,th:first-child{text-align:left}
</style></head><body>%s</body></html>"""
DOWN="#7aa8ff"; UP="#ff7373"; MUTED="#b9bbbd"; ACC="#f5c451"
BG="linear-gradient(160deg,#232526 0%,#3a3d40 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.15)"
TH=f"border-bottom:2px solid rgba(245,196,81,.55);color:{ACC}"
def stage(inner,h):
    return f'<div style="position:relative;width:1080px;height:{h}px;background:{BG};padding:0 70px;display:flex;flex-direction:column;justify-content:center;border-top:8px solid {ACC}">{inner}<div style="position:absolute;bottom:26px;right:70px;font-size:19px;color:#8d8f91">합성 데이터 그래픽 · 10/19 마감 기준</div></div>'
def title(t): return f'<div style="font-size:42px;font-weight:800;margin-bottom:30px;color:#fff">{t}</div>'
def row(cells,th=False):
    st=TH if th else LINE; tag="th" if th else "td"
    return "<tr>"+"".join(f'<{tag} style="{st};{c[1] if isinstance(c,tuple) else ""}">{c[0] if isinstance(c,tuple) else c}</{tag}>' for c in cells)+"</tr>"
def n(v):
    c=UP if v.startswith("+") else DOWN
    return (v,f"color:{c};font-weight:700")
def card(l,v,c="#fff"):
    return f'<div style="background:rgba(255,255,255,.07);border-radius:16px;padding:24px 28px;border-left:5px solid {ACC}"><div style="font-size:25px;color:{MUTED}">{l}</div><div style="font-size:44px;font-weight:800;color:{c};margin-top:6px">{v}</div></div>'
THUMB=f"""<div style="position:relative;width:1080px;height:1080px;background:{BG};text-align:center;padding-top:120px">
<div style="display:inline-block;background:{ACC};color:#232526;font-size:32px;font-weight:900;padding:12px 34px;border-radius:8px">국장 정리 · 10/19</div>
<div style="margin-top:90px;font-size:84px;font-weight:900;color:#fff;line-height:1.3">-3% 출발<br>→ 반전 마감</div>
<div style="margin-top:60px;font-size:200px;font-weight:900;color:{UP};line-height:1">+1.76%</div>
<div style="margin-top:60px;font-size:42px;font-weight:700;color:{MUTED}">코스피 5,768.01 · 코스닥 808.89</div>
<div style="margin-top:16px;font-size:36px;color:{MUTED}">기관 5,747억원 순매수가 받쳤다</div>
<div style="position:absolute;bottom:0;left:0;width:1080px;height:26px;background:{ACC}"></div></div>"""
B1=stage(title("코스피 시가 저점 vs 마감")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">'+
 card("시가(장중 저점)","5,488.41",DOWN)+card("마감","5,768.01",UP)+
 card("시가 등락","-179.64p (-3.17%)",DOWN)+card("마감 등락","+99.96p (+1.76%)",UP)+'</div>'+
 f'<div style="margin-top:26px;font-size:27px;line-height:1.7;color:{MUTED}">코스닥: 773.06(-2.73%) 출발 → 808.89(+1.78%) 마감<br>이달 코스피 누적 -17.11%</div>',720)
B2=stage(title("16일(현지) 미국 AI·반도체주")+'<table>'+row(["종목/지수","등락률"],True)+
 row(["필라델피아 반도체지수",n("-3.83%")])+row(["AMD",n("-5.95%")])+row(["마이크론",n("-5.63%")])+
 row(["SK하이닉스 ADR",n("-6.58%")])+row(["브로드컴",n("-4.52%")])+'</table>'+
 f'<div style="margin-top:22px;font-size:25px;color:{MUTED}">반도체지수 8거래일 연속 하락 · 브렌트유 109.86달러</div>',800)
B3=stage(title("투자자별 순매수(+)·순매도(-)")+'<table>'+row(["구분","코스피","코스닥"],True)+
 row(["기관",n("+5,747억"),n("+669억")])+row(["개인",n("-1조 862억"),n("+640억")])+
 row(["외국인",n("-379억"),n("-1,437억")])+row(["기타법인",n("+5,494억"),n("+143억")])+'</table>'+
 f'<div style="margin-top:24px;font-size:24px;color:{MUTED}">KRX 기준 · 외국인 금액은 매체별로 소폭 상이 (364억~381억)</div>',740)
B4=stage(title("주요 종목 종가 (10/19)")+'<table>'+row(["종목","종가","등락률"],True)+
 row(["삼성SDI","592,000원",n("+11.70%")])+row(["삼성바이오로직스","1,427,000원",n("+9.94%")])+
 row(["LG에너지솔루션","432,000원",n("+7.20%")])+row(["삼성전자","218,000원",n("+1.16%")])+
 row(["SK하이닉스","1,277,000원",n("+0.39%")])+row(["삼성전기","1,170,000원",n("-1.52%")])+'</table>',860)
jobs=[("thumbnail",THUMB,1080),("body-1",B1,720),("body-2",B2,800),("body-3",B3,740),("body-4",B4,860)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,html,h in jobs:
        pg=b.new_page(viewport={"width":1080,"height":h}); pg.set_content(BASE%html); pg.screenshot(path=str(out/f"{name}.png")); pg.close()
    b.close()
