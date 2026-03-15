#!/usr/bin/env python3
import os, sys, re
from collections import defaultdict

lang  = sys.argv[1]
repo  = sys.argv[2]
title = sys.argv[3]
back  = sys.argv[4]

# ── Full 66-book list with abbreviation, full name, category ──────────────────
BOOKS = [
    (1,'創','創世記','律法書'),(2,'出','出埃及記','律法書'),(3,'利','利未記','律法書'),
    (4,'民','民數記','律法書'),(5,'申','申命記','律法書'),
    (6,'書','約書亞記','歷史書'),(7,'士','士師記','歷史書'),(8,'得','路得記','歷史書'),
    (9,'撒上','撒母耳記上','歷史書'),(10,'撒下','撒母耳記下','歷史書'),
    (11,'王上','列王紀上','歷史書'),(12,'王下','列王紀下','歷史書'),
    (13,'代上','歷代志上','歷史書'),(14,'代下','歷代志下','歷史書'),
    (15,'拉','以斯拉記','歷史書'),(16,'尼','尼希米記','歷史書'),(17,'斯','以斯帖記','歷史書'),
    (18,'伯','約伯記','詩歌書'),(19,'詩','詩篇','詩歌書'),(20,'箴','箴言','詩歌書'),
    (21,'傳','傳道書','詩歌書'),(22,'歌','雅歌','詩歌書'),
    (23,'賽','以賽亞書','大先知書'),(24,'耶','耶利米書','大先知書'),
    (25,'哀','耶利米哀歌','大先知書'),(26,'結','以西結書','大先知書'),(27,'但','但以理書','大先知書'),
    (28,'何','何西阿書','小先知書'),(29,'珥','約珥書','小先知書'),(30,'摩','阿摩司書','小先知書'),
    (31,'俄','俄巴底亞書','小先知書'),(32,'拿','約拿書','小先知書'),(33,'彌','彌迦書','小先知書'),
    (34,'鴻','鴻書','小先知書'),(35,'哈','哈巴谷書','小先知書'),(36,'番','西番雅書','小先知書'),
    (37,'該','哈該書','小先知書'),(38,'亞','撒迦利亞書','小先知書'),(39,'瑪','瑪拉基書','小先知書'),
    (40,'太','馬太福音','福音書'),(41,'可','馬可福音','福音書'),
    (42,'路','路加福音','福音書'),(43,'約','約翰福音','福音書'),
    (44,'徒','使徒行傳','使徒行傳'),
    (45,'羅','羅馬書','書信'),(46,'林前','哥林多前書','書信'),(47,'林後','哥林多後書','書信'),
    (48,'加','加拉太書','書信'),(49,'弗','以弗所書','書信'),(50,'腓','腓立比書','書信'),
    (51,'西','歌羅西書','書信'),(52,'帖前','帖撒羅尼迦前書','書信'),(53,'帖後','帖撒羅尼迦後書','書信'),
    (54,'提前','提摩太前書','書信'),(55,'提後','提摩太後書','書信'),(56,'多','提多書','書信'),
    (57,'門','腓利門書','書信'),(58,'來','希伯來書','書信'),(59,'雅','雅各書','書信'),
    (60,'彼前','彼得前書','書信'),(61,'彼後','彼得後書','書信'),
    (62,'約一','約翰一書','書信'),(63,'約二','約翰二書','書信'),(64,'約三','約翰三書','書信'),
    (65,'猶','猶大書','書信'),(66,'啟','啟示錄','啟示錄'),
]

CAT_ORDER = ['律法書','歷史書','詩歌書','大先知書','小先知書','福音書','使徒行傳','書信','啟示錄']
OT_CATS   = {'律法書','歷史書','詩歌書','大先知書','小先知書'}
NT_CATS   = {'福音書','使徒行傳','書信','啟示錄'}

# ── Scan existing PDFs: number in filename → filename ─────────────────────────
bible_dir = f"{lang}/bible"
existing = {}
if os.path.isdir(bible_dir):
    for fname in os.listdir(bible_dir):
        if fname.lower().endswith('.pdf'):
            nums = re.findall(r'\d+', os.path.splitext(fname)[0])
            for n in nums:
                ni = int(n)
                if 1 <= ni <= 66:
                    existing[ni] = fname
                    break

base     = f"/{repo}/{lang}/bible"
back_url = f"/{repo}/{lang}/index.html"

cats = defaultdict(list)
for b in BOOKS:
    cats[b[3]].append(b)

