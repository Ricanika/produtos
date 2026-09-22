// Roda o construtor de malha do visualizador FORA do navegador, com um THREE
// de mentira, e confere o volume assinado contra o STL que o gerador Python
// escreveu. Se os dois divergirem, o 3D que o time ve nao e a peca que vai
// para a ferramentaria.
//
// Uso: node verifica-malha.js [dir-stl] [visualizador.html]
const fs = require('fs');
const html = fs.readFileSync(process.argv[3] || 'visualizador-3d.html', 'utf8');
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
// lê o volume do STL que o gerador Python acabou de escrever, em vez de
// comparar com número fixo que envelhece
function volSTL(caminho){
  const b = fs.readFileSync(caminho);
  const n = b.readUInt32LE(80);
  let v = 0, o = 84;
  for (let i = 0; i < n; i++){
    o += 12;
    const p = [0,1,2].map(k => [b.readFloatLE(o+k*12), b.readFloatLE(o+k*12+4), b.readFloatLE(o+k*12+8)]);
    o += 36 + 2;
    const [a,c,d2] = p;
    v += (a[0]*(c[1]*d2[2]-c[2]*d2[1]) - a[1]*(c[0]*d2[2]-c[2]*d2[0]) + a[2]*(c[0]*d2[1]-c[1]*d2[0]))/6;
  }
  return v/1000;
}
const ARQ = {'pote-600':'pote-600','pote-1200':'pote-1200','pote-1800':'pote-1800',
             'pote-2400':'pote-2400','tampa-teca':'tampa-teca',
             'tampa-pe':'tampa-pe','filete':'filete-tpe'};
const DIR = process.argv[2] || 'stl';
const py = {};
for (const k of Object.keys(ARQ)) py[k] = volSTL(`${DIR}/${ARQ[k]}.stl`);
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
