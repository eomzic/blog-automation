from playwright.sync_api import sync_playwright
import pathlib
here = pathlib.Path(__file__).parent
BASE = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'Pretendard','Apple SD Gothic Neo',-apple-system,sans-serif;color:#f2f2f2}
.stage{position:relative;overflow:hidden}
</style></head><body>%s</body></html>"""
DOWN="#5b8def"; UP="#e05252"; MUTED="#b9bdd6"; ACC="#a78bfa"
BG="linear-gradient(135deg,#1a1a2e 0%,#16213e 100%)"
LINE="border-bottom:1px solid rgba(255,255,255,.14)"
def stage(inner, pad="0 80px"):
    return f'<div class="stage" style="width:1080px;height:1080px;background:{BG};padding:{pad};display:flex;flex-direction:column;justify-content:center">{inner}<div style="position:absolute;bottom:55px;left:80px;font-size:19px;color:#8b90ad">합성 데이터 그래픽 · 10/12 마감 기준 정리</div></div>'

THUMB=f"""<div class="stage" style="width:1080px;height:1080px;background:{BG}">
<div style="position:absolute;top:80px;left:80px;font-size:24px;font-weight:700;color:{ACC};letter-spacing:1px">국장 정리 · 10/12</div>
<div style="position:absolute;top:170px;left:80px;font-size:200px;font-weight:900;color:{DOWN};line-height:1">-3.65%</div>
<div style="position:absolute;top:430px;left:80px;right:80px;font-size:60px;font-weight:800;line-height:1.35;color:#fff">연휴 끝나자마자<br>6,400선 붕괴</div>
<div style="position:absolute;top:660px;left:80px;right:80px;font-size:28px;line-height:1.7;color:{MUTED}">코스피 6,384.24 · 코스닥 849.19(-4.83%)<br>외국인 2조 186억원 순매도</div>
<div style="position:absolute;bottom:0;left:0;width:1080px;height:14px;background:{ACC}"></div></div>"""

def kpi():
    cards=[("코스피","6,384.24","-3.65%","-241.69p"),("코스닥","849.19","-4.83%","-43.08p")]
    g="".join(f'<div style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:50px 36px"><div style="font-size:28px;color:{MUTED};margin-bottom:20px">{n}</div><div style="font-size:60px;font-weight:800;margin-bottom:14px">{v}</div><div style="font-size:44px;font-weight:800;color:{DOWN}">{p}</div><div style="font-size:24px;color:{MUTED};margin-top:8px">{d}</div></div>' for n,v,p,d in cards)
    return stage(f'<div style="font-size:42px;font-weight:800;margin-bottom:12px">연휴 후 첫 거래일, 동반 급락</div><div style="font-size:24px;color:{MUTED};margin-bottom:50px">코스닥은 7/29 이후 최대 낙폭</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:28px">{g}</div><div style="margin-top:44px;border-left:6px solid {ACC};background:rgba(167,139,250,.1);border-radius:0 14px 14px 0;padding:26px 32px;font-size:26px;line-height:1.6">코스피 장중 저점 6,368.49<br>종가 기준 6,400선 이탈은 8/11 이후 처음</div>')

def flows():
    rows=[("코스피","외국인","-2조 186억원",DOWN),("","기관","-1,107억원",DOWN),("","개인","+1조 4,674억원",UP),("코스닥","외국인","-270억원",DOWN),("","기관","-2,228억원",DOWN),("","개인","+2,488억원",UP)]
    t="".join(f'<tr><td style="padding:22px 18px;font-size:28px;font-weight:800;{LINE}">{m}</td><td style="padding:22px 18px;font-size:30px;{LINE}">{w}</td><td style="padding:22px 18px;font-size:32px;font-weight:800;text-align:right;color:{c};{LINE}">{v}</td></tr>' for m,w,v,c in rows)
    return stage(f'<div style="font-size:42px;font-weight:800;margin-bottom:12px">투자자별 순매수·순매도</div><div style="font-size:24px;color:{MUTED};margin-bottom:40px">외국인 매도를 개인이 받아낸 구도</div><table style="width:100%;border-collapse:collapse"><tr><th style="text-align:left;padding:14px 18px;font-size:22px;color:{MUTED};border-bottom:2px solid rgba(255,255,255,.3)">시장</th><th style="text-align:left;padding:14px 18px;font-size:22px;color:{MUTED};border-bottom:2px solid rgba(255,255,255,.3)">주체</th><th style="text-align:right;padding:14px 18px;font-size:22px;color:{MUTED};border-bottom:2px solid rgba(255,255,255,.3)">순매수</th></tr>{t}</table>')

def stocks():
    rows=[("삼성전자","250,500원","-4.39%"),("SK하이닉스","1,605,000원","-4.52%"),("SK스퀘어","984,000원","-6.29%"),("에코프로비엠","115,600원","-10.25%"),("에코프로","84,100원","-8.49%"),("리노공업","-","-11.15%"),("심텍","-","-10.36%"),("레인보우로보틱스","-","-8.86%")]
    t="".join(f'<tr><td style="padding:17px 18px;font-size:28px;font-weight:700;{LINE}">{n}</td><td style="padding:17px 18px;font-size:26px;text-align:right;color:{MUTED};{LINE}">{p}</td><td style="padding:17px 18px;font-size:30px;font-weight:800;text-align:right;color:{DOWN};{LINE}">{c}</td></tr>' for n,p,c in rows)
    return stage(f'<div style="font-size:42px;font-weight:800;margin-bottom:12px">대형 반도체 · 코스닥 낙폭 상위</div><div style="font-size:24px;color:{MUTED};margin-bottom:30px">시총 상위 10종목 중 9개 하락</div><table style="width:100%;border-collapse:collapse"><tr><th style="text-align:left;padding:12px 18px;font-size:21px;color:{MUTED};border-bottom:2px solid rgba(255,255,255,.3)">종목</th><th style="text-align:right;padding:12px 18px;font-size:21px;color:{MUTED};border-bottom:2px solid rgba(255,255,255,.3)">종가</th><th style="text-align:right;padding:12px 18px;font-size:21px;color:{MUTED};border-bottom:2px solid rgba(255,255,255,.3)">등락률</th></tr>{t}</table>')

def steps():
    items=[("1","외국인 수급","순매도가 이어지는지\n(10거래일 연속)"),("2","6,600선 회복","이탈한 기술적\n지지선 되찾기"),("3","실적 시즌 반응","호실적 이후 주가\n반응 확인")]
    c="".join(f'<div style="display:flex;gap:28px;align-items:center;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:36px 40px;margin-bottom:24px"><div style="flex:none;width:76px;height:76px;border-radius:50%;background:{ACC};color:#1a1a2e;font-size:40px;font-weight:900;display:flex;align-items:center;justify-content:center">{n}</div><div><div style="font-size:34px;font-weight:800;margin-bottom:8px">{t}</div><div style="font-size:24px;color:{MUTED};line-height:1.5;white-space:pre-line">{d}</div></div></div>' for n,t,d in items)
    return stage(f'<div style="font-size:42px;font-weight:800;margin-bottom:12px">다음 거래일 체크 포인트</div><div style="font-size:24px;color:{MUTED};margin-bottom:44px">전망이 아니라 확인할 항목 정리</div>{c}')

jobs={"thumbnail.png":THUMB,"body-1.png":kpi(),"body-2.png":flows(),"body-3.png":stocks(),"body-4.png":steps()}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1080})
    for n,h in jobs.items():
        pg.set_content(BASE%h); pg.screenshot(path=str(here.parent/n)); print("saved",n)
    b.close()
