from playwright.sync_api import sync_playwright
import pathlib
here = pathlib.Path(__file__).parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#f6eded}
.stage{position:relative;overflow:hidden}
</style></head><body>%s</body></html>"""
DOWN="#6fa0ff"; UP="#ff6b6b"; MUTED="#d9b8b8"; ACC="#f0b86e"
BG="linear-gradient(135deg,#2d0a0a 0%,#4a1414 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.14)"
TH=f"border-bottom:2px solid rgba(255,255,255,.3);color:{MUTED}"
def stage(inner, pad="0 80px"):
    return f'<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:{pad};display:flex;flex-direction:column;justify-content:center">{inner}<div style="position:absolute;bottom:55px;left:80px;font-size:19px;color:#b88f8f">합성 데이터 그래픽 · 10/13 마감 기준 정리</div></div>'

THUMB=f"""<div class="stage" style="width:1080px;height:1080px;background:{BG}">
<div style="position:absolute;top:90px;left:0;right:0;text-align:center"><span style="display:inline-block;background:{ACC};color:#2d0a0a;font-size:28px;font-weight:800;padding:10px 28px;border-radius:40px">국장 정리 · 10/13 · 사이드카 발동</span></div>
<div style="position:absolute;top:210px;left:0;right:0;text-align:center;font-size:230px;font-weight:900;color:{DOWN};line-height:1">-5.46%</div>
<div style="position:absolute;top:500px;left:80px;right:80px;text-align:center;font-size:68px;font-weight:800;line-height:1.35;color:#fff">장중 6,000선 붕괴,<br>종가는 간신히 방어</div>
<div style="position:absolute;top:780px;left:80px;right:80px;text-align:center;font-size:30px;line-height:1.7;color:{MUTED}">코스피 6,035.35 · 코스닥 837.03(-1.43%)<br>외국인 4조 4,926억원 순매도</div></div>"""

def kpi():
    cards=[("코스피","6,035.35","-5.46%","-348.89p"),("코스닥","837.03","-1.43%","-12.16p")]
    g="".join(f'<div style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:18px;padding:50px 36px"><div style="font-size:28px;color:{MUTED};margin-bottom:20px">{n}</div><div style="font-size:60px;font-weight:800;margin-bottom:14px">{v}</div><div style="font-size:44px;font-weight:800;color:{DOWN}">{p}</div><div style="font-size:24px;color:{MUTED};margin-top:8px">{d}</div></div>' for n,v,p,d in cards)
    return stage(f'<div style="font-size:42px;font-weight:800;margin-bottom:12px">5거래일 연속 하락, 코스피 급락</div><div style="font-size:24px;color:{MUTED};margin-bottom:50px">장중 저점 5,988.22 · VKOSPI 48.45(+18.95%)</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:28px">{g}</div><div style="margin-top:44px;border-left:6px solid {ACC};background:rgba(240,184,110,.1);border-radius:0 14px 14px 0;padding:26px 32px;font-size:26px;line-height:1.6">10/2 종가 7,000선 위 대비 -13.83%<br>하락 660종목 vs 상승 233종목</div>')

def flows():
    rows=[("외국인","-4조 4,926억원",DOWN),("개인","+2조 1,660억원",UP),("기관","+1조 7,317억원",UP)]
    t="".join(f'<tr><td style="padding:34px 18px;font-size:36px;font-weight:700;{LINE}">{w}</td><td style="padding:34px 18px;font-size:44px;font-weight:800;text-align:right;color:{c};{LINE}">{v}</td></tr>' for w,v,c in rows)
    return stage(f'<div style="font-size:42px;font-weight:800;margin-bottom:12px">코스피 투자자별 순매수·순매도</div><div style="font-size:24px;color:{MUTED};margin-bottom:40px">외국인 매도를 개인·기관이 받아낸 구도</div><table style="width:100%;border-collapse:collapse"><tr><th style="text-align:left;padding:14px 18px;font-size:22px;{TH}">주체</th><th style="text-align:right;padding:14px 18px;font-size:22px;{TH}">순매수</th></tr>{t}</table>')

def stocks():
    rows=[("SK스퀘어","-","-12.91%"),("SK하이닉스","1,443,000원","-10.09%"),("삼성전자","232,000원","-7.39%")]
    t="".join(f'<tr><td style="padding:34px 18px;font-size:34px;font-weight:700;{LINE}">{n}</td><td style="padding:34px 18px;font-size:28px;text-align:right;color:{MUTED};{LINE}">{p}</td><td style="padding:34px 18px;font-size:44px;font-weight:800;text-align:right;color:{DOWN};{LINE}">{c}</td></tr>' for n,p,c in rows)
    return stage(f'<div style="font-size:42px;font-weight:800;margin-bottom:12px">반도체 대형주 등락률</div><div style="font-size:24px;color:{MUTED};margin-bottom:30px">LG에너지솔루션·삼성바이오로직스는 상승</div><table style="width:100%;border-collapse:collapse"><tr><th style="text-align:left;padding:12px 18px;font-size:21px;{TH}">종목</th><th style="text-align:right;padding:12px 18px;font-size:21px;{TH}">종가</th><th style="text-align:right;padding:12px 18px;font-size:21px;{TH}">등락률</th></tr>{t}</table>')

def steps():
    items=[("1","코스피 200일선","약 6,376 이탈\n지지·회복 여부"),("2","외국인 수급","순매도 흐름이\n이어지는지"),("3","대외 일정","미국 9월 CPI\nASML·TSMC 실적")]
    c="".join(f'<div style="display:flex;gap:28px;align-items:center;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:18px;padding:36px 40px;margin-bottom:24px"><div style="flex:none;width:76px;height:76px;border-radius:50%;background:{ACC};color:#2d0a0a;font-size:40px;font-weight:900;display:flex;align-items:center;justify-content:center">{n}</div><div><div style="font-size:34px;font-weight:800;margin-bottom:8px">{t}</div><div style="font-size:24px;color:{MUTED};line-height:1.5;white-space:pre-line">{d}</div></div></div>' for n,t,d in items)
    return stage(f'<div style="font-size:42px;font-weight:800;margin-bottom:12px">다음 거래일 체크 포인트</div><div style="font-size:24px;color:{MUTED};margin-bottom:44px">전망이 아니라 확인할 항목 정리</div>{c}')

jobs={"thumbnail.png":THUMB,"body-1.png":kpi(),"body-2.png":flows(),"body-3.png":stocks(),"body-4.png":steps()}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1080})
    for n,h in jobs.items():
        pg.set_content(BASE%h); pg.screenshot(path=str(here.parent/n)); print("saved",n)
    b.close()
