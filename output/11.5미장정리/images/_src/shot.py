import sys
from playwright.sync_api import sync_playwright
src=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch()
    for n in ['thumbnail','body-1','body-2','body-3']:
        w=1080 if n=='thumbnail' else 900
        pg=b.new_page(viewport={'width':w,'height':1080 if n=='thumbnail' else 400})
        pg.goto('file://'+src+'/'+n+'.html')
        if n=='thumbnail': pg.screenshot(path=src+'/../'+n+'.png')
        else: pg.locator('body').screenshot(path=src+'/../'+n+'.png')
    b.close()
