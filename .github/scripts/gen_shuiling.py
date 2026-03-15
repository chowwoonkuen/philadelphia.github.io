#!/usr/bin/env python3
import os, sys

lang  = sys.argv[1]
repo  = sys.argv[2]
title = sys.argv[3]
back  = sys.argv[4]

src_dir   = f"{lang}/shuiling"
thumb_dir = f"/{repo}/assets/thumbs/{lang}/shuiling"
base      = f"/{repo}/{lang}/shuiling"
back_url  = f"/{repo}/{lang}/index.html"

files = sorted([f for f in os.listdir(src_dir) if f.endswith('.pdf')]) if os.path.isdir(src_dir) else []

html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title}</title>
  <link rel="stylesheet" href="/{repo}/assets/css/style.css"/>
  <style>
    .lib-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
      gap: 1.5rem;
    }}
    .book-card {{
      background: var(--surf);
      border: 1px solid var(--border);
      border-radius: var(--r-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow);
      transition: all .22s;
    }}
    .book-card:hover {{
      border-color: var(--gold-lt);
      transform: translateY(-3px);
      box-shadow: var(--shadow-lg);
    }}
    /* Skeleton placeholder — shown until image loads */
    .thumb-wrap {{
      width: 100%;
      aspect-ratio: 1 / 1.414;
      position: relative;
      overflow: hidden;
      background: var(--surf2);
    }}
    .thumb-wrap .skeleton {{
      position: absolute;
      inset: 0;
      border-radius: 0;
    }}
    .book-thumb {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: contain;
      background: var(--surf2);
      opacity: 0;
      transition: opacity .3s;
    }}
    .book-thumb.loaded {{ opacity: 1; }}
    .book-info {{
      padding: .85rem;
      display: flex;
      flex-direction: column;
      gap: .65rem;
      flex: 1;
    }}
    .book-name {{
      font-family: var(--font-s);
      font-size: .8rem;
      color: var(--text);
      line-height: 1.5;
      word-break: break-word;
    }}
    .book-actions {{
      display: flex;
      gap: .5rem;
      margin-top: auto;
    }}
    .book-actions .btn {{ flex: 1; font-size: .78rem; padding: .45rem .4rem; }}
    @media (max-width: 480px) {{
      .lib-grid {{ grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 1rem; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <a href="{back_url}" class="back">{back}</a>
    <h1 class="sec-title">{title}</h1>
    <div class="lib-grid">
'''

for fname in files:
    stem      = fname[:-4]
    thumb_url = f"{thumb_dir}/{stem}.png"
    pdf_url   = f"{base}/{fname}"
    html += f'''      <div class="book-card">
        <div class="thumb-wrap">
          <div class="skeleton"></div>
          <img class="book-thumb"
               src="{thumb_url}"
               alt="{stem}"
               loading="lazy"
               onload="this.classList.add('loaded')"
               onerror="this.parentElement.querySelector('.skeleton').style.background='var(--surf2)';this.remove()"/>
        </div>
        <div class="book-info">
          <p class="book-name">{stem}</p>
          <div class="book-actions">
            <a href="{pdf_url}" target="_blank" class="btn btn-outline">閱讀</a>
            <a href="{pdf_url}" download class="btn btn-gold">下載</a>
          </div>
        </div>
      </div>
'''

if not files:
    html += '      <p style="color:var(--text2);grid-column:1/-1;padding:2rem 0">尚無資料 — 上傳 PDF 後自動顯示</p>\n'

html += '''    </div>
  </div>
</body>
</html>
'''

out = f"{lang}/shuiling/index.html"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Written {out} ({len(files)} books)")
