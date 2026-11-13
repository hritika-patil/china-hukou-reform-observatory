"""Validate tracker references, field formats and preservation of missing evidence."""
import json,re,sys,datetime
from pathlib import Path
root=Path(__file__).resolve().parent.parent
read=lambda name: json.loads((root/'data'/name).read_text(encoding='utf-8'))
provinces,policies,cities=read('provinces.json'),read('policies.json'),read('cities.json')
errors=[]
def ok(cond, msg):
 if not cond:errors.append(msg)
expected={'11','12','13','14','15','21','22','23','31','32','33','34','35','36','37','41','42','43','44','45','46','50','51','52','53','54','61','62','63','64','65'}
code_set={p['code'] for p in provinces}
ok(len(provinces)==31 and code_set==expected,'Mainland jurisdiction set must contain 31 unique codes.')
ok(len({p['code'] for p in provinces})==len(provinces),'Duplicate province codes.')
ids=set()
for p in policies:
 if p['id'] in ids:errors.append('Duplicate policy id '+p['id'])
 ids.add(p['id'])
 ok(p['level'] in ('national','provincial','municipal'),'Bad level '+p['id'])
 ok(p['level']=='national' or p.get('province_code') in code_set,'Local code missing for '+p['id'])
 ok(p['level']!='national' or p.get('province_code') is None,'National source cannot have province code '+p['id'])
 ok(p.get('status')=='source-verified','Policy source must be verified: '+p['id'])
 ok(p.get('url','').startswith('https://'),'Policy URL must be HTTPS '+p['id'])
 ok(bool(p.get('dimensions')) and set(p['dimensions']).issubset({'settlement','education','housing','protection'}),'Bad dimensions '+p['id'])
 for key in ('date','verified_on'):
  try:datetime.date.fromisoformat(p[key])
  except (ValueError,KeyError,TypeError):errors.append('Invalid '+key+' for '+p['id'])
 if p.get('effective_date'):
  try:datetime.date.fromisoformat(p['effective_date'])
  except ValueError:errors.append('Invalid effective date '+p['id'])
for c in cities:ok(c['province_code'] in code_set,'City linked to missing province: '+c['id'])
for code in code_set:
 subset=[c for c in cities if c['province_code']==code]
 ok(any(c.get('priority')=='Primary' for c in subset), 'Missing primary locality for '+code)
 ok(any(c.get('priority')=='Comparative' for c in subset), 'Missing comparison locality for '+code)
with (root/'data/research_matrix.csv').open(encoding='utf-8-sig',newline='') as fp:
 matrix=list(__import__('csv').DictReader(fp))
ok(len(matrix)==124,'Research matrix must have exactly 124 rows (31 x 4).')
for code in code_set:
 ok({r['dimension'] for r in matrix if r['province_code']==code}=={'settlement','education','housing','protection'},'Incomplete four-dimension matrix for '+code)
if errors:
 print('FAILED:', *errors,sep='\n - ');sys.exit(1)
print(f'OK: {len(provinces)} jurisdictions, {len(policies)} policies, {len(cities)} city research records; all structural checks passed.')
# Detailed audit integrity: every jurisdiction × dimension, no fabricated source IDs.
audits=read('audits.json'); doc_by_id={p['id']:p for p in policies}
valid_statuses={'rule-documented','direction-documented','related-document','unverified'}
ok(len(audits)==124 and len({(r['province_code'],r['dimension']) for r in audits})==124,'Exactly 124 distinct audit cells required')
for a in audits:
 ok(a['province_code'] in code_set,'Unknown audit jurisdiction '+a['province_code'])
 ok(a['status'] in valid_statuses,'Unknown audit status '+a['status'])
 ok(len(a['document_ids'])==len(a['source_urls']),'Audit source counts differ '+a['jurisdiction']+' '+a['dimension'])
 for i,url in zip(a['document_ids'],a['source_urls']):
  if i not in doc_by_id:errors.append('Audit cites missing source ID '+i);continue
  p=doc_by_id[i]
  ok(p.get('province_code')==a['province_code'],'Audit cites source of wrong jurisdiction: '+i)
  ok(a['dimension'] in p.get('dimensions',[]),'Audit cites source without dimension: '+i+' '+a['dimension'])
  ok(p['url']==url,'Audit source URL differs from source register '+i)
 if a['status']=='unverified':ok(len(a['document_ids'])==0,'Unverified with source documents '+a['jurisdiction'])
try:
 import csv
 with (root/'data/policy_audits_124.csv').open(encoding='utf-8-sig',newline='') as fp:au_csv=list(csv.DictReader(fp))
 ok(len(au_csv)==124,'The exported audit CSV must have 124 rows')
 for r,a in zip(au_csv,audits):ok(r['Code']==a['province_code'] and r['Evidence status']==a['status'],'Audit CSV out of sync '+a['jurisdiction'])
except Exception as e:errors.append('Unable to validate audit CSV: '+str(e))
missing=[code for code in code_set if not any(p.get('province_code')==code for p in policies)]
ok(not missing,'No official source anchor for province codes: '+','.join(missing))
if errors:
 print('FAILED FULL AUDIT CHECK:',*errors,sep='\n - ');sys.exit(1)
from collections import Counter
print('AUDIT QA: 124 assessments, 31/31 local anchors,',Counter(a['status'] for a in audits),'— source references consistent')
