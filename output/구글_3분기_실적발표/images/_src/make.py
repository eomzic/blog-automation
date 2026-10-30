import os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(BASE)

# 팔레트: 슬레이트-그레이 (#232526 -> #3a3d40) — "방향성 불분명한 날" 용도.
# 이 글 자체가 "본업은 좋아졌는데 순이익 미스로 주가는 급락"하는 엇갈린 신호라 슬레이트가 잘 맞음.
# 직전 글들(10/29=버건디, 삼성전자=버건디, SK하이닉스=딥퍼플-와인, 10/28=네이비퍼플, 10/27=딥그린틸,
# TSMC=딥그린틸)과 겹치지 않도록 선택. 레이아웃도 새로 설계(좌우 분할 대비 구조, 이전처럼 좌측타이틀+우측화살표stat 안씀).
# 액센트: 호박색/amber(성장 지표) + 파랑(주가 하락, 한국 증시 등락 관례 준수).
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Apple SD Gothic Neo',sans-serif;background:#fff}
.card{width:1000px;padding:48px 54px;background:#f4f5f6;border:3px solid #3a3d40;border-radius:20px}
.ribbon{display:inline-block;background:#3a3d40;color:#f4f5f6;font-size:22px;font-weight:700;padding:8px 20px;border-radius:8px;margin-bottom:22px}
h3{font-size:33px;color:#232526;margin-bottom:28px;font-weight:800}
.src{font-size:18px;color:#7a8084;margin-top:24px;line-height:1.6}
.amber{color:#b5790f}
.blue{color:#2f5fa8}
.pillrow{display:flex;gap:18px}
.pill{flex:1;background:#fff;border:2px solid #d8dbdd;border-radius:16px;padding:22px 20px}
.pill b{display:block;font-size:19px;color:#5a6066;margin-bottom:10px;font-weight:700}
.pill span{display:block;font-size:29px;font-weight:900;line-height:1.25}
.pill i{display:block;font-style:normal;font-size:17px;color:#8a9096;margin-top:8px}
.split{display:flex;gap:0;border-radius:14px;overflow:hidden;margin:18px 0}
.half{flex:1;padding:26px 24px}
.half.left{background:#fdf5e8}
.half.right{background:#eaf0fb}
.half .lab{font-size:19px;font-weight:700;color:#5a6066;margin-bottom:8px}
.half .num{font-size:46px;font-weight:900}
.half .sub{font-size:17px;color:#8a9096;margin-top:8px}
.bar{display:flex;align-items:center;margin:15px 0;font-size:21px}
.bar .lab{width:210px;font-weight:700;color:#232526;white-space:nowrap}
.bar .track{flex:1;height:32px;background:#e2e5e7;border-radius:8px;position:relative;overflow:hidden}
.bar .fill{height:100%;border-radius:8px}
.bar .val{width:160px;text-align:right;font-weight:800}
.warn{background:#eceeef;border-left:4px solid #3a3d40;padding:16px 20px;border-radius:8px;font-size:20px;color:#3a3d40;margin-top:16px}
.cards3{display:flex;gap:18px}
.c3{flex:1;background:#fff;border:2px solid #d8dbdd;border-radius:16px;padding:24px 18px;text-align:center}
.c3 .v{font-size:32px;font-weight:900;color:#b5790f}
.c3 .l{font-size:17px;color:#5a6066;margin-top:10px;line-height:1.4}
.vscards{display:flex;gap:22px}
.vc{flex:1;background:#fff;border:2px solid #d8dbdd;border-radius:16px;padding:26px 24px}
.vc .name{font-size:21px;font-weight:800;color:#232526;margin-bottom:4px}
.vc .date{font-size:16px;color:#8a9096;margin-bottom:16px}
.vc .num{font-size:32px;font-weight:900;color:#2f5fa8}
.vc .sub{font-size:17px;color:#5a6066;margin-top:10px;line-height:1.4}
.quote{background:#fff;border:2px solid #d8dbdd;border-left:5px solid #b5790f;border-radius:10px;padding:18px 22px;font-size:19px;color:#3a3d40;margin-top:14px;line-height:1.5}
.quote.b{border-left-color:#2f5fa8}
"""

def card(inner):
    return f"<html><head><meta charset='UTF-8'><style>{CSS}</style></head><body><div class='card'>{inner}</div></body></html>"

def bar(label, pct_width, color, val):
    return f"<div class='bar'><div class='lab'>{label}</div><div class='track'><div class='fill' style='width:{pct_width}%;background:{color}'></div></div><div class='val' style='color:{color}'>{val}</div></div>"

pages = {}

# 썸네일: 슬레이트-그레이, 상단 배지 + 중앙 타이틀 + 좌우 대비 스탯(화살표 없이 세로 구분선)
pages["thumbnail"] = """<html><head><meta charset='UTF-8'><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;font-family:'Apple SD Gothic Neo',sans-serif;
background:linear-gradient(135deg,#232526 0%,#3a3d40 100%);color:#fff;
padding:92px 84px;display:flex;flex-direction:column;justify-content:space-between}
.badge{align-self:flex-start;font-size:26px;font-weight:700;padding:11px 26px;
background:rgba(255,255,255,.08);border-radius:10px;color:#d9dcde;border:1px solid rgba(255,255,255,.18)}
.t{font-size:62px;font-weight:800;line-height:1.46;letter-spacing:-1.3px}
.amber{color:#e0ab52}
.blue{color:#7aa6e8}
.statwrap{display:flex;border-top:1px solid rgba(255,255,255,.18);padding-top:40px}
.stat{flex:1;padding:0 20px}
.stat:first-child{border-right:1px solid rgba(255,255,255,.18)}
.stat .v{font-size:88px;font-weight:900;line-height:1;letter-spacing:-2px}
.stat .l{font-size:23px;color:rgba(255,255,255,.6);margin-top:14px;font-weight:600}
</style></head><body>
<div class='badge'>내일도 주린이 · 실적발표</div>
<div class='t'>알파벳 3분기,<br>매출 <span class='amber'>+25%</span> 클라우드 <span class='amber'>+103%</span><br>근데 주가는 <span class='blue'>급락</span></div>
<div class='statwrap'>
<div class='stat'><div class='v amber'>+103%</div><div class='l'>구글 클라우드 성장률</div></div>
<div class='stat'><div class='v blue'>-10%</div><div class='l'>장외 주가 (발표 당일)</div></div>
</div>
</body></html>"""

# body-1: 매출·영업이익은 늘고 순이익·EPS는 꺾인 대비 (알약형 3연속)
pages["body-1"] = card(
    "<div class='ribbon'>실적 vs 성적표</div>"
    "<h3>본업은 좋아졌는데, 순이익만 꺾였어요</h3>"
    "<div class='pillrow'>"
    "<div class='pill'><b>매출</b><span class='amber'>1,275.8억달러</span><i>전년比 +25%</i></div>"
    "<div class='pill'><b>영업이익</b><span class='amber'>405.76억달러</span><i>전년比 +30%, 이익률 31.8%</i></div>"
    "<div class='pill'><b>순이익·EPS</b><span class='blue' style='font-size:25px'>262억달러<br>2.12달러</span><i>컨센서스 3.01~3.02달러 큰 미스</i></div>"
    "</div>"
    "<div class='warn'>순이익 급감 원인은 지분증권 평가손실 약 87억달러 — 일회성·비현금성 요인이 법인세·순이익·EPS를 끌어내림</div>"
    "<div class='src'>합성 그래픽 · 출처: 알파벳 3Q26 실적 발표(10/28)</div>"
)

# body-2: 구글 클라우드 103% 급증 - 부문별 성장률 막대
pages["body-2"] = card(
    "<div class='ribbon'>부문별 성장률</div>"
    "<h3>클라우드가 103%로 압도적으로 뛰었어요</h3>"
    + bar("구글 클라우드", 100, "#b5790f", "+103%")
    + bar("검색 및 기타", 12, "#c98a2e", "+12%")
    + bar("구글 서비스 전체", 11, "#c98a2e", "+11%")
    + "<div class='warn'>클라우드 영업이익은 약 111억달러(이익률 36.2%, 전년比 약 3배) — 성장뿐 아니라 수익성도 같이 좋아진 구간</div>"
    "<div class='src'>막대 길이는 증가율 비례(시각 보정) · 합성 그래픽 · 출처: 알파벳 3Q26 부문별 실적</div>"
)

# body-3: capex 증가 & FCF 적자 전환 (좌우 분할)
pages["body-3"] = card(
    "<div class='ribbon'>AI 투자와 현금흐름</div>"
    "<h3>쓰는 돈이 버는 돈보다 더 빨리 늘었어요</h3>"
    "<div class='split'>"
    "<div class='half left'><div class='lab'>3분기 capex</div><div class='num amber'>~514억달러</div><div class='sub'>2분기 449억달러에서 증가<br>2026 연간 가이던스 1,950억~2,050억달러 유지</div></div>"
    "<div class='half right'><div class='lab'>잉여현금흐름</div><div class='num blue'>-90.7억달러</div><div class='sub'>2개 분기 연속 적자<br>2분기 -59억달러에서 적자 확대</div></div>"
    "</div>"
    "<div class='warn'>영업현금흐름은 전년比 -13%(영업이익은 +30%) — TPU 재고 확충 + 2018 EU 과징금 52억달러 일시 지급 영향</div>"
    "<div class='src'>합성 그래픽 · 출처: 알파벳 3Q26 실적 발표·컨퍼런스콜(CFO 아나트 아슈케나지 발언)</div>"
)

# body-4: Gemini/AI 지표 3종 카드
pages["body-4"] = card(
    "<div class='ribbon'>AI 제품 지표</div>"
    "<h3>Gemini, 숫자로 보면 꽤 빠르게 퍼지고 있어요</h3>"
    "<div class='cards3'>"
    "<div class='c3'><div class='v'>10억 명</div><div class='l'>Gemini 앱 이용자<br>(구글 역사상 최단기 성장)</div></div>"
    "<div class='c3'><div class='v'>15억 건+</div><div class='l'>3분기 AI 광고 소재 생성<br>(전년比 +7배)</div></div>"
    "<div class='c3'><div class='v'>5년 내 최고</div><div class='l'>검색 쿼리<br>성장률</div></div>"
    "</div>"
    "<div class='src'>합성 그래픽 · 출처: 알파벳 3Q26 실적 콜(CEO 순다르 피차이 발언)</div>"
)

# body-5: 장외 vs 정규장 하락률 비교 + bull/bear 두 시각
pages["body-5"] = card(
    "<div class='ribbon'>시장 반응, 엇갈린 해석</div>"
    "<h3>장외 -10.4%, 다음날도 추가 하락</h3>"
    "<div class='vscards'>"
    "<div class='vc'><div class='name'>10/28 장외</div><div class='date'>발표 직후 반응</div>"
    "<div class='num'>-10.4%</div><div class='sub'>매출은 컨센서스 근접, EPS가 크게 미스</div></div>"
    "<div class='vc'><div class='name'>10/29 정규장</div><div class='date'>한 시점 스냅샷</div>"
    "<div class='num'>-12.23%</div><div class='sub'>285.15달러, 거의 4년만의 매출·순이익 동시 미스</div></div>"
    "</div>"
    "<div class='quote'>\"시장이 잘못된 항목을 팔고 있다 — 지분증권 평가손실은 일회성·비현금성, 본업 지표는 견조해 저가 매수 기회\" (시킹알파 칼럼)</div>"
    "<div class='quote b'>\"클라우드 103% 성장이라는 호재가 전체 실적 미스에 가려졌다\" (시킹알파)</div>"
    "<div class='src'>합성 그래픽 · 출처: 각 매체 보도 종합(Investing.com, Yahoo Finance, Seeking Alpha)</div>"
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
