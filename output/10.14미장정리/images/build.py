import asyncio, os
from playwright.async_api import async_playwright
OUT=os.path.dirname(os.path.abspath(__file__))
RED="#ff5a5f"; BLUE="#5aa2ff"
def col(v): return RED if v>0 else BLUE
FONT="font-family:'Apple SD Gothic Neo',sans-serif"
def bars(rows,title,sub,accent,bg="#201414"):
    mx=max(abs(v) for _,v in rows); h=""
    for n,v in rows:
        h+=f'<div class="r"><div class="n">{n}</div><div class="bw"><div class="b" style="width:{abs(v)/mx*80:.0f}%;background:{col(v)}"></div></div><div class="v" style="color:{col(v)}">{v:+.2f}%</div></div>'
    return f'''<html><head><meta charset="UTF-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:900px;{FONT};background:{bg};color:#fff;padding:44px 48px}}
h1{{font-size:34px;font-weight:800;border-left:6px solid {accent};padding-left:14px}}p{{font-size:20px;color:rgba(255,255,255,.55);margin:8px 0 28px}}
.r{{display:flex;align-items:center;margin:14px 0}}.n{{width:250px;font-size:24px;font-weight:600}}.bw{{flex:1;height:30px;background:rgba(255,255,255,.06);border-radius:6px}}
.b{{height:30px;border-radius:6px}}.v{{width:130px;text-align:right;font-size:26px;font-weight:800}}.f{{margin-top:22px;font-size:16px;color:rgba(255,255,255,.4)}}</style></head><body><h1>{title}</h1><p>{sub}</p>{h}<div class="f">내일도 주린이 · 합성 데이터 그래픽</div></body></html>'''
def table(title,head,rows,hbg):
    t="".join("<tr>"+"".join(f'<td class="{"a" if i==0 else ""}" style="{s if i>0 else ""}">{c}</td>' for i,(c,s) in enumerate(r))+"</tr>" for r in rows)
    th="".join(f"<th>{c}</th>" for c in head)
    return f'''<html><head><meta charset="UTF-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:900px;{FONT};background:#fff;color:#222;padding:40px 44px}}h1{{font-size:32px;font-weight:800;margin-bottom:22px}}
table{{width:100%;border-collapse:collapse}}th{{background:{hbg};color:#fff;font-size:20px;padding:16px;text-align:right}}th:first-child{{text-align:left}}
td{{font-size:25px;padding:22px 16px;text-align:right;border-bottom:1px solid #e5e5e5}}td.a{{text-align:left;font-weight:700}}.f{{margin-top:18px;font-size:15px;color:#999}}</style></head><body><h1>{title}</h1><table><tr>{th}</tr>{t}</table><div class="f">내일도 주린이 · 합성 데이터 그래픽</div></body></html>'''
pages={}
pages['body-1']=table("9월 CPI: 발표치 vs 시장 예상",["항목","발표","예상"],[
 [("전체 CPI 전월比",""),("+0.6%","font-weight:800"),("+0.6%","")],
 [("전체 CPI 전년比",""),("+3.7%",f"font-weight:800;color:{RED}"),("+3.6%","")],
 [("근원 CPI 전월比",""),("+0.3%",f"font-weight:800;color:{RED}"),("+0.2%","")],
 [("근원 CPI 전년比",""),("+2.6%",f"font-weight:800;color:{RED}"),("+2.5%","")]],"#4a1414")
pages['body-2']=table("10/14 미국 3대 지수 마감",["지수","종가","등락률"],[
 [("다우존스",""),("51,621.48",""),("-0.09%",f"color:{BLUE};font-weight:800")],
 [("S&P500",""),("7,718.94",""),("-1.11%",f"color:{BLUE};font-weight:800")],
 [("나스닥 종합",""),("26,692.87",""),("-1.88%",f"color:{BLUE};font-weight:800")]],"#3a3d40")
pages['body-3']=bars([("코어위브",-15.46),("델",-11.36),("오라클",-8.83),("SK하이닉스",-6.06),("마이크론",-4.08),("TSMC",-3.40),("엔비디아",-3.16),("브로드컴",-3.10)],"반도체·AI 인프라 줄하락","SOX -4.30% · 6거래일 연속 하락","#e8a33d")
pages['body-4']=bars([("벤딩스푼즈",41.20),("블랙록",0.73),("모건스탠리",-2.70),("뱅크오브아메리카",-4.76)],"은행·금융 이슈 종목","BofA는 제재 영향, 모건스탠리는 이익 내고도 하락","#c9a26b",bg="#232526")
pages['thumbnail']='''<html><head><meta charset="UTF-8"><style>*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;font-family:'Apple SD Gothic Neo',sans-serif;background:linear-gradient(160deg,#2d0a0a 0%,#4a1414 100%);color:#fff;padding:90px 80px;display:flex;flex-direction:column;justify-content:space-between}
.badge{align-self:flex-start;font-size:28px;font-weight:700;padding:12px 30px;border:2px solid #e8a33d;border-radius:40px;color:#f5cf8a}
.t{font-size:84px;font-weight:800;line-height:1.3;letter-spacing:-2px}
.row{display:flex;align-items:flex-end;justify-content:space-between}.s{font-size:34px;color:rgba(255,255,255,.65);line-height:1.5}
.n{font-size:190px;font-weight:800;color:#5aa2ff;letter-spacing:-6px;line-height:1}</style></head><body>
<div class="badge">내일도 주린이 · 미장 정리</div><div class="t">CPI 쇼크에<br>반도체 6일 연속 하락</div>
<div class="row"><div class="s">나스닥 종합<br>10/14 마감</div><div class="n">-1.88%</div></div></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for k,h in pages.items():
            pg=await b.new_page(viewport={'width':1080 if k=='thumbnail' else 900,'height':1080 if k=='thumbnail' else 400})
            await pg.set_content(h); await pg.wait_for_timeout(300)
            open(f"{OUT}/_src/{k}.html","w").write(h) if os.path.isdir(OUT+"/_src") else None
            await pg.screenshot(path=f"{OUT}/{k}.png",full_page=True)
        await b.close()
asyncio.run(main())