html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title}</title>
  <link rel="stylesheet" href="/{repo}/assets/css/style.css"/>
  <style>
    /* ── Testament section header ── */
    .testament-block {{
      margin-bottom: 2.5rem;
    }}
    .testament-header {{
      display: flex;
      align-items: center;
      gap: .75rem;
      margin-bottom: 1.5rem;
    }}
    .testament-pill {{
      font-family: var(--font-s);
      font-size: .95rem;
      font-weight: 700;
      color: #fff;
      background: var(--gold);
      padding: .3rem .9rem;
      border-radius: 99px;
      white-space: nowrap;
    }}
    .testament-line {{
      flex: 1;
      height: 2px;
      background: var(--border);
      border-radius: 99px;
    }}
    /* ── Category section ── */
    .cat-block {{
      margin-bottom: 1.8rem;
      padding: 1.2rem 1.2rem .8rem;
      background: var(--surf);
      border: 1px solid var(--border);
      border-radius: var(--r-lg);
      box-shadow: var(--shadow);
    }}
    .cat-header {{
      display: flex;
      align-items: center;
      gap: .6rem;
      margin-bottom: 1rem;
    }}
    .cat-label {{
      font-family: var(--font-s);
      font-size: .88rem;
      font-weight: 700;
      color: var(--gold);
      letter-spacing: .06em;
    }}
    .cat-count {{
      font-size: .72rem;
      color: var(--text3);
      background: var(--surf2);
      border: 1px solid var(--border);
      border-radius: 99px;
      padding: .1rem .5rem;
    }}
    /* ── Book grid ── */
    .books-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(72px, 1fr));
      gap: .55rem;
    }}
    .book-tile {{
      aspect-ratio: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      border-radius: var(--r);
      text-align: center;
      padding: .3rem .15rem;
      transition: all .18s;
      position: relative;
    }}
    .book-tile.avail {{
      background: var(--gold-bg);
      border: 1.5px solid var(--gold-lt);
      text-decoration: none;
      cursor: pointer;
    }}
    .book-tile.avail:hover {{
      background: var(--gold);
      border-color: var(--gold);
      transform: scale(1.08);
      box-shadow: 0 4px 14px rgba(154,111,46,.3);
    }}
    .book-tile.avail:hover .book-abbr,
    .book-tile.avail:hover .book-fullname {{ color: #fff !important; }}
    .book-tile.miss {{
      background: var(--miss-bg);
      border: 1.5px dashed var(--miss-bdr);
    }}
    .book-num {{
      position: absolute;
      top: 3px; right: 5px;
      font-size: .48rem;
      color: var(--text3);
      font-family: var(--font-b);
    }}
    .book-abbr {{
      font-family: var(--font-s);
      font-size: 1.05rem;
      font-weight: 700;
      line-height: 1;
    }}
    .book-tile.avail .book-abbr {{ color: var(--gold); }}
    .book-tile.miss  .book-abbr {{ color: var(--text3); }}
    .book-fullname {{
      font-size: .52rem;
      margin-top: .2rem;
      line-height: 1.2;
    }}
    .book-tile.avail .book-fullname {{ color: var(--text2); }}
    .book-tile.miss  .book-fullname {{ color: var(--text3); }}
    /* ── Summary bar ── */
    .stat-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 1.2rem;
      margin-bottom: 2rem;
      padding: .85rem 1.1rem;
      background: var(--surf);
      border: 1px solid var(--border);
      border-radius: var(--r-lg);
      box-shadow: var(--shadow);
    }}
    .stat-item {{ display: flex; align-items: center; gap: .5rem; font-size: .85rem; }}
    .stat-dot {{ width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }}
    .stat-avail {{ background: var(--gold-bg); border: 1.5px solid var(--gold-lt); }}
    .stat-miss  {{ background: var(--miss-bg); border: 1.5px dashed var(--miss-bdr); }}
    @media (max-width: 400px) {{
      .books-grid {{ grid-template-columns: repeat(auto-fill, minmax(62px,1fr)); gap:.4rem; }}
      .book-abbr {{ font-size: .95rem; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <a href="{back_url}" class="back">{back}</a>
    <h1 class="sec-title">{title}</h1>
    <div class="stat-bar">
      <div class="stat-item"><span class="stat-dot stat-avail"></span><span>已上傳 <strong>{len(existing)}</strong> / 66 卷</span></div>
      <div class="stat-item"><span class="stat-dot stat-miss"></span><span>尚未上傳</span></div>
    </div>
'''

# ── Render Old Testament ───────────────────────────────────────────────────────
def render_testament(heading, cat_list):
    out = f'    <div class="testament-block">\n'
    out += f'      <div class="testament-header"><span class="testament-pill">{heading}</span><div class="testament-line"></div></div>\n'
    for cat in cat_list:
        if cat not in cats: continue
        books = cats[cat]
        avail_count = sum(1 for (n,*_) in books if n in existing)
        out += f'      <div class="cat-block">\n'
        out += f'        <div class="cat-header"><span class="cat-label">{cat}</span><span class="cat-count">{avail_count}/{len(books)}</span></div>\n'
        out += f'        <div class="books-grid">\n'
        for (num, abbr, name, _) in books:
            if num in existing:
                url = f"{base}/{existing[num]}"
                out += f'          <a href="{url}" target="_blank" class="book-tile avail" title="{name}（點擊閱讀）">\n'
            else:
                out += f'          <div class="book-tile miss" title="{name}（未上傳）">\n'
            out += f'            <span class="book-num">{num:02d}</span>\n'
            out += f'            <span class="book-abbr">{abbr}</span>\n'
            out += f'            <span class="book-fullname">{name}</span>\n'
            out += '          </a>\n' if num in existing else '          </div>\n'
        out += '        </div>\n      </div>\n'
    out += '    </div>\n'
    return out

ot_label = '舊約聖經' if lang == 'zh-hant' else '旧约圣经'
nt_label = '新約聖經' if lang == 'zh-hant' else '新约圣经'
html += render_testament(ot_label, ['律法書','歷史書','詩歌書','大先知書','小先知書'])
html += render_testament(nt_label, ['福音書','使徒行傳','書信','啟示錄'])

html += '''  </div>
</body>
</html>
'''

out = f"{lang}/bible/index.html"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Written {out} ({len(existing)}/66 uploaded)")
