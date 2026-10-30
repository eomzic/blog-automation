import os
from playwright.sync_api import sync_playwright
BASE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(BASE)
UP="#ff6b6b"; DN="#5aa2ff"
CSS="""*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Apple SD Gothic Neo','Pretendard',sans-serif}
.card{width:1000px;background:linear-gradient(160deg,#232526 0%,#3a3d40 100%);padding:48px 56px;color:#fff}
.eyebrow{font-size:20px;font-weight:700;color:#b8c4a8;margin-bottom:8px}h2{font-size:30px;font-weight:800;margin-bottom:30px}
.row{display:flex;align-items:center;gap:16px;margin-bottom:14px}.nm{width:210px;font-size:22px;font-weight:700}
.track{flex:1;height:34px;position:relative;background:rgba(255,255,255,.06);border-radius:8px}
.mid{position:absolute;left:50%;top:0;bottom:0;width:2px;background:rgba(255,255,255,.3)}
.bar{position:absolute;top:4px;bottom:4px;border-radius:5px}.v{width:110px;text-align:right;font-size:22px;font-weight:800}
.foot{margin-top:18px;font-size:15px;color:rgba(255,255,255,.45)}"""
def chart(eyebrow,title,rows,scale,foot):
    h=""
    for n,v in rows:
        w=abs(v)/scale*50; c=UP if v>0 else DN
        pos=f"left:50%;width:{w}%" if v>0 else f"right:50%;width:{w}%"
        h+=f'<div class="row"><div class="nm">{n}</div><div class="track"><div class="mid"></div><div class="bar" style="{pos};background:{c}"></div></div><div class="v" style="color:{c}">{v:+.2f}%</div></div>'
    return f'<html><head><meta charset="UTF-8"><style>{CSS}</style></head><body><div class="card"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2>{h}<div class="foot">{foot}</div></div></body></html>'
pages={
"body-1":chart("10/12 미국 증시 마감","3대 지수 – 다우만 플러스",[("다우존스",0.38),("S&P500",-0.06),("나스닥 종합",-0.44),("나스닥100",-0.71),("필라델피아 반도체",-2.67)],3,"※ 데이터를 시각화한 합성 그래픽 · 상승=빨강 / 하락=파랑"),
"body-2":chart("S&P500 업종별","방어주는 오르고 기술은 빠졌다",[("에너지",1.45),("필수소비재",1.17),("경기소비재",-0.53),("기술",-1.25)],1.6,"※ 데이터를 시각화한 합성 그래픽 · 상승=빨강 / 하락=파랑"),
"body-3":chart("개별 종목","메타·MS는 웃고 오라클·시스코는 울고",[("메타",3.38),("애플",1.29),("마이크로소프트",1.14),("테슬라",-1.22),("시스코",-2.58),("오라클",-2.84)],3.5,"※ 데이터를 시각화한 합성 그래픽 · 상승=빨강 / 하락=파랑"),
}
for k,v in pages.items(): open(f"{BASE}/{k}.html","w").write(v)
thumb=f'''<html><head><meta charset="UTF-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1080px;font-family:'Apple SD Gothic Neo',sans-serif;background:linear-gradient(160deg,#232526 0%,#3a3d40 100%);color:#fff;padding:90px 80px;position:relative}}
.tag{{font-size:28px;font-weight:700;color:#b8c4a8}}.t{{margin-top:40px;font-size:62px;font-weight:800;line-height:1.3;letter-spacing:-1.5px;width:600px}}
.big{{position:absolute;right:70px;bottom:110px;text-align:right}}.big b{{display:block;font-size:150px;color:{DN};letter-spacing:-5px;line-height:1}}.big span{{font-size:28px;color:rgba(255,255,255,.6)}}
.d{{position:absolute;left:80px;bottom:110px;font-size:30px;color:rgba(255,255,255,.55)}}</style></head><body>
<div class="tag">내일도 주린이 · 미장 정리</div><div class="t">반도체 급락,<br>다우만 웃었다</div>
<div class="d">10/12 컬럼버스 데이</div><div class="big"><b>-2.67%</b><span>필라델피아 반도체지수</span></div></body></html>'''
open(f"{BASE}/thumbnail.html","w").write(thumb)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(device_scale_factor=2)
    pg.set_viewport_size({"width":1080,"height":1080}); pg.goto(f"file://{BASE}/thumbnail.html"); pg.screenshot(path=f"{OUT}/thumbnail.png",clip={"x":0,"y":0,"width":1080,"height":1080})
    for k in pages:
        pg.set_viewport_size({"width":1000,"height":700}); pg.goto(f"file://{BASE}/{k}.html"); pg.query_selector(".card").screenshot(path=f"{OUT}/{k}.png")
    b.close()
