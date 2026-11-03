"""Draw every project figure as SVG into public/fig/.

Diagrams are drawn from the facts in each project page; the Nightly 311 charts use real data
from the pipeline's published data.json (snapshot in scripts/nightly-snapshot.json).
Figures carry their own light "paper" background, like printed figures, so they read the same
in night and day.  Re-run with:  python3 scripts/figures.py
"""
import json, math, os, textwrap
from html import escape

OUT = os.path.join(os.path.dirname(__file__), '..', 'public', 'fig')
os.makedirs(OUT, exist_ok=True)

PAPER, INK, SOFT, FAINT, LINE = '#fbf6f3', '#2b1d1d', '#6a5651', '#9a8580', '#e3d6d0'
EMBER, EMBER_SOFT, SLATE, SLATE_SOFT, OK, BAD = '#c55e2c', '#f6e1d4', '#3f5d78', '#e3eaf1', '#2f7a4f', '#b23a32'
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f'<rect width="{w}" height="{h}" fill="{PAPER}"/>{body}</svg>')


def text(x, y, s, size=13, fill=INK, font=SERIF, anchor='start', weight='400', ls=0, upper=False):
    s = s.upper() if upper else s
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" letter-spacing="{ls}">{escape(s)}</text>')


def wrap(s, width):
    return textwrap.wrap(s, width) or ['']


def box_lines(w, title, sub):
    return wrap(title, max(8, int((w - 18) / 7.4))), (wrap(sub, max(8, int((w - 18) / 6.5))) if sub else [])


def box_height(w, title, sub):
    a, b = box_lines(w, title, sub)
    return len(a) * 17 + len(b) * 14 + 22


def box(x, y, w, h, title, sub='', tone='plain'):
    fill, stroke = {'plain': ('#fff', LINE), 'ember': (EMBER_SOFT, EMBER), 'slate': (SLATE_SOFT, SLATE),
                    'bad': ('#f7e2df', BAD), 'ok': ('#e1efe6', OK)}[tone]
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
    lines, subl = box_lines(w, title, sub)
    total = len(lines) * 17 + len(subl) * 14
    ty = y + h / 2 - total / 2 + 13
    for ln in lines:
        out += text(x + w / 2, ty, ln, 13.5, INK, SERIF, 'middle'); ty += 17
    for ln in subl:
        out += text(x + w / 2, ty, ln, 10.5, SOFT, MONO, 'middle'); ty += 14
    return out


def arrow(x1, y1, x2, y2, color=SOFT, dash=False):
    d = ' stroke-dasharray="4 4"' if dash else ''
    ang = math.atan2(y2 - y1, x2 - x1); a = 7
    p1 = (x2 - a * math.cos(ang - 0.45), y2 - a * math.sin(ang - 0.45))
    p2 = (x2 - a * math.cos(ang + 0.45), y2 - a * math.sin(ang + 0.45))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.3"{d}/>'
            f'<path d="M{x2:.1f},{y2:.1f} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{color}"/>')


