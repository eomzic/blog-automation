import os
from playwright.sync_api import sync_playwright
BASE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(BASE)
# 팔레트: 네이비-퍼플(#1a1a2e->#16213e), 시간외 하락 분위기. 상승=빨강, 하락=파랑(한국 관례)
CSS="""*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Apple SD Gothic Neo',sans-serif;background:#fff}
.card{width:1000px;padding:46px 52px;background:#f3f4fa;border:3px solid #1a1a2e;border-radius:20px}
.tag{display:inline-block;background:#1a1a2e;color:#fff;font-size:21px;font-weight:700;padding:8px 18px;border-radius:8px;margin-bottom:20px}
h3{font-size:33px;color:#16213e;font-weight:800;margin-bottom:26px;line-height:1.3}
.src{font-size:17px;color:#7b7f95;margin-top:22px}
.up{color:#d6342c}.dn{color:#2f5fa8}.nv{color:#16213e}
.row{display:flex;gap:18px}
.box{flex:1;background:#fff;border:2px solid #d9dbe8;border-radius:16px;padding:24px 22px}
.box .l{font-size:19px;font-weight:700;color:#5a5f78;margin-bottom:10px}
.box .n{font-size:38px;font-weight:900}
.box .s{font-size:17px;color:#7b7f95;margin-top:8px;line-height:1.4}
.bar{display:flex;align-items:center;margin:15px 0;font-size:21px}
.bar .lab{width:150px;font-weight:700;color:#16213e}
.bar .track{flex:1;height:34px;background:#e3e5f0;border-radius:8px;overflow:hidden}
.bar .fill{height:100%;border-radius:8px}
.bar .val{width:210px;text-align:right;font-weight:800}
.note{background:#e8eaf5;border-left:5px solid #1a1a2e;padding:16px 20px;border-radius:8px;font-size:20px;color:#16213e;margin-top:18px;line-height:1.5}
.split{display:flex;border-radius:14px;overflow:hidden}
.half{flex:1;padding:28px 24px}
.half.a{background:#fdeceb}.half.b{background:#e8eefa}
.half .l{font-size:19px;font-weight:700;color:#5a5f78;margin-bottom:8px}
.half .n{font-size:46px;font-weight:900}
.half .s{font-size:17px;color:#7b7f95;margin-top:8px}
"""
def page(b): return f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{b}</body></html>"
def bars(items,mx):
    o=""
    for lab,v,txt,c in items:
        o+=f"<div class='bar'><div class='lab'>{lab}</div><div class='track'><div class='fill' style='width:{v/mx*100:.1f}%;background:{c}'></div></div><div class='val' style='color:{c}'>{txt}</div></div>"
    return o
