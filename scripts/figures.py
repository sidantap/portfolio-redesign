"""Draw every project figure as SVG into public/fig/.

Each project gets its own kind of figure, chosen for what that project is about:
  nightly 311   dbt lineage graph (real model names) · incremental load windows · real charts
  comply.       case state machine (from the product's transition table) · a reproducible shuffle
  lakehouse     metadata-driven ingestion config · SCD Type 2 version timeline
  faa           eligibility funnel · quarterly targets with rollover
  cargo         real BTS monthly air cargo ton-miles, 2003 to date
  nurse         one post's path through the NLP pipeline
  chatbot       anatomy of a training sample
  clinical map  world map of study sites (illustrative)
  motus         profitability KPI tree (the dashboards themselves are real screenshots in public/img)
  vidvo         figures live in scripts/figures_vidvo.py
Illustrative figures say so on the figure. Figures carry their own paper background so they
read the same in night and day.  Re-run with:  python3 scripts/figures.py
"""
import json, math, os, random, textwrap
from html import escape

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'public', 'fig')
os.makedirs(OUT, exist_ok=True)

PAPER, INK, SOFT, FAINT, LINE = '#fbf6f3', '#2b1d1d', '#6a5651', '#9a8580', '#e5d8d2'
EMBER, EMBER_SOFT, SLATE, SLATE_SOFT = '#c55e2c', '#f6e1d4', '#3f5d78', '#e3eaf1'
OK, OK_SOFT, BAD, BAD_SOFT, GOLD = '#2f7a4f', '#e1efe6', '#b23a32', '#f7e2df', '#a8801a'
CODE_BG, CODE_INK = '#241a1b', '#f3e6de'
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def save(name, w, h, body, title):
    open(os.path.join(OUT, name + '.svg'), 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
        f'aria-label="{escape(title)}"><title>{escape(title)}</title><rect width="{w}" height="{h}" fill="{PAPER}"/>{body}</svg>')


def T(x, y, s, size=13, fill=INK, font=SERIF, anchor='start', weight='400', ls=0, upper=False, italic=False):
    s = s.upper() if upper else s
    st = ' font-style="italic"' if italic else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" letter-spacing="{ls}"{st}>{escape(s)}</text>')


def head(title, sub):
    return T(40, 42, title, 21) + T(40, 64, sub, 11, FAINT, MONO, ls=0.4)


def arrowhead(x, y, ang, color, a=7):
    p1 = (x - a * math.cos(ang - 0.42), y - a * math.sin(ang - 0.42))
    p2 = (x - a * math.cos(ang + 0.42), y - a * math.sin(ang + 0.42))
    return f'<path d="M{x:.1f},{y:.1f} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{color}"/>'


def curve(x1, y1, x2, y2, color=SOFT, w=1.3, dash=False, head_=True):
    mx = (x1 + x2) / 2
    d = f'M{x1:.1f},{y1:.1f} C{mx:.1f},{y1:.1f} {mx:.1f},{y2:.1f} {x2:.1f},{y2:.1f}'
    da = ' stroke-dasharray="4 4"' if dash else ''
    out = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{da}/>'
    return out + (arrowhead(x2, y2, 0, color) if head_ else '')


def nice(mx, n=4):
    raw = mx / n; mag = 10 ** math.floor(math.log10(raw)); st = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    t = [0]
    while t[-1] < mx: t.append(t[-1] + st)
    return t


# ===================================================================== Nightly 311

def nightly_lineage():
    """dbt lineage: every model and source in the repo, wired by its real ref()/source() calls."""
    cols = {
        'source': ['raw.cincy_311', 'raw.weather_daily', 'raw.nhtsa_complaints'],
        'staging': ['stg_311', 'stg_weather', 'stg_nhtsa'],
        'silver': ['svc_requests_checked', 'weather_daily', 'complaints'],
        'silver ': ['svc_requests', 'svc_requests_quarantine'],
        'gold': ['dim_request_type', 'dim_date', 'fct_service_requests'],
        'gold ': ['fct_daily_requests_weather'],
        'ml': ['ml.predictions', 'ml.live_metrics'],
    }
    seeds = {'status_groups': 'svc_requests_checked', 'component_groups': 'complaints'}
    edges = [('raw.cincy_311', 'stg_311'), ('raw.weather_daily', 'stg_weather'), ('raw.nhtsa_complaints', 'stg_nhtsa'),
             ('stg_311', 'svc_requests_checked'), ('stg_weather', 'weather_daily'), ('stg_nhtsa', 'complaints'),
             ('svc_requests_checked', 'svc_requests'), ('svc_requests_checked', 'svc_requests_quarantine'),
             ('svc_requests', 'dim_request_type'), ('svc_requests', 'dim_date'), ('svc_requests', 'fct_service_requests'),
             ('dim_request_type', 'fct_service_requests'), ('fct_service_requests', 'fct_daily_requests_weather'),
             ('dim_request_type', 'fct_daily_requests_weather'), ('weather_daily', 'fct_daily_requests_weather'),
             ('complaints', 'ml.predictions'), ('ml.predictions', 'ml.live_metrics')]
    tone = {'source': (FAINT, '#fff'), 'staging': (SLATE, SLATE_SOFT), 'silver': (SLATE, '#fff'), 'silver ': (SLATE, '#fff'),
            'gold': (EMBER, EMBER_SOFT), 'gold ': (EMBER, EMBER_SOFT), 'ml': (OK, OK_SOFT)}
    w, h = 1420, 520; x0, colw, gapx = 36, 172, 22
    pos = {}; body = head('Lineage of every table the nightly run builds', 'from the dbt project: each line is a real ref() or source() call')
    for ci, (layer, names) in enumerate(cols.items()):
        x = x0 + ci * (colw + gapx)
        body += T(x, 104, layer.strip(), 10.5, EMBER, MONO, ls=1.6, upper=True)
        n = len(names); step = 330 / n
        for i, nm in enumerate(names):
            pos[nm] = (x, 150 + (i + 0.5) * step - 18, ci)
    for a, b in edges:
        xa, ya, _ = pos[a]; xb, yb, _ = pos[b]
        c = BAD if b == 'svc_requests_quarantine' else (OK if b.startswith('ml.') else SOFT)
        body += curve(xa + colw, ya + 15, xb - 2, yb + 15, c, 1.2)
    for nm, (x, y, ci) in pos.items():
        stroke, fill = tone[list(cols)[ci]]
        if nm == 'svc_requests_quarantine': stroke, fill = BAD, BAD_SOFT
        body += f'<rect x="{x}" y="{y}" width="{colw}" height="30" rx="15" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
        body += f'<circle cx="{x + 14}" cy="{y + 15}" r="4" fill="{stroke}"/>'
        body += T(x + 24, y + 19.5, nm, 10.2, INK, MONO)
    body += T(x0, 472, 'seeds', 10.5, GOLD, MONO, ls=1.6, upper=True)
    for i, (sd, tgt) in enumerate(seeds.items()):
        x = x0 + 80 + i * 190; y = 456
        body += f'<rect x="{x}" y="{y}" width="170" height="26" rx="4" fill="#fff" stroke="{GOLD}" stroke-dasharray="3 3"/>' + T(x + 10, y + 17, sd + '.csv', 10.8, INK, MONO)
        tx, ty, _ = pos[tgt]
        body += f'<path d="M{x + 170:.1f},{y + 13:.1f} C{tx - 30:.1f},{y + 13:.1f} {tx - 40:.1f},{ty + 26:.1f} {tx + 10:.1f},{ty + 30:.1f}" fill="none" stroke="{GOLD}" stroke-width="1.1" stroke-dasharray="3 3"/>'
    lx, ly = 560, 472
    for c, t in [(SLATE, 'cleaned'), (BAD, 'quarantine: rows that break a rule'), (EMBER, 'gold star schema'), (OK, 'model output')]:
        body += f'<circle cx="{lx}" cy="{ly - 4}" r="4" fill="{c}"/>' + T(lx + 10, ly, t, 11, SOFT, MONO); lx += 34 + len(t) * 6.4
    save('nightly-lineage', w, h, body, 'dbt lineage of the nightly pipeline')


