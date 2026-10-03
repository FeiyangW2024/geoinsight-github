from pathlib import Path
import json,random
from pyproj import Geod
R=Path(__file__).resolve().parents[1];pois=json.loads((R/'dist/data/pois.json').read_text());g=Geod(ellps='WGS84');rnd=random.Random(20261003)
pts=[(116.31,39.98),(116.45,39.91),(116.45,39.94),(116.43,39.83)]+[(rnd.uniform(116.15,116.7),rnd.uniform(39.7,40.15)) for _ in range(8)]
results=[]
for i,(lon,lat) in enumerate(pts):
 counts=dict.fromkeys(['coffee','office_building','shopping_center','subway_entrance'],0);nearest=None
 for p in pois:
  d=g.inv(lon,lat,p['lon'],p['lat'])[2]
  if p['included'] and p['category'] in counts:
   if d<=1000:counts[p['category']]+=1
   if p['category']=='subway_entrance' and d<=3000:nearest=d if nearest is None else min(nearest,d)
 results.append({'point':{'id':str(i),'name':'reference','lon':lon,'lat':lat},'counts':counts,'nearest':nearest})
cases=[]
for _ in range(100):
 a,b=rnd.sample(pois,2);cases.append({'args':[a['lon'],a['lat'],b['lon'],b['lat']],'meters':g.inv(a['lon'],a['lat'],b['lon'],b['lat'])[2]})
# Explicit points immediately inside/outside the radius protect boundary comparisons.
for meters in [999.99,1000.01,2999.99,3000.01]:
 lon,lat,_=g.fwd(116.4,39.95,45,meters);cases.append({'args':[116.4,39.95,lon,lat],'meters':meters})
(R/'tests/reference.json').write_text(json.dumps({'results':results,'distance_cases':cases}))
print('Generated independent pyproj reference: 12 points, 104 distances')
