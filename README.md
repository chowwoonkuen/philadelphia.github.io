# 非拉鐵非書簡 Books of Philadelphia

Static GitHub Pages site serving Chinese-language Christian resources.  
**Live site:** https://chowwoonkuen.github.io/philadelphia.github.io/

---

## How to add content

No HTML editing ever needed. Upload a file to the right folder, push to `main`, and the site rebuilds automatically.

### 屬靈書 / 属灵书 (Spiritual Books)

Upload any PDF to `zh-hant/shuiling/` or `zh-hans/shuiling/`.  
A full-page thumbnail is auto-generated on first push. Filename becomes the display title.

### 聖經難字粵音 (Bible)

Upload PDFs to `zh-hant/bible/` or `zh-hans/bible/`.  
The filename **must contain the 2-digit book number** (01–66):

| Book | Correct filename example |
|------|--------------------------|
| 創世記 (Genesis) | `創世記01.pdf` |
| 約翰福音 (John) | `約翰福音43.pdf` |
| 啟示錄 (Revelation) | `啟示錄66.pdf` |

All 66 books are always shown on the page. Missing books appear dimmed until you upload them.

**Book number reference (01–66):**
```
律法書:  創01 出02 利03 民04 申05
歷史書:  書06 士07 得08 撒上09 撒下10 王上11 王下12 代上13 代下14 拉15 尼16 斯17
詩歌書:  伯18 詩19 箴20 傳21 歌22
大先知書: 賽23 耶24 哀25 結26 但27
小先知書: 何28 珥29 摩30 俄31 拿32 彌33 鴻34 哈35 番36 該37 亞38 瑪39
福音書:  太40 可41 路42 約43
使徒行傳: 徒44
書信:    羅45 林前46 林後47 加48 弗49 腓50 西51 帖前52 帖後53
         提前54 提後55 多56 門57 來58 雅59 彼前60 彼後61
         約一62 約二63 約三64 猶65
啟示錄:  啟66
```

### 靈修資料 (Devotional)

Upload PDFs to `zh-hant/devotional/` or `zh-hans/devotional/`.  
Files **must be named** `MM.DD.pdf`:

```
01.01.pdf  = January 1
02.29.pdf  = February 29
12.31.pdf  = December 31
```

The calendar always shows all 366 days. Uploaded days are highlighted in gold; today's date is marked automatically.

### 詩歌 (Poetry / Hymns)

Create one sub-folder per song inside `zh-hant/poetry/` or `zh-hans/poetry/`.  
Put one `.pdf` and one `.mp3` inside the folder. The folder name becomes the song title.

```
zh-hant/poetry/
├── 01 歌名甲/
│   ├── 歌名甲.pdf
│   └── 歌名甲.mp3
├── 02 歌名乙/
│   ├── 歌名乙.pdf
│   └── 歌名乙.mp3
└── ...
```

The song page embeds a PDF viewer and an audio player. Both PDF and MP3 can be downloaded individually.  
If either file is missing the page still loads — it just shows a "not yet uploaded" placeholder for that item.

---

## File structure

```
/
├── index.html                      ← Landing page — DO NOT EDIT
├── assets/
│   ├── css/style.css               ← Stylesheet (edit to change appearance)
│   └── thumbs/                     ← Auto-generated thumbnails (DO NOT EDIT)
├── .github/
│   ├── workflows/generate-pages.yml
│   └── scripts/                    ← Page generator scripts (DO NOT EDIT)
│       ├── gen_shuiling.py
│       ├── gen_bible.py
│       ├── gen_devotional.py
│       └── gen_poetry.py
├── zh-hant/                        ← 繁體 Traditional Chinese
│   ├── index.html                  ← DO NOT EDIT
│   ├── shuiling/                   ← drop PDFs here
│   ├── bible/                      ← drop PDFs here
│   ├── devotional/                 ← drop MM.DD.pdf files here
│   └── poetry/                     ← one sub-folder per song
└── zh-hans/                        ← 簡體 Simplified Chinese (same structure)
```

---

## Regenerating thumbnails

Shuiling thumbnails are regenerated on every push. If an old cropped thumbnail is stuck in the repo, delete it from `assets/thumbs/zh-hant/shuiling/` or `assets/thumbs/zh-hans/shuiling/` and push — it will be recreated as a full-page thumbnail automatically.

---

## Technical notes

- Every deploy stamps `?v=<commit SHA>` onto all CSS links so browsers never serve stale styles.
- Fonts are loaded from `fonts.bunny.net` (privacy-friendly, no Google tracking).
- All pages are fully responsive — works on mobile and desktop.
- The workflow file is `.github/workflows/generate-pages.yml`. Trigger a manual deploy any time via **Actions → Build & Deploy → Run workflow**.
EOF

cp /home/claude/build/README.md /mnt/user-data/outputs/README.md
echo "Done"
