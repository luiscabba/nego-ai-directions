"""Generates index.html for the Nego AI demo film (1920x1080, 102 s, silent)."""
import pathlib
D = pathlib.Path(__file__).parent
FONTS = (D / 'fonts.css').read_text()

GLASS = "background: rgba(16,28,30,.86); border: 1px solid rgba(127,227,192,.32); box-shadow: inset 0 1px 0 rgba(255,255,255,.12), 0 60px 130px rgba(0,0,0,.55)"
MONO = "font-family: 'JetBrains Mono', monospace"
SPARK = "M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM18.5 15.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"
CHECK = "M5 12.5l4.5 4.5L19 7.5"
STAR = "M12 2.8l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17l-5.6 3 1.1-6.2L3 9.4l6.2-.9z"

scenes = []   # (id, start, dur, html)
js = []       # timeline lines

def svg(d, size, stroke=True, extra=''):
    if stroke:
        return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" {extra}><path d="{d}"></path></svg>'
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" aria-hidden="true" {extra}><path fill="currentColor" d="{d}"></path></svg>'

def plate(sid, imgs, left, top, scale0, scale1, ry0, ry1, rx=3, origin='30% 50%', T=0, dur=8, dim=0):
    """App screen on a tilted camera. imgs: list of (file, t_offset) crossfaded in order."""
    layers = ''.join(f'<img id="{sid}-img{i}" class="shot" src="shots/{f}" alt="">' for i, (f, _) in enumerate(imgs))
    dimdiv = f'<div class="dim" style="opacity: {dim}"></div>' if dim else ''
    html = f'''<div id="{sid}-tilt" class="tilt" style="transform-origin: {origin}">
  <div id="{sid}-cam" class="cam" style="left: {left}px; top: {top}px">{layers}{dimdiv}</div>
</div>
<div class="topfade"></div>'''
    js.append(f'tl.fromTo("#{sid}-tilt", {{rotationY: {ry0}, rotationX: {rx}, transformPerspective: 2600}}, {{rotationY: {ry1}, rotationX: {rx}, transformPerspective: 2600, duration: {dur}, ease: "sine.inOut"}}, {T});')
    js.append(f'tl.fromTo("#{sid}-cam", {{scale: {scale0}}}, {{scale: {scale1}, duration: {dur}, ease: "sine.inOut"}}, {T});')
    for i, (_, off) in enumerate(imgs):
        if i == 0:
            continue
        js.append(f'tl.fromTo("#{sid}-img{i}", {{opacity: 0}}, {{opacity: 1, duration: .6, ease: "power1.inOut"}}, {T + off});')
    return html

def caption(sid, text, accent, T):
    js.append(f'tl.fromTo("#{sid}-cap", {{y: -24, opacity: 0}}, {{y: 0, opacity: 1, duration: .7, ease: "power3.out"}}, {T + .5});')
    return f'''<div class="capwrap"><div id="{sid}-cap" class="cap">{text} <span class="acc">{accent}</span></div></div>'''

def pop(sel, T, y=50, dur=.8, scale=None):
    if scale:
        js.append(f'tl.fromTo("{sel}", {{y: {y}, opacity: 0, scale: {scale}}}, {{y: 0, opacity: 1, scale: 1, duration: {dur}, ease: "power3.out"}}, {T});')
    else:
        js.append(f'tl.fromTo("{sel}", {{y: {y}, opacity: 0}}, {{y: 0, opacity: 1, duration: {dur}, ease: "power3.out"}}, {T});')

def scene(sid, start, dur, body, fade=True):
    if fade and start > 0:
        js.append(f'tl.fromTo("#{sid}-in", {{opacity: 0}}, {{opacity: 1, duration: .5, ease: "power1.inOut"}}, {start});')
    scenes.append(f'''<section id="{sid}" class="clip" data-start="{start}" data-duration="{dur}" data-track-index="1">
<div id="{sid}-in" class="in">
{body}
</div>
</section>''')