def pipeline(name, title, stages, notes=(), w=1100, bh=58, gap=14, colw=None, caption=''):
    """Columns of boxes, left to right. Each stage: (label, [(title, sub, tone), ...]).
    Every box links to the next column's boxes through a single bus, so the eye reads the flow."""
    n = len(stages); pad = 40; colgap = 38
    colw = colw or (w - 2 * pad - colgap * (n - 1)) / n
    maxbox = max(len(s[1]) for s in stages)
    bh = max(bh, max(box_height(colw, b[0], b[1]) for st in stages for b in st[1]))
    top = 92; inner = maxbox * bh + (maxbox - 1) * gap
    h = top + inner + 40 + (len(notes) * 22 + 20 if notes else 0)
    body = text(pad, 40, title, 20, INK, SERIF)
    if caption: body += text(pad, 62, caption, 11, FAINT, MONO, ls=0.5)
    centers = []
    for i, (label, boxes) in enumerate(stages):
        x = pad + i * (colw + colgap)
        body += text(x, top - 12, label, 10.5, EMBER, MONO, ls=1.6, upper=True)
        k = len(boxes); col_h = k * bh + (k - 1) * gap; y0 = top + (inner - col_h) / 2
        ys = []
        for j, b in enumerate(boxes):
            y = y0 + j * (bh + gap); body += box(x, y, colw, bh, *b); ys.append(y + bh / 2)
        centers.append((x, ys))
    for i in range(n - 1):
        x1 = centers[i][0] + colw; x2 = centers[i + 1][0]; xm = (x1 + x2) / 2
        a, b = centers[i][1], centers[i + 1][1]
        for y in a: body += f'<line x1="{x1}" y1="{y:.1f}" x2="{xm}" y2="{y:.1f}" stroke="{SOFT}" stroke-width="1.3"/>'
        lo, hi = min(a + b), max(a + b)
        if hi > lo: body += f'<line x1="{xm}" y1="{lo:.1f}" x2="{xm}" y2="{hi:.1f}" stroke="{SOFT}" stroke-width="1.3"/>'
        for y in b: body += arrow(xm, y, x2 - 1, y)
    if notes:
        y = top + inner + 46
        body += f'<line x1="{pad}" y1="{y - 18}" x2="{w - pad}" y2="{y - 18}" stroke="{LINE}"/>'
        for k, v in notes:
            body += text(pad, y, k, 10.5, EMBER, MONO, ls=1.4, upper=True) + text(pad + 150, y, v, 12.5, SOFT, SERIF); y += 22
    open(os.path.join(OUT, name + '.svg'), 'w').write(svg(w, h, body, title))


# ---------------------------------------------------------------- diagrams

pipeline('nightly-architecture', 'Nightly 311: from three public APIs to a dashboard', [
    ('Sources', [('Cincinnati 311', 'Socrata API', 'plain'), ('NOAA weather', 'CDO API · CVG', 'plain'), ('NHTSA complaints', 'flat file', 'plain')]),
    ('Ingest', [('Incremental load', 'watermark − overlap', 'slate'), ('Run log', 'meta.runs, watermarks', 'slate')]),
    ('Bronze', [('raw.*', 'rows exactly as received', 'plain')]),
    ('Silver · dbt', [('Typed, deduplicated', 'one row per request', 'plain'), ('Quarantine', 'bad rows + reason', 'bad'), ('dbt tests', 'stop the run on failure', 'ok')]),
    ('Gold · dbt', [('Star schema', 'fct_service_requests', 'ember'), ('Daily facts', 'requests × weather', 'ember')]),
    ('Serve', [('Classifier', 'bge-small + logistic reg.', 'slate'), ('Dashboard', 'GitHub Pages', 'plain')]),
], notes=[('schedule', 'GitHub Actions, 07:17 UTC every night (about 3 a.m. in Cincinnati)'),
          ('state', 'DuckDB warehouse kept as a gzipped GitHub release asset between runs'),
          ('overlap', '311: 2 days · weather: 7 days · complaints: 3 days, to catch late updates')], w=1180)

pipeline('lakehouse-architecture', 'Medallion lakehouse on Azure Databricks', [
    ('Sources', [('SQL Server', 'CIS · Lucity · LIMS · Antero', 'plain'), ('REST APIs', 'Paycor · KnowBe4 · CivicPlus · ServiceDesk Plus', 'plain')]),
    ('Ingest', [('Config-driven pipelines', 'JSON metadata per table', 'slate'), ('Custom notebooks', 'auth · pagination', 'slate')]),
    ('Bronze', [('Raw Delta tables', 'incremental, append', 'plain')]),
    ('Silver', [('Cleaned & conformed', 'PySpark · Delta Lake', 'plain'), ('Reconciliation', 'SQL checks across SAP & Lucity', 'ok')]),
    ('Gold', [('Dimensions', 'SCD Type 1 and 2', 'ember'), ('Facts', 'for reporting', 'ember')]),
    ('Serve', [('Power BI', 'semantic models', 'plain')]),
], notes=[('orchestration', 'Azure Data Factory, with ADLS Gen2 storage and secrets in Key Vault'),
          ('delivery', 'Azure DevOps CI/CD: pytest, black and pylint run before anything deploys')], w=1180)

