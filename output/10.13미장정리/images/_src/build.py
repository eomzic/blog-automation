import asyncio, os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(HERE)
RED="#ff5a5f"; BLUE="#5aa2ff"
def col(v): return RED if v>0 else BLUE
def bars(rows, title, sub, w=900, accent="#8b7cf6"):
    mx=max(abs(v) for _,v in rows)
    h=""
    for n,v in rows:
        pct=abs(v)/mx*100
        h+=f'<div class="r"><div class="n">{n}</div><div class="bw"><div class="b" style="width:{pct*0.8:.0f}%;background:{col(v)}"></div></div><div class="v" style="color:{col(v)}">{v:+.2f}%</div></div>'
    return f'''<html><head><meta charset="UTF-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;font-family:'Apple SD Gothic Neo',sans-serif;background:#14152b;color:#fff;padding:44px 48px}}
h1{{font-size:34px;font-weight:800;letter-spacing:-1px}}p{{font-size:20px;color:rgba(255,255,255,.55);margin:8px 0 28px}}
.r{{display:flex;align-items:center;margin:14px 0}}.n{{width:260px;font-size:24px;font-weight:600}}.bw{{flex:1;height:30px;background:rgba(255,255,255,.06);border-radius:6px}}
.b{{height:30px;border-radius:6px}}.v{{width:130px;text-align:right;font-size:26px;font-weight:800}}
.f{{margin-top:22px;font-size:16px;color:rgba(255,255,255,.4)}}</style></head><body><h1 style="border-left:6px solid {accent};padding-left:14px">{title}</h1><p>{sub}</p>{h}<div class="f">내일도 주린이 · 합성 데이터 그래픽</div></body></html>'''
pages={}
pages['body-1']=bars([("씨티그룹",-5.60),("웰스파고",-3.10),("JP모간",-0.82),("골드만삭스",-0.23)],"은행 실적 발표 후 주가","10/13 마감 · 씨티·골드만은 이익 예상 상회에도 하락")
pages['body-3']=bars([("어플라이드 머티어리얼즈",-6.69),("마이크론",-3.62),("엔비디아",0.97),("브로드컴",0.73),("AMD",1.90),("인텔",1.44)],"반도체: 메모리·장비 약세, 칩 설계는 반등","SOX 5거래일 연속 하락 · 5일간 8% 넘게 하락",accent="#4cc9b0")
pages['body-4']=bars([("범블",56.58),("메타",2.63),("퀄컴",1.39),("애플",0.09),("도미노피자",-4.76),("존슨앤드존슨",-5.73)],"오늘의 개별 종목","이슈 종목 등락률 · 범블은 비공개 전환 합의",accent="#f0b429")
rows=[("다우존스","51,670.10","-180.45p",-0.35),("S&P500","7,805.45","-1.79p",-0.02),("나스닥 종합","27,204.38","-41.52p",-0.15)]
t="".join(f'<tr><td class="a">{n}</td><td>{c}</td><td style="color:{BLUE}">{d}</td><td style="color:{BLUE};font-weight:800">{p:+.2f}%</td></tr>' for n,c,d,p in rows)
pages['body-2']=f'''<html><head><meta charset="UTF-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:900px;font-family:'Apple SD Gothic Neo',sans-serif;background:#fff;color:#222;padding:40px 44px}}
h1{{font-size:32px;font-weight:800;margin-bottom:22px}}table{{width:100%;border-collapse:collapse}}
th{{background:#1e1f3b;color:#fff;font-size:20px;padding:16px;text-align:right}}th:first-child{{text-align:left}}
td{{font-size:26px;padding:22px 16px;text-align:right;border-bottom:1px solid #e5e5e5}}td.a{{text-align:left;font-weight:700}}
.f{{margin-top:18px;font-size:15px;color:#999}}</style></head><body><h1>10/13 미국 3대 지수 마감</h1><table><tr><th>지수</th><th>종가</th><th>등락 포인트</th><th>등락률</th></tr>{t}</table><div class="f">내일도 주린이 · 합성 데이터 그래픽</div></body></html>'''
pages['thumbnail']='''<html><head><meta charset="UTF-8"><style>*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;font-family:'Apple SD Gothic Neo',sans-serif;background:linear-gradient(160deg,#1a1a2e 0%,#16213e 100%);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.badge{font-size:28px;font-weight:700;padding:12px 30px;border:2px solid #8b7cf6;border-radius:40px;color:#c4bcff}
.t{margin-top:56px;font-size:82px;font-weight:800;line-height:1.3;letter-spacing:-2px}
.s{margin-top:44px;font-size:34px;color:rgba(255,255,255,.65)}
.n{margin-top:50px;font-size:120px;font-weight:800;color:#5aa2ff;letter-spacing:-4px}</style></head><body>
<div class="badge">내일도 주린이 · 미장 정리</div><div class="t">반도체 5일 연속 하락<br>은행은 이익 내고도 하락</div>
<div class="n">-5.60%</div><div class="s">씨티그룹 · 10/13 마감</div></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for k,h in pages.items():
            f=os.path.join(HERE,k+'.html'); open(f,'w').write(h)
            pg=await b.new_page(viewport={'width':1080 if k=='thumbnail' else 900,'height':1080 if k=='thumbnail' else 400})
            await pg.goto('file://'+f)
            await pg.screenshot(path=os.path.join(OUT,k+'.png'),full_page=(k!='thumbnail'))
        await b.close()
asyncio.run(main())
