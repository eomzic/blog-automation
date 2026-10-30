from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path("/Users/eomzic/Desktop/claude/blog/output/10.5미장정리/images")
SRC = OUT / "_src"
FONT = "'Apple SD Gothic Neo','Malgun Gothic','Pretendard',sans-serif"
UP, DOWN = "#ff6b6b", "#5aa9ff"  # 상승=빨강, 하락=파랑 (한국 증시 관례 유지)

BASE_CSS = f"""
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ width:1080px; height:1080px; font-family:{FONT}; color:#f2f7f5; overflow:hidden; }}
"""

def thumb():
    return f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>{BASE_CSS}
body {{ background: linear-gradient(160deg,#0f2027 0%,#134e4a 100%); padding:90px 80px; position:relative; }}
.badge {{ display:inline-block; border:2px solid rgba(242,247,245,.45); border-radius:40px; padding:14px 30px; font-size:34px; color:#cfe9e2; }}
h1 {{ margin-top:130px; font-size:120px; line-height:1.2; font-weight:800; letter-spacing:-2px; }}
.sub {{ margin-top:40px; font-size:44px; color:#a8d8cc; }}
.stat {{ position:absolute; left:80px; bottom:250px; }}
.stat .k {{ font-size:36px; color:#a8d8cc; }}
.stat .v {{ font-size:96px; font-weight:800; color:{UP}; margin-top:6px; }}
.bar {{ position:absolute; left:80px; right:80px; bottom:150px; height:10px; border-radius:6px; background:linear-gradient(90deg,#134e4a,{UP}); }}
.date {{ position:absolute; left:80px; bottom:80px; font-size:36px; color:#7fb5a8; }}
</style></head><body>
<div class="badge">미장정리 · 10/5 월요일 마감</div>
<h1>나스닥 사상최고<br>채권은 울었다</h1>
<div class="sub">국장 휴장일, 미국은 정상 개장</div>

<div class="bar"></div>
<div class="date">2026.10.05</div>
</body></html>"""

def body1():
    rows = [("S&P 500","7,773.95","+0.66%",0.66),("나스닥 종합","27,477.31","+1.05%",1.05),("다우 산업","51,267.90","+0.18%",0.18)]
    bars = ""
    for name, close, pct, v in rows:
        w = int(v/1.05*620)
        bars += f"""<div class="row"><div class="name">{name}</div>
        <div class="track"><div class="fill" style="width:{w}px"></div></div>
        <div class="val"><div class="c">{close}</div><div class="p" style="color:{UP}">{pct}</div></div></div>"""
    return f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>{BASE_CSS}
body {{ background:#0f2027; padding:100px 90px; }}
.tag {{ font-size:34px; color:#7fb5a8; }}
h2 {{ margin-top:24px; font-size:70px; font-weight:800; line-height:1.25; }}
.list {{ margin-top:90px; }}
.row {{ display:flex; align-items:center; height:150px; border-bottom:1px solid rgba(255,255,255,.08); }}
.name {{ width:250px; font-size:38px; color:#cfe9e2; }}
.track {{ flex:1; height:34px; background:rgba(255,255,255,.06); border-radius:17px; overflow:hidden; margin-right:40px; }}
.fill {{ height:100%; background:linear-gradient(90deg,#134e4a,{UP}); border-radius:17px; }}
.val {{ width:270px; text-align:right; }}
.c {{ font-size:40px; font-weight:700; }}
.p {{ font-size:34px; font-weight:700; margin-top:4px; }}
.note {{ position:absolute; left:90px; bottom:110px; font-size:32px; color:#a8d8cc; }}
</style></head><body>
<div class="tag">10/5 뉴욕 정규장 마감 · 등락률</div>
<h2>3대 지수 모두 상승,<br>기술주가 끌어올렸다</h2>
<div class="list">{bars}</div>
<div class="note">막대 길이는 나스닥 등락률 기준 상대 비교 (합성 그래픽)</div>
</body></html>"""

def body2():
    return f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>{BASE_CSS}
body {{ background:#134e4a; padding:80px 90px; }}
.tag {{ font-size:34px; color:#cfe9e2; }}
h2 {{ margin-top:20px; font-size:64px; font-weight:800; line-height:1.25; }}
.grid {{ margin-top:44px; display:flex; flex-direction:column; gap:20px; }}
.card {{ background:rgba(0,0,0,.22); border-left:10px solid {UP}; border-radius:18px; padding:24px 44px; }}
.card .k {{ font-size:34px; color:#a8d8cc; }}
.card .v {{ font-size:58px; font-weight:800; margin-top:6px; }}
.card .d {{ font-size:32px; color:#cfe9e2; margin-top:8px; }}
.card.blue {{ border-left-color:{DOWN}; }}
</style></head><body>
<div class="tag">금리 · 지표 체크</div>
<h2>금리 인상 기대는 꺾였지만<br>물가 압력은 남았다</h2>
<div class="grid">
  <div class="card blue"><div class="k">미 10년물 국채금리</div><div class="v">5.26~5.31%</div><div class="d">장중 2002년 이후 최고 수준 근접</div></div>
  <div class="card blue"><div class="k">10월 연준 동결 확률 (CME)</div><div class="v">약 82%</div><div class="d">9월 말 인상 확률 71%에서 후퇴</div></div>
  <div class="card"><div class="k">ISM 서비스업 지불가격 (9월)</div><div class="v">74</div><div class="d">8월 72.6 → 상승, 비용 압력 재확인</div></div>
</div>
</body></html>"""

def body3():
    cards = [("스페이스X (SPCX)","+5%","모건스탠리 목표가 300달러 제시",UP),
             ("Nu Holdings (NU)","+13%","브라질 관련 강세 보도",UP),
             ("MercadoLibre (MELI)","+9%","브라질 강세 동반",UP),
             ("Moderna","+6.95%","한 매체 기준",UP)]
    items = "".join(f"""<div class="it"><div><div class="n">{n}</div><div class="r">{r}</div></div><div class="pc" style="color:{c}">{p}</div></div>""" for n,p,r,c in cards)
    return f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>{BASE_CSS}
body {{ background:linear-gradient(160deg,#0f2027,#134e4a); padding:100px 90px; }}
.tag {{ font-size:34px; color:#cfe9e2; }}
h2 {{ margin-top:24px; font-size:66px; font-weight:800; line-height:1.25; }}
.list {{ margin-top:50px; }}
.it {{ display:flex; justify-content:space-between; align-items:center; padding:26px 0; border-bottom:1px solid rgba(255,255,255,.1); }}
.n {{ font-size:40px; font-weight:700; }}
.r {{ font-size:30px; color:#a8d8cc; margin-top:8px; }}
.pc {{ font-size:60px; font-weight:800; }}
.foot {{ position:absolute; left:90px; bottom:60px; font-size:30px; color:#7fb5a8; }}
</style></head><body>
<div class="tag">오늘의 주요 종목</div>
<h2>AI·신흥 테마가 강세<br>엔비디아는 신고가</h2>
<div class="list">{items}</div>
<div class="foot">엔비디아 장중 약 237달러 · 기존 최고 종가 235.74달러 경신</div>
</body></html>"""

pages = {"thumbnail.png": thumb(), "body-1.png": body1(), "body-2.png": body2(), "body-3.png": body3()}
for name, html in pages.items():
    (SRC / name.replace(".png", ".html")).write_text(html, encoding="utf-8")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1080,"height":1080})
    for name in pages:
        pg.goto((SRC / name.replace(".png",".html")).as_uri())
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / name), clip={"x":0,"y":0,"width":1080,"height":1080})
        print("saved", name)
    b.close()