LOGO = lambda sid, sz: f'<div id="{sid}-logo" class="logo" style="width: {sz}px; height: {sz}px; border-radius: {int(sz*.28)}px; font-size: {int(sz*.5)}px">N</div>'

# 1 Open 0-6
T = 0
b = plate('s1', [('home_blur.jpg', 0)], -60, -60, 1.35, 1.45, 12, 6, T=T, dur=6.5, dim=.45)
b += f'''<div class="center col" style="gap: 36px">
{LOGO('s1', 170)}
<div id="s1-name" class="big" style="font-size: 128px">Nego AI</div>
<div id="s1-line" class="eyebrow" style="font-size: 24px">Negotiation practice for collection agents</div>
</div>'''
pop('#s1-logo', .3, y=0, dur=1, scale=.6)
pop('#s1-name', 1.0, y=40)
pop('#s1-line', 1.7, y=20)
scene('s1', 0, 6, b)

# 2 Ticket 5.5-14
T = 5.5
b = plate('s2', [('home.jpg', 0)], -90, -60, 1.75, 1.9, 13, 8, T=T, dur=9)
b += f'''<div id="s2-card" class="card" style="left: 1140px; top: 200px; width: 640px; padding: 46px; gap: 22px; border-radius: 38px">
<span class="pill amb" style="font-size: 19px">Coaching ticket · Major</span>
<div style="display: flex; align-items: baseline; gap: 18px"><span id="s2-num" class="big num" style="font-size: 150px; line-height: 1">0</span><span style="font-size: 50px; color: #C3D2CF">calls</span></div>
<div style="font-size: 31px; line-height: 1.4; color: #C3D2CF">No partial offered after a hardship claim</div>
<div class="eyebrow" style="font-size: 18px">QA AI · 16 Oct</div>
</div>'''
b += caption('s2', 'QA AI spots the', 'gap.', T)
pop('#s2-card', T + 1.2, y=60)
js.append(f'tl.fromTo(s2n, {{v: 0}}, {{v: 3, duration: 1.1, ease: "power2.out", onUpdate: () => {{ document.getElementById("s2-num").textContent = Math.round(s2n.v); }}}}, {T + 1.6});')
scene('s2', T, 8.5, b)

# 3 Script 13.5-22
T = 13.5
b = plate('s3', [('script.jpg', 0)], -720, -180, 1.85, 1.98, -12, -7, origin='70% 50%', T=T, dur=9)
b += f'''<div id="s3-card" class="card warm" style="left: 110px; top: 640px; width: 600px; padding: 40px 42px; gap: 16px">
<span class="eyebrow" style="font-size: 19px; color: #F2C287">Debtor cue</span>
<div style="font-size: 40px; font-weight: 600; line-height: 1.35; color: #F2D3A8">Says only half is possible on the 25th.</div>
</div>'''
b += caption('s3', 'Learn the playbook,', 'step by step.', T)
js.append(f'tl.fromTo("#s3-card", {{x: -80, opacity: 0}}, {{x: 0, opacity: 1, duration: .9, ease: "power3.out"}}, {T + 1.6});')
scene('s3', T, 8.5, b)

# 4 Lobby 21.5-28
T = 21.5
b = plate('s4', [('lobby.jpg', 0)], -370, -250, 1.6, 1.75, 0, 0, rx=0, T=T, dur=7)
b += caption('s4', 'Pair up with a', 'teammate.', T)
scene('s4', T, 6.5, b)

