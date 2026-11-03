import os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(BASE)

# 팔레트: 버건디-마룬 (급락·쇼크성 뉴스) — 직전 글들(SK하이닉스=딥퍼플, 10.28=네이비퍼플, 10.27=딥그린틸)과
# 겹치지 않도록 선택. 액센트: 금색(실적/호재) + 파랑(주가 하락, 한국 증시 등락 관례 준수).
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Apple SD Gothic Neo',sans-serif;background:#fff}
.card{width:1000px;padding:48px 54px;background:#fdf7f1;border:3px solid #4a1414;border-radius:20px}
.ribbon{display:inline-block;background:#4a1414;color:#fdf7f1;font-size:22px;font-weight:700;padding:8px 20px;border-radius:8px;margin-bottom:22px}
h3{font-size:34px;color:#2d0a0a;margin-bottom:28px;font-weight:800}
.src{font-size:19px;color:#9c8475;margin-top:24px;line-height:1.6}
.gold{color:#a8671f}
.blue{color:#2f5fa8}
.row3{display:flex;gap:18px}
.pc{flex:1;background:#fff;border:2px solid #e8d9ca;border-radius:16px;padding:22px 20px}
.pc b{display:block;font-size:20px;color:#6b584c;margin-bottom:10px;font-weight:700}
.pc span{display:block;font-size:30px;font-weight:900;line-height:1.25}
.pc i{display:block;font-style:normal;font-size:18px;color:#8a7268;margin-top:8px}
.bar{display:flex;align-items:center;margin:16px 0;font-size:22px}
.bar .lab{width:200px;font-weight:700;color:#2d0a0a;white-space:nowrap}
.bar .track{flex:1;height:34px;background:#f0e4d8;border-radius:8px;position:relative;overflow:hidden}
.bar .fill{height:100%;border-radius:8px}
.bar .val{width:170px;text-align:right;font-weight:800}
.stackwrap{margin:8px 0 20px}
.stack{display:flex;height:52px;border-radius:10px;overflow:hidden;background:#f0e4d8}
.stack div{display:flex;align-items:center;justify-content:center;color:#fff;font-size:21px;font-weight:700}
.flow{display:flex;align-items:center;gap:16px;margin:22px 0;font-size:24px;font-weight:700}
.flow .pt{background:#fff;border:2px solid #e8d9ca;border-radius:12px;padding:14px 22px;color:#2d0a0a}
.flow .arrow{color:#b08a5a;font-size:26px}
.warn{background:#fbeeee;border-left:4px solid #4a1414;padding:16px 20px;border-radius:8px;font-size:21px;color:#5a2020;margin-top:18px}
.vscards{display:flex;gap:22px}
.vc{flex:1;background:#fff;border:2px solid #e8d9ca;border-radius:16px;padding:26px 24px}
.vc .name{font-size:22px;font-weight:800;color:#2d0a0a;margin-bottom:4px}
.vc .date{font-size:17px;color:#9c8475;margin-bottom:16px}
.vc .num{font-size:34px;font-weight:900;color:#2d0a0a}
.vc .sub{font-size:18px;color:#8a7268;margin:8px 0 16px}
.vc .chg{display:inline-block;font-size:26px;font-weight:900;padding:6px 16px;border-radius:8px}
.rank{display:flex;align-items:center;margin:14px 0;font-size:23px}
.rank .n{width:230px;font-weight:700;color:#2d0a0a}
.rank .track{flex:1;height:30px;background:#f0e4d8;border-radius:7px;overflow:hidden}
.rank .fill{height:100%;border-radius:7px;background:linear-gradient(90deg,#d4a24c,#a8671f)}
.rank .v{width:110px;text-align:right;font-weight:800;color:#a8671f}
"""

def card(inner):
    return f"<html><head><meta charset='UTF-8'><style>{CSS}</style></head><body><div class='card'>{inner}</div></body></html>"

def bar(label, pct_width, color, val):
    return f"<div class='bar'><div class='lab'>{label}</div><div class='track'><div class='fill' style='width:{pct_width}%;background:{color}'></div></div><div class='val' style='color:{color}'>{val}</div></div>"

def rank(label, pct_width, val, highlight=False):
    extra = "box-shadow:inset 0 0 0 2px #a8671f;" if highlight else ""
    return f"<div class='rank' style='{extra}border-radius:8px;padding:4px 6px'><div class='n'>{label}</div><div class='track'><div class='fill' style='width:{pct_width}%'></div></div><div class='v'>{val}</div></div>"

pages = {}

pages["thumbnail"] = """<html><head><meta charset='UTF-8'><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;font-family:'Apple SD Gothic Neo',sans-serif;
background:linear-gradient(145deg,#2d0a0a 0%,#4a1414 100%);color:#fff;
padding:96px 88px;display:flex;flex-direction:column;justify-content:space-between}
.badge{align-self:flex-start;font-size:27px;font-weight:700;padding:12px 28px;
background:rgba(255,255,255,.1);border-radius:10px;color:#f3d5c6;border-left:5px solid #c9922f}
.t{font-size:70px;font-weight:800;line-height:1.42;letter-spacing:-1.5px}
.gold{color:#e0ab52}
.blue{color:#6fa0e8}
.stats{display:flex;align-items:flex-end;gap:40px}
.stat{flex:1}
.stat .v{font-size:112px;font-weight:900;line-height:1;letter-spacing:-3px}
.stat .l{font-size:25px;color:rgba(255,255,255,.62);margin-top:16px;font-weight:600}
.arrow{font-size:40px;color:rgba(255,255,255,.3);font-weight:800;padding-bottom:30px}
</style></head><body>
<div class='badge'>내일도 주린이 · 실적발표</div>
<div class='t'>삼성전자 3분기,<br><span class='gold'>역대 최대</span> 실적인데<br>주가는 <span class='blue'>거꾸로 급락</span></div>
<div class='stats'>
<div class='stat'><div class='v gold'>107조</div><div class='l'>영업이익 (+783%)</div></div>
<div class='arrow'>&rarr;</div>
<div class='stat'><div class='v blue'>-5%</div><div class='l'>주가 (장중)</div></div>
</div>
</body></html>"""

# body-1: 핵심 포인트 카드 — 매출/영업이익/주가 3연속 대비
pages["body-1"] = card(
    "<div class='ribbon'>실적 vs 주가</div>"
    "<h3>삼성전자 3분기: 실적은 역대급, 주가는 역주행</h3>"
    "<div class='row3'>"
    "<div class='pc'><b>매출</b><span class='gold'>195.3조원</span><i>전년比 +126.9%</i></div>"
    "<div class='pc'><b>영업이익</b><span class='gold'>107.4조원</span><i>전년比 +783.1%, 분기 최초 100조 돌파</i></div>"
    "<div class='pc'><b>주가(장중)</b><span class='blue'>-4.75%~-5.37%</span><i>코스피도 동반 약 -2.6%</i></div>"
    "</div>"
    "<div class='src'>영업이익은 컨센서스 근소 상회, 순이익은 컨센서스 대비 약 -12.8%<br>합성 그래픽 · 출처: 삼성전자 3Q26 실적 공시·컨퍼런스콜(10/29)</div>"
)

# body-2: 사업부문별 영업이익 비교 (가로 막대, sqrt 스케일)
pages["body-2"] = card(
    "<div class='ribbon'>사업부문별 손익</div>"
    "<h3>메모리가 다 벌고, 완제품은 적자</h3>"
    + bar("DS(반도체)", 100, "#a8671f", "106.5조")
    + bar("디스플레이", 32, "#c98a2e", "1.1조")
    + bar("하만", 24, "#c98a2e", "0.6조")
    + bar("DX(모바일·가전)", 28, "#2f5fa8", "-0.8조")
    + "<div class='warn'>DS 영업이익률 72%(역대 최대), 이익의 약 99%가 메모리 한 곳에서 발생. DX는 칩플레이션(부품원가 상승)으로 적자 전환.</div>"
    "<div class='src'>막대 길이는 절대값의 제곱근 비례(시각 보정) · 합성 그래픽 · 출처: 삼성전자 3Q26 사업부문별 실적</div>"
)

# body-3: 주주환원 집행 vs 잔여 (스택 바 + 연기 플로우)
pages["body-3"] = card(
    "<div class='ribbon'>주주환원 진행 상황</div>"
    "<h3>주주환원 90~110조원 중 어디까지 왔나</h3>"
    "<div class='stackwrap'><div class='stack'>"
    "<div style='width:33%;background:#a8671f'>집행 약 35조</div>"
    "<div style='width:67%;background:#d9c3a8;color:#4a1414'>잔여 55~75조</div>"
    "</div></div>"
    "<div class='flow'><div class='pt'>지금 (2026.10)</div><div class='arrow'>&rarr;</div>"
    "<div class='pt' style='border-color:#2f5fa8;color:#2f5fa8'>2027년 1월 이사회</div></div>"
    "<div class='warn'>자사주 매입·소각 '구체안'은 여기서 확정 — 규모·시점 모두 아직 비공개. 삼성생명·삼성화재 지분율이 금산법 10% 한도에 근접해 보통주 소각 시 한도 초과 우려도 변수.</div>"
    "<div class='src'>합성 그래픽 · 출처: 삼성전자 3Q26 컨퍼런스콜(CFO 박순철 발언)</div>"
)

# body-4: SK하이닉스 vs 삼성전자 비교 카드
pages["body-4"] = card(
    "<div class='ribbon'>하루 차이, 정반대 반응</div>"
    "<h3>어제는 오르고, 오늘은 내렸다</h3>"
    "<div class='vscards'>"
    "<div class='vc'><div class='name'>SK하이닉스</div><div class='date'>발표 10/28</div>"
    "<div class='num'>83.33조</div><div class='sub'>컨센서스 대비 +8.3% 서프라이즈</div>"
    "<div class='chg' style='background:#fbeeee;color:#c0392b'>+1.61%</div></div>"
    "<div class='vc'><div class='name'>삼성전자</div><div class='date'>발표 10/29</div>"
    "<div class='num'>107.44조</div><div class='sub'>영업이익 소폭 상회, 순이익·DS는 눈높이 미달</div>"
    "<div class='chg' style='background:#eaf0fb;color:#2f5fa8'>-4.75~-5.37%</div></div>"
    "</div>"
    "<div class='src'>영업이익 절대 규모는 삼성전자가 크지만, 서프라이즈 강도·주가 반응은 정반대<br>합성 그래픽 · 출처: 각 사 3Q26 실적 공시</div>"
)

# body-5: 목표주가 증권사별 비교 (랭킹 바)
pages["body-5"] = card(
    "<div class='ribbon'>4분기 전망</div>"
    "<h3>증권사 목표주가, 대체로 상향</h3>"
    + rank("유안타증권", 100, "63만원", True)
    + rank("KB증권", 93, "61만원")
    + rank("SK증권", 89, "60만원")
    + rank("한화투자증권", 83, "58만원")
    + rank("유진투자증권", 76, "56만원")
    + rank("DS투자·신한투자", 69, "53만원")
    + "<div class='src'>메모리 공급부족 심화·HBM4 확대 전망 반영 · 정확한 액수는 교차 확인 기준, 참고용<br>합성 그래픽 · 출처: 각 증권사 리포트 종합</div>"
)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(device_scale_factor=2)
    for name, html in pages.items():
        path = f"{BASE}/{name}.html"
        with open(path, "w") as f:
            f.write(html)
        if name == "thumbnail":
            pg.set_viewport_size({"width": 1080, "height": 1080})
            pg.goto(f"file://{path}")
            pg.wait_for_timeout(150)
            pg.screenshot(path=f"{OUT}/{name}.png", clip={"x": 0, "y": 0, "width": 1080, "height": 1080})
        else:
            pg.set_viewport_size({"width": 1000, "height": 1000})
            pg.goto(f"file://{path}")
            pg.wait_for_timeout(150)
            pg.query_selector(".card").screenshot(path=f"{OUT}/{name}.png")
    b.close()

print("done")
