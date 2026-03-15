#!/usr/bin/env python3
import os, sys, glob

lang  = sys.argv[1]
repo  = sys.argv[2]
title = sys.argv[3]
back  = sys.argv[4]

poetry_dir = f"{lang}/poetry"
base       = f"/{repo}/{lang}/poetry"
back_url   = f"/{repo}/{lang}/index.html"

songs = []
if os.path.isdir(poetry_dir):
    for entry in sorted(os.scandir(poetry_dir), key=lambda e: e.name):
        if not entry.is_dir(): continue
        pdfs = sorted(glob.glob(os.path.join(entry.path, '*.pdf')))
        mp3s = sorted(glob.glob(os.path.join(entry.path, '*.mp3')))
        songs.append({
            'name':     entry.name,
            'pdf':      pdfs[0] if pdfs else None,
            'mp3':      mp3s[0] if mp3s else None,
            'pdf_name': os.path.basename(pdfs[0]) if pdfs else None,
            'mp3_name': os.path.basename(mp3s[0]) if mp3s else None,
        })

# ── Individual song pages ──────────────────────────────────────────────────────
SONG_CSS = f'''  <link rel="stylesheet" href="/{repo}/assets/css/style.css"/>
  <style>
    html, body {{ height: 100%; }}
    body {{ display: flex; flex-direction: column; }}
    .song-wrap {{ flex: 1; display: flex; flex-direction: column; max-width: 960px; margin: 0 auto; width: 100%; padding: 1.2rem 1rem 2rem; }}
    .song-title {{ font-family: var(--font-s); font-size: clamp(1.1rem,3vw,1.6rem); font-weight: 700; color: var(--text); margin-bottom: 1.2rem; }}
    /* PDF viewer */
    .pdf-section {{
      flex: 1;
      background: var(--surf);
      border: 1px solid var(--border);
      border-radius: var(--r-lg);
      overflow: hidden;
      margin-bottom: 1rem;
      min-height: 55vh;
      box-shadow: var(--shadow);
      display: flex;
      flex-direction: column;
    }}
    .pdf-section iframe {{
      flex: 1;
      width: 100%;
      min-height: 55vh;
      border: none;
      display: block;
    }}
    .pdf-missing {{
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text3);
      font-size: .9rem;
      padding: 2rem;
    }}
    /* Audio player */
    .audio-section {{
      background: var(--surf);
      border: 1px solid var(--border);
      border-radius: var(--r-lg);
      padding: 1rem 1.2rem;
      margin-bottom: 1rem;
      box-shadow: var(--shadow);
    }}
    .audio-label {{ font-size: .78rem; color: var(--text2); margin-bottom: .6rem; font-weight: 500; }}
    audio {{ width: 100%; }}
    .audio-missing {{ color: var(--text3); font-size: .85rem; padding: .5rem 0; }}
    /* Download row */
    .dl-row {{ display: flex; gap: .75rem; flex-wrap: wrap; }}
    .dl-row .btn {{ min-width: 130px; }}
  </style>'''

for s in songs:
    song_url = f"{base}/{s['name']}"
    pdf_url  = f"{song_url}/{s['pdf_name']}" if s['pdf'] else None
    mp3_url  = f"{song_url}/{s['mp3_name']}" if s['mp3'] else None

    sh = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{s['name']}</title>
{SONG_CSS}
</head>
<body>
  <div class="song-wrap">
    <a href="{base}/index.html" class="back">{title}</a>
    <h1 class="song-title">{s['name']}</h1>
'''
    # PDF section
    if pdf_url:
        sh += f'''    <div class="pdf-section">
      <iframe src="{pdf_url}" title="{s['name']}"></iframe>
    </div>
'''
    else:
        sh += '''    <div class="pdf-section">
      <div class="pdf-missing">PDF 尚未上傳</div>
    </div>