pipeline('powerbi-migration', 'Moving a Crystal report to Power BI', [
    ('Legacy', [('Crystal Report', 'logic inside the report', 'plain')]),
    ('Rebuild the data', [('SQL Server view', 'logic moved into SQL', 'slate'), ('Validate', 'against the legacy output', 'ok')]),
    ('Model', [('Semantic model', 'star schema · DAX measures', 'ember')]),
    ('Run', [('On-prem gateway', 'scheduled refresh', 'plain')]),
    ('Share', [('Workspace / app', 'access per department', 'plain')]),
], notes=[('scale', '40–50 reports migrated, plus 10–20 new reports for seven departments'),
          ('result', '20–40 staff hours of manual reporting removed each week')], w=1100)

pipeline('faa-selection', 'One quarter of FAA random testing', [
    ('Employees', [('Master list', 'from SharePoint', 'plain')]),
    ('Eligibility', [('Eligible pool', 'active, safety-sensitive', 'slate')]),
    ('Targets', [('Quarterly target', 'annual rate share + rollover', 'ember')]),
    ('Draw', [('Drug + alcohol', 'random selection', 'plain'), ('Drug only', 'random selection', 'plain')]),
    ('Checks', [('Deduplicate', 'against prior selections', 'ok')]),
    ('Record', [('SharePoint', 'results · history · audit log', 'slate')]),
], notes=[('target', 'quarter = ⌈annual rate × average pool ÷ 4⌉ + tests missed last quarter (rollover)'),
          ('access', 'Microsoft Graph API with Azure AD and OAuth 2.0; Excel exports and KPIs for the program manager')], w=1100)

pipeline('comply-system', 'comply.: one record from HR system to inspector', [
    ('HR system', [('Workday · ADP · UKG', 'Paycor · BambooHR', 'plain')]),
    ('Sync', [('Identity resolution', 'aliases · rehires', 'slate'), ('Coverage rules', 'which jobs are tested', 'slate')]),
    ('Review', [('Approval queue', 'every pool change + HR reason', 'ember')]),
    ('Draw', [('Seeded selection', 'xoshiro128** · Fisher–Yates', 'plain'), ('Re-check', 'anyone can reproduce it', 'ok')]),
    ('Testing', [('Case', 'notice → site → result', 'plain'), ('Alerts', 'gaps before an inspector', 'bad')]),
    ('Audit', [('Inspection packet', 'MIS draft · audit trail', 'slate')]),
], notes=[('rules', '14 CFR Part 120 and 49 CFR Part 40; rate math from FAA AC 120-126A'),
          ('tested', '28 unit tests on selection, rates and compliance logic')], w=1180)

pipeline('chatbot-pipeline', 'From a university website to a fine-tuned model', [
    ('Collect', [('nku.edu pages', 'Python crawler', 'plain')]),
    ('Extract', [('Page text', 'Jina AI reader', 'slate')]),
    ('Curate', [('1,611 samples', 'cleaned by hand', 'ember')]),
    ('Format', [('Instruction / input / output', 'GPT-4o + manual review', 'slate')]),
    ('Train', [('Fine-tune GPT-2', '1.5B parameters', 'ember')]),
    ('Evaluate', [('10 NKU questions', 'vs. ChatGPT: +10–15%', 'ok')]),
], w=1100)

pipeline('nurse-pipeline', 'Reading first-year nurses’ posts at scale', [
    ('Collect', [('Forum posts', 'web scraping', 'plain')]),
    ('Clean', [('Clean text', 'normalize posts', 'slate'), ('Lemmatize', 'NLTK', 'slate')]),
    ('Classify', [('Theme classifier', 'scikit-learn', 'ember')]),
    ('Themes', [('Stress', '', 'plain'), ('Depression', '', 'plain'), ('Workplace', '', 'plain'), ('Wellbeing', '', 'plain')]),
    ('Explore', [('R Shiny dashboard', 'sentiment over time', 'slate')]),
], w=1100, bh=44)

pipeline('cargo-flow', 'Cargo After COVID: two decades of BTS data, explorable', [
    ('Source', [('BTS tables', 'U.S. air cargo, 2003–2025', 'plain')]),
    ('Transform', [('Clean & reshape', 'R', 'slate'), ('KPIs', 'computed in R', 'ember')]),
    ('Explore', [('Filters', 'choose what to compare', 'plain'), ('Trend views', '2003–2025, pre and post COVID', 'plain')]),
    ('Publish', [('R Shiny app', 'shinyapps.io', 'slate')]),
], w=1000)