# 5 Countdown 27.5-32
T = 27.5
rings = ''
for i, n in enumerate([3, 2, 1]):
    rings += f'''<div id="s5-r{n}" class="cd"><svg viewBox="0 0 520 520" width="520" height="520" aria-hidden="true"><circle cx="260" cy="260" r="248" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="6"></circle><circle id="s5-a{n}" cx="260" cy="260" r="248" fill="none" stroke="#7FE3C0" stroke-width="6" stroke-linecap="round" stroke-dasharray="1558" transform="rotate(-90 260 260)"></circle></svg><span class="big num" style="font-size: 260px; line-height: 1">{n}</span></div>'''
    t0 = T + .4 + i * 1.05
    js.append(f'tl.fromTo("#s5-r{n}", {{opacity: 0, scale: 1.4}}, {{opacity: 1, scale: 1, duration: .45, ease: "power3.out"}}, {t0});')
    js.append(f'tl.fromTo("#s5-a{n}", {{attr: {{"stroke-dashoffset": 1558}}}}, {{attr: {{"stroke-dashoffset": 0}}, duration: 1.0, ease: "none"}}, {t0});')
    js.append(f'tl.to("#s5-r{n}", {{opacity: 0, scale: .85, duration: .25, ease: "power2.in"}}, {t0 + .85});')
rings += '<div id="s5-live" class="cd"><span class="big" style="font-size: 150px; color: #7FE3C0">Live</span></div>'
js.append(f'tl.fromTo("#s5-live", {{opacity: 0, scale: .7}}, {{opacity: 1, scale: 1, duration: .35, ease: "back.out(2)"}}, {T + 3.6});')
b = rings + f'<div class="bottomline eyebrow" style="font-size: 22px">Affordable Partial Payment · with Jomar D.</div>'
scene('s5', T, 4.5, b)

# 6 Live 31.5-44
T = 31.5
b = plate('s6', [('live_01.jpg', 0), ('live_03.jpg', 3.4), ('live_05.jpg', 7.0), ('live_07.jpg', 10.6)], -60, -50, 1.5, 1.6, 12, 8, T=T, dur=12.5)
pts = [('Verify identity', '00:32', 2.0), ('Confirm PTP date and amount', '01:20', 6.2), ('Probe ability to pay', '02:40', 99), ('Offer partial if needed', '', 99), ('Recap and close', '', 99)]
rows = ''
for i, (t, tm, met_at) in enumerate(pts):
    rows += f'''<div class="pt"><span class="dot"><span id="s6-d{i}" class="dotfill">{svg(CHECK, 16, extra='style="stroke-width: 3"')}</span></span><span style="flex: 1">{t}</span><span id="s6-t{i}" class="tm">{tm}</span></div>'''
    if met_at < 50:
        js.append(f'tl.fromTo("#s6-d{i}", {{opacity: 0, scale: .4}}, {{opacity: 1, scale: 1, duration: .35, ease: "back.out(2)"}}, {T + met_at});')
        js.append(f'tl.fromTo("#s6-t{i}", {{opacity: 0}}, {{opacity: 1, duration: .3}}, {T + met_at});')
b += f'''<div id="s6-card" class="card" style="left: 1290px; top: 560px; width: 580px; padding: 26px; gap: 8px">
<div style="display: flex; justify-content: space-between; font-size: 27px; font-weight: 600; padding-bottom: 8px"><span>Required points</span><span class="mono" style="color: #9FB3AF">5 steps</span></div>
{rows}
</div>'''
b += caption('s6', 'Every required point,', 'tracked live.', T)
pop('#s6-card', T + 1.0, y=50)
js.append('for (let i = 2; i < 5; i++) { tl.set("#s6-t" + i, {opacity: 0}, 0); }')
scene('s6', T, 12.5, b)

