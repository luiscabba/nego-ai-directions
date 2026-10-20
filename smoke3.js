const {JSDOM}=require('jsdom');const fs=require('fs');
const dom=new JSDOM(fs.readFileSync('public/index.html','utf8'),{runScripts:'outside-only',pretendToBeVisual:true,url:'https://x.test/'});
const w=dom.window; w.scrollTo=()=>{};
for (const src of ['public/vendor/morphdom-umd.min.js','public/dc-runtime.js']) w.eval(fs.readFileSync(src,'utf8'));
const inst=w.DCRuntime.mount(w.document.getElementById('app'),w.document.getElementById('tpl'),w.document.getElementById('logic').textContent);
const app=w.document.getElementById('app');
const seq=[['home'],['books'],['script'],['hub'],['lobby',{},{ready:true}],['count',{},{cd:1}],['live',{},{tick:9}],['proc',{},{pstep:2,pp:40}],['results',{},{score:84,passed:true,ph:120}],['progress'],['team',{role:'tl'}],['review',{role:'tl'}]];
let i=0,out=[];
function next(){ if(i>0){const txt=app.textContent.replace(/\s+/g,' ').trim(); out.push(seq[i-1][0]+': '+(txt.includes('AI hint')?'HINT ':'')+txt.length);}
 if(i===seq.length){console.log(out.join('\n'));inst.stop();process.exit(0);}
 const [sc,ex,st]=seq[i++]; inst.go(sc,ex); if(st) inst.setState(st); setTimeout(next,80);}
next();
