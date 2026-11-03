"""VIDVO figures, from Team #2's KCV fellowship decks (Research 1, 2 and 4).
  vidvo-pdiagram   the P-diagram: inputs, control factors, noise factors, outputs
  vidvo-fishbone   failure modes by category, with the TRL scale underneath
Re-run with:  python3 scripts/figures_vidvo.py
"""
import math, os
from figures import (save, T, head, arrowhead, PAPER, INK, SOFT, FAINT, LINE, EMBER, EMBER_SOFT, SLATE, SLATE_SOFT,
                     OK, OK_SOFT, BAD, BAD_SOFT, GOLD, SERIF, MONO)


def pdiagram():
    w, h = 1180, 520
    body = head('Vidvo as a system: what goes in, what we control, what we can’t', 'P-diagram from our Technology Operation Description · KCV Innovation Fellowship, Research 4')
    cx, cy, bw, bh = 590, 290, 300, 150
    body += f'<rect x="{cx - bw / 2}" y="{cy - bh / 2}" width="{bw}" height="{bh}" rx="10" fill="{EMBER_SOFT}" stroke="{EMBER}" stroke-width="1.6"/>'
    body += T(cx, cy - 26, 'Vidvo', 22, INK, SERIF, 'middle')
    for i, s in enumerate(['input layer → prompt processing', '→ model inference → rendering', '→ export (codecs, aspect ratios)']):
        body += T(cx, cy + 2 + i * 18, s, 11, SOFT, MONO, 'middle')

    def group(x, y, title, items, color, soft, anchor):
        out = T(x, y, title, 11, color, MONO, anchor, ls=1.6, upper=True)
        for i, it in enumerate(items):
            yy = y + 16 + i * 38; tw = len(it) * 7.2 + 26; xx = x - tw if anchor == 'end' else (x - tw / 2 if anchor == 'middle' else x)
            out += f'<rect x="{xx:.1f}" y="{yy}" width="{tw:.1f}" height="28" rx="14" fill="{soft}" stroke="{color}"/>' + T(xx + tw / 2, yy + 18.5, it, 12, INK, SERIF, 'middle')
        return out
    body += group(60, 200, 'inputs', ['User prompts', 'Pre-defined templates', 'User uploads (media)'], SLATE, SLATE_SOFT, 'start')
    body += group(1120, 200, 'outputs', ['Final video file', 'Preview frames', 'Error logs'], OK, OK_SOFT, 'end')
    for y in (232, 270, 308):
        body += f'<line x1="290" y1="{y}" x2="{cx - bw / 2 - 4}" y2="{cy}" stroke="{SLATE}" stroke-width="1.1"/>'
    body += arrowhead(cx - bw / 2 - 2, cy, 0, SLATE)
    for y in (232, 270, 308):
        body += f'<line x1="{cx + bw / 2}" y1="{cy}" x2="{930}" y2="{y}" stroke="{OK}" stroke-width="1.1"/>' + arrowhead(930, y, math.atan2(y - cy, 930 - cx - bw / 2), OK)
    ctrl = ['Resolution settings', 'Export parameters', 'GPU allocation limits']
    body += T(cx, 100, 'control factors · we set these', 11, GOLD, MONO, 'middle', ls=1.4, upper=True)
    x = cx - 330
    for c in ctrl:
        tw = len(c) * 7.2 + 26
        body += f'<rect x="{x:.1f}" y="{112}" width="{tw:.1f}" height="28" rx="4" fill="#f3ead2" stroke="{GOLD}"/>' + T(x + tw / 2, 130.5, c, 12, INK, SERIF, 'middle'); x += tw + 18
    body += f'<line x1="{cx}" y1="146" x2="{cx}" y2="{cy - bh / 2 - 3}" stroke="{GOLD}" stroke-width="1.3"/>' + arrowhead(cx, cy - bh / 2 - 2, math.pi / 2, GOLD)
    noise = ['Internet instability', 'API throttling', 'Unclear user prompts', 'High traffic load']
    body += T(cx, h - 26, 'noise factors · we can’t control these, only design for them', 11, BAD, MONO, 'middle', ls=1.4, upper=True)
    x = cx - 420
    for c in noise:
        tw = len(c) * 7.2 + 26
        body += f'<rect x="{x:.1f}" y="{h - 82}" width="{tw:.1f}" height="28" rx="4" fill="{BAD_SOFT}" stroke="{BAD}" stroke-dasharray="4 3"/>' + T(x + tw / 2, h - 63.5, c, 12, INK, SERIF, 'middle'); x += tw + 18
    body += f'<line x1="{cx}" y1="{h - 86}" x2="{cx}" y2="{cy + bh / 2 + 3}" stroke="{BAD}" stroke-width="1.3" stroke-dasharray="4 3"/>' + arrowhead(cx, cy + bh / 2 + 2, -math.pi / 2, BAD)
    save('vidvo-pdiagram', w, h, body, 'Vidvo P-diagram')