# 7 Hint 43.5-52
T = 43.5
b = plate('s7', [('live_09_blur.jpg', 0)], -60, -90, 1.75, 1.85, 12, 9, T=T, dur=8.5, dim=.35)
b += f'''<div id="s7-card" class="card hintcard" style="left: 210px; top: 300px; width: 1500px; padding: 52px 58px; flex-direction: row; gap: 40px; align-items: flex-start">
<div class="sp" style="width: 108px; height: 108px; border-radius: 32px">{svg(SPARK, 56)}</div>
<div style="display: flex; flex-direction: column; gap: 18px; min-width: 0"><span class="eyebrow" style="font-size: 22px; color: #7FE3C0">AI hint · Hardship cue</span><div id="s7-say" class="big" style="font-size: 64px; line-height: 1.2">Offer a split now: ₱6,000 on 25 Oct, ₱6,000 on 8 Nov</div></div>
</div>
<div id="s7-quote" class="quote" style="left: 210px; top: 150px"><span class="mono" style="color: #F2C287; margin-right: 14px">JOMAR</span>Medyo mahirap ngayon. Nawalan ako ng sideline.</div>
<div id="s7-reply" class="quote" style="left: 210px; top: 760px"><span class="mono" style="color: #7FE3C0; margin-right: 14px">RICA</span>Pwede po nating hatiin: ₱6,000 sa 25 Oct at ₱6,000 sa 8 Nov.</div>'''
b += caption('s7', 'Coached in', 'the moment.', T)
pop('#s7-quote', T + .6, y=30)
js.append(f'tl.fromTo("#s7-card", {{y: 80, opacity: 0, scale: .88}}, {{y: 0, opacity: 1, scale: 1, duration: .9, ease: "power3.out"}}, {T + 1.6});')
js.append(f'tl.fromTo("#s7-say", {{clipPath: "inset(0 100% 0 0)"}}, {{clipPath: "inset(0 0% 0 0)", duration: 1.6, ease: "none"}}, {T + 2.2});')
pop('#s7-reply', T + 5.0, y=30)
scene('s7', T, 8.5, b)

# 8 Scoring 51.5-58
T = 51.5
steps = [('Recording saved', 'M12 3a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V6a3 3 0 0 1 3-3zM5 11a7 7 0 0 0 14 0'), ('Transcribing', 'M5 6h14M5 11h14M5 16h9'), ('Analyzing', 'M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3M8 12h8'), ('Scoring', 'M4 16a8 8 0 1 1 16 0M12 16l4-5')]
row = ''
for i, (t, d) in enumerate(steps):
    row += f'''<div class="step"><div class="sbox"><div class="lay wait">{svg(d, 76)}</div><div id="s8-run{i}" class="lay run">{svg(d, 76)}</div><div id="s8-done{i}" class="lay done">{svg(CHECK, 76, extra='style="stroke-width: 2.4"')}</div></div><span id="s8-l{i}" class="slabel">{t}</span></div>'''
    if i < 3:
        row += f'<div class="conn"><div id="s8-c{i}" class="connfill"></div></div>'
    t0 = T + .7 + i * 1.25
    js.append(f'tl.fromTo("#s8-run{i}", {{opacity: 0}}, {{opacity: 1, duration: .3}}, {t0});')
    js.append(f'tl.fromTo("#s8-l{i}", {{color: "#6F827E"}}, {{color: "#E6F0EE", duration: .3}}, {t0});')
    js.append(f'tl.fromTo("#s8-done{i}", {{opacity: 0, scale: .6}}, {{opacity: 1, scale: 1, duration: .35, ease: "back.out(2)"}}, {t0 + 1.0});')
    if i < 3:
        js.append(f'tl.fromTo("#s8-c{i}", {{scaleX: 0}}, {{scaleX: 1, duration: .4, ease: "power2.inOut"}}, {t0 + .95});')
b = plate('s8', [('proc_blur.jpg', 0)], -120, -135, 1.5, 1.55, 0, 0, rx=0, T=T, dur=6.5, dim=.5)
b += f'<div class="center"><div class="steps">{row}</div></div>'
b += caption('s8', 'Scored in', 'seconds.', T)
scene('s8', T, 6.5, b)

