import sys
from playwright.sync_api import sync_playwright
BLUE="#7fb0ff"; RED="#ff7070"
BASE="""<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Apple SD Gothic Neo","Pretendard","Malgun Gothic",sans-serif;color:#f1f3f4;%s}
.up{color:%s}.dn{color:%s}
table{border-collapse:collapse;width:100%%}
td,th{padding:14px 18px;font-size:26px;text-align:left;border-bottom:1px solid #4a4f54}
th{font-size:22px;color:#aeb6bd;font-weight:600}
td.r,th.r{text-align:right}
h2{font-size:30px;margin-bottom:18px;color:#cfe3e0}
.note{margin-top:16px;font-size:20px;color:#9aa3aa}
.card{background:#2b2f33;border:1px solid #454b50;border-radius:16px;padding:22px 26px}
.big{font-size:58px;font-weight:800}
.lbl{font-size:21px;color:#9fb0b5;margin-bottom:6px}
.row{display:flex;gap:20px;margin-bottom:20px}.row>.card{flex:1}
</style></head><body>%s</body></html>"""
def page(w,body,bg="background:#232526;padding:36px;width:%dpx"):
    return BASE%(bg%w if "%d" in bg else bg,RED,BLUE,body)
def chg(v): 
    c="up" if v>=0 else "dn"; return f'<span class="{c}">{v:+.2f}%</span>'
imgs={}
imgs["body-1"]=(900,f"""<h2>10/30 코스피·코스닥 마감</h2>
<div class="row"><div class="card"><div class="lbl">코스피</div><div class="big">5,730.74</div><div style="font-size:30px;margin-top:6px"><span class="dn">-206.92p</span> {chg(-3.48)}</div></div>
<div class="card"><div class="lbl">코스닥</div><div class="big">724.38</div><div style="font-size:30px;margin-top:6px"><span class="dn">-28.85p</span> {chg(-3.83)}</div></div></div>
<div class="card"><table><tr><th></th><th class="r">코스피</th><th class="r">코스닥</th></tr>
<tr><td>시가</td><td class="r">5,760.35</td><td class="r">737.76</td></tr>
<tr><td>장중 저점</td><td class="r">5,599.42</td><td class="r">717.27</td></tr>
<tr><td>사이드카</td><td class="r" colspan="2">10:04 매도 발동</td></tr></table></div>
<div class="note">한국거래소 집계 보도 기반 합성 그래픽 · 코스피 이틀 연속 하락</div>""")
imgs["body-2"]=(900,f"""<h2>간밤 미국 빅테크 → 국내 반도체</h2>
<div class="card"><table><tr><th>구분</th><th class="r">등락률</th></tr>
<tr><td>알파벳</td><td class="r">{chg(-12.6)}</td></tr>
<tr><td>아마존</td><td class="r">{chg(-4.3)}</td></tr>
<tr><td>샌디스크</td><td class="r">{chg(-5.3)}</td></tr>
<tr><td>나스닥</td><td class="r">{chg(-1.38)}</td></tr>
<tr><td>S&amp;P500</td><td class="r">{chg(-0.30)}</td></tr>
<tr><td>다우</td><td class="r">{chg(-0.25)}</td></tr></table></div>
<div class="note">핵심: AI 투자 수익성(잉여현금흐름) 우려 확산</div>""")
imgs["body-3"]=(900,f"""<h2>반도체·대형주 마감 (10/30)</h2>
<div class="card"><table><tr><th>종목</th><th class="r">종가</th><th class="r">등락률</th></tr>
<tr><td>SK하이닉스</td><td class="r">1,418,000</td><td class="r">{chg(-7.08)}</td></tr>
<tr><td>삼성전기</td><td class="r">1,196,000</td><td class="r">{chg(-7.50)}</td></tr>
<tr><td>SK스퀘어</td><td class="r">897,000</td><td class="r">{chg(-5.88)}</td></tr>
<tr><td>삼성전자우</td><td class="r">174,100</td><td class="r">{chg(-5.33)}</td></tr>
<tr><td>삼성전자</td><td class="r">225,000</td><td class="r">{chg(-3.02)}</td></tr>
<tr><td>현대차</td><td class="r">—</td><td class="r">{chg(-3.59)}</td></tr></table></div>
<div class="note">단위: 원 · 뉴스핌·서울신문 마감 기준</div>""")
imgs["body-4"]=(900,"""<h2>투자자별 수급 (코스피)</h2>
<div class="card"><table><tr><th></th><th class="r">현물</th><th class="r">선물</th></tr>
<tr><td>외국인</td><td class="r dn">-1조 6,173억</td><td class="r up">+1조 1,470억</td></tr>
<tr><td>기관</td><td class="r up">+7,426억</td><td class="r dn">-1조 1,192억</td></tr>
<tr><td>개인</td><td class="r up">+6,210억</td><td class="r dn">-82억</td></tr></table></div>
<div class="note">선물은 아시아경제 보도 기준 · 매체별 수십억원 차이 있음</div>""")
imgs["body-5"]=(900,f"""<h2>업종별 등락 (코스피)</h2>
<div class="row"><div class="card"><div class="lbl">상승</div><table>
<tr><td>제약</td><td class="r">{chg(4.9)}</td></tr><tr><td>운송창고</td><td class="r">{chg(1.33)}</td></tr><tr><td>음식료담배</td><td class="r">{chg(1.08)}</td></tr></table></div>
<div class="card"><div class="lbl">하락</div><table>
<tr><td>의료정밀</td><td class="r">{chg(-7.13)}</td></tr><tr><td>건설</td><td class="r">{chg(-6.22)}</td></tr><tr><td>운송장비</td><td class="r">{chg(-4.88)}</td></tr><tr><td>전기전자</td><td class="r">{chg(-4.67)}</td></tr></table></div></div>
<div class="note">삼성바이오로직스 +8.86% (1,487,000원)가 제약 업종 견인</div>""")
thumb=f"""<div style="width:1080px;height:1080px;background:linear-gradient(160deg,#232526,#3a3d40);padding:90px 90px;position:relative">
<div style="display:inline-block;border:2px solid #7fd6c8;color:#7fd6c8;font-size:30px;font-weight:700;padding:8px 22px;border-radius:30px">10/30 국장 정리</div>
<div style="font-size:84px;font-weight:800;line-height:1.25;margin-top:70px">외국인 1.6조 매도<br>사이드카 발동</div>
<div style="font-size:150px;font-weight:900;margin-top:70px" class="dn">-3.48%</div>
<div style="font-size:38px;color:#b9c2c8;margin-top:20px">코스피 5,730 · SK하이닉스 -7.08%</div></div>"""
with sync_playwright() as p:
    b=p.chromium.launch(); 
    for n,(w,body) in imgs.items():
        pg=b.new_page(viewport={"width":w,"height":100}); pg.set_content(page(w,body)); pg.screenshot(path=f"../{n}.png",full_page=True)
    pg=b.new_page(viewport={"width":1080,"height":1080}); pg.set_content(BASE%("margin:0",RED,BLUE,thumb)); pg.screenshot(path="../thumbnail.png")
    b.close()
