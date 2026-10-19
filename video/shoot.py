import asyncio, glob, json
from playwright.async_api import async_playwright
EXE=sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))
EXE=EXE[-1] if EXE else sorted(glob.glob('/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell'))[-1]
R={'rica':'review','kim':'review','paolo':'open','ben':'open','leo':'open'}
DONE={'score':84,'passed':True,'tk':R}
S={
 'home':{},
 'script':{'screen':'script','step':2},
 'lobby':{'screen':'lobby','ready':True},
 'results':dict(screen='results',ph=0,**DONE),
 'results_p1':dict(screen='results',ph=96,**DONE),
 'results_p2':dict(screen='results',ph=176,**DONE),
 'results_p3':dict(screen='results',ph=256,**DONE),
 'transcript':dict(screen='results',tab='transcript',ph=176,stars=0,**DONE),
 'team':dict(role='tl',screen='team',**DONE),
 'review':dict(role='tl',screen='review',ph=40,**DONE),
 'review_p':dict(role='tl',screen='review',ph=200,**DONE),
 'closed':dict(role='tl',screen='team',score=84,passed=True,tk=dict(R,rica='closed')),
 'proc':{'screen':'proc','pstep':1,'pp':40},
}
for t in [1,3,5,7,9,11,13,15,17]: S['live_%02d'%t]={'screen':'live','tick':t}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=EXE,args=['--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1440,'height':900},device_scale_factor=1.5)
        for name,st in S.items():
            await pg.goto('file://'+__import__('os').path.abspath('harness/app.html'))
            await pg.add_style_tag(content='*{animation:none!important;transition:none!important}.toast{display:none!important}.dc-switch{display:none!important}')
            await pg.wait_for_timeout(300)
            await pg.evaluate('st=>{const i=window.__inst;i.stop();clearTimeout(i.tt);i.setState(Object.assign({toast:""},st));}',st)
            await pg.wait_for_timeout(250)
            await pg.evaluate('document.fonts.ready')
            await pg.screenshot(path=f'shots/{name}.png')
        await b.close()
asyncio.run(main())
print('ok')
