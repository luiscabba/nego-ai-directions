const {JSDOM}=require('jsdom');const fs=require('fs');
const f=process.argv[2];
const dom=new JSDOM(fs.readFileSync('public/flows/'+f,'utf8'),{runScripts:'outside-only',pretendToBeVisual:true});
const w=dom.window; w.scrollTo=()=>{};
for (const src of ['public/vendor/morphdom-umd.min.js','public/dc-runtime.js']) w.eval(fs.readFileSync(src,'utf8'));
const inst=w.DCRuntime.mount(w.document.getElementById('app'),w.document.getElementById('tpl'),w.document.getElementById('logic').textContent);
const app=w.document.getElementById('app');
const shots=[];
const seq=[['home'],['books'],['book',{bank:'amihan'}],['script',{step:2}],['hub'],['lobby'],['live'],['results'],['progress']];
let i=0;
function next(){ if(i>0){ const txt=app.textContent.replace(/\s+/g,' ').trim(); shots.push(seq[i-1][0]+': '+txt.length+' | '+txt.slice(0,90)); }
  if(i===seq.length){ console.log(shots.join('\n')); inst.stop(); process.exit(0);} 
  const [sc,ex]=seq[i++]; inst.go(sc,ex); if(sc==='lobby') inst.setState({ready:true}); if(sc==='live') inst.setState({tick:12}); if(sc==='results') inst.setState({score:84,passed:true}); setTimeout(next,80);}
next();
