import os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(BASE)

JOBS = [
    ("thumbnail.html", "thumbnail.png", 1080, 1080, True),
    ("body-1.html", "body-1.png", 1000, 1200, False),
    ("body-2.html", "body-2.png", 1000, 1300, False),
    ("body-3.html", "body-3.png", 1000, 1300, False),
    ("body-4.html", "body-4.png", 1000, 1000, False),
    ("body-5.html", "body-5.png", 1000, 1300, False),
    ("body-6.html", "body-6.png", 1000, 1100, False),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(device_scale_factor=2)
    for html_name, png_name, w, h, full_square in JOBS:
        page.set_viewport_size({"width": w, "height": h})
        page.goto(f"file://{os.path.join(BASE, html_name)}")
        page.wait_for_timeout(150)
        out_path = os.path.join(OUT, png_name)
        if full_square:
            page.screenshot(path=out_path, clip={"x": 0, "y": 0, "width": w, "height": h})
        else:
            el = page.query_selector(".card")
            el.screenshot(path=out_path)
        print("saved", out_path)
    browser.close()
