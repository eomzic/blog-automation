import asyncio, os
from playwright.async_api import async_playwright

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(D)
F = "font-family:'Apple SD Gothic Neo','Malgun Gothic',sans-serif;"
BL = "#2b6cff"   # 하락(파랑) - 관례색, 절대 변경 금지
RD = "#e0393e"   # 상승(빨강) - 관례색, 절대 변경 금지
ACCENT = "#ff6b6b"   # 버건디-마룬 팔레트의 보조 포인트 컬러 (오늘은 급락/쇼크성 뉴스라 버건디-마룬 선택, 직전 두 편이 네이비-퍼플이라 로테이션)

def page(w, body, bg="#ffffff"):
    return f"<html><head><meta charset='utf-8'></head><body style=\"margin:0;{F}background:{bg};width:{w}px\">{body}</body></html>"

def table(head, rows, aligns=None):
    n = len(head)
    aligns = aligns or (["left"] + ["right"] * (n - 1))
    th = "".join(
        f"<th style='padding:14px 18px;text-align:{aligns[i]};background:#3a1010;color:#fff;font-size:22px'>{h}</th>"
        for i, h in enumerate(head)
    )
    tr = ""
    for r in rows:
        tds = ""
        for i, c in enumerate(r):
            col = "#222"
            if c.startswith("-"):
                col = BL
            elif c.startswith("+"):
                col = RD
            tds += f"<td style='padding:14px 18px;text-align:{aligns[i]};border-bottom:1px solid #e5e5e5;font-size:22px;color:{col};font-weight:{700 if i == 0 else 600}'>{c}</td>"
        tr += f"<tr>{tds}</tr>"
    return f"<table style='width:100%;border-collapse:collapse'><tr>{th}</tr>{tr}</table>"

imgs = {}

# 대표 이미지 (버건디-마룬, 좌측정렬 + 우하단 큰 숫자 강조 — 직전 2편 연속 네이비-퍼플/중앙정렬이라 로테이션)
imgs['thumbnail'] = (1080, 1080, f"""
<div style="width:1080px;height:1080px;background:linear-gradient(135deg,#2d0a0a,#4a1414);color:#fff;position:relative;overflow:hidden">
  <div style="position:absolute;top:80px;left:80px;background:{ACCENT};padding:12px 28px;border-radius:30px;font-size:30px;font-weight:700;color:#2d0a0a">내일도 주린이 · 시황</div>
  <div style="position:absolute;top:240px;left:80px;right:80px">
    <div style="font-size:48px;color:#ffb3b3;font-weight:700;line-height:1.5">美 중간선거 '블루 스윕' 확정</div>
    <div style="font-size:80px;font-weight:800;color:#fff;line-height:1.3;margin-top:20px">코스피 급등하다<br>급락 반전</div>
  </div>
  <div style="position:absolute;bottom:90px;left:80px;right:80px;text-align:right">
    <div style="font-size:30px;color:#ffd6d6">장중 +2.43% → 마감권 </div>
    <div style="font-size:150px;font-weight:800;color:{BL};line-height:1">-3.83%</div>
  </div>
</div>
""")

# body-1: 하원·상원 구도 변화 비교
imgs['body-1'] = (900, 400, f"""
<div style='padding:30px'>
  <div style='font-size:28px;font-weight:800;margin-bottom:16px'>2026 美 중간선거 결과 - 상·하원 구도</div>
  {table(["구분", "민주당", "공화당"], [["상원", "51석", "39석"], ["하원(전망)", "약 235석", "약 160석"]])}
  <div style='font-size:18px;color:#777;margin-top:12px'>합성 데이터 그래픽 · 하원은 개표 집계 기준 전망치</div>
</div>
""")

# body-2: 반도체 대형주 등락률 카드
imgs['body-2'] = (900, 420, f"""
<div style="padding:30px;background:#3a1010">
  <div style="border-left:8px solid {ACCENT};background:#4a1414;padding:34px 36px">
    <div style="font-size:30px;color:#ffb3b3;font-weight:700">선거 개표일 반도체 대형주</div>
    <div style="display:flex;gap:40px;margin-top:16px">
      <div>
        <div style="font-size:26px;color:#ffd6d6">삼성전자</div>
        <div style="font-size:70px;font-weight:800;color:{BL}">-4.78%</div>
      </div>
      <div>
        <div style="font-size:26px;color:#ffd6d6">SK하이닉스</div>
        <div style="font-size:70px;font-weight:800;color:{BL}">-6.51%</div>
      </div>
    </div>
    <div style="font-size:26px;color:#fff;margin-top:20px;line-height:1.6">AI 데이터센터 규제 강화 우려가 선반영</div>
  </div>
</div>
""")

# body-3: 시나리오별 코스피 4분기 목표지수 비교
imgs['body-3'] = (900, 460, f"""
<div style='padding:30px'>
  <div style='font-size:28px;font-weight:800;margin-bottom:16px'>선거 전 증권가 시나리오별 코스피 4분기 목표</div>
  {table(["시나리오", "확률(추정)", "4분기 목표"], [["민주 블루스윕", "63%", "5,200~6,700"], ["의회 분점", "28%", "5,200~6,700"], ["공화 레드스윕", "8%", "4,950 하향"]])}
  <div style='font-size:18px;color:#777;margin-top:12px'>합성 데이터 그래픽 · 선거 전 증권가 전망 기준</div>
</div>
""")

# body-4: 중간선거 이후 코스피·S&P500 수익률 비교
imgs['body-4'] = (900, 260, f"""
<div style="padding:30px;background:#f5f7fb">
  <div style="font-size:28px;font-weight:800;margin-bottom:18px">중간선거 1년 뒤 수익률 비교</div>
  <div style="display:flex;gap:20px">
    <div style="flex:1;background:#fff;border-top:6px solid {ACCENT};padding:24px">
      <div style="font-size:24px;color:#555">2018년 중간선거</div>
      <div style="font-size:22px;color:#777;margin-top:10px">S&amp;P500 <span style="color:{RD};font-weight:700">+11.66%</span></div>
      <div style="font-size:22px;color:#777">코스피 <span style="color:{RD};font-weight:700">+2.61%</span></div>
    </div>
    <div style="flex:1;background:#fff;border-top:6px solid {ACCENT};padding:24px">
      <div style="font-size:24px;color:#555">2022년 중간선거</div>
      <div style="font-size:22px;color:#777;margin-top:10px">S&amp;P500 <span style="color:{RD};font-weight:700">+14.49%</span></div>
      <div style="font-size:22px;color:#777">코스피 <span style="color:{RD};font-weight:700">+0.94%</span></div>
    </div>
  </div>
  <div style='font-size:18px;color:#999;margin-top:14px'>합성 데이터 그래픽 · 두 시기 모두 美 기준금리 인상기</div>
</div>
""")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, (w, vh, body) in imgs.items():
            html = page(w, body)
            open(f"{D}/{name}.html", "w").write(html)
            pg = await b.new_page(viewport={'width': w, 'height': vh})
            await pg.set_content(html)
            await pg.screenshot(path=f"{OUT}/{name}.png", full_page=True)
        await b.close()

asyncio.run(main())
