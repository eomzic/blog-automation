import re, html, pathlib
d = pathlib.Path(__file__).parent.parent.parent
txt = (d/"draft.md").read_text()
alts = re.findall(r"\[image: (.+?)\]", txt)
for i,a in enumerate(alts,1):
    txt = txt.replace(f"[image: {a}]", f"![{a}](./images/body-{i}.png)")
(d/"draft.md").write_text(txt); (d/"final.md").write_text(txt)
P='<p style="font-size:15px; line-height:1.8; color:#333333; margin:0 0 18px 0;">%s</p>'
out=[]; title=""
def inline(s): return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(s, quote=False))
for line in txt.split("\n"):
    l=line.strip()
    if not l: continue
    if l.startswith("# "): title=l[2:]; continue
    if l=="---": out.append('<hr style="border:none; border-top:1px solid #e5e5e5; margin:36px 0;">'); continue
    if l.startswith("## "): out.append(f'<p style="margin:40px 0 16px 0; line-height:1.4;"><b style="font-size:24px; color:#222222;">{html.escape(l[3:],quote=False)}</b></p>'); continue
    if l.startswith("> "):
        t=html.escape(l[2:].strip("*"),quote=False)
        out.append(f'<table style="width:100%; border-collapse:collapse; margin:20px 0;"><tr><td style="border-left:4px solid #03a54a; background-color:#f0faf3; padding:12px 16px;"><p style="margin:0; font-size:16px; font-weight:700; line-height:1.6; color:#03a54a;">{t}</p></td></tr></table>'); continue
    m=re.match(r"!\[(.+?)\]\((.+?)\)",l)
    if m: out.append(f'<img src="{m[2]}" alt="{html.escape(m[1])}" style="max-width:100%; height:auto; display:block; margin:20px auto;">'); continue
    out.append(P%inline(l))
t=html.escape(title,quote=False)
(d/"final.html").write_text(f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><title>{t}</title></head>
<body><div style="width:700px; margin:0 auto; font-family:'Apple SD Gothic Neo','Malgun Gothic','Nanum Gothic',sans-serif;">
<div id="post-title" style="font-size:24px; font-weight:700;">{t}</div>
<div id="post-body">
'''+"\n".join(out)+"\n</div></div></body></html>\n")
