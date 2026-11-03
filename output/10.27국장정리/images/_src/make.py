from playwright.sync_api import sync_playwright
import pathlib
out = pathlib.Path(__file__).parent.parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#e6f5f1}
table{border-collapse:collapse;width:100%%}
td,th{padding:18px 16px;font-size:28px;text-align:right}
td:first-child,th:first-child{text-align:left}
</style></head><body>%s</body></html>"""
DOWN="#7aa8ff"; UP="#ff7373"; MUTED="#9fc7bf"; ACC="#5eead4"
BG="linear-gradient(160deg,#0f2027 0%,#134e4a 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.15)"
TH=f"border-bottom:2px solid rgba(94,234,212,.6);color:{ACC}"
def stage(inner,h):
    return f'<div style="position:relative;width:1080px;height:{h}px;background:{BG};padding:0 70px;display:flex;flex-direction:column;justify-content:center;border-top:10px solid {ACC}">{inner}<div style="position:absolute;bottom:18px;right:70px;font-size:19px;color:#7fb0a7">합성 데이터 그래픽 · 10/27 마감 기준</div></div>'
def title(t): return f'<div style="font-size:42px;font-weight:800;margin-bottom:30px;color:#fff">{t}</div>'
def row(cells,th=False):
    st=TH if th else LINE; tag="th" if th else "td"
    return "<tr>"+"".join(f'<{tag} style="{st};{c[1] if isinstance(c,tuple) else ""}">{c[0] if isinstance(c,tuple) else c}</{tag}>' for c in cells)+"</tr>"
def n(v):
    c=UP if v.startswith("+") else DOWN
    return (v,f"color:{c};font-weight:700")
def step(num,h,b,c="#fff"):
    return f'<div style="display:flex;align-items:center;margin-bottom:18px"><div style="min-width:110px;height:68px;border-radius:34px;background:{ACC};color:#0f2027;font-size:26px;font-weight:900;display:flex;align-items:center;justify-content:center;flex:none">{num}</div><div style="margin-left:26px;background:rgba(255,255,255,.07);border-radius:16px;padding:16px 26px;flex:1"><div style="font-size:30px;font-weight:800;color:{c}">{h}</div><div style="font-size:24px;color:{MUTED};margin-top:4px">{b}</div></div></div>'
def card(l,v,sub,c):
    return f'<div style="background:rgba(255,255,255,.07);border-radius:16px;padding:28px 30px;border-bottom:5px solid {ACC}"><div style="font-size:26px;color:{MUTED}">{l}</div><div style="font-size:54px;font-weight:900;color:{c};margin-top:8px">{v}</div><div style="font-size:24px;color:{MUTED};margin-top:6px">{sub}</div></div>'
THUMB=f"""<div style="position:relative;width:1080px;height:1080px;background:{BG};text-align:center;padding-top:150px">
<div style="font-size:40px;font-weight:800;color:{ACC};letter-spacing:2px">10/27 국장 정리</div>
<div style="margin-top:110px;font-size:190px;font-weight:900;color:{UP};line-height:1">+3.09%</div>
<div style="margin-top:50px;font-size:70px;font-weight:800;color:#fff;line-height:1.35">코스피 5,638 반등<br>앤트로픽 IPO 훈풍</div>
<div style="margin-top:50px;font-size:36px;color:{MUTED}">매수 사이드카 발동 · 삼성전자 +4.23%</div>
<div style="position:absolute;left:0;bottom:0;width:1080px;height:40px;background:{ACC}"></div></div>"""
B1=stage(title("10/27 지수 마감")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'+
 card("코스피","5,638.34","+168.87p · 장중 최고 5,737.61",UP)+card("코스닥","743.83","+16.62p · 장중 최고 760.59",UP)+
 card("코스피 등락률","+3.09%","시가 5,658.65 (+3.46%)",UP)+card("코스닥 등락률","+2.29%","4거래일 만의 상승",UP)+'</div>',640)
B2=stage(title("앤트로픽 S-1 핵심 수치")+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'+
 card("올해 상반기 매출","162.9억달러","전년 동기 대비 약 +1,300%",UP)+card("상반기 영업손실","6.9억달러","지난해 상반기 21.4억달러에서 축소",ACC)+
 card("컴퓨팅 비용 1달러당 매출","2.1달러","지난해 1분기 0.4달러",UP)+card("IPO 목표","최대 2조달러","기업가치 · 1,000억달러 조달",'#fff')+'</div>',640)
B3=stage(title("종목·업종 등락률 (10/27)")+'<table>'+row(["종목·업종","등락률"],True)+
 row(["SK스퀘어",n("+7.67%")])+row(["SK하이닉스",n("+5.18%")])+row(["삼성전자",n("+4.23%")])+row(["삼성생명",n("+3.45%")])+
 row(["LG에너지솔루션",n("+2.00%")])+row(["전기·전자 업종",n("+4.48%")])+row(["제약 업종",n("-3.01%")])+row(["삼성바이오로직스",n("-5.37%")])+'</table>',900)
B4=stage(title("코스피 수급, 매체별 집계가 달랐어요")+'<table>'+row(["투자자","헤럴드·폴리뉴스","한경·이투데이"],True)+
 row(["외국인",n("+5,910억"),n("+8,360억")])+row(["기관",n("+2,820억"),n("+4,180억~4,346억")])+row(["개인",n("-9,490억"),n("-1조 4,000억대")])+'</table><div style="font-size:25px;color:'+MUTED+';margin-top:24px">집계 시점 차이로 추정 · 외국인 선물은 940억 순매도(폴리뉴스)</div>',640)
B5=stage(title("이번 주 일정 (한국시간)")+
 step("10/28","SK하이닉스 3분기 실적","주주환원·특별배당 발표 여부 주목")+
 step("10/29","삼성전자 확정 실적 · FOMC","금리 동결 예상, 이후 추가 인상 가능성 주목")+
 step("10/29","마이크로소프트 · 알파벳 실적","AI 투자 수익성 확인")+
 step("10/30","아마존 · 인텔 · 샌디스크 실적","빅테크 실적 마무리"),700)
jobs=[("thumbnail",THUMB,1080),("body-1",B1,640),("body-2",B2,640),("body-3",B3,900),("body-4",B4,640),("body-5",B5,700)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,html,h in jobs:
        pg=b.new_page(viewport={"width":1080,"height":h}); pg.set_content(BASE%html); pg.screenshot(path=str(out/f"{name}.png")); pg.close()
    b.close()
