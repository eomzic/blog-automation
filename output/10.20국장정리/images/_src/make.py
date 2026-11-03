from playwright.sync_api import sync_playwright
import pathlib
out = pathlib.Path(__file__).parent.parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#f4ecec}
table{border-collapse:collapse;width:100%%}
td,th{padding:20px 16px;font-size:29px;text-align:right}
td:first-child,th:first-child{text-align:left}
</style></head><body>%s</body></html>"""
DOWN="#7aa8ff"; UP="#ff7373"; MUTED="#cdb8b8"; ACC="#ff9a76"
BG="linear-gradient(160deg,#2d0a0a 0%,#4a1414 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.15)"
TH=f"border-bottom:2px solid rgba(255,154,118,.6);color:{ACC}"
def stage(inner,h):
    return f'<div style="position:relative;width:1080px;height:{h}px;background:{BG};padding:0 70px;display:flex;flex-direction:column;justify-content:center;border-left:12px solid {ACC}">{inner}<div style="position:absolute;bottom:26px;right:70px;font-size:19px;color:#a58e8e">합성 데이터 그래픽 · 10/20 마감 기준</div></div>'
def title(t): return f'<div style="font-size:42px;font-weight:800;margin-bottom:30px;color:#fff">{t}</div>'
def row(cells,th=False):
    st=TH if th else LINE; tag="th" if th else "td"
    return "<tr>"+"".join(f'<{tag} style="{st};{c[1] if isinstance(c,tuple) else ""}">{c[0] if isinstance(c,tuple) else c}</{tag}>' for c in cells)+"</tr>"
def n(v):
    c=UP if v.startswith("+") else DOWN
    return (v,f"color:{c};font-weight:700")
def card(l,v,c="#fff"):
    return f'<div style="background:rgba(255,255,255,.07);border-radius:16px;padding:24px 28px;border-top:5px solid {ACC}"><div style="font-size:25px;color:{MUTED}">{l}</div><div style="font-size:42px;font-weight:800;color:{c};margin-top:6px">{v}</div></div>'
def pt(h,b):
    return f'<div style="background:rgba(255,255,255,.07);border-radius:16px;padding:22px 28px;margin-bottom:16px;border-left:6px solid {ACC}"><div style="font-size:30px;font-weight:800;color:#fff">{h}</div><div style="font-size:25px;color:{MUTED};margin-top:8px;line-height:1.5">{b}</div></div>'
THUMB=f"""<div style="position:relative;width:1080px;height:1080px;background:{BG};padding:110px 90px">
<div style="display:inline-block;border:3px solid {ACC};color:{ACC};font-size:30px;font-weight:800;padding:10px 28px;border-radius:40px">10/20 국장 정리</div>
<div style="margin-top:80px;font-size:200px;font-weight:900;color:{DOWN};line-height:1">-3.73%</div>
<div style="margin-top:50px;font-size:72px;font-weight:900;color:#fff;line-height:1.35">이틀 반등이<br>하루 만에 반납</div>
<div style="position:absolute;left:90px;bottom:110px;font-size:40px;font-weight:700;color:{MUTED};line-height:1.6">코스피 5,552.74 · 코스닥 781.97<br>기관 1조 48억원 순매도</div>
<div style="position:absolute;right:0;top:0;width:60px;height:1080px;background:{ACC}"></div></div>"""
B1=stage(title("투자자별 코스피 순매수(+)·순매도(-)")+'<table>'+row(["구분","10/19","10/20"],True)+
 row(["기관",n("+5,747억"),n("-1조 48억")])+row(["외국인",n("-379억"),n("-5,300억")])+
 row(["개인",n("-1조 862억"),n("+8,981억")])+row(["기타법인",n("+5,494억"),n("+6,367억")])+'</table>'+
 f'<div style="margin-top:24px;font-size:24px;color:{MUTED}">10/19는 직전 글 기준(KRX), 10/20 외국인·기관 금액은 매체별 소폭 상이</div>',720)
B2=stage(title("10/20 지수 마감 카드")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">'+
 card("코스피 시가(=장중 고점)","5,733.57")+card("코스피 장중 저점","5,493.24",DOWN)+
 card("코스피 마감","5,552.74 (-3.73%)",DOWN)+card("코스닥 마감","781.97 (-3.33%)",DOWN)+'</div>'+
 f'<div style="margin-top:26px;font-size:27px;line-height:1.7;color:{MUTED}">상승 118 · 하락 773 · 보합 24종목<br>거래대금 약 16조원 · 원/달러 1,328.1원</div>',700)
B3=stage(title("하락 원인, 소스별로 보면")+
 pt("키움증권 한지영","코어위브 신용·AI주 불확실성 / 반도체 실적 의구심 / 메타 실적 경계 / 수출기업 달러 매도로 환율 1,330원 하회")+
 pt("대신증권 이경민","전일 반등 이후 차익실현")+
 pt("서울경제","프랑스 혼란·중동 긴장에 따른 금리·유가 상승 언급")+
 pt("치킨스탁","미 10년물 4거래일 연속 하락 → 금리 때문은 아님, 단정할 근거 없음"),820)
B4=stage(title("주요 종목 종가 (10/20)")+'<table>'+row(["종목","종가","등락률"],True)+
 row(["삼성전자","211,500원",n("-2.98%")])+row(["SK하이닉스","1,223,000원",n("-4.23%")])+
 row(["LG에너지솔루션","414,000원",n("-4.17%")])+row(["현대차","310,000원",n("-4.91%")])+
 row(["삼성바이오로직스","1,391,000원",n("-2.52%")])+row(["KB금융","160,900원",n("-1.11%")])+'</table>',860)
jobs=[("thumbnail",THUMB,1080),("body-1",B1,720),("body-2",B2,700),("body-3",B3,820),("body-4",B4,860)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,html,h in jobs:
        pg=b.new_page(viewport={"width":1080,"height":h}); pg.set_content(BASE%html); pg.screenshot(path=str(out/f"{name}.png")); pg.close()
    b.close()
