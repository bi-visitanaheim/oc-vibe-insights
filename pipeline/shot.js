const { chromium } = require('playwright');
(async () => {
  const fs = require('fs'), os = require('os'), path = require('path');
  const OUT = process.env.SHOT_DIR || fs.mkdtempSync(path.join(os.tmpdir(), 'ocv-shots-'));
  const body = fs.readFileSync('oc-vibe-insights.html','utf8');
  fs.writeFileSync(path.join(OUT,'preview.html'), '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'+body+'</body></html>');
  const b = await chromium.launch();
  const shots = [['ov-light',1440,'light','summary'],['ocv-light',1440,'light','ocv'],['ocv-dark',1440,'dark','ocv'],['ocv-mobile',390,'light','ocv'],['appx-light',1440,'light','appx'],['appx-mobile',390,'light','appx'],['night-dark',1440,'dark','night'],['notes-mobile',390,'light','notes'],['notes-light',1440,'light','notes']];
  for (const [n,w,scheme,hash] of shots) {
    const p = await b.newPage({viewport:{width:w,height:1000}, colorScheme:scheme});
    const errs=[]; p.on('pageerror', e=>errs.push(e.message)); p.on('console', m=>{ if(m.type()==='error') errs.push(m.text()); });
    await p.goto('file://'+path.join(OUT,'preview.html')+'#'+hash); await p.waitForTimeout(600);
    const ov = await p.evaluate(()=>document.documentElement.scrollWidth - window.innerWidth);
    await p.screenshot({path:path.join(OUT,`${n}.png`), fullPage:true});
    console.log(n, 'overflow', ov, errs.join(' | '));
    await p.close();
  }
  await b.close();
  console.log('Screenshots in', OUT);
})();
