import csv,zipfile,io,json,hashlib,collections,pathlib
import sys
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '.'); pairs={}; excluded=set(); totals=collections.Counter(); names={}
def key(r):return (r['SG_UF'],str(int(r['CD_MUNICIPIO'])),str(int(r['NR_ZONA'])),str(int(r['NR_SECAO'])))
def read(fn):
 with zipfile.ZipFile(root/fn) as z:
  for n in z.namelist():
   if n.endswith('_BR.csv'):
    with z.open(n) as f:yield from csv.DictReader(io.TextIOWrapper(f,encoding='latin1'),delimiter=';')
seen=set()
for r in read('votacao_secao_2026_BR.zip'):
 if r['CD_CARGO']!='1' or r['NR_TURNO'] not in ('1','2'):continue
 t=r['NR_TURNO'];k=key(r);n=r['NR_VOTAVEL'];v=int(r['QT_VOTOS']);totals[t+':'+n]+=v
 p=pairs.setdefault(k,dict(zip(['uf','mun','z','s'],k),nm=r['NM_MUNICIPIO']))
 p.setdefault('a'+t,0);p.setdefault('b'+t,0)
 if n in ('13','22'):
  ident=(*k,t,n);assert ident not in seen,ident;seen.add(ident)
  p[('a' if n=='22' else 'b')+t]+=v;names[n]=r['NM_VOTAVEL']
print('votes read',len(pairs),dict(totals),names,flush=True)
detail_seen=set();detail_totals=collections.Counter()
for r in read('detalhe_votacao_secao_2026.zip'):
 if r['CD_CARGO']!='1' or r['NR_TURNO'] not in ('1','2'):continue
 t=r['NR_TURNO']
 for field in ['QT_COMPARECIMENTO','QT_VOTOS_NOMINAIS','QT_VOTOS_BRANCOS','QT_VOTOS_NULOS']:detail_totals[t+':'+field]+=int(r[field])
 k=key(r);ident=(*k,t);assert ident not in detail_seen,ident;detail_seen.add(ident)
 if r['ST_SECAO_ANULADA'].lower() in ('sim','s') or r['ST_SECAO_INSTALADA'].lower() in ('não','nao','n'):excluded.add(k)
 if k in pairs:
  p=pairs[k]
  for a,b in [('comp','QT_COMPARECIMENTO'),('br','QT_VOTOS_BRANCOS'),('nu','QT_VOTOS_NULOS')]:p[a+t]=int(r[b])
  p['detail'+t]=True
print('details read',len(detail_seen),dict(detail_totals),flush=True)
for t in ['1','2']:
 assert sum(v for k,v in totals.items() if k.startswith(t+':') and k not in [t+':95',t+':96'])==detail_totals[t+':QT_VOTOS_NOMINAIS']
 assert totals[t+':95']==detail_totals[t+':QT_VOTOS_BRANCOS']
 assert totals[t+':96']==detail_totals[t+':QT_VOTOS_NULOS']
 assert sum(v for k,v in totals.items() if k.startswith(t+':'))==detail_totals[t+':QT_COMPARECIMENTO']

places={}; candidates=[];unpaired=0; counts={str(n):[0,0] for n in [55,60,65,70]}
for k,p in pairs.items():
 if k in excluded:continue
 if any('a'+t not in p or not p.get('detail'+t) or p['a'+t]+p['b'+t]<=0 for t in ['1','2']):unpaired+=1;continue
 for t in ['1','2']:p['sum'+t]=p['a'+t]+p['b'+t];p.pop('detail'+t,None)
 pk=k[:2];place=places.setdefault(pk,{'uf':p['uf'],'mun':p['mun'],'nm':p['nm'],'total':0});place['total']+=1
 keep=False
 for n in [55,60,65,70]:
  a=p['a1']*100>=n*p['sum1'] and p['b2']*100>=n*p['sum2'];b=p['b1']*100>=n*p['sum1'] and p['a2']*100>=n*p['sum2'];counts[str(n)][0]+=a;counts[str(n)][1]+=b
  if a or b:keep=True
 if keep:candidates.append(p)
sources=[]
for f in ['votacao_secao_2026_BR.zip','detalhe_votacao_secao_2026.zip']:sources.append({'file':f,'sha256':hashlib.file_digest(open(root/f,'rb'),'sha256').hexdigest()})
out={'schema':1,'source':'TSE — Resultados 2026','places':list(places.values()),'candidates':candidates,'excluded':len(excluded),'unpaired':unpaired,'total':sum(p['total'] for p in places.values()),'counts':counts,'detailTotals':dict(detail_totals),'voteTotals':dict(totals),'sources':sources}
p=pathlib.Path(__file__).parent/'public/data/results.json';p.write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
print('DONE',out['total'],counts,'candidate sections',len(candidates),'bytes',p.stat().st_size,flush=True)