# 9 Results 57.5-68
T = 57.5
b = plate('s9', [('results.jpg', 0), ('results_p1.jpg', 3.2), ('results_p2.jpg', 5.6), ('results_p3.jpg', 8.0)], -190, -90, 1.55, 1.65, -10, -6, origin='70% 50%', T=T, dur=10.5)
b += '<div class="fadeL"></div>'
b += f'''<div id="s9-card" class="card" style="left: 100px; top: 210px; width: 560px; padding: 48px; align-items: center; gap: 28px; border-radius: 44px">
<div id="s9-ring" class="ring" style="width: 340px; height: 340px"><div class="ringin" style="width: 284px; height: 284px"><span id="s9-num" class="big num" style="font-size: 120px; line-height: 1">0</span><span class="eyebrow" style="font-size: 20px">/ 100</span></div></div>
<span id="s9-pill" class="pill ok" style="font-size: 20px">Passed · Sent to TL</span>
</div>'''
b += caption('s9', 'Know exactly', 'what to fix.', T)
pop('#s9-card', T + .8, y=60)
js.append(f'tl.fromTo(s9n, {{v: 0}}, {{v: 84, duration: 1.6, ease: "power2.out", onUpdate: () => {{ document.getElementById("s9-num").textContent = Math.round(s9n.v); document.getElementById("s9-ring").style.background = "conic-gradient(#7FE3C0 " + (s9n.v * 3.6) + "deg, rgba(255,255,255,.08) 0deg)"; }}}}, {T + 1.3});')
pop('#s9-pill', T + 3.0, y=10, dur=.5, scale=.7)
scene('s9', T, 10.5, b)

# 10 Rating 67.5-74
T = 67.5
stars = ''.join(f'<span id="s10-st{i}" class="star">{svg(STAR, 104, stroke=False)}</span>' for i in range(5))
b = plate('s10', [('transcript_blur.jpg', 0)], 0, -180, 1.75, 1.85, 13, 9, T=T, dur=7, dim=.25)
b += f'''<div id="s10-card" class="card warm" style="left: 540px; top: 240px; width: 840px; padding: 52px; align-items: center; gap: 34px">
<span style="font-size: 36px; font-weight: 600">Rate Jomar as debtor</span>
<div style="display: flex; gap: 16px">{stars}</div>
<div style="display: flex; gap: 14px"><span id="s10-t0" class="tag">Realistic</span><span id="s10-t1" class="tag">Followed brief</span></div>
</div>'''
b += caption('s10', 'Partners score the', 'debtor too.', T)
pop('#s10-card', T + .8, y=60)
for i in range(5):
    js.append(f'tl.fromTo("#s10-st{i}", {{color: "rgba(255,255,255,.18)", scale: .7}}, {{color: "#F2C287", scale: 1, duration: .3, ease: "back.out(3)"}}, {T + 1.8 + i * .22});')
for i in range(2):
    pop(f'#s10-t{i}', T + 3.2 + i * .35, y=10, dur=.4, scale=.8)
scene('s10', T, 6.5, b)

# 11 Team 73.5-82
T = 73.5
b = plate('s11', [('team.jpg', 0)], -90, -225, 1.65, 1.75, 14, 9, rx=4, T=T, dur=8.5)
b += f'''<div id="s11-row" class="card" style="left: 240px; top: 420px; width: 1470px; padding: 30px 40px; flex-direction: row; align-items: center; gap: 30px; border-color: rgba(127,227,192,.6); border-radius: 30px">
<div style="display: flex; align-items: center; gap: 24px; flex: 1"><div class="av">RM</div><div style="display: flex; flex-direction: column; gap: 4px"><span style="font-size: 36px; font-weight: 600">Rica Manalo</span><span style="font-size: 24px; color: #9FB3AF">Affordable Partial Payment · Today</span></div></div>
<span class="mono" style="font-size: 46px; color: #7FE3C0; width: 120px">84</span>
<span class="pill info" style="font-size: 22px">Needs review</span>
<span id="s11-btn" class="btnp" style="font-size: 26px; padding: 18px 34px">Review</span>
</div>'''
b += caption('s11', 'Team leads see who', 'needs them.', T)
js.append(f'tl.fromTo("#s11-row", {{y: 40, opacity: 0, scale: .96}}, {{y: -10, opacity: 1, scale: 1, duration: .9, ease: "power3.out"}}, {T + 1.6});')
js.append(f'tl.to("#s11-btn", {{scale: .93, duration: .12, yoyo: true, repeat: 1, ease: "power1.inOut"}}, {T + 6.6});')
scene('s11', T, 8.5, b)