def fishbone():
    w, h = 1180, 560
    body = head('Where an export could go wrong, and how ready the technology is', 'failure modes from our TOD and TRL analysis, as an Ishikawa diagram · KCV Innovation Fellowship, Research 4')
    spine_y, x0, x1 = 250, 60, 960
    body += f'<line x1="{x0}" y1="{spine_y}" x2="{x1}" y2="{spine_y}" stroke="{INK}" stroke-width="2.4"/>' + arrowhead(x1 + 4, spine_y, 0, INK, 12)
    body += f'<rect x="{x1 + 14}" y="{spine_y - 40}" width="176" height="80" rx="8" fill="{BAD_SOFT}" stroke="{BAD}" stroke-width="1.5"/>'
    body += T(x1 + 102, spine_y - 8, 'A failed or', 15, INK, SERIF, 'middle') + T(x1 + 102, spine_y + 14, 'off-brand export', 15, INK, SERIF, 'middle')
    bones = [('Technology', ['GPU / render pipeline overload', 'Codec or export failures', 'Autosave not triggering'], 340, -1),
             ('Measurement', ['No QC step before export', 'Vague or unclear prompts'], 740, -1),
             ('Environment', ['Network throttling', 'High user load'], 340, 1),
             ('Method', ['Incorrect branding placement', 'No aspect-ratio presets', 'Missing copyright filtering'], 740, 1)]
    for name, causes, bx, side in bones:
        tip_y = spine_y + side * 150; tip_x = bx - 120
        body += f'<line x1="{tip_x}" y1="{tip_y}" x2="{bx + 60}" y2="{spine_y}" stroke="{EMBER}" stroke-width="1.8"/>'
        body += T(tip_x - 6, tip_y + (-10 if side < 0 else 22), name, 12, EMBER, MONO, 'start', ls=1.4, upper=True)
        for i, c in enumerate(causes):
            f = (i + 1) / (len(causes) + 1)
            px = tip_x + (bx + 60 - tip_x) * f; py = tip_y + (spine_y - tip_y) * f
            tl = len(c) * 6.6 + 14
            body += f'<line x1="{px - tl - 12:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="{SOFT}" stroke-width="1"/>' + arrowhead(px, py, 0, SOFT, 5)
            body += T(px - 14 - side * 0, py - 6, c, 12.5, INK, SERIF, 'end')
    # TRL scale
    ty = h - 96; tx0, tw = 60, 1060
    body += T(tx0, ty - 14, 'technology readiness level', 11, SLATE, MONO, ls=1.4, upper=True)
    for i in range(1, 10):
        x = tx0 + (i - 1) * tw / 9; cw = tw / 9 - 6
        fill = EMBER if i in (3, 4) else (EMBER_SOFT if i in (5, 6, 7) else '#fff')
        st = EMBER if i <= 7 and i >= 3 else LINE
        body += f'<rect x="{x:.1f}" y="{ty}" width="{cw:.1f}" height="30" rx="4" fill="{fill}" stroke="{st}"/>' + T(x + cw / 2, ty + 20, f'TRL {i}', 12, '#fff' if i in (3, 4) else INK, MONO, 'middle')
    body += T(tx0 + 2.5 * tw / 9, ty + 52, 'now: 3–4 · early prototype', 11.5, EMBER, MONO, 'middle')
    body += T(tx0 + 5.5 * tw / 9, ty + 52, 'next: 5–7 · build countermeasures and validate them', 11.5, SOFT, MONO, 'middle')
    save('vidvo-fishbone', w, h, body, 'Vidvo failure modes and technology readiness')


if __name__ == '__main__':
    pdiagram(); fishbone(); print('vidvo figures written')
