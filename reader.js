'use strict';
const reader=document.getElementById('reader');
const nav=document.getElementById('pageNav');
const counter=document.getElementById('counter');
const modeButton=document.getElementById('mode');
const nextButtons=['next','nextBottom'].map(id=>document.getElementById(id));
const prevButtons=['prev','prevBottom'].map(id=>document.getElementById(id));
let pages=[],figures=[],current=1,continuous=false,observer;
const clampPage=value=>Math.max(1,Math.min(pages.length,Math.trunc(Number(value))||1));
const pageFromHash=()=>clampPage(/^#p(\d+)$/.exec(location.hash)?.[1]);

function loadImage(index,priority=false){
  const figure=figures[index];
  if(!figure)return;
  const img=figure.querySelector('img');
  if(img.dataset.loaded)return;
  img.dataset.loaded='true';
  img.fetchPriority=priority?'high':'low';
  img.src=img.dataset.src;
}
function showPage(value,scroll=false){
  current=clampPage(value);
  figures.forEach((f,i)=>{f.hidden=!continuous&&i!==current-1});
  Array.from(nav.children).forEach((a,i)=>{
    if(i===current-1)a.setAttribute('aria-current','page');
    else a.removeAttribute('aria-current');
  });
  counter.textContent=`${current} / ${pages.length}`;
  nextButtons.forEach(b=>b.disabled=current===pages.length);
  prevButtons.forEach(b=>b.disabled=current===1);
  loadImage(current-1,true);
  if(scroll)figures[current-1].scrollIntoView({block:'start',behavior:'instant'});
  if(!continuous){
    observer?.disconnect();
    // Load only the current page and one page ahead in single-page mode.
    loadImage(current);
  }else if(observer){
    figures.forEach(f=>observer.observe(f));
  }else{
    figures.forEach((_,i)=>loadImage(i));
  }
}
function go(delta){
  const next=clampPage(current+delta);
  if(next!==current)location.hash=`p${next}`;
}

async function init(){
  try{
    const response=await fetch('pages.json',{cache:'no-cache'});
    if(!response.ok)throw new Error(`HTTP ${response.status}`);
    const manifest=await response.json();
    pages=manifest.pages;
    if(!Array.isArray(pages)||pages.length!==16)throw new Error('ページ情報が不正です');
    const fragment=document.createDocumentFragment();
    pages.forEach((page,i)=>{
      const url=`${page.file}?v=${page.sha256.slice(0,12)}`;
      const anchor=document.createElement('a');
      anchor.href=`#p${page.page}`;
      anchor.textContent=String(page.page).padStart(2,'0');
      anchor.setAttribute('aria-label',`${page.page}ページへ`);
      nav.append(anchor);
      const figure=document.createElement('figure');
      figure.id=`p${page.page}`;
      figure.hidden=true;
      const img=document.createElement('img');
      img.dataset.src=url;
      img.width=page.width;img.height=page.height;
      img.alt=`第1話 ${page.page}ページ${page.page===16?'、1話完':''}`;
      img.decoding='async';
      const error=document.createElement('p');
      error.className='image-error';error.hidden=true;
      const retry=document.createElement('button');
      retry.textContent='画像を再読み込み';
      retry.addEventListener('click',()=>{error.hidden=true;img.src=url+`&retry=${Date.now()}`});
      error.append('画像を読み込めませんでした。 ',retry);
      img.addEventListener('error',()=>{error.hidden=false});
      img.addEventListener('load',()=>{error.hidden=true});
      const caption=document.createElement('figcaption');
      const label=document.createElement('span');label.textContent=`${page.page} / ${pages.length}`;
      const full=document.createElement('a');
      full.href=url;full.target='_blank';full.rel='noopener';full.textContent='画像を拡大';
      caption.append(label,full);figure.append(img,error,caption);fragment.append(figure);
    });
    reader.replaceChildren(fragment);
    figures=Array.from(reader.querySelectorAll('figure'));
    if('IntersectionObserver' in window){
      observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
        if(entry.isIntersecting){loadImage(figures.indexOf(entry.target));observer.unobserve(entry.target)}
      }),{rootMargin:'600px 0px'});
    }
    nextButtons.forEach(b=>b.addEventListener('click',()=>go(1)));
    prevButtons.forEach(b=>b.addEventListener('click',()=>go(-1)));
    window.addEventListener('hashchange',()=>showPage(pageFromHash(),true));
    window.addEventListener('keydown',event=>{
      if(event.altKey||event.ctrlKey||event.metaKey||event.target.isContentEditable||event.target.matches('input,textarea,select'))return;
      if(event.key==='ArrowLeft'){event.preventDefault();go(1)}
      if(event.key==='ArrowRight'){event.preventDefault();go(-1)}
    });
    modeButton.addEventListener('click',()=>{
      continuous=!continuous;
      modeButton.textContent=continuous?'1ページずつ読む':'全ページを縦に読む';
      modeButton.setAttribute('aria-pressed',String(continuous));
      showPage(current,true);
    });
    window.addEventListener('beforeprint',()=>figures.forEach((_,i)=>loadImage(i)));
    showPage(pageFromHash());
  }catch(error){
    document.getElementById('status').textContent='読み込めませんでした。ページを再読み込みしてください。';
    [...nextButtons,...prevButtons,modeButton].forEach(b=>b.disabled=true);
  }
}
init();
