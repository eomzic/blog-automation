from playwright.sync_api import sync_playwright
import pathlib
out = pathlib.Path(__file__).parent.parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#fde8e8}
table{border-collapse:collapse;width:100%%}
td,th{padding:18px 16px;font-size:28px;text-align:right}
td:first-child,th:first-child{text-align:left}
</style></head><body>%s</body></html>"""
DOWN="#8db4ff"; UP="#ff8080"; MUTED="#e0b4b4"; ACC="#f5a97a"
BG="linear-gradient(170deg,#2d0a0a 0%,#4a1414 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.15)"
TH=f"border-bottom:2px solid {ACC};color:{ACC}"
def stage(inner,h):
    return f'<div style="position:relative;width:1080px;height:{h}px;background:{BG};padding:0 70px 30px;display:flex;flex-direction:column;justify-content:center;border-top:10px solid {ACC}">{inner}<div style="position:absolute;bottom:14px;right:70px;font-size:19px;color:#b48a8a">합성 데이터 그래픽 · 10/29 기준</div></div>'
def title(t): return f'<div style="font-size:42px;font-weight:800;margin-bottom:30px;color:#fff">{t}</div>'
def row(cells,th=False):
    st=TH if th else LINE; tag="th" if th else "td"
    return "<tr>"+"".join(f'<{tag} style="{st};{c[1] if isinstance(c,tuple) else ""}">{c[0] if isinstance(c,tuple) else c}</{tag}>' for c in cells)+"</tr>"
def n(v):
    c=UP if v.startswith("+") else DOWN
    return (v,f"color:{c};font-weight:700")
def card(l,v,sub,c):
    return f'<div style="background:rgba(0,0,0,.25);border-radius:6px;padding:26px 30px;border-left:6px solid {ACC}"><div style="font-size:26px;color:{MUTED}">{l}</div><div style="font-size:52px;font-weight:900;color:{c};margin-top:8px">{v}</div><div style="font-size:24px;color:{MUTED};margin-top:6px">{sub}</div></div>'
def item(k,h,b):
    return f'<div style="display:flex;align-items:flex-start;margin-bottom:20px"><div style="min-width:120px;font-size:26px;font-weight:800;color:{ACC};padding-top:6px">{k}</div><div><div style="font-size:30px;font-weight:800;color:#fff">{h}</div><div style="font-size:24px;color:{MUTED};margin-top:4px">{b}</div></div></div>'
THUMB=f"""<div style="position:relative;width:1080px;height:1080px;background:{BG}">
<div style="position:absolute;top:80px;left:0;right:0;text-align:center"><span style="background:{ACC};color:#2d0a0a;font-size:34px;font-weight:900;padding:10px 30px;border-radius:6px">10/29 국장 정리</span></div>
<div style="position:absolute;top:250px;left:0;right:0;text-align:center;font-size:84px;font-weight:800;color:#fff;line-height:1.3">6,000선 하루 만에 반납<br>코스피 5,937</div>
<div style="position:absolute;top:560px;left:0;right:0;text-align:center;font-size:210px;font-weight:900;color:{DOWN};line-height:1">-1.24%</div>
<div style="position:absolute;top:840px;left:0;right:0;text-align:center;font-size:38px;color:{MUTED}">삼성전자 -4.13% · 코스닥 -2.34%</div>
<div style="position:absolute;bottom:0;left:0;right:0;height:26px;background:{ACC}"></div></div>"""
B1=stage(title("삼성전자 3분기 확정 실적")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'+
 card("매출","195조 2,532억","전년 대비 +126.9%",UP)+card("영업이익","107조 4,405억","전년 대비 +783.1%",UP)+
 card("영업이익률(계산)","약 55%","기사 수치로 직접 계산",'#fff')+card("주가 반응","-4.13%","232,000원 · 주주환원 세부안 연기",DOWN)+'</div>',640)
B2=stage(title("10/29 지수 마감")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'+
 card("코스피","5,937.66","-74.78p · 전일 6,012.44",DOWN)+card("코스닥","753.23","-18.05p · -2.34%",DOWN)+
 card("코스피 장중 고점","6,100.11","시가 6,017.22",UP)+card("코스피 장중 저점","5,817.92","-3.24% · 일중 변동폭 약 4.7%",DOWN)+'</div>',640)
B3=stage(title("주요 종목 종가·등락률 (10/29)")+'<table>'+row(["종목","종가","등락률"],True)+
 row(["SK스퀘어","-",n("+3.47%")])+row(["SK하이닉스","1,526,000원",n("+2.62%")])+row(["KB금융","-",n("+1.82%")])+
 row(["삼성전자","232,000원",n("-4.13%")])+row(["에코프로","-",n("-4.43%")])+row(["에코프로비엠","-",n("-5.64%")])+row(["레인보우로보틱스","-",n("-6.55%")])+row(["LG에너지솔루션","-",n("-8.60%")])+'</table>',960)
B4=stage(title("투자자별 수급 – 시점별 스냅샷")+'<table>'+row(["코스피","10:52","14:20"],True)+
 row(["외국인",n("+4,128억"),n("-1,683억")])+row(["기관",n("-3,080억"),n("-7,956억")])+row(["개인",n("-1,954억"),n("+7,716억")])+'</table><div style="font-size:25px;color:'+MUTED+';margin-top:24px">마감 확정치 아님 · 출처: 머니투데이 · 파이낸셜뉴스</div>',620)
B5=stage(title("체크할 일정과 변수")+
 item("오늘 밤","9월 PCE · 3분기 GDP 속보치","한국시간 21:30 발표 예정")+
 item("미국","알파벳 시간외 급락","EPS·매출 하회, 잉여현금흐름 91억달러 적자")+
 item("연준","12월 인상 확률 85.0%","CME 페드워치, 전날 78.3%")+
 item("내년 1월","삼성전자 잔여 주주환원","이사회에서 발표 예정"),700)
jobs=[("thumbnail",THUMB,1080),("body-1",B1,640),("body-2",B2,640),("body-3",B3,960),("body-4",B4,620),("body-5",B5,700)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,html,h in jobs:
        pg=b.new_page(viewport={"width":1080,"height":h}); pg.set_content(BASE%html); pg.screenshot(path=str(out/f"{name}.png")); pg.close()
    b.close()
