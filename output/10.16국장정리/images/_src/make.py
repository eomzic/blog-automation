from playwright.sync_api import sync_playwright
import pathlib
out = pathlib.Path(__file__).parent.parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#eef6f4}
.stage{position:relative;overflow:hidden}
table{border-collapse:collapse;width:100%%}
td,th{padding:20px 16px;font-size:30px;text-align:right}
td:first-child,th:first-child{text-align:left}
</style></head><body>%s</body></html>"""
DOWN="#6fa0ff"; UP="#ff6b6b"; MUTED="#a9c9c4"; ACC="#5eead4"
BG="linear-gradient(135deg,#0f2027 0%,#134e4a 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.14)"
TH=f"border-bottom:2px solid rgba(255,255,255,.3);color:{MUTED}"
def stage(inner,h):
    return f'<div class="stage" style="width:1080px;height:{h}px;background:{BG};padding:0 70px;display:flex;flex-direction:column;justify-content:center">{inner}<div style="position:absolute;bottom:30px;left:70px;font-size:19px;color:#7fa8a2">합성 데이터 그래픽 · 10/16 마감 기준 정리</div></div>'
def title(t): return f'<div style="font-size:42px;font-weight:800;margin-bottom:30px;color:#fff">{t}</div>'
THUMB=f"""<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:90px 80px">
<div><span style="border:3px solid {ACC};color:{ACC};font-size:30px;font-weight:800;padding:10px 28px;border-radius:30px">국장 정리 · 10/16</span></div>
<div style="margin-top:70px;font-size:80px;font-weight:900;color:#fff;line-height:1.25">하루 만에<br>반등</div>
<div style="margin-top:40px;font-size:210px;font-weight:900;color:{UP};line-height:1">+2.05%</div>
<div style="margin-top:50px;font-size:42px;font-weight:700;color:{MUTED};line-height:1.5">코스피 5,668.05 · 코스닥 794.78 (+4.46%)</div>
<div style="margin-top:14px;font-size:36px;color:{MUTED}">환율 1,331.4원 · 2년 만의 최저</div></div>"""
def row(cells,th=False):
    st=TH if th else LINE; tag="th" if th else "td"
    return "<tr>"+"".join(f'<{tag} style="{st};{c[1] if isinstance(c,tuple) else ""}">{c[0] if isinstance(c,tuple) else c}</{tag}>' for c in cells)+"</tr>"
def n(v):
    c=UP if v.startswith("+") else DOWN
    return (v,f"color:{c};font-weight:700")
def card(l,v,c="#fff"):
    return f'<div style="background:rgba(255,255,255,.08);border-radius:16px;padding:24px 28px"><div style="font-size:25px;color:{MUTED}">{l}</div><div style="font-size:46px;font-weight:800;color:{c};margin-top:6px">{v}</div></div>'
B1=stage(title("10/16 원·달러 환율")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">'+
 card("종가","1,331.4원")+card("전일 대비","-13.2원 (-0.98%)",DOWN)+
 card("최저 기준","2024.10.2 이후")+card("장중 저점","1,331.0원")+'</div>'+
 f'<div style="margin-top:26px;font-size:27px;line-height:1.7;color:{MUTED}">· 장 후반 수출기업 달러 매도(네고)<br>· 워시 연준 의장 "회의 결과 미리 판단 안 해"<br>· 장 종반 외국인 커스터디 달러 매도</div>',800)
B2=stage(title("장중 고점 vs 마감")+'<table>'+row(["구분","코스피","코스닥"],True)+
 row(["전일 종가","5,554.22","760.82"])+row(["마감",("5,668.05","font-weight:700"),("794.78","font-weight:700")])+
 row(["등락률",n("+2.05%"),n("+4.46%")])+row(["장중 고점","5,809.94 (+4.6%)","800선 회복 (+6%대)"])+'</table>'+
 f'<div style="margin-top:26px;font-size:26px;color:{MUTED}">코스닥 12:55경 매수 사이드카 발동</div>',780)
B3=stage(title("주요 종목 등락 (10/16 종가)")+'<table>'+row(["종목","종가","등락률"],True)+
 row(["삼성전자","215,500원",n("+2.62%")])+row(["SK하이닉스","1,272,000원",n("+0.79%")])+
 row(["알테오젠(코스닥)","234,000원",n("+9.60%")])+row(["에코프로(코스닥)","81,300원",n("+0.62%")])+'</table>',700)
B4=stage(title("투자자별 순매수(+)·순매도(-)")+'<table>'+row(["구분","코스피","코스닥"],True)+
 row(["외국인",n("+1,721억"),n("-950억")])+row(["기관",n("-5,559억"),n("+1,657억")])+
 row(["개인",n("-4,434억"),n("-884억")])+'</table>'+
 f'<div style="margin-top:26px;font-size:24px;color:{MUTED}">브릿지경제 마감 집계 기준 (매체별로 외국인 금액 상이)</div>',700)
jobs=[("thumbnail",THUMB,1080),("body-1",B1,800),("body-2",B2,780),("body-3",B3,700),("body-4",B4,700)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,html,h in jobs:
        pg=b.new_page(viewport={"width":1080,"height":h}); pg.set_content(BASE%html); pg.screenshot(path=str(out/f"{name}.png")); pg.close()
    b.close()