# 12 Review 81.5-90
T = 81.5
b = plate('s12', [('review.jpg', 0), ('review_p.jpg', 3.4)], 660, -150, 1.35, 1.45, 8, 4, T=T, dur=8.5)
b += f'''<div id="s12-card" class="card" style="left: 120px; top: 260px; width: 700px; padding: 46px; gap: 26px">
<div style="display: flex; justify-content: space-between; align-items: center"><span style="font-size: 33px; font-weight: 600">Decision</span><div style="display: flex; padding: 6px; border-radius: 99px; background: rgba(255,255,255,.06)"><span style="padding: 12px 24px; border-radius: 99px; background: rgba(255,255,255,.14); font-size: 24px">Approve</span><span style="padding: 12px 24px; font-size: 24px; color: #9FB3AF">Redo</span></div></div>
<div style="padding: 22px 24px; border-radius: 22px; background: rgba(255,255,255,.05); font-size: 26px; line-height: 1.5; color: #C3D2CF">Good recovery after the hardship cue. Offer the split earlier next time.</div>
<span id="s12-btn" class="btnp" style="font-size: 29px; padding: 22px; text-align: center">Approve and close ticket</span>
</div>'''
b += caption('s12', 'Review, approve,', 'close.', T)
pop('#s12-card', T + 1.0, y=60)
js.append(f'tl.to("#s12-btn", {{scale: .94, boxShadow: "0 0 0 10px rgba(127,227,192,.35)", duration: .14, yoyo: true, repeat: 1, ease: "power1.inOut"}}, {T + 6.6});')
scene('s12', T, 8.5, b)

# 13 Closed 89.5-96
T = 89.5
chips = ['QA AI flag', 'Practice', 'Score', 'TL review', 'Closed']
cols = ['#F2C287', '#E6F0EE', '#E6F0EE', '#A9C1FF', '#7FE3C0']
loop = ''
for i, (c, col) in enumerate(zip(chips, cols)):
    loop += f'<div id="s13-c{i}" class="chip" style="color: {col}">{c}</div>'
    if i < 4:
        loop += f'<svg id="s13-a{i}" viewBox="0 0 40 16" width="56" height="22" aria-hidden="true"><path d="M2 8h32M28 2l6 6-6 6" fill="none" stroke="#6F827E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
    js.append(f'tl.fromTo("#s13-c{i}", {{opacity: .2, y: 10}}, {{opacity: 1, y: 0, duration: .35, ease: "power2.out"}}, {T + 2.0 + i * .45});')
    if i < 4:
        js.append(f'tl.fromTo("#s13-a{i}", {{opacity: 0}}, {{opacity: 1, duration: .3}}, {T + 2.2 + i * .45});')
TICK = svg(CHECK, 46, extra='style="stroke-width: 2.6"')
b = plate('s13', [('closed_blur.jpg', 0)], -120, -135, 1.5, 1.56, 0, 0, rx=0, T=T, dur=6.5, dim=.5)
b += f'''<div class="center col" style="gap: 84px; padding-bottom: 40px">
<div id="s13-toast" class="toastbig"><span class="tick">{TICK}</span>Ticket closed · Rica notified</div>
<div class="loop">{loop}</div>
</div>'''
b += caption('s13', 'From QA flag to', 'closed ticket.', T)
js.append(f'tl.fromTo("#s13-toast", {{y: -70, opacity: 0, scale: .9}}, {{y: 0, opacity: 1, scale: 1, duration: .7, ease: "back.out(1.6)"}}, {T + .8});')
scene('s13', T, 6.5, b)

# 14 End 95.5-102
T = 95.5
b = f'''<div class="center col" style="gap: 36px">
{LOGO('s14', 160)}
<div id="s14-name" class="big" style="font-size: 116px">Nego AI</div>
<div id="s14-by" class="eyebrow" style="font-size: 24px">S.P. Madrid</div>
</div>'''
js.append(f'tl.fromTo("#s14-logo", {{y: 80, opacity: 0}}, {{y: 0, opacity: 1, duration: 1.1, ease: "power3.out"}}, {T + .6});')
pop('#s14-name', T + 1.3, y=40)
pop('#s14-by', T + 1.9, y=20)
scene('s14', T, 6.5, b)

