// Roda o construtor de malha do visualizador FORA do navegador, com um THREE
// de mentira, e confere o volume assinado contra o que o gerador Python fez.
const fs = require('fs');
const html = fs.readFileSync('potes-3d.html', 'utf8');
const ini = html.indexOf('  function anel(');
const fim = html.indexOf('  var G = {};');
const fonte = html.slice(ini, fim);

global.THREE = {
  BufferGeometry: function(){
    this.setAttribute = (n,a) => { this.pos = a.array; };
    this.setIndex = i => { this.idx = i; };
    this.computeVertexNormals = () => {};
  },
  Float32BufferAttribute: function(a){ this.array = a; }
};
const DATA = JSON.parse(fs.readFileSync('perfis.json','utf8'));
const SEG = DATA.seg, M = SEG*4;
const fn = new Function('DATA','SEG','M','THREE', fonte + '; return {anel, geom};');
const { geom } = fn(DATA, SEG, M, global.THREE);

function volume(g){
  let v = 0;
  for (let t = 0; t < g.idx.length; t += 3){
    const p = [0,1,2].map(k => { const i = g.idx[t+k]*3; return [g.pos[i], g.pos[i+1], g.pos[i+2]]; });
    const [a,b,c] = p;
    v += (a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0]))/6;
  }
  return v;
}
// o visualizador usa (x, z, -y): rotação, mantém o volume e a mão
const py = {'pote-600':45.1,'pote-1200':74.2,'pote-1800':108.6,'pote-2400':147.2,'tampa':21.5,'aro':2.3};
let ok = true;
console.log('peça          volume na malha JS   volume no STL Python   desvio');
for (const k of Object.keys(DATA.pecas)){
  const g = geom(DATA.pecas[k]);
  const v = volume(g)/1000;
  const d = 100*(v/py[k]-1);
  if (v <= 0 || Math.abs(d) > 1) ok = false;
  console.log(`${k.padEnd(13)} ${v.toFixed(2).padStart(12)} cm³ ${py[k].toFixed(2).padStart(16)} cm³ ${d.toFixed(2).padStart(8)}%`);
}
console.log('\ntodas positivas e batendo com o Python:', ok);
