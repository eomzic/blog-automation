from playwright.sync_api import sync_playwright
import pathlib
out = pathlib.Path(__file__).parent.parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#f1eaff}
table{border-collapse:collapse;width:100%%}
td,th{padding:18px 16px;font-size:28px;text-align:right}
td:first-child,th:first-child{text-align:left}
</style></head><body>%s</body></html>"""
DOWN="#7aa8ff"; UP="#ff7373"; MUTED="#c4b0e6"; ACC="#fbbf24"
BG="linear-gradient(160deg,#1e0a3c 0%,#3d1a5c 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.15)"
TH=f"border-bottom:2px solid rgba(251,191,36,.6);color:{ACC}"
def stage(inner,h):
    return f'<div style="position:relative;width:1080px;height:{h}px;background:{BG};padding:0 70px 20px;display:flex;flex-direction:column;justify-content:center;border-left:12px solid {ACC}">{inner}<div style="position:absolute;bottom:16px;right:70px;font-size:19px;color:#a38cc9">합성 데이터 그래픽 · 10/28 마감 기준</div></div>'
def title(t): return f'<div style="font-size:42px;font-weight:800;margin-bottom:30px;color:#fff">{t}</div>'
def row(cells,th=False):
    st=TH if th else LINE; tag="th" if th else "td"
    return "<tr>"+"".join(f'<{tag} style="{st};{c[1] if isinstance(c,tuple) else ""}">{c[0] if isinstance(c,tuple) else c}</{tag}>' for c in cells)+"</tr>"
def n(v):
    c=UP if v.startswith("+") else DOWN
    return (v,f"color:{c};font-weight:700")
def card(l,v,sub,c):
    return f'<div style="background:rgba(255,255,255,.08);border-radius:16px;padding:28px 30px;border-top:5px solid {ACC}"><div style="font-size:26px;color:{MUTED}">{l}</div><div style="font-size:54px;font-weight:900;color:{c};margin-top:8px">{v}</div><div style="font-size:24px;color:{MUTED};margin-top:6px">{sub}</div></div>'
def item(h,b):
    return f'<div style="display:flex;align-items:flex-start;margin-bottom:18px"><div style="width:44px;height:44px;border-radius:10px;border:3px solid {ACC};flex:none;margin-top:6px"></div><div style="margin-left:22px"><div style="font-size:30px;font-weight:800;color:#fff">{h}</div><div style="font-size:24px;color:{MUTED};margin-top:4px">{b}</div></div></div>'
THUMB=f"""<div style="position:relative;width:1080px;height:1080px;background:{BG};padding:120px 90px;border-left:16px solid {ACC}">
<div style="display:inline-block;background:{ACC};color:#1e0a3c;font-size:34px;font-weight:900;padding:10px 28px;border-radius:30px">10/28 국장 정리</div>
<div style="margin-top:90px;font-size:80px;font-weight:800;color:#fff;line-height:1.3">코스피 6,000선<br>10거래일 만에 탈환</div>
<div style="margin-top:60px;font-size:230px;font-weight:900;color:{UP};line-height:1">+6.63%</div>
<div style="margin-top:50px;font-size:38px;color:{MUTED}">SK하이닉스 +10.89% · 삼성전자 +9.01%</div></div>"""
B1=stage(title("10/28 지수 마감")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'+
 card("코스피","6,012.44","+374.10p · 전일 5,638.34",UP)+card("코스닥","771.28","+27.45p",UP)+
 card("코스피 등락률","+6.63%","10거래일 만의 6,000선",UP)+card("코스닥 등락률","+3.69%","환율 1,338.2원 (15:30)",UP)+'</div>',640)
B2=stage(title("SK하이닉스 3분기 실적")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'+
 card("매출","104조 6,155억","전분기 대비 +31.9%",UP)+card("영업이익","83조 3,338억","전분기 대비 +37.6%",UP)+
 card("영업이익률(계산)","약 79.7%","기사 수치로 직접 계산",'#fff')+card("주주환원","연 100조원 안팎","8월 40조 자사주 포함",ACC)+'</div>',640)
B3=stage(title("종목 종가·등락률 (10/28)")+'<table>'+row(["종목","종가","등락률"],True)+
 row(["SK스퀘어","921,000원",n("+11.23%")])+row(["삼성전자우","190,100원",n("+11.10%")])+row(["SK하이닉스","1,487,000원",n("+10.89%")])+
 row(["삼성전자","242,000원",n("+9.01%")])+row(["이수페타시스","-",n("+8.76%")])+row(["삼성전기","1,306,000원",n("+8.74%")])+row(["대덕전자","-",n("+8.07%")])+'</table>',860)
B4=stage(title("투자자별 순매수 (10/28)")+'<table>'+row(["투자자","코스피","코스닥"],True)+
 row(["외국인",n("+8,158억"),n("-1,849억")])+row(["기관",n("+9,608억"),n("+2,239억")])+row(["개인",n("-1조 8,016억"),n("-307억")])+'</table><div style="font-size:25px;color:'+MUTED+';margin-top:24px">출처: 블록미디어 · 아이뉴스24</div>',620)
B5=stage(title("이번 주 체크할 변수")+
 item("AI 자금조달 부담","유안타: 고객사 현금흐름·자금조달은 남은 검증 변수")+
 item("삼성전자 실적 · 미국 빅테크 실적","급등 후 변동성 확대 가능성")+
 item("FOMC 결정","이번 주 대기 중")+
 item("11/3 미국 중간선거","유안타증권이 꼽은 주요 변수"),700)
jobs=[("thumbnail",THUMB,1080),("body-1",B1,640),("body-2",B2,640),("body-3",B3,860),("body-4",B4,620),("body-5",B5,700)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,html,h in jobs:
        pg=b.new_page(viewport={"width":1080,"height":h}); pg.set_content(BASE%html); pg.screenshot(path=str(out/f"{name}.png")); pg.close()
    b.close()
