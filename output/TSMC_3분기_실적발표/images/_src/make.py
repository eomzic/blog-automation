import os
from playwright.sync_api import sync_playwright
BASE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(BASE)
CSS="""*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Apple SD Gothic Neo',sans-serif;background:#fff}
.card{width:1000px;padding:44px 52px;background:#f4faf8;border:3px solid #134e4a;border-radius:24px}
h3{font-size:36px;color:#0f2027;margin-bottom:26px}.src{font-size:20px;color:#6b7c78;margin-top:22px}
table{width:100%;border-collapse:collapse;font-size:28px}th{background:#134e4a;color:#fff;padding:14px 18px;text-align:left}
td{padding:14px 18px;border-bottom:2px solid #d3e6e1;color:#223}td.r{text-align:right;font-weight:800;color:#0b6b5e}
.bar{height:34px;background:#2fa89a;border-radius:8px}.row{display:flex;align-items:center;margin:16px 0;font-size:28px}
.lab{width:200px;color:#0f2027;font-weight:700}.val{margin-left:16px;font-weight:800;color:#0b6b5e;width:90px}
.cards{display:flex;gap:20px}.k{flex:1;background:#fff;border:2px solid #b9dcd5;border-radius:16px;padding:24px}
.k b{display:block;font-size:22px;color:#4d6660;margin-bottom:10px}.k span{font-size:38px;font-weight:800;color:#0b6b5e}.k i{display:block;font-style:normal;font-size:20px;color:#6b7c78;margin-top:8px}
.tl{position:relative;margin:10px 0}.ev{display:flex;gap:20px;align-items:center;margin:18px 0;font-size:28px}.t{width:150px;font-weight:800;color:#0b6b5e}
.dot{width:20px;height:20px;border-radius:50%;background:#2fa89a}.dn{color:#1d6fe0;font-weight:800}"""
def card(b): return f"<html><head><meta charset='UTF-8'><style>{CSS}</style></head><body><div class='card'>{b}</div></body></html>"
def bars(items,mx):
    return "".join(f"<div class='row'><div class='lab'>{n}</div><div class='bar' style='width:{v/mx*560}px'></div><div class='val'>{v}%</div></div>" for n,v in items)
pages={
"thumbnail":"""<html><head><meta charset='UTF-8'><style>*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;font-family:'Apple SD Gothic Neo',sans-serif;background:linear-gradient(160deg,#0f2027 0%,#134e4a 100%);color:#fff;padding:90px 80px;display:flex;flex-direction:column;align-items:center;text-align:center;justify-content:center;gap:50px}
.badge{font-size:28px;font-weight:700;padding:12px 34px;background:rgba(255,255,255,.12);border-radius:40px;color:#9be8d8}
.t{font-size:92px;font-weight:800;line-height:1.3;letter-spacing:-2px}.s{font-size:36px;color:rgba(255,255,255,.7)}
.bar{width:420px;height:10px;border-radius:5px;background:#2fd4b8}</style></head><body>
<div class='badge'>내일도 주린이 · 실적발표</div><div class='t'>TSMC 3분기<br>순이익 사상 최대</div><div class='bar'></div>
<div class='s'>7,630억 대만달러 · 전년比 +68.7%</div></body></html>""",
"body-1":card("<h3>TSMC 2026년 3분기 실적 한눈에</h3><table><tr><th>항목</th><th style='text-align:right'>실적</th><th style='text-align:right'>비교</th></tr>"
 "<tr><td>매출(달러)</td><td class='r'>467.2억</td><td class='r'>+41.2% YoY</td></tr>"
 "<tr><td>순이익(대만달러)</td><td class='r'>7,630.6억</td><td class='r'>+68.7% YoY</td></tr>"
 "<tr><td>ADR당 EPS</td><td class='r'>$4.60</td><td class='r'>예상 $4.42</td></tr>"
 "<tr><td>순이익률</td><td class='r'>51.1%</td><td class='r'>전년 45.7%</td></tr></table><div class='src'>합성 그래픽 · 출처: TSMC 3Q26 실적 발표(10/15)</div>"),
"body-2":card("<h3>공정별 웨이퍼 매출 비중</h3>"+bars([("2나노",8),("3나노",33),("5나노",28),("7나노",10)],33)+"<div class='src'>7나노 이하 합계 79% · 매출총이익률 66.4%(-1.3%p, 2나노 희석)<br>합성 그래픽 · 출처: TSMC 3Q26</div>"),
"body-3":card("<h3>플랫폼별 매출 비중 (전분기比)</h3>"+bars([("HPC",68),("스마트폰",21),("차량",4),("IoT",4)],68)+"<div class='src'>HPC +22% · 스마트폰 +10% · 차량 +23% · IoT +5% QoQ<br>합성 그래픽 · 출처: TSMC 3Q26</div>"),
"body-4":card("<h3>4분기 가이던스와 투자 계획</h3><div class='cards'><div class='k'><b>4Q 매출 가이던스</b><span>523~543억$</span><i>중간값 전분기比 약 +14%</i></div><div class='k'><b>2026 설비투자</b><span>600~640억$</span><i>3분기 138.4억$ 집행</i></div><div class='k'><b>연간 매출 성장률</b><span>약 44%</span><i>달러 기준, 상향</i></div></div><div class='src'>4Q 매출총이익률 65~67% · 영업이익률 56.5~58.5%<br>합성 그래픽 · 출처: TSMC 3Q26</div>"),
"body-5":card("<h3>10/15 하루, 시간 순서로 보면</h3><div class='ev'><div class='t'>오전</div><div class='dot'></div><div>코스피 5,554.22 (<span class='dn'>-7.57%</span>), 서킷브레이커</div></div>"
 "<div class='ev'><div class='t'>15:00</div><div class='dot'></div>TSMC 3분기 실적 설명회 시작</div>"
 "<div class='ev'><div class='t'>15:30</div><div class='dot'></div><div>국장 마감 – 삼성전자 <span class='dn'>-9.48%</span>, 하이닉스 <span class='dn'>-11.06%</span></div></div>"
 "<div class='ev'><div class='t'>10/16~</div><div class='dot'></div>실적·가이던스 반영 여부는 이후 장에서 확인</div><div class='src'>합성 그래픽 · 한국시간 기준</div>"),
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