def nightly_windows():
    w, h = 1100, 360; L, R = 150, 40
    body = head('Each night loads only what changed, plus a safety overlap', 'Cincinnati 311 · watermark = newest date_last_update already loaded · overlap = 2 days · dates illustrative')
    days = 12; x = lambda d: L + (w - L - R) * d / days
    for d in range(days + 1):
        body += f'<line x1="{x(d):.1f}" y1="92" x2="{x(d):.1f}" y2="{h - 56}" stroke="{LINE}"/>'
        if d < days: body += T((x(d) + x(d + 1)) / 2, h - 36, f'Oct {20 + d}', 10.5, FAINT, MONO, 'middle')
    for i, (a, b) in enumerate([(0, 4), (2, 6), (4, 8), (6, 10), (8, 12)]):
        y = 108 + i * 38
        body += T(L - 16, y + 17, f'night {i + 1}', 12.5, INK, SERIF, 'end')
        if i:
            body += f'<rect x="{x(a):.1f}" y="{y}" width="{x(a + 2) - x(a):.1f}" height="24" rx="4" fill="{GOLD}" opacity="0.3"/>'
            body += f'<rect x="{x(a + 2):.1f}" y="{y}" width="{x(b) - x(a + 2):.1f}" height="24" rx="4" fill="{EMBER}"/>'
        else:
            body += f'<rect x="{x(a):.1f}" y="{y}" width="{x(b) - x(a):.1f}" height="24" rx="4" fill="{EMBER}"/>'
        body += f'<line x1="{x(b):.1f}" y1="{y - 4}" x2="{x(b):.1f}" y2="{y + 28}" stroke="{INK}" stroke-width="2"/>'
    body += f'<rect x="{L}" y="{h - 22}" width="12" height="10" fill="{EMBER}"/>' + T(L + 18, h - 13, 'new rows since the watermark', 11, SOFT, MONO)
    body += f'<rect x="{L + 260}" y="{h - 22}" width="12" height="10" fill="{GOLD}" opacity="0.45"/>' + T(L + 278, h - 13, 're-read overlap: catches requests closed or edited late', 11, SOFT, MONO)
    body += f'<line x1="{L + 690}" y1="{h - 24}" x2="{L + 690}" y2="{h - 9}" stroke="{INK}" stroke-width="2"/>' + T(L + 698, h - 13, 'watermark after the run', 11, SOFT, MONO)
    save('nightly-windows', w, h, body, 'Incremental load windows with overlap')


D = json.load(open(os.path.join(HERE, 'nightly-snapshot.json')))
SNAP = D['generated_at'][:10]


def nightly_requests():
    rows = D['daily']; w, h = 1100, 380; L, R, Tp, B = 70, 30, 92, 46; iw, ih = w - L - R, h - Tp - B
    tk = nice(max(r['requests'] for r in rows)); top = tk[-1]
    body = head('311 requests per day, last 90 days', f'gold.fct_daily_requests_weather · real data · snapshot {SNAP}')
    for v in tk:
        y = Tp + ih - ih * v / top
        body += f'<line x1="{L}" x2="{w - R}" y1="{y:.1f}" y2="{y:.1f}" stroke="{LINE}"/>' + T(L - 10, y + 4, f'{v:,}', 11, FAINT, MONO, 'end')
    step = iw / len(rows); bw = max(1, step - 2)
    for i, r in enumerate(rows):
        hh = ih * r['requests'] / top; x = L + i * step + 1; y = Tp + ih - hh; rr = min(3, bw / 2, hh)
        wet = (r.get('precip_in') or 0) >= 0.25
        body += (f'<path d="M{x:.1f},{Tp + ih} V{y + rr:.1f} Q{x:.1f},{y:.1f} {x + rr:.1f},{y:.1f} H{x + bw - rr:.1f} '
                 f'Q{x + bw:.1f},{y:.1f} {x + bw:.1f},{y + rr:.1f} V{Tp + ih} Z" fill="{SLATE if wet else EMBER}"/>')
        if i % 14 == 0: body += T(x + bw / 2, h - 18, f'{MON[int(r["day"][5:7]) - 1]} {int(r["day"][8:])}', 11, FAINT, MONO, 'middle')
    body += f'<rect x="{w - R - 330}" y="{Tp - 24}" width="10" height="10" fill="{EMBER}"/>' + T(w - R - 314, Tp - 15, 'dry day', 11, SOFT, MONO)
    body += f'<rect x="{w - R - 240}" y="{Tp - 24}" width="10" height="10" fill="{SLATE}"/>' + T(w - R - 224, Tp - 15, '≥ 0.25 in of rain at CVG', 11, SOFT, MONO)
    save('nightly-requests', w, h, body, '311 requests per day, colored by rain')