CSS = '''
body{margin:0;background:#0A1012;color:#E6F0EE;font-family:Sora,system-ui,sans-serif}
#root{position:relative;width:100%;height:100%;overflow:hidden;background:#0A1012}
.bg{position:absolute;inset:0;overflow:hidden}
.blob{position:absolute;border-radius:50%}
.clip{position:absolute;inset:0;overflow:hidden}
.in{position:absolute;inset:0}
.tilt{position:absolute;inset:0}
.cam{position:absolute;width:1440px;height:900px;transform-origin:0 0;border-radius:28px;overflow:hidden;box-shadow:0 80px 180px rgba(0,0,0,.65),0 0 0 1px rgba(255,255,255,.08)}
.shot{position:absolute;inset:0;width:1440px;height:900px;display:block}
.dim{position:absolute;inset:0;background:#0A1012}
.topfade{position:absolute;left:0;right:0;top:0;height:300px;background:linear-gradient(rgba(10,16,18,.92) 15%,rgba(10,16,18,0))}
.fadeL{position:absolute;left:0;top:0;bottom:0;width:1100px;background:linear-gradient(90deg,#0A1012 40%,rgba(10,16,18,0))}
.center{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.col{flex-direction:column}
.big{font-weight:700;letter-spacing:-.03em}
.num{font-variant-numeric:tabular-nums}
.mono{font-family:'JetBrains Mono',monospace}
.eyebrow{font-family:'JetBrains Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:#9FB3AF}
.logo{background:linear-gradient(140deg,#5FE0B4,#2A9D7C);color:#06231A;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:0 0 120px rgba(127,227,192,.45)}
.card{position:absolute;display:flex;flex-direction:column;border-radius:36px;GLASSX}
.card.warm{background:rgba(40,32,20,.92);border-color:rgba(242,194,135,.45)}
.hintcard{background:linear-gradient(120deg,rgba(30,70,60,.95),rgba(30,44,80,.93));border-color:rgba(127,227,192,.55);box-shadow:0 0 180px rgba(127,227,192,.25),0 70px 140px rgba(0,0,0,.5)}
.sp{background:rgba(127,227,192,.2);color:#7FE3C0;display:flex;align-items:center;justify-content:center;flex:none}
.pill{align-self:center;font-family:'JetBrains Mono',monospace;padding:10px 20px;border-radius:99px}
.card .pill{align-self:flex-start}
#s9-card .pill{align-self:center}
.pill.amb{background:rgba(242,194,135,.16);color:#F2C287}
.pill.ok{background:rgba(127,227,192,.15);color:#7FE3C0}
.pill.info{background:rgba(110,150,240,.2);color:#A9C1FF}
.capwrap{position:absolute;left:0;right:0;top:60px;display:flex;justify-content:center}
.cap{padding:20px 44px;border-radius:26px;font-size:46px;font-weight:700;letter-spacing:-.01em;GLASSX}
.acc{color:#7FE3C0}
.pt{display:flex;align-items:center;gap:18px;padding:18px 22px;border-radius:20px;font-size:26px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08)}
.dot{position:relative;width:32px;height:32px;border-radius:50%%;border:2px solid rgba(255,255,255,.22);flex:none}
.dotfill{opacity:0;position:absolute;inset:-2px;border-radius:50%%;background:#7FE3C0;color:#06231A;display:flex;align-items:center;justify-content:center}
.tm{font-family:'JetBrains Mono',monospace;font-size:19px;color:#7FE3C0}
.quote{position:absolute;padding:20px 30px;border-radius:22px;background:rgba(10,16,18,.78);border:1px solid rgba(255,255,255,.1);font-size:32px;color:#C3D2CF}
.cd{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.cd svg{position:absolute;left:700px;top:280px;filter:drop-shadow(0 0 18px rgba(127,227,192,.5))}
.bottomline{position:absolute;left:0;right:0;bottom:90px;text-align:center}
.steps{display:flex;align-items:flex-start}
.step{display:flex;flex-direction:column;align-items:center;gap:26px;width:280px}
.sbox{position:relative;width:180px;height:180px}
.lay{position:absolute;inset:0;border-radius:50px;display:flex;align-items:center;justify-content:center}
.lay.wait{background:rgba(255,255,255,.06);color:#6F827E}
.lay.run{background:rgba(127,227,192,.18);color:#7FE3C0;box-shadow:0 0 0 12px rgba(127,227,192,.12),0 0 90px rgba(127,227,192,.4)}
.lay.done{background:#7FE3C0;color:#06231A}
.slabel{font-size:32px;font-weight:600;color:#6F827E}
.conn{width:100px;height:5px;margin-top:88px;border-radius:3px;background:rgba(255,255,255,.12);overflow:hidden}
.connfill{width:100%%;height:5px;background:linear-gradient(90deg,#7FE3C0,#A9C1FF);transform-origin:left center}
.ring{border-radius:50%%;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.08);box-shadow:0 0 100px rgba(127,227,192,.3)}
.ringin{border-radius:50%%;background:#0F1A1C;display:flex;flex-direction:column;align-items:center;justify-content:center}
.star{color:rgba(255,255,255,.18);display:block}
.tag{padding:14px 26px;border-radius:99px;font-size:26px;background:rgba(127,227,192,.14);color:#7FE3C0;border:1px solid rgba(127,227,192,.36)}
.av{width:84px;height:84px;border-radius:50%%;background:rgba(127,227,192,.14);border:1px solid rgba(127,227,192,.35);color:#7FE3C0;font-weight:600;font-size:28px;display:flex;align-items:center;justify-content:center;flex:none}
.btnp{border-radius:99px;font-weight:600;background:linear-gradient(140deg,#7FE3C0,#3FB68B);color:#06231A;display:block}
.toastbig{display:flex;align-items:center;gap:30px;padding:28px 52px 28px 28px;border-radius:99px;background:rgba(16,30,30,.94);border:1px solid rgba(127,227,192,.5);box-shadow:0 0 150px rgba(127,227,192,.25);font-size:52px;font-weight:600}
.tick{width:90px;height:90px;border-radius:50%%;background:#7FE3C0;color:#06231A;display:flex;align-items:center;justify-content:center}
.loop{display:flex;align-items:center;gap:20px}
.chip{padding:24px 36px;border-radius:26px;font-size:33px;font-weight:600;GLASSX}
'''.replace('%%','%').replace('GLASSX', GLASS)

HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920, height=1080">
<title>Nego AI demo</title>
<script src="vendor/gsap.min.js"></script>
<style>
{FONTS}
{CSS}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="102">
<div class="bg" aria-hidden="true">
<div id="b1" class="blob" style="left: -300px; top: -360px; width: 1350px; height: 1050px; background: radial-gradient(closest-side, rgba(38,160,128,.45), transparent)"></div>
<div id="b2" class="blob" style="right: -330px; top: 180px; width: 1230px; height: 960px; background: radial-gradient(closest-side, rgba(46,86,170,.38), transparent)"></div>
<div id="b3" class="blob" style="left: 630px; bottom: -540px; width: 1050px; height: 840px; background: radial-gradient(closest-side, rgba(214,140,50,.2), transparent)"></div>
</div>
{chr(10).join(scenes)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const s2n = {{ v: 0 }}, s9n = {{ v: 0 }};
tl.fromTo("#b1", {{x: 0, y: 0}}, {{x: 260, y: 140, duration: 51, ease: "sine.inOut", yoyo: true, repeat: 1}}, 0);
tl.fromTo("#b2", {{x: 0, y: 0}}, {{x: -220, y: 180, duration: 51, ease: "sine.inOut", yoyo: true, repeat: 1}}, 0);
{chr(10).join(js)}
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
(D / 'index.html').write_text(HTML)
print('scenes', len(scenes), 'tweens', len(js))
