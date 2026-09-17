const fs=require('fs');
const h=fs.readFileSync('modelo3d.html','utf8');
const js=h.slice(h.lastIndexOf('<script>')+8, h.lastIndexOf('</script>'));
let fills=0, pts=[], cur=[], nan=0;
const ctx={ setTransform(){}, clearRect(){}, beginPath(){cur=[];},
  moveTo(x,y){cur.push([x,y]);}, lineTo(x,y){cur.push([x,y]);}, closePath(){},
  fill(){fills++; for(const p of cur){ if(!isFinite(p[0])||!isFinite(p[1])) nan++; } pts.push(...cur);},
  stroke(){}, set fillStyle(v){}, set strokeStyle(v){}, set lineWidth(v){} };
const L={}; const press={};
function el(id){ return { id, style:{}, textContent:'', value:'0', width:0, height:0,
  clientWidth:900, clientHeight:480, getContext:()=>ctx,
  addEventListener(t,f){ (L[id]=L[id]||{})[t]=f; }, setPointerCapture(){},
  getAttribute(){ return press[id]||'false'; },
  setAttribute(k,v){ press[id]=v; }, click(){ if(L[id]&&L[id].click) L[id].click(); }, appendChild(){}, parentNode:{appendChild(){}} }; }
const nodes={}; ['cv','scrub','play','tCorte','tZoom','tPilha','tReset','rFase','rCurso','rQueda','rJunta']
  .forEach(i=>nodes[i]=el(i));
global.document={ getElementById:i=>nodes[i]||el(i), createElement:()=>el('x'), body:{appendChild(){}} };
global.window={ devicePixelRatio:1, addEventListener(){} };
global.requestAnimationFrame=f=>1; global.cancelAnimationFrame=()=>{};
new Function(js)();

let ultimoFiltro=null;
function cena(nome, soCentro){
  fills=0; pts=[]; nan=0;
  L.cv.pointerdown({clientX:0,clientY:0,pointerId:1});
  L.cv.pointermove({clientX:1,clientY:0,pointerId:1});   // força redesenho
  L.cv.pointerup({});
  const xs=pts.map(p=>p[0]), ys=pts.map(p=>p[1]);
  // no zoom, o resto do pote sai do quadro de proposito; o que importa e que
  // ALGO relevante esteja enquadrado e nada seja NaN
  const dentro=pts.filter(p=>p[0]>=0&&p[0]<=900&&p[1]>=0&&p[1]<=480).length;
  const fora=pts.length-dentro;
  console.log(`${nome.padEnd(26)} faces ${String(fills).padStart(5)}  X ${Math.min(...xs).toFixed(0).padStart(5)}..${Math.max(...xs).toFixed(0).padStart(4)}  Y ${Math.min(...ys).toFixed(0).padStart(4)}..${Math.max(...ys).toFixed(0).padStart(4)}  NaN ${nan}  fora ${String(fora).padStart(5)}  dentro ${(100*(pts.length-fora)/pts.length).toFixed(0)}%`);
  return fills;
}
const a=cena('aberto (pousando)');
nodes.scrub.value='1000'; L.scrub.input();
const b=cena('fechado');
L.tCorte.click(); const c=cena('fechado + corte');
L.tPilha.click(); const d=cena('corte + pote empilhado');
L.tZoom.click();  const e=cena('+ zoom na borda');
L.tReset.click(); const f=cena('reenquadrado');
console.log('\n'+([a,b,c,d,e,f].every(v=>v>200) ? 'TODOS OS ESTADOS DESENHAM' : 'ALGUM ESTADO FALHOU'));
console.log('corte remove faces?', c<b ? `sim (${b} -> ${c})` : `NAO (${b} -> ${c})`);
console.log('pilha adiciona faces?', d>c ? `sim (${c} -> ${d})` : `NAO (${c} -> ${d})`);
