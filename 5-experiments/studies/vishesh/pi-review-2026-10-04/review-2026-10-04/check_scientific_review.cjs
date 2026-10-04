const assert=require('node:assert/strict');
const path=require('node:path');
const fs=require('node:fs');
const {chromium}=require(process.env.REVIEW_PLAYWRIGHT_MODULE||'playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.REVIEW_BROWSER_PATH?{executablePath:process.env.REVIEW_BROWSER_PATH}:{channel:'chrome'})});
 const page=await browser.newPage({viewport:{width:1440,height:1050}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const url='file://'+path.resolve('review-2026-10-04/scientific-review.html');await page.goto(url);
 assert.equal(await page.locator('#overview .card').count(),10);
 assert.equal(await page.locator('.study').count(),21);assert.equal(await page.locator('.proposal').count(),16);
 assert.equal(await page.locator('#areas .card').count(),8);
 const bad=await page.locator('a[href^="#"]').evaluateAll(as=>as.filter(a=>!document.getElementById(a.getAttribute('href').slice(1))).map(a=>a.getAttribute('href')));assert.deepEqual(bad,[]);
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await page.screenshot({path:'/tmp/grove-scientific-desktop.png'});
 await page.locator('#study-group').selectOption('antsy');assert.equal(await page.locator('.study:not([hidden])').count(),2);
 await page.locator('#study-search').fill('OCR');assert.equal(await page.locator('.study:not([hidden])').count(),1);
 await page.locator('#expand').click();assert(await page.locator('#SCI-ANTSY-V4').getAttribute('open')!==null);
 await page.locator('#study-search').fill('nonexistent-query-987');assert.equal(await page.locator('.study:not([hidden])').count(),0);assert(await page.locator('#empty').isVisible());
 await page.evaluate(()=>location.hash='SCI-PHANTOM-COAST');await page.waitForFunction(()=>document.querySelector('#SCI-PHANTOM-COAST').open);
 assert.equal(await page.locator('.study:not([hidden])').count(),21);assert.equal(await page.locator('#study-search').inputValue(),'');
 await page.goto(url+'#SCI-RD');assert(await page.locator('#SCI-RD').getAttribute('open')!==null);
 await page.setViewportSize({width:390,height:844});await page.goto(url);await page.emulateMedia({reducedMotion:'reduce'});await page.screenshot({path:'/tmp/grove-scientific-mobile.png'});
 for(const id of ['overview','criteria','studies','areas','portfolio','scope']){await page.locator('#'+id).scrollIntoViewIfNeeded();assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'mobile overflow '+id);}
 await page.evaluate(()=>location.hash='SCI-ANTSY-V4');await page.waitForFunction(()=>document.querySelector('#SCI-ANTSY-V4').open);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'expanded mobile tables');await page.screenshot({path:'/tmp/grove-scientific-expanded-mobile.png'});
 await page.goto('file://'+path.resolve('review-2026-10-04/index.html'));assert.equal(await page.locator('a[href="scientific-review.html"]').count(),1);
 assert.deepEqual(errors,[]);await browser.close();
 const result={named_project_cards:10,study_reviews:21,proposal_reviews:16,areas:8,broken_internal_anchors:bad,filters:true,deep_links:true,empty_state:true,mobile_overflow:false,original_report_link:true,js_errors:errors};fs.writeFileSync('review-2026-10-04/scientific-presentation-checks.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
})().catch(e=>{console.error(e);process.exit(1)});
