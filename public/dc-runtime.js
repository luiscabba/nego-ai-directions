/* Minimal standalone runtime for the Nego AI flow mockups.
   Renders an x-dc template (holes, sc-if, sc-for, onX handlers) and patches the DOM with morphdom,
   so CSS animations only replay on elements that are actually new. */
(function () {
  class DCLogic {
    constructor(props) { this.props = props || {}; this.state = {}; }
    setState(patch) {
      const next = typeof patch === 'function' ? patch(this.state, this.props) : patch;
      this.state = Object.assign({}, this.state, next);
      if (this.__schedule) this.__schedule();
    }
    forceUpdate() { if (this.__schedule) this.__schedule(); }
    renderVals() { return {}; }
  }

  const HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  const WHOLE = /^\s*\{\{\s*([^}]+?)\s*\}\}\s*$/;
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const VOID = new Set(['area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr']);

  function lookup(path, scope) {
    if (path === 'true') return true;
    if (path === 'false') return false;
    if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
    if (/^'.*'$|^".*"$/.test(path)) return path.slice(1, -1);
    const parts = path.split('.');
    let v = scope;
    for (const p of parts) { if (v == null) return undefined; v = v[p]; }
    return v;
  }
  const interp = (str, scope) => str.replace(HOLE, (_, p) => { const v = lookup(p, scope); return v == null ? '' : String(v); });

  function render(node, scope, ctx) {
    if (node.nodeType === 3) return esc(interp(node.nodeValue, scope));
    if (node.nodeType !== 1) return '';
    const tag = node.tagName.toLowerCase();
    if (tag === 'sc-if') {
      const m = (node.getAttribute('value') || '').match(WHOLE);
      return (m && lookup(m[1], scope)) ? kids(node, scope, ctx) : '';
    }
    if (tag === 'sc-for') {
      const m = (node.getAttribute('list') || '').match(WHOLE);
      const list = (m && lookup(m[1], scope)) || [];
      const as = node.getAttribute('as') || 'item';
      return list.map((item, i) => kids(node, Object.assign(Object.create(scope), { [as]: item, $index: i }), ctx)).join('');
    }
    let out = '<' + tag;
    for (const a of Array.from(node.attributes)) {
      const name = a.name;
      if (name.startsWith('hint-')) continue;
      const whole = a.value.match(WHOLE);
      if (/^on[a-z]+$/.test(name) && whole) {
        const fn = lookup(whole[1], scope);
        if (typeof fn === 'function') {
          const id = 'h' + (ctx.handlers.length);
          ctx.handlers.push(fn);
          out += ' data-dc-' + name.slice(2) + '="' + id + '"';
        }
        continue;
      }
      out += ' ' + name + '="' + esc(interp(a.value, scope)) + '"';
    }
    out += '>';
    if (VOID.has(tag)) return out;
    return out + kids(node, scope, ctx) + '</' + tag + '>';
  }
  function kids(node, scope, ctx) {
    const src = node.tagName && node.tagName.toLowerCase() === 'template' ? node.content : node;
    let s = '';
    for (const c of Array.from(src.childNodes)) s += render(c, scope, ctx);
    return s;
  }

  function mount(root, tplEl, logicSrc) {
    const Component = new Function('DCLogic', logicSrc + '\n;return Component;')(DCLogic);
    const inst = new Component({});
    let ctx = { handlers: [] };
    let queued = false;
    let lastScreen = null;
    const draw = () => {
      queued = false;
      ctx = { handlers: [] };
      const vals = inst.renderVals();
      const screen = Object.keys(vals).filter(k => /^is[A-Z]/.test(k) && vals[k] === true).join();
      const html = '<div id="' + root.id + '">' + kids(tplEl.content ? { tagName: 'template', content: tplEl.content } : tplEl, vals, ctx) + '</div>';
      window.morphdom(root, html, {
        onBeforeElUpdated: (from, to) => {
          // keep live animations running when only the class string is unchanged
          return !from.isEqualNode(to);
        }
      });
      if (screen !== lastScreen) { if (lastScreen !== null) window.scrollTo(0, 0); lastScreen = screen; }
    };
    inst.__schedule = () => { if (!queued) { queued = true; requestAnimationFrame(draw); } };
    ['click', 'input', 'change'].forEach(type => {
      root.addEventListener(type, e => {
        const el = e.target.closest('[data-dc-' + type + ']');
        if (!el || !root.contains(el)) return;
        const fn = ctx.handlers[Number(el.getAttribute('data-dc-' + type).slice(1))];
        if (fn) fn(e);
      });
    });
    draw();
    if (inst.componentDidMount) inst.componentDidMount();
    return inst;
  }

  window.DCRuntime = { mount };
})();
