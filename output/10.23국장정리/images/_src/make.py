from playwright.sync_api import sync_playwright
import pathlib
out = pathlib.Path(__file__).parent.parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#e8f3f0}
table{border-collapse:collapse;width:100%%}
td,th{padding:20px 16px;font-size:29px;text-align:right}
td:first-child,th:first-child{text-align:left}
</style></head><body>%s</body></html>"""
DOWN="#7aa8ff"; UP="#ff7373"; MUTED="#a9c9c2"; ACC="#5eead4"
BG="linear-gradient(150deg,#0f2027 0%,#134e4a 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.15)"
TH=f"border-bottom:2px solid rgba(94,234,212,.6);color:{ACC}"
def stage(inner,h):
    return f'<div style="position:relative;width:1080px;height:{h}px;background:{BG};padding:0 70px;display:flex;flex-direction:column;justify-content:center;border-top:10px solid {ACC}">{inner}<div style="position:absolute;bottom:22px;right:70px;font-size:19px;color:#78a39b">합성 데이터 그래픽 · 10/23 마감 기준</div></div>'
def title(t): return f'<div style="font-size:42px;font-weight:800;margin-bottom:30px;color:#fff">{t}</div>'
def row(cells,th=False):
    st=TH if th else LINE; tag="th" if th else "td"
    return "<tr>"+"".join(f'<{tag} style="{st};{c[1] if isinstance(c,tuple) else ""}">{c[0] if isinstance(c,tuple) else c}</{tag}>' for c in cells)+"</tr>"
def n(v):
    c=UP if v.startswith("+") else DOWN
    return (v,f"color:{c};font-weight:700")
def step(num,h,b,c="#fff"):
    return f'<div style="display:flex;align-items:center;margin-bottom:18px"><div style="width:68px;height:68px;border-radius:50%;background:{ACC};color:#0f2027;font-size:34px;font-weight:900;display:flex;align-items:center;justify-content:center;flex:none">{num}</div><div style="margin-left:26px;background:rgba(255,255,255,.07);border-radius:16px;padding:16px 26px;flex:1"><div style="font-size:30px;font-weight:800;color:{c}">{h}</div><div style="font-size:24px;color:{MUTED};margin-top:4px">{b}</div></div></div>'
def card(l,v,c="#fff"):
    return f'<div style="background:rgba(255,255,255,.07);border-radius:16px;padding:24px 28px;border-top:5px solid {ACC}"><div style="font-size:25px;color:{MUTED}">{l}</div><div style="font-size:42px;font-weight:800;color:{c};margin-top:6px">{v}</div></div>'
THUMB=f"""<div style="position:relative;width:1080px;height:1080px;background:{BG};padding:100px 90px;text-align:center">
<div style="display:inline-block;background:{ACC};color:#0f2027;font-size:32px;font-weight:900;padding:12px 34px;border-radius:8px">10/23 국장 정리</div>
<div style="margin-top:110px;font-size:62px;font-weight:700;color:{MUTED}">장중 -4%대에서</div>
<div style="margin-top:20px;font-size:190px;font-weight:900;color:{UP};line-height:1">+0.30%</div>
<div style="margin-top:60px;font-size:68px;font-weight:900;color:#fff;line-height:1.35">낙폭 전부 되돌린<br>코스피 5,550</div>
<div style="margin-top:70px;font-size:36px;color:{MUTED}">SK하이닉스 +4.42% · 코스닥 -1.62%</div>
<div style="position:absolute;left:0;bottom:0;width:1080px;height:36px;background:{ACC}"></div></div>"""
B1=stage(title("코스피 오늘 하루 흐름")+
 step(1,"개장 5,403.17 (-2.36%)","간밤 미국 반도체주 급락 여파",DOWN)+
 step(2,"장중 낙폭 -4% 넘어 5,300선 부근","정확한 저점은 기사마다 미명시",DOWN)+
 step(3,"SK하이닉스 반등, 5,500선 회복","솔리다임 상장 절차 중단 소식")+
 step(4,"마감 5,550.30 (+0.30%)","기관 8,723억원 순매수",UP),780)
B2=stage(title("코스피 주요 종목 종가 (10/23)")+'<table>'+row(["종목","등락률"],True)+
 row(["SK하이닉스 (1,277,000원)",n("+4.42%")])+row(["삼성전자 (215,500원)",n("+0.47%")])+
 row(["삼성바이오로직스",n("+7.71%")])+row(["SK스퀘어",n("+3.20%")])+
 row(["KB금융",n("-3.29%")])+row(["현대차",n("-1.99%")])+row(["LG에너지솔루션",n("-1.79%")])+'</table>',880)
B3=stage(title("투자자별 순매수(+)·순매도(-)")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">'+
 card("코스피 외국인","-9,941억원",DOWN)+card("코스피 기관","+8,723억원",UP)+
 card("코스닥 외국인","-416억원",DOWN)+card("코스닥 기관","-248억원",DOWN)+
 card("코스피 개인","+527억원",UP)+card("코스닥 개인","+631억원",UP)+'</div>'+
 f'<div style="margin-top:26px;font-size:25px;color:{MUTED}">외국인·기관 금액은 매체별 몇 억원 차이 있음</div>',700)
B4=stage(f'<div style="font-size:30px;color:{ACC};font-weight:800;margin-bottom:18px">코스닥 시총 상위, HLB만 올랐어요</div><div style="font-size:50px;font-weight:900;color:#fff;line-height:1.4;margin-bottom:34px">에코프로 <span style="color:{DOWN}">-5.83%</span> · 에코프로비엠 <span style="color:{DOWN}">-5.50%</span><br>리노공업 <span style="color:{DOWN}">-4.05%</span> · 주성엔지니어링 <span style="color:{DOWN}">-3.64%</span><br>HLB <span style="color:{UP}">+0.73%</span></div><div style="font-size:26px;color:{MUTED}">코스닥 751.69 (-1.62%) · 이차전지주 약세</div>',620)
jobs=[("thumbnail",THUMB,1080),("body-1",B1,780),("body-2",B2,880),("body-3",B3,700),("body-4",B4,620)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,html,h in jobs:
        pg=b.new_page(viewport={"width":1080,"height":h}); pg.set_content(BASE%html); pg.screenshot(path=str(out/f"{name}.png")); pg.close()
    b.close()
