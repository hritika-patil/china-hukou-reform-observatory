"""Refresh the public audit CSVs and research matrix from evidence-linked JSON.

Never fills missing evidence with presumed permissiveness/restrictiveness.
Manual audit findings and unresolved research fields live in data/audits.json.
"""
from pathlib import Path
import csv, json
R=Path(__file__).resolve().parent.parent
D=R/'data'
read=lambda f:json.loads((D/f).read_text(encoding='utf-8'))
provinces,policies,cities,audits=map(read,['provinces.json','policies.json','cities.json','audits.json'])
bypro={p['code']:p for p in provinces}
byid={p['id']:p for p in policies}

def write(name,headers,rows):
 with (D/name).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(headers);w.writerows(rows)

write('policy_audits_124.csv',['Province','Code','Dimension','Evidence status','Source IDs','Evidence types','Documented finding','What remains unverified','Primary-source URL(s)','Last reviewed'],[
 [a['jurisdiction'],a['province_code'],a['dimension'],a['status'],'; '.join(a['document_ids']),'; '.join(a['evidence_type']),a['finding'],a['unresolved'],'; '.join(a['source_urls']),a['verified_on']] for a in audits])
write('source_register.csv',['ID','Jurisdiction','Level','Document date / publication date','Document title','Government agency','Evidence type','Source type','Dimensions','URL','Summary','Finding','Original date uncertain'],[
 [p['id'],bypro.get(p['province_code'],{}).get('name','National') if p.get('province_code') else 'National',p['level'],p['date'],p['title_zh'] or p['title'],p['agency'],p.get('evidence_type',''),p.get('source_tier',''),'; '.join(p['dimensions']),p['url'],p['summary'],p.get('finding',''),str(p.get('original_issuance_date_uncertain',False))] for p in sorted(policies,key=lambda x:x['id'])])
rows=[]
for a in audits:
 p=bypro[a['province_code']];anchors=[c for c in cities if c['province_code']==p['code']]
 primary=next((c['name'] for c in anchors if c.get('priority')=='Primary' and not c['id'].endswith('-0')),'')
 secondary=next((c['name'] for c in anchors if c.get('priority')=='Comparative'),'')
 rows.append([p['code'],p['name'],p['name_zh'],p['type'],p['region'],a['dimension'],a['status'],len(a['document_ids']),'; '.join(a['document_ids']),primary,secondary,'Cross-check legal validity; verify applicant-level municipality/district rules and outcomes separately.',a['verified_on'],a['finding'],'; '.join(a['evidence_type']),'; '.join(a['source_urls']),a['unresolved']])
write('research_matrix.csv',['province_code','jurisdiction','name_zh','jurisdiction_type','region','dimension','status','verified_local_documents','document_ids','primary_locality','comparison_locality','research_protocol','last_database_update','documented_finding','evidence_type','source_urls','unresolved'],rows)
print('Refreshed 124 audit entries,',len(policies),'sources, 31-jurisdiction research matrix')
