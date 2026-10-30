import os
from playwright.sync_api import sync_playwright
BASE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(BASE)
CSS="""*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Apple SD Gothic Neo',sans-serif;background:#fff}
.card{width:1000px;padding:44px 52px;background:#faf6fd;border:3px solid #3d1a5c;border-radius:24px}
h3{font-size:36px;color:#1e0a3c;margin-bottom:26px}.src{font-size:20px;color:#7a6b88;margin-top:22px}
table{width:100%;border-collapse:collapse;font-size:27px}th{background:#3d1a5c;color:#fff;padding:14px 18px;text-align:left}
td{padding:14px 18px;border-bottom:2px solid #e6d8f0;color:#2a1a3a}td.r{text-align:right;font-weight:800;color:#6a2c9a}
.row{display:flex;align-items:center;margin:18px 0;font-size:27px}.lab{width:250px;color:#1e0a3c;font-weight:700}
.bar{height:38px;border-radius:8px}.val{margin-left:16px;font-weight:800;color:#6a2c9a}
.cards{display:flex;gap:20px}.k{flex:1;background:#fff;border:2px solid #d9c3e8;border-radius:16px;padding:24px}
.k b{display:block;font-size:22px;color:#6b5a7a;margin-bottom:10px}.k span{font-size:36px;font-weight:800;color:#6a2c9a}.k i{display:block;font-style:normal;font-size:20px;color:#7a6b88;margin-top:8px}
.ev{display:flex;gap:20px;align-items:center;margin:20px 0;font-size:27px}.t{width:170px;font-weight:800;color:#6a2c9a}.dot{width:20px;height:20px;border-radius:50%;background:#a15ad0;flex:none}
.stack{display:flex;height:60px;border-radius:10px;overflow:hidden;margin:10px 0 18px}.stack div{display:flex;align-items:center;justify-content:center;color:#fff;font-size:24px;font-weight:700}"""
def card(b): return f"<html><head><meta charset='UTF-8'><style>{CSS}</style></head><body><div class='card'>{b}</div></body></html>"
def bar(l,v,mx,c,txt): return f"<div class='row'><div class='lab'>{l}</div><div class='bar' style='width:{v/mx*480}px;background:{c}'></div><div class='val'>{txt}</div></div>"
pages={
"thumbnail":"""<html><head><meta charset='UTF-8'><style>*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;font-family:'Apple SD Gothic Neo',sans-serif;background:linear-gradient(150deg,#1e0a3c 0%,#3d1a5c 100%);color:#fff;padding:100px 90px;display:flex;flex-direction:column;justify-content:space-between}
.badge{align-self:flex-start;font-size:28px;font-weight:700;padding:12px 32px;background:rgba(255,255,255,.12);border-radius:40px;color:#e0c2f5}
.t{font-size:84px;font-weight:800;line-height:1.3;letter-spacing:-2px}.big{font-size:260px;font-weight:900;color:#d9a8ff;line-height:1;text-align:right;letter-spacing:-8px}
.s{font-size:34px;color:rgba(255,255,255,.72)}</style></head><body>
<div class='badge'>내일도 주린이 · 실적발표</div><div class='t'>SK하이닉스<br>3분기 영업이익<br>83조 3,338억</div>
<div><div class='big'>80%</div><div class='s' style='text-align:right'>영업이익률 · 매출 첫 100조 돌파</div></div></body></html>""",
"body-1":card("<h3>SK하이닉스 2026년 3분기 실적 한눈에</h3><table><tr><th>항목</th><th style='text-align:right'>실적</th><th style='text-align:right'>전분기比</th></tr>"
 "<tr><td>매출</td><td class='r'>104조 6,155억</td><td class='r'>+32%</td></tr>"
 "<tr><td>영업이익</td><td class='r'>83조 3,338억</td><td class='r'>+38%</td></tr>"
 "<tr><td>영업이익률</td><td class='r'>약 80%</td><td class='r'>-</td></tr>"
 "<tr><td>순이익</td><td class='r'>39조 7,756억</td><td class='r'>순이익률 38%</td></tr></table><div class='src'>합성 그래픽 · 출처: SK하이닉스 3Q26 실적 공시(10/28)</div>"),
"body-2":card("<h3>영업이익: 예상 vs 실제 (조원)</h3>"+bar("컨센서스",76.964,83.3338,"#c9a5e0","76.96조")+bar("실제",83.3338,83.3338,"#6a2c9a","83.33조")+"<div class='src'>컨센서스 대비 약 +8.3% (직접 계산) · FnGuide 발표 전 집계<br>합성 그래픽 · 출처: 머니투데이(10/19), SK하이닉스 공시</div>"),
"body-3":card("<h3>3분기 영업이익: 삼성전자 vs SK하이닉스</h3><div class='cards'><div class='k'><b>삼성전자 (10/8 잠정)</b><span>107조 4,000억</span><i>매출 약 195조원 · 전사 기준</i></div><div class='k'><b>SK하이닉스 (10/28 확정)</b><span>83조 3,338억</span><i>매출 104조 6,155억 · 영업이익률 80%</i></div></div><div class='src'>합성 그래픽 · 출처: 각 사 공시, 언론 보도</div>"),
"body-4":card("<h3>올해 주주환원 약 100조원 구성</h3><div class='stack'><div style='width:33%;background:#a15ad0'>배당 30조+</div><div style='width:67%;background:#3d1a5c'>자사주 매입·소각 60조+</div></div><div class='cards'><div class='k'><b>이번 이사회 배당</b><span>14조원</span><i>주당 2만원 (실적 1만+특별 1만)</i></div><div class='k'><b>이번 자사주 매입</b><span>20조원</span><i>10조 소각 · 10조 임직원 보상</i></div></div><div class='src'>잉여현금흐름 50% 이상 환원 방침 · 3분기 말 순현금 98조 7,000억<br>합성 그래픽 · 출처: SK하이닉스 공시</div>"),
"body-5":card("<h3>4분기 이후 로드맵</h3><div class='ev'><div class='t'>4분기</div><div class='dot'></div><div>HBM4 출하·매출 모두 HBM3E 추월 전망</div></div>"
 "<div class='ev'><div class='t'>연말까지</div><div class='dot'></div><div>청주 M15X 생산능력 최대한 확대</div></div>"
 "<div class='ev'><div class='t'>2027년</div><div class='dot'></div><div>용인 1기 팹 가동 등 투자 올해보다 크게 증가</div></div>"
 "<div class='ev'><div class='t'>2027~28년</div><div class='dot'></div><div>14개 고객 장기계약, 생산능력 50% 이상 확보</div></div><div class='src'>합성 그래픽 · 출처: SK하이닉스 3Q26 실적 발표</div>"),
}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(device_scale_factor=2)
    for n,h in pages.items():
        open(f"{BASE}/{n}.html","w").write(h)
        pg.set_viewport_size({"width":1080 if n=="thumbnail" else 1000,"height":1080 if n=="thumbnail" else 760})
        pg.goto(f"file://{BASE}/{n}.html"); pg.wait_for_timeout(150)
        if n=="thumbnail": pg.screenshot(path=f"{OUT}/{n}.png",clip={"x":0,"y":0,"width":1080,"height":1080})
        else: pg.query_selector(".card").screenshot(path=f"{OUT}/{n}.png")
    b.close()
