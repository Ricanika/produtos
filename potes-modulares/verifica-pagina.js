// Roda a LOGICA da pagina do visualizador fora do navegador, com um three.js
// e um DOM de mentira, e percorre todas as combinacoes de vista e tampa.
//
// O verifica-malha.js cobre a geometria; este cobre o resto: montagem da cena,
// troca de botao, textos do HUD. Sem isso, um erro em monta() so apareceria no
// navegador de quem abrisse a pagina - e daqui nao da para abrir, porque o
// proxy nao deixa baixar o three.js do CDN.
//
// Uso: node verifica-pagina.js [visualizador.html]
const fs = require('fs');
const src = process.argv[2] || 'visualizador-3d.html';
const html = fs.readFileSync(src, 'utf8');

function V3(x, y, z){ this.x=x||0; this.y=y||0; this.z=z||0;
  this.set = function(a,b,c){ this.x=a; this.y=b; this.z=c; return this; }; }
function Obj(){
  this.children = []; this.position = new V3(); this.renderOrder = 0;
  this.add = function(o){ this.children.push(o); return this; };
  this.remove = function(o){ const i = this.children.indexOf(o); if (i>=0) this.children.splice(i,1); };
}
const malhas = [];
global.THREE = {
  BufferGeometry: function(){
    this.setAttribute = function(){ return this; };
    this.setIndex = function(i){ this.idx = i; return this; };
    this.computeVertexNormals = function(){};
    this.setFromPoints = function(){ return this; };
  },
  Float32BufferAttribute: function(a){ this.array = a; },
  Vector3: V3,
  Plane: function(){},
  Group: Obj,
  Scene: Obj,
  Mesh: function(g, m){ Obj.call(this);
    if (!g) throw new Error('Mesh sem geometria');
    if (!m) throw new Error('Mesh sem material');
    this.geometry = g; malhas.push(this); },
  Line: function(g, m){ Obj.call(this); this.geometry = g; this.material = m; },
  LineBasicMaterial: function(){}, MeshPhysicalMaterial: function(o){ Object.assign(this, o); },
  HemisphereLight: Obj, DirectionalLight: Obj, AmbientLight: Obj,
  PerspectiveCamera: function(){ Obj.call(this);
    this.lookAt = function(){}; this.updateProjectionMatrix = function(){}; },
  WebGLRenderer: function(){ this.setPixelRatio = function(){}; this.setSize = function(){};
    this.render = function(){}; this.localClippingEnabled = false; },
  DoubleSide: 2
};

// ---- DOM de mentira, so o que a pagina usa ----
const els = {};
function El(id){
  this.id = id; this.textContent = ''; this.clientWidth = 900; this.clientHeight = 500;
  this.width = 0; this.height = 0; this.handlers = {};
  this.addEventListener = (n, f) => { this.handlers[n] = f; };
  this.setPointerCapture = () => {};
  this.querySelectorAll = () => this.botoes || [];
  this.setAttribute = (k, v) => { this.attrs = this.attrs || {}; this.attrs[k] = v; };
  this.getAttribute = k => (this.attrs || {})[k];
}
// os botoes reais, lidos do HTML, para clicar em cada um de verdade
function grupo(id, attr){
  const el = new El(id);
  const bloco = html.slice(html.indexOf(`id="${id}"`));
  const fim = bloco.indexOf('</div>');
  el.botoes = [...bloco.slice(0, fim).matchAll(new RegExp(`${attr}="([^"]+)"`, 'g'))].map(m => {
    const b = new El(attr + ':' + m[1]);
    b.setAttribute(attr, m[1]);
    b.closest = () => b;
    return b;
  });
  els[id] = el;
  return el;
}
['g-vista','g-tampa','g-aro'].forEach(id =>
  grupo(id, id === 'g-vista' ? 'data-v' : id === 'g-tampa' ? 'data-t' : 'data-a'));
['cena','hud-t','hud-d'].forEach(id => { els[id] = new El(id); });
global.document = { getElementById: id => els[id] || new El(id) };
global.window = { matchMedia: () => ({ matches: true }) };
global.matchMedia = global.window.matchMedia;
global.devicePixelRatio = 1;
let quadros = 0;
global.requestAnimationFrame = () => { quadros++; };

const script = html.slice(html.lastIndexOf('<script>') + 8, html.lastIndexOf('</script>'));
new Function('THREE','document','window','matchMedia','devicePixelRatio','requestAnimationFrame',
             script)(global.THREE, global.document, global.window, global.matchMedia, 1,
                     global.requestAnimationFrame);

let ok = quadros > 0;
if (!ok) console.log('FALHA: a pagina nem chegou a desenhar o primeiro quadro');

// clica em cada combinacao de vista x tampa x aro, como um usuario faria
const VISTAS = els['g-vista'].botoes, TAMPAS = els['g-tampa'].botoes, AROS = els['g-aro'].botoes;
console.log('vista x tampa: malhas na cena e texto do HUD');
for (const v of VISTAS) for (const t of TAMPAS) for (const a of AROS){
  els['g-vista'].handlers.click({ target: v });
  els['g-tampa'].handlers.click({ target: t });
  malhas.length = 0;           // so o ultimo monta() conta
  els['g-aro'].handlers.click({ target: a });
  const vv = v.getAttribute('data-v'), tt = t.getAttribute('data-t');
  const n = malhas.length, d = els['hud-d'].textContent;
  const vazio = n === 0, mudo = !d || d.length < 20;
  if (a.getAttribute('data-a') === '1'){
    if (vazio || mudo) ok = false;
    console.log(`  ${(vv+' / '+tt).padEnd(22)} ${String(n).padStart(3)} malhas  ${vazio||mudo?'FALHA':'ok'}  ${d.slice(0,58)}…`);
  } else if (vazio) { ok = false; console.log(`  ${vv} / ${tt} sem aro: FALHA, cena vazia`); }
}
console.log('\npagina monta em todas as combinacoes:', ok);
process.exit(ok ? 0 : 1);
