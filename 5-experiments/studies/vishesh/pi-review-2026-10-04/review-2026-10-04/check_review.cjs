const assert=require('node:assert/strict');
const path=require('node:path');
const fs=require('node:fs');
const {chromium}=require(process.env.REVIEW_PLAYWRIGHT_MODULE||'playwright');
(async()=>{
 const b=await chromium.launch({headless:true,...(process.env.REVIEW_BROWSER_PATH?{executablePath:process.env.REVIEW_BROWSER_PATH}:{channel:'chrome'})});
 const p=await b.newPage({viewport:{width:1440,height:1050}});const errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto('file://'+path.resolve('review-2026-10-04/index.html'));
 const findings=await p.locator('.finding').count();assert(findings>=47);
 const bad=await p.locator('a[href^="#"]').evaluateAll(as=>as.filter(a=>!document.getElementById(a.getAttribute('href').slice(1))).map(a=>a.getAttribute('href')));assert.deepEqual(bad,[]);
 assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await p.screenshot({path:'/tmp/grove-review-desktop.png'});
 await p.locator('#severity').selectOption('P1');let count=await p.locator('.finding:not([hidden])').count();assert(count>=11);
 await p.locator('#search').fill('budget');assert((await p.locator('.finding:not([hidden])').count())>=1);
 await p.locator('#expand').click();assert(await p.locator('.finding:not([hidden])').first().getAttribute('open')!==null);
 await p.locator('#search').fill('');await p.locator('#severity').selectOption('');
 await p.locator('#project').selectOption('avalon-swarm');assert.equal(await p.locator('.finding:not([hidden])').count(),7);await p.locator('#project').selectOption('');
 await p.evaluate(()=>location.hash='EP-01');assert(await p.locator('#EP-01').getAttribute('open')!==null);
 await p.setViewportSize({width:390,height:844});await p.goto('file://'+path.resolve('review-2026-10-04/index.html'));await p.emulateMedia({reducedMotion:'reduce'});await p.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));await p.screenshot({path:'/tmp/grove-review-mobile.png'});
 for(const id of ['agents','projects','findings','proposals','standards','coverage']){await p.locator('#'+id).scrollIntoViewIfNeeded();assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'mobile overflow '+id)}
 await p.locator('.coverage summary').click();await p.locator('#file-search').fill('AGENTS.md');assert.equal(await p.locator('.coverage tbody tr:not([hidden])').count(),1);
 assert.deepEqual(errors,[]);await b.close();
 const result={findings,priority_filter:true,project_filter:true,text_search:true,deep_links:true,mobile_overflow:false,coverage_search:true,js_errors:errors};fs.writeFileSync(path.resolve('review-2026-10-04/presentation-checks.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
})().catch(e=>{console.error(e);process.exit(1)});