P={}
P['body-1']=f"""<div class='card'><div class='tag'>FY2026 4분기 · 9월 분기</div><h3>매출·EPS 모두 컨센서스를 넘겼어요</h3>
<div class='row'><div class='box'><div class='l'>매출</div><div class='n up'>1,144.8억$</div><div class='s'>전년比 +12%<br>컨센서스 1,133.9억$</div></div>
<div class='box'><div class='l'>EPS</div><div class='n up'>2.10$</div><div class='s'>전년比 +14%<br>컨센서스 1.99$</div></div>
<div class='box'><div class='l'>순이익</div><div class='n nv'>307.1억$</div><div class='s'>9월 분기 기록<br>전년 274.7억$</div></div></div>
<div class='note'>EPS 2.10$ 중 약 0.05$는 관세 환급 효과예요</div><div class='src'>출처: 애플 8-K, CNBC(LSEG) · 합성 그래픽</div></div>"""
P['body-2']=f"""<div class='card'><div class='tag'>제품군별 매출 (억달러)</div><h3>아이폰·Mac이 끌고, iPad·웨어러블은 뒷걸음</h3>
{bars([('iPhone',575.8,'575.8 (+17%)','#d6342c'),('Mac',107.9,'107.9 (+24%)','#d6342c'),('iPad',62.3,'62.3 (-10%대)','#2f5fa8'),('웨어러블·홈',83.0,'83.0 (-8%)','#2f5fa8')],600)}
<div class='note'>아이폰 18 프로 판매는 출시 후 8일치만 반영됐어요</div><div class='src'>출처: 애플 8-K · 합성 그래픽</div></div>"""
P['body-3']=f"""<div class='card'><div class='tag'>서비스 부문</div><h3>금액은 역대 최대, 성장 속도는 꺾이는 중</h3>
<div class='split'><div class='half a'><div class='l'>이번 분기 서비스 매출</div><div class='n up'>315.7억$</div><div class='s'>전년 287.5억$ · +9.8% · 역대 최대</div></div>
<div class='half b'><div class='l'>12월 분기 성장 가이던스</div><div class='n dn'>+8~9%</div><div class='s'>이번 분기도 2022년 이후 가장 느린 성장</div></div></div>
<div class='note'>서비스 매출총이익률 76.0%</div><div class='src'>출처: 애플 8-K, CNBC · 합성 그래픽</div></div>"""
P['body-4']=f"""<div class='card'><div class='tag'>지역별 매출 (억달러)</div><h3>중화권 +21%, 일본만 소폭 감소</h3>
{bars([('미주',486.8,'486.8 (+10%)','#d6342c'),('유럽',320.1,'320.1 (+12%)','#d6342c'),('중화권',175.4,'175.4 (+21%)','#d6342c'),('기타 아태',97.1,'97.1 (+15%)','#d6342c'),('일본',65.4,'65.4 (-1%)','#2f5fa8')],500)}
<div class='src'>출처: 애플 8-K 지역별 순매출 · 합성 그래픽</div></div>"""
P['body-5']=f"""<div class='card'><div class='tag'>12월 분기 가이던스</div><h3>매출은 기대 이상, 마진은 기대 이하</h3>
<div class='split'><div class='half a'><div class='l'>매출 성장 가이던스</div><div class='n up'>+7~10%</div><div class='s'>시장 기대 약 +6.1%</div></div>
<div class='half b'><div class='l'>매출총이익률 가이던스</div><div class='n dn'>45~46%</div><div class='s'>시장 기대 약 46.3% · 이번 분기 47.9%</div></div></div>
<div class='note'>메모리 비용이 6월 분기보다 올랐다고 애플이 밝혔어요</div><div class='src'>출처: CNBC · 합성 그래픽</div></div>"""
thumb="""<html><head><meta charset='utf-8'><style>*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;background:linear-gradient(135deg,#1a1a2e,#16213e);font-family:'Apple SD Gothic Neo',sans-serif;color:#fff;position:relative;overflow:hidden}
.badge{position:absolute;top:70px;left:80px;background:#fff;color:#16213e;font-size:30px;font-weight:800;padding:12px 26px;border-radius:10px}
.big{position:absolute;top:210px;left:80px;right:80px;font-size:98px;font-weight:900;line-height:1.2}
.big span{color:#ff7a70}
.sub{position:absolute;top:660px;left:80px;right:80px;font-size:42px;color:#c9cbe6;line-height:1.5}
.circ{position:absolute;right:-120px;bottom:-120px;width:420px;height:420px;border-radius:50%;background:rgba(255,255,255,.07)}
.foot{position:absolute;bottom:70px;left:80px;font-size:30px;color:#9a9dc2}</style></head><body>
<div class='badge'>애플 실적발표 · 11/2</div>
<div class='big'>매출 <span>1,145억$</span><br>역대급인데<br>시간외는 하락</div>
<div class='sub'>EPS 2.10$ 컨센서스 상회<br>12월 분기 마진 가이던스 45~46%</div>
<div class='circ'></div><div class='foot'>내일도 주린이</div></body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1100,'height':900})
    for k,h in P.items():
        pg.set_content(page(h)); pg.locator('.card').screenshot(path=f"{OUT}/{k}.png")
    pg.set_viewport_size({'width':1080,'height':1080}); pg.set_content(thumb); pg.screenshot(path=f"{OUT}/thumbnail.png")
    b.close()
