from playwright.sync_api import sync_playwright
import pathlib
here = pathlib.Path(__file__).parent
out = here.parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#eef0f2}
.stage{position:relative;overflow:hidden}
table{border-collapse:collapse;width:100%%}
td,th{padding:20px 16px;font-size:30px;text-align:right}
td:first-child,th:first-child{text-align:left}
</style></head><body>%s</body></html>"""
DOWN="#6fa0ff"; UP="#ff6b6b"; MUTED="#b4bac0"; ACC="#7fd1c7"
BG="linear-gradient(135deg,#232526 0%,#3a3d40 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.14)"
TH=f"border-bottom:2px solid rgba(255,255,255,.3);color:{MUTED}"
def stage(inner, w=1080, h=1080, pad="0 70px"):
    return f'<div class="stage" style="width:{w}px;height:{h}px;background:{BG};padding:{pad};display:flex;flex-direction:column;justify-content:center">{inner}<div style="position:absolute;bottom:34px;left:70px;font-size:19px;color:#8e949a">합성 데이터 그래픽 · 10/14 마감 기준 정리</div></div>'
def title(t): return f'<div style="font-size:42px;font-weight:800;margin-bottom:30px;color:#fff">{t}</div>'

THUMB=f"""<div class="stage" style="width:1080px;height:1080px;background:{BG}">
<div style="position:absolute;top:90px;left:80px"><span style="background:{ACC};color:#1c2a28;font-size:28px;font-weight:800;padding:10px 26px;border-radius:8px">국장 정리 · 10/14</span></div>
<div style="position:absolute;top:210px;left:80px;font-size:96px;font-weight:900;color:{MUTED};line-height:1.2">6거래일 연속 하락</div>
<div style="position:absolute;top:340px;left:80px;font-size:250px;font-weight:900;color:{DOWN};line-height:1">-0.44%</div>
<div style="position:absolute;top:660px;left:80px;right:80px;font-size:66px;font-weight:800;line-height:1.4;color:#fff">6,190 찍고 막판 반납,<br>6,000선 턱걸이</div>
<div style="position:absolute;top:900px;left:80px;font-size:30px;line-height:1.6;color:{MUTED}">코스피 6,008.81 · 코스닥 823.88(-1.57%)<br>외국인 코스피 1조 1,796억원 순매도</div></div>"""

def row(cells, th=False):
    st = TH if th else LINE
    tag = "th" if th else "td"
    return "<tr>"+"".join(f'<{tag} style="{st};{c[1] if isinstance(c,tuple) else ""}">{c[0] if isinstance(c,tuple) else c}</{tag}>' for c in cells)+"</tr>"

# body1: intraday card
def kv(label, val, color="#fff"):
    return f'<div style="background:rgba(255,255,255,.07);border-radius:16px;padding:26px 30px"><div style="font-size:26px;color:{MUTED}">{label}</div><div style="font-size:54px;font-weight:800;color:{color};margin-top:6px">{val}</div></div>'
B1 = stage(title("코스피 장중 흐름 (10/14)")+
 '<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'+
 kv("시가","6,062.08")+kv("장중 고점","6,190.65",UP)+kv("장중 저점","5,944.65",DOWN)+kv("종가","6,008.81 (-0.44%)",DOWN)+
 '</div>'+f'<div style="margin-top:30px;font-size:28px;line-height:1.6;color:{MUTED}">상승 503 · 하락 371 · 거래대금 19조 9,300억원<br>코스닥 823.88 (-1.57%) · 고점 846.95 / 저점 813.49</div>',
 h=900)

# body2: investor flows
def n(v):
    c = UP if v.startswith("+") else DOWN
    return (v, f"color:{c};font-weight:700")
B2 = stage(title("투자자별 순매수(+)·순매도(-)")+'<table>'+
 row(["구분","코스피","코스닥"],True)+
 row(["외국인",n("-1조 1,796억"),n("-2,140억")])+
 row(["기관",n("+8,085억"),n("-1,811억")])+
 row(["개인",n("-3,143억"),n("+3,853억")])+'</table>'+
 f'<div style="margin-top:26px;font-size:26px;color:{MUTED}">코스피 기타법인 약 +6,000억원 (세계일보)</div>', h=800)

# body3: stocks
def pc(v):
    if v=="보합": return (v,f"color:{MUTED};font-weight:700")
    return n(v)
B3 = stage(title("주요 종목 등락")+'<table>'+
 row(["종목","종가/등락","등락률"],True)+
 row(["삼성전자","232,000원",pc("보합")])+
 row(["SK하이닉스","1,419,000원",pc("-1.66%")])+
 row(["삼성SDI","—",pc("+5.54%")])+
 row(["LG에너지솔루션","—",pc("+2.93%")])+
 row(["신한지주","—",pc("-4.71%")])+
 row(["삼성생명","—",pc("-3.71%")])+'</table>', h=920)

# body4: checkpoints diagram
def step(i,t,s):
    return f'<div style="display:flex;align-items:center;gap:24px;background:rgba(255,255,255,.07);border-radius:16px;padding:24px 28px;margin-bottom:18px"><div style="min-width:64px;height:64px;border-radius:50%;background:{ACC};color:#1c2a28;font-size:34px;font-weight:900;display:flex;align-items:center;justify-content:center">{i}</div><div><div style="font-size:34px;font-weight:800;color:#fff">{t}</div><div style="font-size:25px;color:{MUTED};margin-top:4px">{s}</div></div></div>'
B4 = stage(title("다음 거래일 체크 포인트")+
 step(1,"미국 CPI 결과","발표 앞두고 외국인 경계심리 지속")+
 step(2,"외국인 수급 방향","오늘 코스피 -1조 1,796억원, 오후에 집중")+
 step(3,"6,000선·5,500선 지지","오늘 저점 5,944.65, 어제 지지 구간 5,500~6,000 초반")+
 step(4,"환율 1,338.3원","전일 대비 -6.8원, 원화 강세", ), h=860)

jobs=[("thumbnail",THUMB,1080,1080),("body-1",B1,1080,900),("body-2",B2,1080,800),("body-3",B3,1080,920),("body-4",B4,1080,860)]
with sync_playwright() as p:
    b=p.chromium.launch(); 
    for name,html,w,h in jobs:
        pg=b.new_page(viewport={"width":w,"height":h}); pg.set_content(BASE%html); pg.screenshot(path=str(out/f"{name}.png")); pg.close()
    b.close()
