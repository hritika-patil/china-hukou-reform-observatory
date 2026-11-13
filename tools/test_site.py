"""QA smoke test via about:blank (some CI sandboxes block all browser networking)."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent.parent
provinces=json.loads((root/'data/provinces.json').read_text())
policies=json.loads((root/'data/policies.json').read_text())
cities=json.loads((root/'data/cities.json').read_text())
audits=json.loads((root/'data/audits.json').read_text())
# Synthetic polygons for interaction testing only — never used on the published site.
mock=[]
for i,pr in enumerate(provinces):
 c=i%7;r=i//7;lon=73+c*8;lat=53-r*7
 mock.append({'type':'Feature','geometry':{'type':'Polygon','coordinates':[[[lon,lat],[lon+7,lat],[lon+7,lat-6],[lon,lat-6],[lon,lat]]]},'properties':{'id':pr['code']+'0000','name':pr['name']}})
DATA={'data/provinces.json':provinces,'data/policies.json':policies,'data/cities.json':cities,'data/audits.json':audits}
import re
html=(root/'index.html').read_text().replace('<script src="app.js" defer></script>','').replace('<link rel="stylesheet" href="styles.css" />','')
html=re.sub(r'<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>', '', html)
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for size in [(1440,1000),(390,844)]:
  page=browser.new_page(viewport={'width':size[0],'height':size[1]},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='domcontentloaded')
  page.add_style_tag(content=(root/'styles.css').read_text())
  page.evaluate('''([data,geometry]) => { window.fetch = async u => new Response(JSON.stringify(String(u).includes('provinces.json') && String(u).includes('cn-atlas') ? geometry : data[String(u)]),{status:200,headers:{'Content-Type':'application/json'}}); }''',[DATA,{'type':'FeatureCollection','features':mock}])
  page.add_script_tag(content=(root/'app.js').read_text())
  page.locator('.map-region').first.wait_for(timeout=10000)
  assert page.locator('.map-region').count()==31
  assert page.locator('.province-chip').count()==31
  assert page.locator('#coverage-body tr').count()==31
  assert page.locator('#metric-localities').inner_text()==str(len(audits))
  assert page.locator('#audit-body tr').count()==124
  page.locator('#audit-status').select_option('unverified')
  assert page.locator('#audit-body tr').count()==38
  page.locator('#audit-status').select_option('all')
  page.locator('#audit-dimension').select_option('education')
  assert page.locator('#audit-body tr').count()==31
  page.locator('#audit-dimension').select_option('all')
  page.locator('#coverage-search').fill('Urumqi')
  assert page.locator('#coverage-body tr').count()==1
  page.locator('#coverage-search').fill('')
  assert page.locator('#records-body tr').count()==len(policies)
  page.locator('button[data-province="31"]').click()
  assert page.locator('.panel-title').inner_text()=='Shanghai'
  assert page.locator('.panel-doc').count()==1
  page.locator('#dimension').select_option('housing')
  assert page.locator('.panel-doc').count()==0
  page.locator('#dimension').select_option('education')
  assert page.locator('.panel-doc').count()==1
  page.locator('#year').select_option('2024')
  assert page.locator('.panel-doc').count()==0
  page.locator('#year').select_option('2026')
  page.locator('#panel-compare').click()
  assert page.locator('.compare-card').count()==1
  page.locator('#compare-select').select_option('51')
  page.locator('#compare-add-btn').click()
  assert page.locator('.compare-card').count()==2
  page.locator('#records-search').fill('Shanghai')
  assert page.locator('#records-body tr').count()==1
  page.locator('#province-search').fill('guiyang')
  assert page.locator('.province-chip').count()==1
  page.locator('#province-search').fill('')
  target='/mnt/data/china-hukou-'+('desktop' if size[0]>700 else 'mobile')+'-preview.png'
  page.evaluate('window.scrollTo(0,0)')
  page.screenshot(path=target,full_page=True,timeout=12000)
  print('OK viewport',size,'SVG regions 31, records 46, 124 assessments, comparison, filters, search, no JS errors; screenshot:',target)
  assert not errors,errors
  print('Document overflow width:',page.evaluate('document.documentElement.scrollWidth'))
  page.close()
 browser.close()
