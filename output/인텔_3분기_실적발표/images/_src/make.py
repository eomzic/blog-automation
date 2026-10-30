import os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(BASE)

# 팔레트: 네이비-퍼플 (#1a1a2e -> #16213e, 하락/약세 마감용).
# 직전 글들(10.30국장정리=슬레이트그레이, 구글3Q=슬레이트그레이 계열, 아마존3Q=슬레이트그레이,
# 삼성전자3Q=버건디-마룬)과 겹치지 않도록 선택.
# 레이아웃도 최근 3편(아마존·구글·삼성전자)이 전부 "배지 상단 + 중앙정렬 타이틀/스탯"이었던 것과 달리
# 좌측정렬 타이틀 + 우측 대형 퍼센트 강조 레이아웃으로 변경.
# 액센트: 골드/앰버(실적 호조, 개선 신호) + 파랑(주가 하락, 한국 증시 등락 관례 준수).
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Apple SD Gothic Neo',sans-serif;background:#fff}
.card{width:1000px;padding:48px 54px;background:#f5f5f8;border:3px solid #2a2f5e;border-radius:20px}
.ribbon{display:inline-block;background:#2a2f5e;color:#f5f5f8;font-size:22px;font-weight:700;padding:8px 20px;border-radius:8px;margin-bottom:22px}
h3{font-size:34px;color:#1a1a2e;margin-bottom:28px;font-weight:800}
.src{font-size:19px;color:#8b8fa3;margin-top:24px;line-height:1.6}
.gold{color:#b4853a}
.blue{color:#2f5fa8}
.pointgrid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.point{background:#fff;border:2px solid #dcdee8;border-radius:16px;padding:20px 22px}
.point .k{font-size:18px;color:#8b8fa3;font-weight:700;margin-bottom:8px}
.point .v{font-size:27px;font-weight:900;color:#1a1a2e}
.point .s{font-size:16px;color:#8b8fa3;margin-top:6px}
.flow{display:flex;align-items:center;gap:14px;margin:20px 0;font-size:21px;font-weight:700}
.flow .pt{background:#fff;border:2px solid #dcdee8;border-radius:12px;padding:16px 18px;color:#1a1a2e;flex:1;text-align:center}
.flow .arrow{color:#9a9fb0;font-size:26px}
.warn{background:#eef0fa;border-left:4px solid #2a2f5e;padding:16px 20px;border-radius:8px;font-size:21px;color:#1a1a2e;margin-top:18px}
.vscards{display:flex;gap:22px}
.vc{flex:1;background:#fff;border:2px solid #dcdee8;border-radius:16px;padding:24px 22px}
.vc .name{font-size:21px;font-weight:800;color:#1a1a2e;margin-bottom:4px}
.vc .date{font-size:16px;color:#8b8fa3;margin-bottom:14px}
.vc .num{font-size:30px;font-weight:900;color:#1a1a2e}
.vc .sub{font-size:17px;color:#8b8fa3;margin:8px 0 14px}
.vc .chg{display:inline-block;font-size:24px;font-weight:900;padding:6px 16px;border-radius:8px}
.bigstat{display:flex;align-items:baseline;gap:20px;margin:22px 0}
.bigstat .v{font-size:76px;font-weight:900;line-height:1}
.bigstat .l{font-size:20px;color:#8b8fa3;font-weight:700}
"""

def card(inner):
    return f"<html><head><meta charset='UTF-8'><style>{CSS}</style></head><body><div class='card'>{inner}</div></body></html>"

pages = {}

# 썸네일: 좌측정렬 타이틀 + 우측 대형 퍼센트 강조 레이아웃
# (직전 3편의 '배지 상단 + 중앙정렬' 패턴과 다르게 구성 — 좌/우 분할형)
pages["thumbnail"] = """<html><head><meta charset='UTF-8'><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;font-family:'Apple SD Gothic Neo',sans-serif;
background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);
color:#fff;padding:80px 76px;display:flex;flex-direction:column;justify-content:space-between;position:relative;overflow:hidden}
.glow1{position:absolute;top:-120px;right:-120px;width:420px;height:420px;border-radius:50%;
background:radial-gradient(circle, rgba(111,147,214,.22), transparent 70%)}
.glow2{position:absolute;bottom:-100px;left:-80px;width:360px;height:360px;border-radius:50%;
background:radial-gradient(circle, rgba(180,133,58,.14), transparent 70%)}
.badge{align-self:flex-start;font-size:25px;font-weight:700;padding:11px 26px;background:rgba(255,255,255,.1);
border-radius:30px;color:#d4d7e6;letter-spacing:.5px;position:relative;z-index:1}
.rowwrap{flex:1;display:flex;align-items:center;position:relative;z-index:1}
.row{display:flex;align-items:center;gap:36px;width:100%}
.left{flex:1}
.t{font-size:54px;font-weight:800;line-height:1.35;letter-spacing:-1.2px}
.blue{color:#7fa8e8}
.right{text-align:right}
.big{font-size:148px;font-weight:900;line-height:1;letter-spacing:-4px;color:#7fa8e8}
.biglab{font-size:24px;color:rgba(255,255,255,.6);font-weight:600;margin-top:12px}
.foot{display:flex;flex-direction:column;gap:24px;position:relative;z-index:1}
.sub{font-size:25px;color:rgba(255,255,255,.65);font-weight:600}
.rule{width:100%;height:1px;background:rgba(255,255,255,.16)}
.datewrap{display:flex;justify-content:space-between;align-items:center}
.date{font-size:20px;color:rgba(255,255,255,.4);font-weight:600;letter-spacing:1px}
.rec{font-size:18px;color:#d9b876;font-weight:700;background:rgba(180,133,58,.18);padding:6px 16px;border-radius:20px}
</style></head><body>
<div class='glow1'></div><div class='glow2'></div>
<div class='badge'>내일도 주린이 · 실적발표</div>
<div class='rowwrap'>
<div class='row'>
<div class='left'>
<div class='t'>인텔 3분기 실적은<br>기대 이상이었는데<br>주가는 <span class='blue'>역사적 폭락</span></div>
</div>
<div class='right'>
<div class='big'>-27%</div>
<div class='biglab'>10/30 하루 낙폭</div>
</div>
</div>
</div>
<div class='foot'>
<div class='sub'>매출 +21% 비트 · 4분기 가이던스 쇼크</div>
<div class='rule'></div>
<div class='datewrap'>
<div class='date'>2026 Q3 EARNINGS · 10.31</div>
<div class='rec'>1974년 이후 최악</div>
</div>
</div>
</body></html>"""

# body-1: 주가 폭락 그 자체 (핵심 포인트 카드 템플릿)
pages["body-1"] = card(
    "<div class='ribbon'>역대급 폭락</div>"
    "<h3>1974년 이후 최악의 하루</h3>"
    "<div class='bigstat'><div class='v blue'>-27%</div><div class='l'>10/30 정규장 종가 기준<br>(장중 한때 -30%)</div></div>"
    "<div class='pointgrid'>"
    "<div class='point'><div class='k'>발표 당일 애프터마켓</div><div class='v blue'>-20%대</div><div class='s'>10/29 장 마감 후</div></div>"
    "<div class='point'><div class='k'>1974년 7월 기록</div><div class='v'>-29.9%</div><div class='s'>그동안의 역대 최악 하루</div></div>"
    "</div>"
    "<div class='warn'>실적 자체는 가이던스를 넘겼는데도 주가가 무너진 건, 다음 분기 가이던스가 시장 예상을 크게 밑돌았기 때문.</div>"
    "<div class='src'>합성 그래픽 · 출처: Benzinga·Yahoo Finance·KuCoin 등 10/30 보도 종합(매체별 27~30%로 소폭 차이)</div>"
)

# body-2: 3분기 매출·순이익·EPS 비교 (포인트 카드 템플릿)
pages["body-2"] = card(
    "<div class='ribbon'>3분기 핵심 수치</div>"
    "<h3>매출·EPS는 비트, 순이익은 감소</h3>"
    "<div class='pointgrid'>"
    "<div class='point'><div class='k'>매출</div><div class='v gold'>165억 달러</div><div class='s'>전년比 +21%, 컨센서스(약 164.4억) 상회</div></div>"
    "<div class='point'><div class='k'>순이익</div><div class='v blue'>33.2억 달러</div><div class='s'>전년 41억 달러 대비 -18%</div></div>"
    "<div class='point'><div class='k'>Non-GAAP EPS</div><div class='v gold'>0.52달러</div><div class='s'>예상(0.39~0.41달러) 크게 상회</div></div>"
    "<div class='point'><div class='k'>GAAP 매출총이익률</div><div class='v gold'>43.0%</div><div class='s'>전년比 +4.8%p</div></div>"
    "</div>"
    "<div class='src'>합성 그래픽 · 출처: 인텔 3Q26 실적 공시(10/29)</div>"
)

# body-3: 파운드리 매출 성장과 영업손실 개선 추이 (단계별 플로우 템플릿)
pages["body-3"] = card(
    "<div class='ribbon'>Intel Foundry · 18A</div>"
    "<h3>매출은 늘고, 적자는 줄고</h3>"
    "<div class='flow'>"
    "<div class='pt'>파운드리 매출<br><b style='font-size:26px;color:#1a1a2e'>67억 달러</b><br><span style='font-size:15px;color:#8b8fa3'>전년比 +58%</span></div>"
    "<div class='arrow'>&rarr;</div>"
    "<div class='pt'>영업손실<br><b style='font-size:26px;color:#2f5fa8'>19억 달러</b><br><span style='font-size:15px;color:#8b8fa3'>전분기比 2.36억 개선</span></div>"
    "<div class='arrow'>&rarr;</div>"
    "<div class='pt'>18A 공정 원가<br><b style='font-size:26px;color:#b4853a'>-40%</b><br><span style='font-size:15px;color:#8b8fa3'>1분기 이후 절감</span></div>"
    "</div>"
    "<div class='warn'>18A 기반 클라이언트 CPU 매출 비중: 1분기 5% 미만 → 이번 분기 약 1/3 수준까지 상승.</div>"
    "<div class='src'>합성 그래픽 · 출처: 인텔 3Q26 실적 공시·어닝콜 트랜스크립트</div>"
)

# body-4: 4분기 가이던스 vs 컨센서스 (비교 표 템플릿)
pages["body-4"] = card(
    "<div class='ribbon'>4분기 가이던스 쇼크</div>"
    "<h3>가이던스가 컨센서스를 크게 밑돌았다</h3>"
    "<div class='vscards'>"
    "<div class='vc'><div class='name'>인텔 가이던스</div><div class='date'>4분기 매출</div>"
    "<div class='num blue'>150억~160억 달러</div><div class='sub'>Non-GAAP EPS 0.25달러</div>"
    "<div class='chg' style='background:#eaf0fb;color:#2f5fa8'>하단 제시</div></div>"
    "<div class='vc'><div class='name'>시장 컨센서스</div><div class='date'>4분기 매출 예상</div>"
    "<div class='num'>약 170.5억 달러</div><div class='sub'>EPS 예상 약 0.43달러</div>"
    "<div class='chg' style='background:#f3ecdf;color:#b4853a'>기대치</div></div>"
    "</div>"
    "<div class='warn'>BofA(145→100달러)·로스캐피탈(120→70달러) 등 다수 투자은행이 목표가를 하향. 공통 이유: PC 수요 둔화, 파운드리 생산 제약, 공급 개선 지연.</div>"
    "<div class='src'>합성 그래픽 · 출처: 인텔 IR 가이던스, Benzinga·CNBC·gurufocus 애널리스트 리포트 종합(10/30)</div>"
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