pipeline('clinical-map', 'Where clinical studies run, in one view', [
    ('Sources', [('Medidata', 'clinical trial data', 'plain'), ('Other study sources', 'internal', 'plain')]),
    ('Integrate', [('SQL · Snowflake', 'join and standardize sites', 'slate')]),
    ('Clean', [('Clean & validate', 'Python · SQL · R', 'ok')]),
    ('Explore', [('R Shiny map', 'studies by country and site', 'ember')]),
    ('Use', [('Proposals', 'research & RFP teams', 'plain')]),
], w=1060)

pipeline('motus-flow', 'Freight data to two decisions', [
    ('Source', [('Turvo', 'loads · carriers · P&L', 'plain')]),
    ('Model', [('KPIs', 'emissions · margin', 'slate'), ('Forecast', 'trend projection', 'slate')]),
    ('Dashboards', [('CO2 emissions', 'Tableau Cloud', 'ember'), ('Regional profit', '4 regions · 49 states', 'ember'), ('Scorecards', 'customer profitability', 'ember')]),
    ('Outcome', [('−12.4% emissions', 'contributed to', 'ok'), ('+15% profitability', 'contributed to', 'ok')]),
], w=1000)


# ---------------------------------------------------------------- SCD Type 2 illustration

def scd2():
    w, h = 1000, 330
    body = text(40, 40, 'SCD Type 2: keep history instead of overwriting it', 20)
    body += text(40, 62, 'illustration with made-up rows · a meter changes size, and both versions are kept', 11, FAINT, MONO)
    cols = [('meter_key', 110), ('meter_id', 110), ('size', 90), ('valid_from', 140), ('valid_to', 140), ('is_current', 120)]
    rows = [('1041', 'M-2207', '5/8 in', '2024-03-01', '2026-04-14', 'false'),
            ('2310', 'M-2207', '1 in', '2026-04-15', '9999-12-31', 'true'),
            ('1042', 'M-3318', '3/4 in', '2025-01-10', '9999-12-31', 'true')]
    x0, y = 40, 100
    x = x0
    for c, cw in cols:
        body += text(x, y, c, 11, EMBER, MONO, ls=0.8); x += cw
    body += f'<line x1="{x0}" y1="{y + 10}" x2="{x}" y2="{y + 10}" stroke="{INK}"/>'
    for r_i, r in enumerate(rows):
        y += 36; x = x0
        if r_i == 1:
            body += f'<rect x="{x0 - 8}" y="{y - 22}" width="{x - x0 + 16 - 0}" height="32" fill="{EMBER_SOFT}"/>'.replace(f'{x - x0 + 16 - 0}', str(sum(c[1] for c in cols) + 16))
        for (c, cw), v in zip(cols, r):
            body += text(x, y, v, 13, INK if r_i != 0 else FAINT, MONO); x += cw
        body += f'<line x1="{x0}" y1="{y + 12}" x2="{x0 + sum(c[1] for c in cols)}" y2="{y + 12}" stroke="{LINE}"/>'
    nx = x0 + sum(c[1] for c in cols) + 30
    body += text(nx, 140, 'old version: closed,', 12.5, SOFT) + text(nx, 158, 'kept for history', 12.5, SOFT)
    body += text(nx, 176, 'new version: current', 12.5, EMBER)
    y += 50
    for k, v in [('type 1', 'overwrite in place, for corrections where history doesn’t matter'),
                 ('type 2', 'new row with a new surrogate key; facts join to the version that was true then')]:
        body += text(40, y, k, 10.5, EMBER, MONO, ls=1.4, upper=True) + text(150, y, v, 13, SOFT); y += 24
    open(os.path.join(OUT, 'lakehouse-scd2.svg'), 'w').write(svg(w, h, body, 'SCD Type 2 illustration'))


scd2()


# ---------------------------------------------------------------- star schema (Power BI)

