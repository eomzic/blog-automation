from playwright.sync_api import sync_playwright
import pathlib
out = pathlib.Path(__file__).parent.parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#e9e9f7}
table{border-collapse:collapse;width:100%%}
td,th{padding:18px 16px;font-size:28px;text-align:right}
td:first-child,th:first-child{text-align:left}
</style></head><body>%s</body></html>"""
DOWN="#7aa8ff"; UP="#ff7373"; MUTED="#a9a9d0"; ACC="#b79cff"
BG="linear-gradient(155deg,#1a1a2e 0%,#16213e 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.15)"
TH=f"border-bottom:2px solid rgba(183,156,255,.6);color:{ACC}"
def stage(inner,h):
    return f'<div style="position:relative;width:1080px;height:{h}px;background:{BG};padding:0 70px;display:flex;flex-direction:column;justify-content:center;border-left:12px solid {ACC}">{inner}<div style="position:absolute;bottom:20px;right:70px;font-size:19px;color:#8585b0">합성 데이터 그래픽 · 10/26 마감 기준</div></div>'
def title(t): return f'<div style="font-size:42px;font-weight:800;margin-bottom:30px;color:#fff">{t}</div>'
def row(cells,th=False):
    st=TH if th else LINE; tag="th" if th else "td"
    return "<tr>"+"".join(f'<{tag} style="{st};{c[1] if isinstance(c,tuple) else ""}">{c[0] if isinstance(c,tuple) else c}</{tag}>' for c in cells)+"</tr>"
def n(v):
    c=UP if v.startswith("+") else DOWN
    return (v,f"color:{c};font-weight:700")
def step(num,h,b,c="#fff"):
    return f'<div style="display:flex;align-items:center;margin-bottom:18px"><div style="width:68px;height:68px;border-radius:50%;background:{ACC};color:#1a1a2e;font-size:26px;font-weight:900;display:flex;align-items:center;justify-content:center;flex:none">{num}</div><div style="margin-left:26px;background:rgba(255,255,255,.07);border-radius:16px;padding:16px 26px;flex:1"><div style="font-size:30px;font-weight:800;color:{c}">{h}</div><div style="font-size:24px;color:{MUTED};margin-top:4px">{b}</div></div></div>'
def card(l,v,sub,c):
    return f'<div style="background:rgba(255,255,255,.07);border-radius:16px;padding:28px 30px;border-top:5px solid {ACC}"><div style="font-size:26px;color:{MUTED}">{l}</div><div style="font-size:54px;font-weight:900;color:{c};margin-top:8px">{v}</div><div style="font-size:24px;color:{MUTED};margin-top:6px">{sub}</div></div>'
THUMB=f"""<div style="position:relative;width:1080px;height:1080px;background:{BG};padding:100px 90px">
<div style="display:inline-block;border:3px solid {ACC};color:{ACC};font-size:32px;font-weight:800;padding:10px 30px;border-radius:40px">10/26 국장 정리</div>
<div style="margin-top:130px;font-size:150px;font-weight:900;color:{DOWN};line-height:1">코스닥<br>-3.26%</div>
<div style="margin-top:70px;font-size:64px;font-weight:800;color:#fff;line-height:1.35">코스피 5,469<br>7개월 만의 최저 종가</div>
<div style="margin-top:60px;font-size:36px;color:{MUTED}">원·달러 1,323.1원 · 외국인 7,400억대 순매도</div>
<div style="position:absolute;right:0;top:0;width:36px;height:1080px;background:{ACC}"></div></div>"""
B1=stage(title("10/26 지수 마감")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'+
 card("코스피","5,469.47","-80.83p · 장중 5,455~5,566",DOWN)+card("코스닥","727.21","-24.48p · 장중 727.20~745.95",DOWN)+
 card("코스피 등락률","-1.46%","4/6 이후 최저 종가",DOWN)+card("코스닥 등락률","-3.26%","7/31 이후 최저",DOWN)+'</div>',640)
B2=stage(title("업종·종목 등락률 (10/26)")+'<table>'+row(["종목·업종","등락률"],True)+
 row(["삼성물산 (코스피)",n("+1.39%")])+row(["삼성생명 (코스피)",n("+0.61%")])+
 row(["삼성전자 (코스피)",n("-1.16%")])+row(["현대차 (코스피)",n("-2.54%")])+row(["KB금융 (코스피)",n("-3.79%")])+
 row(["의료·정밀기기 업종",n("-5.88%")])+row(["주성엔지니어링 (코스닥)",n("-6.84%")])+row(["원익IPS (코스닥)",n("-6.49%")])+row(["이오테크닉스 (코스닥)",n("-6.19%")])+'</table>',960)
B3=stage(f'<div style="font-size:30px;color:{ACC};font-weight:800;margin-bottom:18px">원화 강세, 주간 종가 기준 2024년 10월 이후 최저</div><div style="font-size:120px;font-weight:900;color:#fff;line-height:1.1">1,323.1<span style="font-size:54px">원</span></div><div style="font-size:32px;color:{DOWN};font-weight:800;margin-top:10px">전 거래일 주간 종가 대비 -1.5원</div><div style="font-size:26px;color:{MUTED};margin-top:30px">반도체 기업 달러 매도 · 달러인덱스 101.67</div>',560)
B4=stage(title("이번 주 일정 (한국시간)")+
 step("10/28","SK하이닉스 3분기 실적","추가 주주환원 재원 30조원+ 추정 (NH투자증권)")+
 step("10/29","삼성전자 실적 · FOMC","금리 동결 예상, 추가 인상 가능성 주목")+
 step("10/29","마이크로소프트 · 알파벳 실적","AI 투자 수익성 확인")+
 step("10/30","아마존 · 인텔 · 샌디스크 실적","빅테크 실적 마무리"),700)
jobs=[("thumbnail",THUMB,1080),("body-1",B1,640),("body-2",B2,960),("body-3",B3,560),("body-4",B4,700)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,html,h in jobs:
        pg=b.new_page(viewport={"width":1080,"height":h}); pg.set_content(BASE%html); pg.screenshot(path=str(out/f"{name}.png")); pg.close()
    b.close()
