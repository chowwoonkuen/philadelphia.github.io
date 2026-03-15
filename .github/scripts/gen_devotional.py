#!/usr/bin/env python3
import os, sys, re

lang  = sys.argv[1]
repo  = sys.argv[2]
title = sys.argv[3]
back  = sys.argv[4]
ver   = sys.argv[5] if len(sys.argv) > 5 else 'dev'

MONTHS = ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']
DAYS   = [31,29,31,30,31,30,31,31,30,31,30,31]

dev_dir  = f"{lang}/devotional"
base     = f"/{repo}/{lang}/devotional"
back_url = f"/{repo}/{lang}/index.html"

existing = set()
if os.path.isdir(dev_dir):
    for fname in os.listdir(dev_dir):
        m = re.match(r'^(\d{2})\.(\d{2})\.pdf$', fname)
        if m:
            existing.add((int(m.group(1)), int(m.group(2))))

total   = sum(DAYS)
present = len(existing)

html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title}</title>
  <link rel="stylesheet" href="/{repo}/assets/css/style.css?v={ver}"/>
  <style>
    .progress-row {{
      display: flex;
      align-items: center;
      gap: 1rem;
      margin-bottom: 1.5rem;
      font-size: .85rem;
      color: var(--text2);
    }}
    .progress-bar {{
      flex: 1;
      height: 6px;
      background: var(--surf3);
      border-radius: 99px;
      overflow: hidden;
    }}
    .progress-fill {{
      height: 100%;
      background: linear-gradient(90deg, var(--gold), var(--gold-lt));
      border-radius: 99px;
      width: {present/total*100:.1f}%;
    }}
    /* ── Legend ── */
    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 1.5rem;
      font-size: .8rem;
      color: var(--text2);
    }}
    .legend-item {{ display: flex; align-items: center; gap: .4rem; }}
    .leg-dot {{ width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }}
    .leg-avail {{ background: var(--gold-bg); border: 1.5px solid var(--gold-lt); }}
    .leg-miss  {{ background: var(--miss-bg); border: 1.5px dashed var(--miss-bdr); }}
    .leg-today {{ background: var(--today-bg); border: 1.5px solid var(--today-bdr); }}
    /* ── Month tabs ── */
    .month-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: .4rem;
      margin-bottom: 1.5rem;
    }}
    .mtab {{
      padding: .35rem .8rem;
      border-radius: 99px;
      font-size: .82rem;
      border: 1px solid var(--border);
      color: var(--text2);
      background: var(--surf);
      cursor: pointer;
      transition: all .18s;
    }}
    .mtab:hover {{ border-color: var(--gold-lt); color: var(--gold); background: var(--gold-bg); }}
    .mtab.active {{ background: var(--gold); border-color: var(--gold); color: #fff; font-weight: 600; }}
    /* ── Month panel ── */
    .month-panel {{ display: none; }}
    .month-panel.visible {{ display: block; }}
    .month-name {{
      font-family: var(--font-s);
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 1rem;
    }}
    .days-grid {{
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: .4rem;
    }}
    .day-tile {{
      aspect-ratio: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      border-radius: var(--r);
      font-size: .8rem;
      transition: all .18s;
      position: relative;
      cursor: default;
    }}
    .day-tile.avail {{
      background: var(--gold-bg);
      border: 1.5px solid var(--gold-lt);
      text-decoration: none;
      cursor: pointer;
      color: var(--text);
    }}
    .day-tile.avail:hover {{
      background: var(--gold);
      border-color: var(--gold);
      transform: scale(1.1);
      box-shadow: 0 3px 12px rgba(154,111,46,.25);
      z-index: 1;
    }}
    .day-tile.avail:hover .day-num {{ color: #fff; }}
    .day-tile.miss {{
      background: var(--miss-bg);
      border: 1.5px dashed var(--miss-bdr);
      color: var(--text3);
    }}
    .day-tile.today-hi {{
      background: var(--today-bg) !important;
      border: 2px solid var(--today-bdr) !important;
      box-shadow: 0 0 0 3px rgba(120,31,16,.2);
    }}
    .day-tile.today-hi .day-num {{ color: #ffcba4 !important; }}
    .day-num {{ font-size: .85rem; font-weight: 500; line-height: 1; }}
    .day-dot {{
      width: 4px; height: 4px;
      border-radius: 50%;
      background: var(--gold);
      margin-top: 2px;
    }}
    .day-tile.miss .day-dot {{ background: var(--text3); opacity: .4; }}
    .day-tile.today-hi .day-dot {{ background: #ffcba4; }}
    @media (max-width: 380px) {{
      .days-grid {{ gap: .25rem; }}
      .day-num {{ font-size: .75rem; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <a href="{back_url}" class="back">{back}</a>
    <h1 class="sec-title">{title}</h1>

    <div class="progress-row">
      <span>已上傳 <strong>{present}</strong> / {total} 天</span>
      <div class="progress-bar"><div class="progress-fill"></div></div>
    </div>

    <div class="legend">
      <div class="legend-item"><span class="leg-dot leg-avail"></span><span>已上傳（點擊閱讀）</span></div>
      <div class="legend-item"><span class="leg-dot leg-miss"></span><span>尚未上傳</span></div>
      <div class="legend-item"><span class="leg-dot leg-today"></span><span>今天</span></div>
    </div>

    <div class="month-tabs">
'''
for i, mname in enumerate(MONTHS):
    html += f'      <button class="mtab" onclick="showMonth({i})" id="tab{i}">{mname}</button>\n'
html += '    </div>\n'

for mi, mname in enumerate(MONTHS):
    mm   = mi + 1
    days = DAYS[mi]
    # First month is visible by default (JS will switch to today's month)
    vis  = ' visible' if mi == 0 else ''
    html += f'    <div class="month-panel{vis}" id="mpanel{mi}">\n'
    html += f'      <div class="month-name">{mname}</div>\n'
    html += '      <div class="days-grid">\n'
    for d in range(1, days + 1):
        date_str = f'{mm:02d}.{d:02d}'
        if (mm, d) in existing:
            url = f"{base}/{date_str}.pdf?v={ver}"
            html += f'        <a href="{url}" target="_blank" class="day-tile avail" data-date="{date_str}" title="{date_str}（點擊閱讀）">\n'
            html += f'          <span class="day-num">{d}</span><div class="day-dot"></div>\n        </a>\n'
        else:
            html += f'        <div class="day-tile miss" data-date="{date_str}" title="{date_str}（未上傳）">\n'
            html += f'          <span class="day-num">{d}</span><div class="day-dot"></div>\n        </div>\n'
    html += '      </div>\n    </div>\n'

html += '''  </div>
  <script>
    function showMonth(idx) {
      document.querySelectorAll('.month-panel').forEach(function(el) { el.classList.remove('visible'); });
      document.querySelectorAll('.mtab').forEach(function(el) { el.classList.remove('active'); });
      document.getElementById('mpanel' + idx).classList.add('visible');
      document.getElementById('tab' + idx).classList.add('active');
    }
    (function() {
      var t  = new Date();
      var mm = String(t.getMonth() + 1).padStart(2, '0');
      var dd = String(t.getDate()).padStart(2, '0');
      var el = document.querySelector('[data-date="' + mm + '.' + dd + '"]');
      if (el) { el.classList.add('today-hi'); }
      showMonth(t.getMonth());
    })();
  </script>
</body>
</html>
'''

out = f"{lang}/devotional/index.html"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Written {out} ({present}/{total} days)")
