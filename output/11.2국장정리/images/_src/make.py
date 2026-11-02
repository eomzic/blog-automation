from playwright.sync_api import sync_playwright
import os
OUT=os.path.dirname(os.path.abspath(__file__))+"/.."
BLUE="#7fb0ff"; RED="#ff7a7a"
CSS="""*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Apple SD Gothic Neo","Pretendard","Malgun Gothic",sans-serif;color:#eef7f5}
.up{color:%s}.dn{color:%s}
table{border-collapse:collapse;width:100%%}
td,th{padding:14px 18px;font-size:26px;text-align:left;border-bottom:1px solid #2f6b66}
th{font-size:22px;color:#9fd0c8;font-weight:600}
td.r,th.r{text-align:right}
h2{font-size:30px;margin-bottom:18px;color:#bff0e6}
.note{margin-top:16px;font-size:20px;color:#8fbfb7}
.card{background:#12403f;border:1px solid #2f6b66;border-radius:16px;padding:22px 26px}
.big{font-size:58px;font-weight:800}
.lbl{font-size:21px;color:#9fd0c8;margin-bottom:6px}
.row{display:flex;gap:20px;margin-bottom:20px}.row>.card{flex:1}
.pill{display:inline-block;padding:8px 18px;border-radius:30px;background:#1d5c58;font-size:24px;margin:6px 8px 6px 0}
"""%(RED,BLUE)
def chg(v):
    c="up" if v>=0 else "dn"; return f'<span class="{c}">{v:+.2f}%</span>'
def pt(v):
    c="up" if v>=0 else "dn"; return f'<span class="{c}">{v:+,.2f}p</span>'
def won(v):
    c="up" if v>=0 else "dn"; return f'<span class="{c}">{v:+,}</span>'
BG="background:#0f2a2c;padding:36px;width:900px"
imgs={}
imgs["body-1"]=f"""<h2>11/2 코스피·코스닥 마감</h2>
<div class="row"><div class="card"><div class="lbl">코스피</div><div class="big">5,859.08</div><div style="font-size:30px;margin-top:6px">{pt(128.34)} {chg(2.24)}</div></div>
<div class="card"><div class="lbl">코스닥</div><div class="big">734.36</div><div style="font-size:30px;margin-top:6px">{pt(9.98)} {chg(1.38)}</div></div></div>
<div class="card"><table><tr><th></th><th class="r">코스피</th><th class="r">코스닥</th></tr>
<tr><td>전일 종가</td><td class="r">5,730.74</td><td class="r">724.38</td></tr>
<tr><td>시가</td><td class="r">5,637.77</td><td class="r">716.44</td></tr>
<tr><td>장중 저점</td><td class="r">5,616.50</td><td class="r">—</td></tr>
<tr><td>장중 고점</td><td class="r">5,910.83</td><td class="r">—</td></tr></table></div>
<div class="note">언론 보도 수치 기반 합성 그래픽 · 고점은 매체별 5,908~5,911</div>"""
imgs["body-2"]=f"""<h2>투자자별 순매수 (11/2)</h2>
<div class="card"><table><tr><th>구분</th><th class="r">코스피(억원)</th><th class="r">코스닥(억원)</th></tr>
<tr><td>기관</td><td class="r">{won(12329)}</td><td class="r">{won(623)}</td></tr>
<tr><td>개인</td><td class="r">{won(-13475)}</td><td class="r">{won(-260)}</td></tr>
<tr><td>외국인</td><td class="r">{won(-3731)}</td><td class="r">{won(-322)}</td></tr></table></div>
<div class="note">참고: 10/30 외국인 코스피 -16,173억원 · 서울신문·블록미디어 기준</div>"""
imgs["body-3"]=f"""<h2>반도체 대형주 마감 (11/2)</h2>
<div class="card"><table><tr><th>종목</th><th class="r">종가(원)</th><th class="r">등락률</th></tr>
<tr><td>SK스퀘어</td><td class="r">950,000</td><td class="r">{chg(5.91)}</td></tr>
<tr><td>SK하이닉스</td><td class="r">1,472,000</td><td class="r">{chg(3.81)}</td></tr>
<tr><td>삼성전자</td><td class="r">229,000</td><td class="r">{chg(1.78)}</td></tr>
<tr><td>삼성전자우</td><td class="r">177,000</td><td class="r">{chg(1.67)}</td></tr></table></div>
<div class="note">전일 종가: SK하이닉스 1,418,000원 · 삼성전자 225,000원</div>"""
imgs["body-4"]=f"""<h2>낙폭과대 순환매 · 엇갈린 종목</h2>
<div class="row"><div class="card"><div class="lbl">한화에어로스페이스</div><div class="big">{chg(6.32)}</div></div>
<div class="card"><div class="lbl">삼성바이오로직스</div><div class="big">{chg(-4.37)}</div></div></div>
<div class="card"><div class="lbl" style="margin-bottom:12px">저PBR 공시 종목</div>
<span class="pill">현대제철 <span class="up">+11%대</span></span><span class="pill">롯데쇼핑 <span class="up">약 +9%</span></span><span class="pill">이마트 <span class="up">약 +7%</span></span>
<div class="lbl" style="margin:18px 0 12px">코스닥</div>
<span class="pill">HLB <span class="up">+4.25%</span></span><span class="pill">에코프로 <span class="up">+2.22%</span></span><span class="pill">알테오젠 <span class="up">+0.71%</span></span></div>
<div class="note">inews24·블록미디어 보도 기반</div>"""
thumb=f"""<html><head><meta charset="utf-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1080px;font-family:"Apple SD Gothic Neo","Pretendard",sans-serif;color:#fff;background:linear-gradient(160deg,#0f2027 0%,#134e4a 100%);padding:90px 80px;position:relative}}
.tag{{font-size:30px;color:#8fe3d3;letter-spacing:2px;margin-bottom:40px}}
.t{{font-size:76px;font-weight:800;line-height:1.25;width:560px}}
.sub{{font-size:34px;color:#b5ddd5;margin-top:36px;line-height:1.5;width:560px}}
.num{{position:absolute;right:80px;top:700px;text-align:right}}
.num b{{display:block;font-size:210px;line-height:1;color:#ff8a8a;font-weight:900}}
.num span{{font-size:36px;color:#b5ddd5}}
.bar{{position:absolute;left:80px;bottom:90px;width:200px;height:10px;border-radius:5px;background:#8fe3d3}}
</style></head><body><div class="tag">내일도 주린이 · 국장 정리 11/2</div>
<div class="t">5,616에서<br>5,910까지,<br>하루 만에<br>뒤집었다</div>
<div class="sub">코스피 5,859.08<br>기관 +1조 2,329억원</div>
<div class="num"><b>+2.24%</b><span>코스피 반등 마감</span></div><div class="bar"></div></body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,body in imgs.items():
        pg=b.new_page(viewport={"width":900,"height":100})
        pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="{BG}">{body}</body></html>')
        pg.locator("body").screenshot(path=f"{OUT}/{n}.png")
    pg=b.new_page(viewport={"width":1080,"height":1080})
    pg.set_content(thumb); pg.screenshot(path=f"{OUT}/thumbnail.png")
    b.close()