'''
    # Audio section
    sh += '    <div class="audio-section">\n'
    sh += '      <div class="audio-label">🎵 音頻播放</div>\n'
    if mp3_url:
        sh += f'      <audio controls preload="metadata"><source src="{mp3_url}" type="audio/mpeg"/>您的瀏覽器不支援音頻播放。</audio>\n'
    else:
        sh += '      <div class="audio-missing">MP3 尚未上傳</div>\n'
    sh += '    </div>\n'

    # Download row
    sh += '    <div class="dl-row">\n'
    if pdf_url:
        sh += f'      <a href="{pdf_url}" download class="btn btn-gold">⬇ 下載 PDF</a>\n'
        sh += f'      <a href="{pdf_url}" target="_blank" class="btn btn-outline">🔗 在瀏覽器打開 PDF</a>\n'
    if mp3_url:
        sh += f'      <a href="{mp3_url}" download class="btn btn-outline">⬇ 下載 MP3</a>\n'
    sh += '    </div>\n  </div>\n</body>\n</html>\n'

    out = f"{lang}/poetry/{s['name']}/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(sh)

# ── Poetry listing page ────────────────────────────────────────────────────────
html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title}</title>
  <link rel="stylesheet" href="/{repo}/assets/css/style.css"/>
  <style>
    .song-list {{ display: flex; flex-direction: column; gap: .65rem; max-width: 720px; }}
    .song-row {{
      display: flex;
      align-items: center;
      background: var(--surf);
      border: 1px solid var(--border);
      border-radius: var(--r-lg);
      padding: 1rem 1.2rem;
      gap: 1rem;
      text-decoration: none;
      color: var(--text);
      box-shadow: var(--shadow);
      transition: all .2s;
    }}
    .song-row:hover {{ background: var(--gold-bg); border-color: var(--gold-lt); transform: translateX(4px); }}
    .song-num {{ font-size: .75rem; color: var(--text3); min-width: 22px; font-family: var(--font-b); font-weight: 600; }}
    .song-info {{ flex: 1; }}
    .song-name {{ font-family: var(--font-s); font-size: 1rem; color: var(--text); font-weight: 600; }}
    .song-badges {{ display: flex; gap: .35rem; margin-top: .3rem; flex-wrap: wrap; }}
    .badge {{ font-size: .65rem; padding: .15rem .5rem; border-radius: 99px; border: 1px solid; font-weight: 500; }}
    .badge-pdf {{ border-color: #9a6f2e; color: #9a6f2e; background: #fdf3e3; }}
    .badge-mp3 {{ border-color: #2d7a4f; color: #2d7a4f; background: #edf7f1; }}
    .badge-miss {{ border-color: var(--miss-bdr); color: var(--text3); background: var(--miss-bg); }}
    .song-arrow {{ color: var(--text3); font-size: 1.1rem; }}
  </style>
</head>
<body>
  <div class="page">
    <a href="{back_url}" class="back">{back}</a>
    <h1 class="sec-title">{title}</h1>
    <div class="song-list">
'''
for i, s in enumerate(songs, 1):
    song_url  = f"{base}/{s['name']}/index.html"
    pdf_badge = '<span class="badge badge-pdf">PDF ✓</span>' if s['pdf'] else '<span class="badge badge-miss">PDF 待上傳</span>'
    mp3_badge = '<span class="badge badge-mp3">MP3 ✓</span>' if s['mp3'] else '<span class="badge badge-miss">MP3 待上傳</span>'
    html += f'''      <a href="{song_url}" class="song-row">
        <span class="song-num">{i:02d}</span>
        <div class="song-info">
          <div class="song-name">{s['name']}</div>
          <div class="song-badges">{pdf_badge}{mp3_badge}</div>
        </div>
        <span class="song-arrow">›</span>
      </a>
'''
if not songs:
    html += '      <p style="color:var(--text2);padding:2rem 0">尚未上傳詩歌 — 請在 poetry/ 目錄下建立各詩歌子資料夾</p>\n'
html += f'''    </div>
  </div>
</body>
</html>
'''
out = f"{lang}/poetry/index.html"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Written {out} ({len(songs)} songs)")
