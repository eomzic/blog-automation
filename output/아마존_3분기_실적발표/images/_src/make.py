import os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(BASE)

# 팔레트: 슬레이트-그레이 (보합·방향성 불분명 — AWS는 역대급, 주가는 급락이라 '혼조' 성격에 맞춤).
# 직전 글들(10.29국장정리=버건디, 삼성전자3Q=버건디, 10.28국장정리=네이비퍼플, SK하이닉스3Q=딥퍼플와인)과
# 겹치지 않도록 선택. 레이아웃도 최근 3편이 전부 "좌측정렬+배지 좌상단"이었던 것과 달리 중앙정렬로 변경.
# 액센트: 티얼(AWS/좋은 신호) + 파랑(주가 하락, 한국 증시 등락 관례 준수).
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Apple SD Gothic Neo',sans-serif;background:#fff}
.card{width:1000px;padding:48px 54px;background:#f4f5f6;border:3px solid #3a3d40;border-radius:20px}
.ribbon{display:inline-block;background:#3a3d40;color:#f4f5f6;font-size:22px;font-weight:700;padding:8px 20px;border-radius:8px;margin-bottom:22px}
h3{font-size:34px;color:#232526;margin-bottom:28px;font-weight:800}
.src{font-size:19px;color:#8b9094;margin-top:24px;line-height:1.6}
.teal{color:#2a8a82}
.blue{color:#2f5fa8}
.row3{display:flex;gap:18px}
.pc{flex:1;background:#fff;border:2px solid #dde0e2;border-radius:16px;padding:22px 20px}
.pc b{display:block;font-size:20px;color:#6b7073;margin-bottom:10px;font-weight:700}
.pc span{display:block;font-size:28px;font-weight:900;line-height:1.25}
.pc i{display:block;font-style:normal;font-size:17px;color:#8b9094;margin-top:8px}
.bar{display:flex;align-items:center;margin:16px 0;font-size:22px}
.bar .lab{width:210px;font-weight:700;color:#232526;white-space:nowrap}
.bar .track{flex:1;height:34px;background:#e4e6e8;border-radius:8px;position:relative;overflow:hidden}
.bar .fill{height:100%;border-radius:8px}
.bar .val{width:160px;text-align:right;font-weight:800}
.flow{display:flex;align-items:center;gap:14px;margin:20px 0;font-size:21px;font-weight:700}
.flow .pt{background:#fff;border:2px solid #dde0e2;border-radius:12px;padding:16px 18px;color:#232526;flex:1;text-align:center}
.flow .arrow{color:#9aa0a4;font-size:26px}
.warn{background:#eef3f3;border-left:4px solid #2a8a82;padding:16px 20px;border-radius:8px;font-size:21px;color:#1f4f4a;margin-top:18px}
.vscards{display:flex;gap:22px}
.vc{flex:1;background:#fff;border:2px solid #dde0e2;border-radius:16px;padding:24px 22px}
.vc .name{font-size:21px;font-weight:800;color:#232526;margin-bottom:4px}
.vc .date{font-size:16px;color:#8b9094;margin-bottom:14px}
.vc .num{font-size:30px;font-weight:900;color:#232526}
.vc .sub{font-size:17px;color:#8b9094;margin:8px 0 14px}
.vc .chg{display:inline-block;font-size:24px;font-weight:900;padding:6px 16px;border-radius:8px}
.rank{display:flex;align-items:center;margin:14px 0;font-size:22px}
.rank .n{width:210px;font-weight:700;color:#232526}
.rank .track{flex:1;height:30px;background:#e4e6e8;border-radius:7px;overflow:hidden}
.rank .fill{height:100%;border-radius:7px}
.rank .v{width:130px;text-align:right;font-weight:800}
.pointgrid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.point{background:#fff;border:2px solid #dde0e2;border-radius:16px;padding:20px 22px}
.point .k{font-size:18px;color:#8b9094;font-weight:700;margin-bottom:8px}
.point .v{font-size:27px;font-weight:900;color:#232526}
.point .s{font-size:16px;color:#8b9094;margin-top:6px}
"""

def card(inner):
    return f"<html><head><meta charset='UTF-8'><style>{CSS}</style></head><body><div class='card'>{inner}</div></body></html>"

def bar(label, pct_width, color, val):
    return f"<div class='bar'><div class='lab'>{label}</div><div class='track'><div class='fill' style='width:{pct_width}%;background:{color}'></div></div><div class='val' style='color:{color}'>{val}</div></div>"

def rank(label, pct_width, val, color="#2a8a82"):
    return f"<div class='rank'><div class='n'>{label}</div><div class='track'><div class='fill' style='width:{pct_width}%;background:{color}'></div></div><div class='v' style='color:{color}'>{val}</div></div>"

pages = {}

# 썸네일: 중앙정렬 레이아웃 (직전 3편의 '배지 좌상단 + 좌측정렬'과 다르게 구성)
# space-between으로 상(배지)/중(타이틀+숫자)/하(부제+구분선+라벨)에 고르게 배분해 하단 여백 과다 문제를 방지.
pages["thumbnail"] = """<html><head><meta charset='UTF-8'><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;font-family:'Apple SD Gothic Neo',sans-serif;
background:radial-gradient(circle at 80% 15%, rgba(255,255,255,.06), transparent 45%),linear-gradient(160deg,#232526 0%,#3a3d40 100%);
color:#fff;padding:84px 80px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;text-align:center;position:relative}
.badge{font-size:25px;font-weight:700;padding:11px 26px;background:rgba(255,255,255,.1);
border-radius:30px;color:#cfd3d5;letter-spacing:.5px}
.mid{display:flex;flex-direction:column;align-items:center}
.t{font-size:62px;font-weight:800;line-height:1.38;letter-spacing:-1.3px;margin-bottom:56px}
.teal{color:#5fc9bd}
.blue{color:#7fa8e8}
.stats{display:flex;align-items:center;gap:30px;justify-content:center}
.stat .v{font-size:92px;font-weight:900;line-height:1;letter-spacing:-2.5px}
.stat .l{font-size:23px;color:rgba(255,255,255,.6);margin-top:14px;font-weight:600}
.arrow{font-size:34px;color:rgba(255,255,255,.3);font-weight:800}
.foot{display:flex;flex-direction:column;align-items:center;gap:26px;width:100%}
.sub{font-size:25px;color:rgba(255,255,255,.6);font-weight:600}
.rule{width:100%;height:1px;background:rgba(255,255,255,.14)}
.date{font-size:20px;color:rgba(255,255,255,.4);font-weight:600;letter-spacing:1px}
.corner{position:absolute;top:0;right:0;width:280px;height:280px;
background:radial-gradient(circle at top right, rgba(95,201,189,.2), transparent 70%)}
.corner2{position:absolute;bottom:0;left:0;width:300px;height:220px;
background:radial-gradient(circle at bottom left, rgba(127,168,232,.14), transparent 70%)}
</style></head><body>
<div class='corner'></div>
<div class='corner2'></div>
<div class='badge'>내일도 주린이 · 실적발표</div>
<div class='mid'>
<div class='t'>아마존 3분기, AWS는 날았는데<br>주가는 <span class='blue'>거꾸로 급락</span></div>
<div class='stats'>
<div class='stat'><div class='v teal'>+61%</div><div class='l'>영업이익</div></div>
<div class='arrow'>&rarr;</div>
<div class='stat'><div class='v blue'>-5~7%</div><div class='l'>주가(시간외)</div></div>
</div>
</div>
<div class='foot'>
<div class='sub'>AWS +39% · 현금흐름은 적자</div>
<div class='rule'></div>
<div class='date'>2026 Q3 EARNINGS · 10.30</div>
</div>
</body></html>"""

# body-1: 사업부문별 성장률 비교 (비교 표 템플릿)
pages["body-1"] = card(
    "<div class='ribbon'>사업부문별 온도차</div>"
    "<h3>AWS는 질주, 전자상거래·광고는 주춤</h3>"
    "<div class='row3'>"
    "<div class='pc'><b>AWS</b><span class='teal'>+39.3%</span><i>459.8억 달러, 영업이익률 38.7%</i></div>"
    "<div class='pc'><b>온라인 스토어</b><span class='blue'>+2%</span><i>684.7억 달러, 컨센서스 하회</i></div>"
    "<div class='pc'><b>광고</b><span class='blue'>컨센서스 하회</span><i>196.4억 달러</i></div>"
    "</div>"
    "<div class='warn'>AWS 영업이익이 전사 영업이익의 60% 이상을 차지 — 사실상 아마존을 떠받치는 건 클라우드 한 곳.</div>"
    "<div class='src'>합성 그래픽 · 출처: 아마존 3Q26 실적 공시(10/29)</div>"
)

# body-2: 3분기 핵심 수치 (포인트 카드 템플릿)
pages["body-2"] = card(
    "<div class='ribbon'>3분기 핵심 수치</div>"
    "<h3>매출·영업이익은 늘었는데 EPS가 발목</h3>"
    "<div class='pointgrid'>"
    "<div class='point'><div class='k'>매출</div><div class='v'>2,019.4억 달러</div><div class='s'>전년比 +12%, 컨센서스 소폭 하회</div></div>"
    "<div class='point'><div class='k'>영업이익</div><div class='v teal'>281억 달러</div><div class='s'>전년比 +61%, 영업이익률 13.9%(역대 최고)</div></div>"
    "<div class='point'><div class='k'>순이익</div><div class='v'>207억 달러</div><div class='s'>전년 212억 달러 — 작년 앤스로픽 평가이익 기저효과</div></div>"
    "<div class='point'><div class='k'>EPS</div><div class='v blue'>1.89달러</div><div class='s'>컨센서스 1.97달러 하회</div></div>"
    "</div>"
    "<div class='src'>합성 그래픽 · 출처: 아마존 3Q26 실적 공시·컨센서스(블룸버그 집계)</div>"
)

# body-3: capex·FCF 추이 (단계별 플로우 템플릿)
pages["body-3"] = card(
    "<div class='ribbon'>AI 투자가 만든 적자</div>"
    "<h3>capex는 늘고, 현금흐름은 마이너스로</h3>"
    "<div class='flow'>"
    "<div class='pt'>2026년 capex 가이던스<br><b style='font-size:26px;color:#232526'>약 2,200억 달러</b><br><span style='font-size:15px;color:#8b9094'>유지</span></div>"
    "<div class='arrow'>&rarr;</div>"
    "<div class='pt'>3분기 현금 capex<br><b style='font-size:26px;color:#232526'>759억 달러</b><br><span style='font-size:15px;color:#8b9094'>대부분 AWS·AI</span></div>"
    "<div class='arrow'>&rarr;</div>"
    "<div class='pt'>최근 12개월 FCF<br><b style='font-size:26px;color:#2f5fa8'>-424억 달러</b><br><span style='font-size:15px;color:#8b9094'>전년比 적자 약 5배</span></div>"
    "</div>"
    "<div class='warn'>AWS 수주잔고는 2분기 말 4,960억 달러→3분기 말 5,780억 달러로 증가. "
    "재시 CEO: \"용량을 설치하는 속도만큼 고객이 가져간다.\"</div>"
    "<div class='src'>합성 그래픽 · 출처: 아마존 3Q26 컨퍼런스콜·실적 공시</div>"
)

# body-4: 증권사 목표주가 비교 (비교 표 템플릿)
pages["body-4"] = card(
    "<div class='ribbon'>4분기 전망 · 증권사 반응</div>"
    "<h3>목표주가, 상향과 하향이 동시에</h3>"
    "<div class='vscards'>"
    "<div class='vc'><div class='name'>상향한 쪽</div><div class='date'>모건스탠리·UBS·티그레스</div>"
    "<div class='num teal'>335→350달러</div><div class='sub'>클라우드 성장·수익성 개선에 주목 (모건스탠리)</div>"
    "<div class='chg' style='background:#eef3f3;color:#2a8a82'>톱픽 유지</div></div>"
    "<div class='vc'><div class='name'>하향한 쪽</div><div class='date'>웰스파고·캔터 피츠제럴드</div>"
    "<div class='num blue'>338→329달러</div><div class='sub'>capex·비용 부담을 이유로 하향</div>"
    "<div class='chg' style='background:#eaf0fb;color:#2f5fa8'>투자의견은 유지</div></div>"
    "</div>"
    "<div class='warn'>4분기 매출 전망 2,400억~2,470억 달러 / 영업이익 전망 285억~335억 달러 — 연말 성수기 포함에도 기대치엔 다소 못 미친다는 평가.</div>"
    "<div class='src'>합성 그래픽 · 출처: 각 증권사 리포트 종합(10/30 기준)</div>"
)

# body-5: AWS·애저·구글클라우드 성장률 비교 (막대 템플릿)
pages["body-5"] = card(
    "<div class='ribbon'>같은 주 클라우드 삼국지</div>"
    "<h3>성장률만 보면 AWS가 3위</h3>"
    + bar("구글클라우드", 100, "#2a8a82", "+100%대")
    + bar("마이크로소프트 애저", 70, "#4fa39a", "+48%")
    + bar("AWS", 58, "#8b9094", "+39.3%")
    + "<div class='warn'>셋 다 역대급 성장인데 유독 1위 사업자 아마존만 주가 급락. 재시 CEO가 언급한 메모리·전력 공급부족은 삼성전자·SK하이닉스 메모리 수요와도 맞닿아 있는 지점.</div>"
    "<div class='src'>막대 길이는 참고용 상대 비교(절대 매출 규모와는 무관) · 합성 그래픽 · 출처: 각사 10/28~10/29 실적 발표 종합</div>"
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