def nightly_accuracy():
    rows = D['live_metrics']; test = D['offline_metrics']['accuracy'] * 100
    w, h = 1100, 350; L, R, Tp, B = 70, 150, 92, 46; iw, ih = w - L - R, h - Tp - B; lo, hi = 60, 100
    X = lambda i: L + iw * i / max(1, len(rows) - 1); Y = lambda v: Tp + ih - ih * (v - lo) / (hi - lo)
    body = head('Accuracy on complaints the model has never seen', f'ml.live_metrics · scored nightly against NHTSA’s own tags · snapshot {SNAP}')
    for v in range(lo, hi + 1, 10):
        body += f'<line x1="{L}" x2="{L + iw}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"/>' + T(L - 10, Y(v) + 4, f'{v}%', 11, FAINT, MONO, 'end')
    body += f'<line x1="{L}" x2="{L + iw}" y1="{Y(test):.1f}" y2="{Y(test):.1f}" stroke="{SLATE}" stroke-width="1.5" stroke-dasharray="5 5"/>' + T(L + iw + 10, Y(test) + 4, f'test set {test:.1f}%', 11.5, SLATE, MONO)
    pts = ' '.join(f'{X(i):.1f},{Y(r["accuracy"] * 100):.1f}' for i, r in enumerate(rows))
    body += f'<polyline points="{pts}" fill="none" stroke="{EMBER}" stroke-width="2.2" stroke-linejoin="round"/>'
    last = rows[-1]['accuracy'] * 100
    body += f'<circle cx="{X(len(rows) - 1):.1f}" cy="{Y(last):.1f}" r="4.5" fill="{EMBER}" stroke="{PAPER}" stroke-width="2"/>' + T(L + iw + 10, Y(last) + 4, f'live {last:.1f}%', 11.5, EMBER, MONO)
    for i in (0, len(rows) // 2, len(rows) - 1):
        d = rows[i]['day']; body += T(X(i), h - 18, f'{MON[int(d[5:7]) - 1]} {int(d[8:])}', 11, FAINT, MONO, 'middle')
    save('nightly-accuracy', w, h, body, 'Live classifier accuracy by night')


def nightly_f1():
    pc = D['offline_metrics']['per_class']; rows = sorted(pc.items(), key=lambda kv: -kv[1]['f1-score'])
    w = 1100; L, R, Tp = 230, 120, 92; rh = 28; h = Tp + len(rows) * rh + 34; iw = w - L - R
    body = head('Precision, recall and F1 by vehicle component', 'held-out test set · bge-small embeddings + logistic regression · dot = precision, ring = recall, bar = F1')
    sx = lambda v: L + iw * (max(0.5, v) - 0.5) / 0.5
    for v in (0.5, 0.75, 1):
        body += f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{Tp - 8}" y2="{Tp + len(rows) * rh - 6}" stroke="{LINE}"/>' + T(sx(v), h - 10, f'{v:.2f}', 10.5, FAINT, MONO, 'middle')
    for i, (k, v) in enumerate(rows):
        y = Tp + i * rh
        body += T(L - 12, y + 15, k, 13, INK, SERIF, 'end')
        body += f'<rect x="{L}" y="{y + 4}" width="{sx(v["f1-score"]) - L:.1f}" height="{rh - 14}" rx="3" fill="{EMBER_SOFT}"/>'
        body += f'<line x1="{sx(v["precision"]):.1f}" x2="{sx(v["recall"]):.1f}" y1="{y + 11}" y2="{y + 11}" stroke="{SOFT}"/>'
        body += f'<circle cx="{sx(v["precision"]):.1f}" cy="{y + 11}" r="4.5" fill="{EMBER}"/>'
        body += f'<circle cx="{sx(v["recall"]):.1f}" cy="{y + 11}" r="4.5" fill="{PAPER}" stroke="{SLATE}" stroke-width="1.8"/>'
        body += T(w - R + 14, y + 15, f'F1 {v["f1-score"]:.2f}', 11, SOFT, MONO)
    save('nightly-f1', w, h, body, 'Precision, recall and F1 by component')


# ===================================================================== comply.

def comply_states():
    """The testing case state machine, transcribed from src/domain/cases.ts in complyDOT."""
    w, h = 1180, 470
    body = head('Every selected employee becomes a case with a fixed set of moves', 'transcribed from the product’s transition table · outlined = final state')
    N = {'selected': (100, 200, 'To schedule'), 'site_confirmed': (300, 200, 'Site booked'), 'notified': (500, 200, 'Notified'),
         'collected': (710, 200, 'Collected'), 'awaiting_mro': (910, 200, 'With MRO'), 'result_recorded': (1080, 310, 'Result in'),
         'employer_review': (610, 350, 'DER review'), 'excused': (340, 400, 'Excused'), 'cancelled': (890, 400, 'Cancelled')}
    E = [('selected', 'site_confirmed'), ('site_confirmed', 'notified'), ('notified', 'collected'), ('collected', 'awaiting_mro'),
         ('awaiting_mro', 'result_recorded'), ('collected', 'result_recorded'), ('notified', 'employer_review'),
         ('employer_review', 'result_recorded'), ('employer_review', 'excused'), ('selected', 'excused'), ('site_confirmed', 'excused'),
         ('selected', 'cancelled'), ('site_confirmed', 'cancelled'), ('collected', 'cancelled'), ('awaiting_mro', 'cancelled')]
    rw, rh = 128, 40

    def edge(a, b):
        (x1, y1, _), (x2, y2, _) = N[a], N[b]
        ang = math.atan2(y2 - y1, x2 - x1)

        def clip(x, y, s):
            dx, dy = math.cos(ang) * s, math.sin(ang) * s
            t = min((rw / 2 + 2) / abs(dx) if dx else 9e9, (rh / 2 + 2) / abs(dy) if dy else 9e9)
            return x + dx * t, y + dy * t
        sx, sy = clip(x1, y1, 1); ex, ey = clip(x2, y2, -1)
        c = BAD if b in ('cancelled', 'excused') else (EMBER if b == 'employer_review' else SOFT)
        da = ' stroke-dasharray="4 4"' if b in ('cancelled', 'excused') else ''
        return f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{c}" stroke-width="1.3"{da}/>' + arrowhead(ex, ey, ang, c)
    body += ''.join(edge(a, b) for a, b in E)
    for k, (x, y, lab) in N.items():
        final = k in ('result_recorded', 'excused', 'cancelled')
        fill = OK_SOFT if k == 'result_recorded' else (BAD_SOFT if k in ('excused', 'cancelled') else (EMBER_SOFT if k == 'employer_review' else '#fff'))
        stroke = OK if k == 'result_recorded' else (BAD if k in ('excused', 'cancelled') else (EMBER if k == 'employer_review' else SLATE))
        if final: body += f'<rect x="{x - rw / 2 - 5}" y="{y - rh / 2 - 5}" width="{rw + 10}" height="{rh + 10}" rx="25" fill="none" stroke="{stroke}"/>'
        body += f'<rect x="{x - rw / 2}" y="{y - rh / 2}" width="{rw}" height="{rh}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'
        body += T(x, y + 5, lab, 13.5, INK, SERIF, 'middle')
    body += T(500, 150, '14 CFR 120.109(b)(8)', 10, FAINT, MONO, 'middle') + T(500, 164, 'no rescheduling once notified', 10.5, EMBER, MONO, 'middle')
    body += T(910, 164, 'drug tests only', 10.5, FAINT, MONO, 'middle')
    body += T(610, 396, 'refusals are the DER’s call', 10.5, EMBER, MONO, 'middle')
    body += T(40, h - 18, 'excused and cancelled need a written reason · only Result in counts toward the annual rate', 11, SOFT, MONO)
    save('comply-states', w, h, body, 'Testing case state machine')


def comply_draw():
    w, h = 1180, 420
    body = head('A draw anyone can re-run and get the same names', 'partial Fisher–Yates over the sorted pool · random numbers from a seeded xoshiro128** stream · pool and seed illustrative')
    pool = ['Ames', 'Brooks', 'Chen', 'Diaz', 'Evans', 'Fox', 'Gray', 'Hale']
    rng = random.Random(41); arr = pool[:]; steps = []
    for i in range(3):
        j = rng.randrange(i, len(arr)); arr[i], arr[j] = arr[j], arr[i]; steps.append((i, j, arr[:]))
    cw, chh, x0 = 104, 34, 230

    def row(y, items, label, hi=(), sel=0, sub=''):
        out = T(x0 - 16, y + 18, label, 12.5, INK, SERIF, 'end')
        if sub: out += T(x0 - 16, y + 33, sub, 10, FAINT, MONO, 'end')
        for k, nm in enumerate(items):
            x = x0 + k * (cw + 6)
            fill = EMBER_SOFT if k < sel else '#fff'; stroke = SLATE if k in hi else (EMBER if k < sel else LINE)
            out += f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="{1.8 if k in hi else 1.1}"/>' + T(x + cw / 2, y + 22, nm, 13, INK, MONO, 'middle')
        return out
    body += row(96, pool, 'sorted pool', sub='by employee ID')
    for n, (i, j, a) in enumerate(steps):
        y = 96 + (n + 1) * 66
        body += row(y, a, f'step {n + 1}', hi={i, j}, sel=i + 1, sub=f'r = {j} · swap {i}↔{j}')
        if i != j:
            xa, xb = x0 + i * (cw + 6) + cw / 2, x0 + j * (cw + 6) + cw / 2
            body += f'<path d="M{xa:.1f},{y - 3} Q{(xa + xb) / 2:.1f},{y - 24} {xb:.1f},{y - 3}" fill="none" stroke="{SLATE}" stroke-width="1.3"/>'
    body += T(x0, h - 30, 'shaded = the selection · the seed is stored with the draw, so re-running it reproduces exactly these names', 11.5, SOFT, MONO)
    save('comply-draw', w, h, body, 'Reproducible draw with a partial Fisher–Yates shuffle')


# ===================================================================== Lakehouse

def lakehouse_config():
    w, h = 1180, 470
    body = head('Adding a table is a config entry, not new code', 'metadata-driven ingestion · illustrative config: names and keys are made up, the pattern is real')
    code = ['{', '  "source": "lucity",', '  "table": "work_orders",', '  "load": "incremental",', '  "watermark": "modified_at",',
            '  "keys": ["work_order_id"],', '  "silver": {', '    "dedupe_on": ["work_order_id"],', '    "schema": "work_orders.json"',
            '  },', '  "gold": { "scd": 2,', '            "track": ["status", "asset_id"] }', '}']
    cx, cy, cwid = 40, 92, 440
    body += f'<rect x="{cx}" y="{cy}" width="{cwid}" height="{len(code) * 22 + 34}" rx="8" fill="{CODE_BG}"/>'
    body += T(cx + 16, cy + 22, 'pipelines/lucity/work_orders.json', 10.5, '#bfa79c', MONO)
    for i, ln in enumerate(code):
        y = cy + 50 + i * 22
        if ':' in ln and '"' in ln.split(':')[0]:
            k, v = ln.split(':', 1)
            body += f'<text x="{cx + 16}" y="{y}" font-family="{MONO}" font-size="12.5" xml:space="preserve"><tspan fill="#f0a77a">{escape(k)}</tspan><tspan fill="{CODE_INK}">:{escape(v)}</tspan></text>'
        else:
            body += f'<text x="{cx + 16}" y="{y}" font-family="{MONO}" font-size="12.5" fill="{CODE_INK}" xml:space="preserve">{escape(ln)}</text>'
    steps = [('Data Factory reads the config', 'one generic pipeline for every SQL Server table', SLATE, SERIF),
             ('bronze.lucity_work_orders', 'rows newer than modified_at, appended as Delta', FAINT, MONO),
             ('silver.work_orders', 'typed, deduplicated on work_order_id', SLATE, MONO),
             ('gold.dim_work_order', 'SCD 2 on status and asset_id', EMBER, MONO)]
    sx = 560
    for i, (t, s, c, f) in enumerate(steps):
        y = 104 + i * 86
        body += f'<rect x="{sx}" y="{y}" width="580" height="58" rx="6" fill="#fff" stroke="{c}" stroke-width="1.3"/><rect x="{sx}" y="{y}" width="6" height="58" fill="{c}"/>'
        body += T(sx + 22, y + 25, t, 14, INK, f) + T(sx + 22, y + 44, s, 11, SOFT, MONO)
        if i: body += f'<line x1="{sx + 40}" y1="{y - 28}" x2="{sx + 40}" y2="{y - 3}" stroke="{SOFT}"/>' + arrowhead(sx + 40, y - 2, math.pi / 2, SOFT)
    body += curve(cx + cwid, cy + 140, sx - 2, 133, EMBER, 1.5)
    body += T(sx, h - 22, 'REST APIs don’t fit one template, so they get notebooks for each API’s auth and pagination', 11, SOFT, MONO)
    save('lakehouse-config', w, h, body, 'Metadata-driven ingestion')


def lakehouse_scd2():
    w, h = 1180, 400; L, R = 210, 60
    body = head('SCD Type 2 keeps every version on a timeline', 'illustration with made-up rows · a meter changes size; a reading joins to the version that was true at the time')
    t0, t1 = 2024.0, 2027.0; X = lambda t: L + (w - L - R) * (t - t0) / (t1 - t0)
    for yr in range(2024, 2028):
        body += f'<line x1="{X(yr):.1f}" y1="96" x2="{X(yr):.1f}" y2="{h - 64}" stroke="{LINE}"/>' + T(X(yr), h - 44, str(yr), 11, FAINT, MONO, 'middle')
    rows = [('M-2207 · key 1041', 2024.17, 2026.29, 'size 5/8 in · valid_to 2026-04-14', False),
            ('M-2207 · key 2310', 2026.29, 2027.0, 'size 1 in · is_current', True),
            ('M-3318 · key 1042', 2025.03, 2027.0, 'size 3/4 in · is_current', True)]
    for i, (lab, a, b, txt, cur) in enumerate(rows):
        y = 116 + i * 56
        body += T(L - 16, y + 20, lab, 12, INK, MONO, 'end')
        body += f'<rect x="{X(a):.1f}" y="{y}" width="{X(b) - X(a):.1f}" height="30" rx="5" fill="{EMBER_SOFT if cur else "#efe5e0"}" stroke="{EMBER if cur else FAINT}"/>'
        body += T(X(a) + 12, y + 20, txt, 11.5, INK if cur else SOFT, MONO)
    for t, lab, r in [(2025.6, 'reading, Aug 2025', 0), (2026.7, 'reading, Sep 2026', 1)]:
        yy = 116 + r * 56 + 15
        body += f'<line x1="{X(t):.1f}" y1="{h - 74}" x2="{X(t):.1f}" y2="{yy + 15:.1f}" stroke="{SLATE}" stroke-dasharray="3 3"/><circle cx="{X(t):.1f}" cy="{yy:.1f}" r="5" fill="{SLATE}"/>' + T(X(t), h - 58, lab, 10.5, SLATE, MONO, 'middle')
    body += T(40, h - 14, 'type 1 overwrites in place, for corrections · type 2 adds a row, so history stays answerable', 11, SOFT, MONO)
    save('lakehouse-scd2', w, h, body, 'SCD Type 2 versions on a timeline')


# ===================================================================== FAA randomizer

def faa_funnel():
    w, h = 1180, 430
    body = head('Who can be selected, and how many each quarter', 'how the rules narrow the list and set the quarterly count · numbers illustrative, not company data')
    steps = [('All employees', 'master list', 1400), ('Safety-sensitive', 'pilots, mechanics, dispatchers…', 900), ('Active this quarter', 'leave and terminations removed', 820)]
    fx, fw = 40, 520
    for i, (t, s, n) in enumerate(steps):
        y = 96 + i * 72; ww = fw * n / steps[0][2]; x = fx + (fw - ww) / 2
        body += f'<rect x="{x:.1f}" y="{y}" width="{ww:.1f}" height="56" rx="6" fill="{SLATE_SOFT if i < 2 else EMBER_SOFT}" stroke="{SLATE if i < 2 else EMBER}"/>'
        body += T(fx + fw / 2, y + 25, f'{t} · {n:,}', 14, INK, SERIF, 'middle') + T(fx + fw / 2, y + 43, s, 10.5, SOFT, MONO, 'middle')
    body += T(fx + fw / 2, 330, 'eligible pool', 11, EMBER, MONO, 'middle', ls=1.4, upper=True)
    bx, by, bw_, bh_ = 640, 110, 70, 220
    q = [(52, 0), (52, 4), (52, 2), (52, 5)]; mx = 64
    body += T(bx, 100, 'drug tests per quarter', 11, EMBER, MONO, ls=1.4, upper=True)
    for i, (base, roll) in enumerate(q):
        x = bx + 10 + i * (bw_ + 40); yb = by + bh_; hb = bh_ * base / mx; hr = bh_ * roll / mx
        body += f'<rect x="{x}" y="{yb - hb:.1f}" width="{bw_}" height="{hb:.1f}" fill="{EMBER}"/>'
        if roll: body += f'<rect x="{x}" y="{yb - hb - hr - 2:.1f}" width="{bw_}" height="{hr:.1f}" fill="{GOLD}"/>'
        body += T(x + bw_ / 2, yb - hb - hr - 10, f'{base + roll}', 12, INK, MONO, 'middle') + T(x + bw_ / 2, yb + 20, f'Q{i + 1}', 11, FAINT, MONO, 'middle')
    body += f'<line x1="{bx}" y1="{by + bh_}" x2="{bx + 450}" y2="{by + bh_}" stroke="{INK}"/>'
    body += f'<rect x="{bx}" y="{h - 70}" width="10" height="10" fill="{EMBER}"/>' + T(bx + 16, h - 61, 'quarter share of the annual target', 11, SOFT, MONO)
    body += f'<rect x="{bx}" y="{h - 50}" width="10" height="10" fill="{GOLD}"/>' + T(bx + 16, h - 41, 'rollover: selected last quarter, not completed', 11, SOFT, MONO)
    body += T(40, h - 16, 'annual target = rate × average pool size · e.g. 25% × 820 ≈ 205 drug tests a year ≈ 52 a quarter', 11, SOFT, MONO)
    save('faa-funnel', w, h, body, 'Eligibility funnel and quarterly targets')


# ===================================================================== Cargo After COVID (real BTS data)

def cargo_trend():
    rows = json.load(open(os.path.join(HERE, 'bts-air-cargo.json')))
    ki = 'u_s_air_carrier_cargo_millions_of_revenue_ton_miles_international'; kd = 'u_s_air_carrier_cargo_millions_of_revenue_ton_miles_domestic'
    rows = [r for r in rows if r.get(ki) and r.get(kd)]
    pts = [(int(r['date'][:4]) + (int(r['date'][5:7]) - 1) / 12, float(r[ki]) / 1e6, float(r[kd]) / 1e6) for r in rows]

    def roll(idx):
        return [sum(p[idx] for p in pts[max(0, i - 11):i + 1]) / len(pts[max(0, i - 11):i + 1]) for i in range(len(pts))]
    ri, rd = roll(1), roll(2)
    w, h = 1180, 440; L, R, Tp, B = 80, 160, 96, 62; iw, ih = w - L - R, h - Tp - B
    t0, t1 = pts[0][0], pts[-1][0] + 1 / 12; tk = nice(max(max(p[1], p[2]) for p in pts)); top = tk[-1]
    X = lambda t: L + iw * (t - t0) / (t1 - t0); Y = lambda v: Tp + ih - ih * v / top
    last = rows[-1]['date'][:7]
    body = head('U.S. air carrier cargo, 2003 to today', f'millions of revenue ton-miles per month · Bureau of Transportation Statistics · through {last}')
    body += f'<rect x="{X(2020.17):.1f}" y="{Tp}" width="{X(2022.0) - X(2020.17):.1f}" height="{ih}" fill="{EMBER_SOFT}"/>' + T(X(2021.08), Tp + 16, 'covid', 10.5, EMBER, MONO, 'middle', ls=1.4, upper=True)
    for v in tk:
        body += f'<line x1="{L}" x2="{L + iw}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"/>' + T(L - 10, Y(v) + 4, f'{v:,.0f}', 11, FAINT, MONO, 'end')
    for yr in range(2004, int(t1) + 1, 4): body += T(X(yr), Tp + ih + 20, str(yr), 11, FAINT, MONO, 'middle')
    for idx, col, r in ((1, SLATE, ri), (2, EMBER, rd)):
        body += '<polyline points="' + ' '.join(f'{X(p[0]):.1f},{Y(p[idx]):.1f}' for p in pts) + f'" fill="none" stroke="{col}" stroke-width="1" opacity="0.3"/>'
        body += '<polyline points="' + ' '.join(f'{X(p[0]):.1f},{Y(v):.1f}' for p, v in zip(pts, r)) + f'" fill="none" stroke="{col}" stroke-width="2.4" stroke-linejoin="round"/>'
        body += T(L + iw + 10, Y(r[-1]) + 4, 'international' if idx == 1 else 'domestic', 12, col, MONO)
    body += T(40, h - 12, 'thin lines: monthly · thick lines: 12-month average · published BTS series, shown as context for the app', 10.5, FAINT, MONO)
    save('cargo-trend', w, h, body, 'U.S. air cargo ton-miles, 2003 to today')


# ===================================================================== Nurse sentiment

def nurse_walk():
    w, h = 1180, 470
    body = head('One post’s path through the pipeline', 'made-up example post and scores · the steps are the pipeline’s')
    post = 'Third night shift in a row and I’m exhausted. My preceptor is great but I cried in the break room again. Is it supposed to feel like this?'
    y = 92
    body += T(40, y + 16, 'post', 10.5, EMBER, MONO, ls=1.4, upper=True)
    body += f'<rect x="150" y="{y - 6}" width="990" height="62" rx="6" fill="#fff" stroke="{LINE}"/>'
    for i, ln in enumerate(textwrap.wrap('“' + post + '”', 118)):
        body += T(166, y + 18 + i * 20, ln, 14, INK, SERIF, italic=True)
    y += 92
    body += T(40, y + 12, 'clean', 10.5, EMBER, MONO, ls=1.4, upper=True)
    body += T(150, y + 12, 'third night shift row exhausted preceptor great cried break room supposed feel', 13, SOFT, MONO)
    body += T(150, y + 32, 'lowercase · punctuation and stop words removed', 10.5, FAINT, MONO)
    y += 64
    body += T(40, y + 17, 'lemmatize', 10.5, EMBER, MONO, ls=1.4, upper=True)
    toks = [('third', None), ('night', None), ('shift', 'work'), ('row', None), ('exhaust', 'stress'), ('preceptor', 'work'), ('great', 'well'),
            ('cry', 'dep'), ('break', 'work'), ('room', None), ('suppose', None), ('feel', None)]
    col = {'stress': (BAD, BAD_SOFT), 'dep': (SLATE, SLATE_SOFT), 'work': (GOLD, '#f3ead2'), 'well': (OK, OK_SOFT), None: (LINE, '#fff')}
    x = 150
    for t, c in toks:
        tw = len(t) * 8.2 + 20; s, f = col[c]
        body += f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="26" rx="13" fill="{f}" stroke="{s}"/>' + T(x + tw / 2, y + 17.5, t, 12.5, INK, MONO, 'middle'); x += tw + 8
    body += T(150, y + 46, 'exhausted → exhaust, cried → cry: forms of a word count as one', 10.5, FAINT, MONO)
    y += 86
    body += T(40, y + 14, 'classify', 10.5, EMBER, MONO, ls=1.4, upper=True)
    for i, (k, v, c) in enumerate([('Stress', .78, BAD), ('Depression', .46, SLATE), ('Workplace', .61, GOLD), ('Wellbeing', .12, OK)]):
        bx = 150 + i * 250
        body += T(bx, y + 12, k, 13, INK) + f'<rect x="{bx}" y="{y + 20}" width="200" height="10" rx="5" fill="#efe5e0"/><rect x="{bx}" y="{y + 20}" width="{200 * v:.0f}" height="10" rx="5" fill="{c}"/>'
    body += T(150, y + 50, 'posts are then counted by theme over time in the R Shiny dashboard', 10.5, FAINT, MONO)
    save('nurse-walk', w, h, body, 'One post through the NLP pipeline')


# ===================================================================== NKU chatbot

def chatbot_sample():
    w, h = 1180, 500
    body = head('Anatomy of one training sample', 'the question and answer are the real example from our poster; the layout is the instruction format we trained on')
    cx, cy, cwid = 40, 92, 700
    lines = [('instruction', 'Answer the question about Northern Kentucky University.'), ('input', 'What is the mission of NKU?'),
             ('output', 'As a public comprehensive university located in a major metropolitan area, NKU delivers innovative, student-centered education and engages in impactful, scholarly, and creative endeavors. These efforts empower graduates to have fulfilling careers and meaningful lives while contributing to the economic, civic, and social vitality of the region.')]
    body += f'<rect x="{cx}" y="{cy}" width="{cwid}" height="350" rx="8" fill="{CODE_BG}"/>'
    y = cy + 30; body += T(cx + 18, y, '{', 13, CODE_INK, MONO); y += 24; ys = {}
    for k, v in lines:
        ys[k] = y; body += T(cx + 34, y, f'"{k}":', 13, '#f0a77a', MONO); y += 22
        for ln in textwrap.wrap('"' + v + '"', 74): body += T(cx + 52, y, ln, 12.5, CODE_INK, MONO); y += 19
        y += 10
    body += T(cx + 18, y, '}', 13, CODE_INK, MONO)
    notes = [('instruction', 'the task, the same for every NKU sample'), ('input', 'a question someone might really ask'),
             ('output', 'the answer, formatted with GPT-4o from the page text and reviewed by hand')]
    for k, t in notes:
        yy = ys[k] - 4
        body += f'<line x1="{cx + cwid}" y1="{yy}" x2="{cx + cwid + 34}" y2="{yy}" stroke="{EMBER}"/><circle cx="{cx + cwid}" cy="{yy}" r="3" fill="{EMBER}"/>'
        body += T(cx + cwid + 44, yy - 4, k, 10.5, EMBER, MONO, ls=1.4, upper=True)
        for i, ln in enumerate(textwrap.wrap(t, 42)): body += T(cx + cwid + 44, yy + 14 + i * 17, ln, 13, SOFT)
    body += T(40, h - 24, 'nku.edu pages → text (Jina reader) → 1,611 samples like this one → fine-tune GPT-2 (1.5B) → +10–15% vs. ChatGPT on 10 NKU questions', 11, SOFT, MONO)
    save('chatbot-sample', w, h, body, 'Anatomy of a training sample')


# ===================================================================== Clinical study map

def clinical_world():
    polys = json.load(open(os.path.join(HERE, 'world-land-110m.json')))
    w, h = 1180, 560; L, Tp, iw, ih = 40, 80, 1100, 440; lat0, lat1 = -58, 80
    X = lambda lon: L + iw * (lon + 180) / 360; Y = lambda lat: Tp + ih * (lat1 - lat) / (lat1 - lat0)
    body = head('One map instead of a spreadsheet per proposal', 'what the R Shiny map shows: study sites by country, sized by number of studies · sites and counts illustrative, not Medpace data')
    for p in polys:
        if all(lat < lat0 for _, lat in p): continue
        body += '<path d="M' + ' L'.join(f'{X(lon):.1f},{Y(max(lat0 - 2, lat)):.1f}' for lon, lat in p) + ' Z" fill="#ece0d9" stroke="#d8c8c0" stroke-width="0.6"/>'
    sites = [('United States', -97, 39, 34), ('Canada', -96, 57, 9), ('Mexico', -102, 23, 6), ('Brazil', -51, -12, 8), ('Argentina', -64, -35, 5),
             ('United Kingdom', -2, 53, 11), ('Germany', 10, 51, 14), ('Poland', 19, 52, 10), ('Spain', -4, 40, 8), ('Italy', 12, 43, 7),
             ('South Africa', 24, -29, 5), ('India', 78, 22, 7), ('China', 104, 35, 9), ('South Korea', 128, 36.5, 6), ('Japan', 138, 37, 6), ('Australia', 134, -25, 8)]
    mx = max(s[3] for s in sites)
    for nm, lon, lat, n in sorted(sites, key=lambda s: -s[3]):
        body += f'<circle cx="{X(lon):.1f}" cy="{Y(lat):.1f}" r="{4 + 14 * math.sqrt(n / mx):.1f}" fill="{EMBER}" fill-opacity="0.55" stroke="{EMBER}"/>'
    labels = {'United States': (-150, 30, 'United States · 34'), 'Canada': (-150, 62, 'Canada · 9'), 'Germany': (-40, 68, 'Europe: Germany 14 · UK 11 · Poland 10'),
              'China': (112, 52, 'China · 9'), 'Brazil': (-38, -20, 'Brazil · 8'), 'Australia': (146, -36, 'Australia · 8')}
    for nm, lon, lat, n in sites:
        if nm in labels:
            lx, ly, txt = labels[nm]
            body += f'<line x1="{X(lon):.1f}" y1="{Y(lat):.1f}" x2="{X(lx):.1f}" y2="{Y(ly) - 4:.1f}" stroke="{FAINT}" stroke-width="0.8"/>' + T(X(lx), Y(ly) - 8, txt, 10.5, INK, MONO, 'middle')
    body += f'<rect x="44" y="{h - 108}" width="250" height="62" rx="6" fill="{PAPER}" stroke="{LINE}"/>'
    body += T(60, h - 84, 'filters by study attributes', 11, SOFT, MONO) + T(60, h - 64, 'hover a site for its studies', 11, SOFT, MONO)
    save('clinical-world', w, h, body, 'World map of clinical study sites (illustrative)')


# ===================================================================== Motus

def motus_tree():
    w, h = 1180, 470
    body = head('What “profitable” breaks down into', 'KPI tree behind the profitability scorecards and the regional dashboard')
    nodes = {'gp': (590, 125, 'Gross profit', 'per load, customer, region'),
             'rev': (330, 235, 'Revenue', 'what customers pay'), 'margin': (590, 235, 'Margin %', 'gross profit ÷ revenue'), 'cost': (850, 235, 'Carrier cost', 'what carriers are paid'),
             'cust': (170, 365, 'By customer', 'profitability scorecards'), 'reg': (440, 365, 'By region', '4 regions · 49 states'),
             'lane': (740, 365, 'By carrier', 'top vs. lower-ranked'), 'fc': (1010, 365, 'Forecast', 'revenue by carrier')}
    E = [('gp', 'rev'), ('gp', 'cost'), ('gp', 'margin'), ('rev', 'cust'), ('rev', 'reg'), ('margin', 'reg'), ('cost', 'lane'), ('rev', 'fc'), ('cost', 'fc')]
    bw, bh = 200, 58
    for a, b in E:
        (x1, y1, *_), (x2, y2, *_) = nodes[a], nodes[b]
        body += f'<path d="M{x1},{y1 + bh / 2} C{x1},{(y1 + y2) / 2 + 10} {x2},{(y1 + y2) / 2 - 10} {x2},{y2 - bh / 2 - 2}" fill="none" stroke="{SOFT}" stroke-width="1.2"/>' + arrowhead(x2, y2 - bh / 2 - 1, math.pi / 2, SOFT)
    for k, (x, y, t, s) in nodes.items():
        top = k == 'gp'; leaf = k in ('cust', 'reg', 'lane', 'fc')
        fill = EMBER_SOFT if top else (SLATE_SOFT if leaf else '#fff'); st = EMBER if top else (SLATE if leaf else LINE)
        body += f'<rect x="{x - bw / 2}" y="{y - bh / 2}" width="{bw}" height="{bh}" rx="{29 if top else 6}" fill="{fill}" stroke="{st}" stroke-width="1.3"/>'
        body += T(x, y - 2, t, 14.5, INK, SERIF, 'middle') + T(x, y + 16, s, 10.5, SOFT, MONO, 'middle')
    body += T(40, h - 20, 'each leaf is a view in Tableau Cloud on data from Turvo · together they contributed to a 15% rise in profitability', 11, SOFT, MONO)
    save('motus-tree', w, h, body, 'Profitability KPI tree')


def motus_forecast():
    w, h = 1180, 380; L, R, Tp, B = 70, 40, 92, 52; iw, ih = w - L - R, h - Tp - B
    body = head('Emissions: where they were, and where they were heading', 'shape of the CO2 dashboard’s trend and forecast view · values illustrative, not company data')
    rnd = random.Random(7); hist = []; v = 100
    for m in range(24):
        v = v * (1 + rnd.uniform(-0.03, 0.035)) + 4 * math.sin(m / 1.9); hist.append(v)
    fc = []; v2 = hist[-1]
    for m in range(9):
        v2 *= 0.988; fc.append(v2)
    allv = hist + fc; lo, hi = 70, 130
    X = lambda i: L + iw * i / (len(allv) - 1); Y = lambda v: Tp + ih - ih * (v - lo) / (hi - lo)
    for v in (80, 100, 120): body += f'<line x1="{L}" x2="{L + iw}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"/>' + T(L - 10, Y(v) + 4, f'{v}', 11, FAINT, MONO, 'end')
    n0 = len(hist) - 1
    up = [Y(v * (1 + 0.012 * (i + 1))) for i, v in enumerate(fc)]; dn = [Y(v * (1 - 0.012 * (i + 1))) for i, v in enumerate(fc)]
    d = f'M{X(n0):.1f},{Y(hist[-1]):.1f} ' + ' '.join(f'L{X(n0 + 1 + i):.1f},{up[i]:.1f}' for i in range(len(fc))) + ' ' + ' '.join(f'L{X(n0 + 1 + i):.1f},{dn[i]:.1f}' for i in reversed(range(len(fc)))) + ' Z'
    body += f'<path d="{d}" fill="{EMBER}" opacity="0.16"/>'
    body += '<polyline points="' + ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, v in enumerate(hist)) + f'" fill="none" stroke="{INK}" stroke-width="2"/>'
    body += f'<polyline points="{X(n0):.1f},{Y(hist[-1]):.1f} ' + ' '.join(f'{X(n0 + 1 + i):.1f},{Y(v):.1f}' for i, v in enumerate(fc)) + f'" fill="none" stroke="{EMBER}" stroke-width="2" stroke-dasharray="6 5"/>'
    body += f'<line x1="{X(n0):.1f}" y1="{Tp}" x2="{X(n0):.1f}" y2="{Tp + ih}" stroke="{FAINT}" stroke-dasharray="2 4"/>' + T(X(n0) - 8, Tp + 14, 'actual', 11, INK, MONO, 'end') + T(X(n0) + 8, Tp + 14, 'forecast · with range', 11, EMBER, MONO)
    body += T(40, h - 18, 'index, first month = 100 · the real dashboard contributed to a 12.4% overall drop in emissions', 11, SOFT, MONO)
    save('motus-forecast', w, h, body, 'Emissions trend and forecast (illustrative)')


if __name__ == '__main__':
    for f in os.listdir(OUT):
        if f.endswith('.svg') and not f.startswith('vidvo-'): os.remove(os.path.join(OUT, f))
    for fn in (nightly_lineage, nightly_windows, nightly_requests, nightly_accuracy, nightly_f1, comply_states, comply_draw,
               lakehouse_config, lakehouse_scd2, faa_funnel, cargo_trend, nurse_walk, chatbot_sample, clinical_world, motus_tree):
        fn()
    print('wrote', sorted(os.listdir(OUT)))
