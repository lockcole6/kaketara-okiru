'use strict';
const jump=document.querySelector('#jump');
const figures=Array.from(document.querySelectorAll('.pages figure'));
if(jump&&figures.length){
  const clamp=value=>Math.max(1,Math.min(figures.length,Math.trunc(Number(value))||1));
  let queued=false;
  function updateVisiblePage(){
    queued=false;
    // Follow the page crossing the reading line below the sticky toolbar.
    const readingLine=Math.min(window.innerHeight*.35,280);
    let visible=1;
    for(let i=0;i<figures.length;i++){
      if(figures[i].getBoundingClientRect().top<=readingLine)visible=i+1;
      else break;
    }
    jump.value=String(visible);
  }
  function goToPage(value){
    const page=clamp(value);
    jump.value=String(page);
    const img=figures[page-1].querySelector('img');
    img.loading='eager';
    figures[page-1].scrollIntoView({block:'start',behavior:'instant'});
    history.replaceState(null,'','#p'+page);
    updateVisiblePage();
  }
  jump.addEventListener('change',()=>goToPage(jump.value));
  window.addEventListener('scroll',()=>{
    if(!queued){queued=true;requestAnimationFrame(updateVisiblePage)}
  },{passive:true});
  window.addEventListener('resize',updateVisiblePage);
  function goToHash(){
    const match=/^#p(\d+)$/.exec(location.hash);
    if(match)goToPage(match[1]);
    else updateVisiblePage();
  }
  window.addEventListener('hashchange',goToHash);
  window.addEventListener('keydown',event=>{
    if(event.altKey||event.ctrlKey||event.metaKey||event.target.isContentEditable||event.target.matches('input,textarea,select'))return;
    if(event.key==='ArrowLeft'||event.key==='ArrowRight'){
      event.preventDefault();
      goToPage(Number(jump.value)+(event.key==='ArrowLeft'?1:-1));
    }
  });
  window.addEventListener('beforeprint',()=>figures.forEach(f=>{f.querySelector('img').loading='eager'}));
  goToHash();
}