def star():
    w, h = 900, 420
    body = text(40, 40, 'The shape every migrated report ends up in', 20)
    body += text(40, 62, 'illustrative star schema · one fact table, conformed dimensions, measures in DAX', 11, FAINT, MONO)
    cx, cy = 450, 240
    dims = [('Date', 'calendar · fiscal', 160, 130), ('Department', 'owner', 740, 130), ('Asset', 'type · location', 160, 350), ('Customer', 'account', 740, 350), ('Status', 'open · closed', 450, 110)]
    for t, s, x, y in dims:
        body += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{SOFT}" stroke-width="1.2"/>'
    for t, s, x, y in dims:
        body += box(x - 75, y - 26, 150, 52, t, s, 'plain')
    body += box(cx - 95, cy - 36, 190, 72, 'Fact table', 'one row per event · keys + numbers', 'ember')
    open(os.path.join(OUT, 'powerbi-star.svg'), 'w').write(svg(w, h, body, 'Illustrative star schema'))


star()


# ---------------------------------------------------------------- real charts: Nightly 311

D = json.load(open(os.path.join(os.path.dirname(__file__), 'nightly-snapshot.json')))
SNAP = D['generated_at'][:10]


def nice_ticks(mx, n=4):
    raw = mx / n; mag = 10 ** math.floor(math.log10(raw)); step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    t = [0]
    while t[-1] < mx: t.append(t[-1] + step)
    return t


def requests_chart():
    rows = D['daily']; w, h = 1100, 380; L, R, T, B = 70, 30, 90, 46
    iw, ih = w - L - R, h - T - B
    mx = max(r['requests'] for r in rows); tk = nice_ticks(mx); top = tk[-1]
    body = text(40, 40, '311 requests per day, last 90 days', 20) + text(40, 62, f'real data from the nightly run · snapshot {SNAP}', 11, FAINT, MONO)
    for v in tk:
        y = T + ih - ih * v / top
        body += f'<line x1="{L}" x2="{w - R}" y1="{y:.1f}" y2="{y:.1f}" stroke="{LINE}"/>' + text(L - 10, y + 4, f'{v:,}', 11, FAINT, MONO, 'end')
    step = iw / len(rows); bw = max(1, step - 2)
    for i, r in enumerate(rows):
        hh = ih * r['requests'] / top; x = L + i * step + 1; y = T + ih - hh
        rr = min(3, bw / 2, hh)
        body += (f'<path d="M{x:.1f},{T + ih} V{y + rr:.1f} Q{x:.1f},{y:.1f} {x + rr:.1f},{y:.1f} H{x + bw - rr:.1f} '
                 f'Q{x + bw:.1f},{y:.1f} {x + bw:.1f},{y + rr:.1f} V{T + ih} Z" fill="{EMBER}"/>')
        if i % 14 == 0:
            m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(r['day'][5:7]) - 1]
            body += text(x + bw / 2, h - 18, f'{m} {int(r["day"][8:])}', 11, FAINT, MONO, 'middle')
    avg = sum(r['requests'] for r in rows) / len(rows)
    body += text(w - R, T - 14, f'average {avg:,.0f} a day · weekends dip', 11.5, SOFT, MONO, 'end')
    open(os.path.join(OUT, 'nightly-requests.svg'), 'w').write(svg(w, h, body, '311 requests per day'))


