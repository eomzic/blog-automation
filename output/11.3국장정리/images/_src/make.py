import asyncio, os
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(D)
F="font-family:'Apple SD Gothic Neo','Malgun Gothic',sans-serif;"
BL="#2b6cff"; RD="#e0393e"
def page(w,body,bg="#ffffff"):
    return f"<html><head><meta charset='utf-8'></head><body style=\"margin:0;{F}background:{bg};width:{w}px\">{body}</body></html>"
def table(head,rows,cols):
    th="".join(f"<th style='padding:14px 18px;text-align:{'left' if i==0 else 'right'};background:#1e2a4a;color:#fff;font-size:22px'>{h}</th>" for i,h in enumerate(head))
    tr=""
    for r in rows:
        tds=""
        for i,c in enumerate(r):
            col="#222"
            if i>0 and c.startswith("-") and len(c)>1: col=BL
            if i>0 and c.startswith("+"): col=RD
            tds+=f"<td style='padding:14px 18px;text-align:{'left' if i==0 else 'right'};border-bottom:1px solid #e5e5e5;font-size:22px;color:{col};font-weight:{700 if i==0 else 600}'>{c}</td>"
        tr+=f"<tr>{tds}</tr>"
    return f"<table style='width:100%;border-collapse:collapse'><tr>{th}</tr>{tr}</table>"
imgs={}
imgs['thumbnail']=(1080,f"""<div style="width:1080px;height:1080px;background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;position:relative">
<div style="position:absolute;top:90px;left:90px;background:#2b6cff;padding:12px 28px;border-radius:30px;font-size:32px;font-weight:700">내일도 주린이 · 국장 정리</div>
<div style="position:absolute;top:300px;left:90px;right:90px;text-align:center"><div style="font-size:70px;color:#9db7ff;font-weight:700">11/3 코스피</div>
<div style="font-size:190px;font-weight:800;color:#6f9bff;line-height:1.1">-3.59%</div>
<div style="font-size:60px;font-weight:700;margin-top:20px">5,648.79</div>
<div style="font-size:42px;color:#c9d2ea;margin-top:50px;line-height:1.5">반등 하루 만에 반납<br>코스닥은 700선 턱밑</div></div></div>""")
imgs['body-1']=(900,"<div style='padding:30px'><div style='font-size:28px;font-weight:800;margin-bottom:16px'>투자자별 순매수 (11/3)</div>"+table(["시장","외국인","기관","개인"],[["코스피","-1조 5,154억","-5,147억","+1조 6,644억"],["코스닥","-749억","-2,346억","+3,199억"]],4)+"<div style='font-size:18px;color:#777;margin-top:12px'>합성 데이터 그래픽 · 단위 원 · 매수 +, 매도 -</div></div>")
imgs['body-2']=(900,f"""<div style="padding:30px;background:#16213e"><div style="border-left:8px solid {BL};background:#1e2a4a;padding:34px 36px">
<div style="font-size:30px;color:#9db7ff;font-weight:700">간밤 미국 AI 관련주</div>
<div style="font-size:84px;font-weight:800;color:#6f9bff;margin:10px 0">오라클 -8.8%</div>
<div style="font-size:34px;color:#fff;line-height:1.6">마이크론 -5.8% · 엔비디아 -1.3%<br><span style="color:#c9d2ea;font-size:28px">200억달러 조달 계획과 AI 투자 수익성 우려</span></div></div></div>""")
imgs['body-3']=(900,"<div style='padding:30px'><div style='font-size:28px;font-weight:800;margin-bottom:16px'>반도체·부품 종가와 등락률</div>"+table(["종목","종가","등락률"],[["SK하이닉스","1,398,000원","-5.03%"],["삼성전자","219,500원","-4.15%"],["SK스퀘어","899,000원","-5.37%"],["삼성전기","1,105,000원","-7.38%"],["이오테크닉스","-","-8.56%"],["원익IPS","-","-7.14%"]],3)+"<div style='font-size:18px;color:#777;margin-top:12px'>합성 데이터 그래픽</div></div>")
imgs['body-4']=(900,f"""<div style="padding:30px;background:#f5f7fb"><div style="font-size:28px;font-weight:800;margin-bottom:18px">마감 지수</div>
<div style="display:flex;gap:20px">
<div style="flex:1;background:#fff;border-top:6px solid {BL};padding:24px"><div style="font-size:24px;color:#555">코스피</div><div style="font-size:52px;font-weight:800">5,648.79</div><div style="font-size:30px;color:{BL};font-weight:700">-3.59%</div><div style="font-size:20px;color:#666;margin-top:10px;line-height:1.6">시가 5,715.19<br>장중 저점 5,615.80<br>상승 221 · 하락 658</div></div>
<div style="flex:1;background:#fff;border-top:6px solid {BL};padding:24px"><div style="font-size:24px;color:#555">코스닥</div><div style="font-size:52px;font-weight:800">704.39</div><div style="font-size:30px;color:{BL};font-weight:700">-4.08%</div><div style="font-size:20px;color:#666;margin-top:10px;line-height:1.6">장중 저점 702.34<br>상승 322 · 하락 1,350<br>거래대금 5조 3,307억</div></div></div></div>""")
imgs['body-5']=(900,"<div style='padding:30px'><div style='font-size:28px;font-weight:800;margin-bottom:16px'>시총 상위주 등락률</div>"+table(["종목","등락률"],[["삼성바이오로직스","+2.11%"],["KB금융","-1.30%"],["현대차","-3.31%"],["삼성생명","-3.86%"],["LG에너지솔루션","-5.06%"]],2)+"<div style='font-size:18px;color:#777;margin-top:12px'>합성 데이터 그래픽</div></div>")
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for n,(w,h) in imgs.items():
            html=page(w,h); open(f"{D}/{n}.html","w").write(html)
            pg=await b.new_page(viewport={'width':w,'height':1080 if n=='thumbnail' else 400})
            await pg.set_content(html)
            await pg.screenshot(path=f"{OUT}/{n}.png",full_page=True)
        await b.close()
asyncio.run(main())