def accuracy_chart():
    rows = D['live_metrics']; test = D['offline_metrics']['accuracy'] * 100
    w, h = 1100, 360; L, R, T, B = 70, 150, 90, 46; iw, ih = w - L - R, h - T - B
    lo, hi = 60, 100
    X = lambda i: L + iw * i / max(1, len(rows) - 1); Y = lambda v: T + ih - ih * (v - lo) / (hi - lo)
    body = text(40, 40, 'Classifier accuracy on complaints it has never seen', 20) + text(40, 62, f'scored every night against NHTSA’s own tags · snapshot {SNAP}', 11, FAINT, MONO)
    for v in range(lo, hi + 1, 10):
        body += f'<line x1="{L}" x2="{L + iw}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"/>' + text(L - 10, Y(v) + 4, f'{v}%', 11, FAINT, MONO, 'end')
    body += f'<line x1="{L}" x2="{L + iw}" y1="{Y(test):.1f}" y2="{Y(test):.1f}" stroke="{SLATE}" stroke-width="1.5" stroke-dasharray="5 5"/>'
    body += text(L + iw + 10, Y(test) + 4, f'test set {test:.1f}%', 11.5, SLATE, MONO)
    pts = ' '.join(f'{X(i):.1f},{Y(r["accuracy"] * 100):.1f}' for i, r in enumerate(rows))
    body += f'<polyline points="{pts}" fill="none" stroke="{EMBER}" stroke-width="2.2" stroke-linejoin="round"/>'
    last = rows[-1]['accuracy'] * 100
    body += f'<circle cx="{X(len(rows) - 1):.1f}" cy="{Y(last):.1f}" r="4.5" fill="{EMBER}" stroke="{PAPER}" stroke-width="2"/>'
    body += text(L + iw + 10, Y(last) + 4, f'live {last:.1f}%', 11.5, EMBER, MONO)
    for i in (0, len(rows) // 2, len(rows) - 1):
        d = rows[i]['day']; m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(d[5:7]) - 1]
        body += text(X(i), h - 18, f'{m} {int(d[8:])}', 11, FAINT, MONO, 'middle')
    open(os.path.join(OUT, 'nightly-accuracy.svg'), 'w').write(svg(w, h, body, 'Live classifier accuracy by night'))


def f1_chart():
    pc = D['offline_metrics']['per_class']; rows = sorted(pc.items(), key=lambda kv: -kv[1]['f1-score'])
    w = 1100; L, R, T = 230, 80, 90; rh = 26; h = T + len(rows) * rh + 30; iw = w - L - R
    body = text(40, 40, 'F1 score by vehicle component', 20) + text(40, 62, 'held-out test set · bge-small embeddings + logistic regression', 11, FAINT, MONO)
    for v in (0, .25, .5, .75, 1):
        x = L + iw * v
        body += f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{T - 8}" y2="{T + len(rows) * rh - 6}" stroke="{LINE}"/>' + text(x, h - 8, f'{v:.2f}', 10.5, FAINT, MONO, 'middle')
    for i, (k, v) in enumerate(rows):
        y = T + i * rh; f = v['f1-score']
        body += text(L - 12, y + 12, k, 13, INK, SERIF, 'end')
        body += f'<rect x="{L}" y="{y + 2}" width="{iw * f:.1f}" height="{rh - 10}" rx="3" fill="{EMBER}"/>'
        body += text(L + iw * f + 8, y + 12, f'{f:.2f}', 11, SOFT, MONO)
    open(os.path.join(OUT, 'nightly-f1.svg'), 'w').write(svg(w, h, body, 'F1 score by component'))


def quarantine_chart():
    q = D['quarantine']; tot = D['quarantine_total']
    names = {'closed_before_created': 'Closed before it was created', 'missing_location': 'No location', 'location_outside_city': 'Location outside the city'}
    w = 1100; L, R, T = 260, 120, 90; rh = 34; h = T + len(q) * rh + 50; iw = w - L - R; mx = max(r['rows'] for r in q)
    body = text(40, 40, f'Why {tot} rows were held in quarantine', 20) + text(40, 62, f'rows that broke a data quality rule, kept with the reason · snapshot {SNAP}', 11, FAINT, MONO)
    for i, r in enumerate(q):
        y = T + i * rh; ww = iw * r['rows'] / mx
        body += text(L - 12, y + 16, names.get(r['dq_reason'], r['dq_reason']), 13.5, INK, SERIF, 'end')
        body += f'<rect x="{L}" y="{y + 4}" width="{ww:.1f}" height="{rh - 14}" rx="3" fill="{BAD}"/>' + text(L + ww + 8, y + 17, f'{r["rows"]}', 12, SOFT, MONO)
    body += text(40, h - 16, 'everything else passed the checks and reached the gold layer', 11.5, FAINT, MONO)
    open(os.path.join(OUT, 'nightly-quarantine.svg'), 'w').write(svg(w, h, body, 'Quarantine reasons'))


requests_chart(); accuracy_chart(); f1_chart(); quarantine_chart()
print('wrote', sorted(os.listdir(OUT)))
