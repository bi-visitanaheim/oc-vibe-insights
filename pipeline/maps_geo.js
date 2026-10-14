/* Map geometry for OC Vibe Insights (Oct. 13, 2026). Run: node maps_geo.js > maps_geo.json
   U.S. states: us-atlas 3.0.1 (U.S. Census Bureau cartographic boundaries), Albers USA projection.
   World countries: world-atlas 2.0.2 (Natural Earth 1:110m), Natural Earth projection.
   Points: metro areas at their principal city and countries at their geographic center (positioning only; values come from the report tables). */
const d3 = require('d3-geo'), topo = require('topojson-client');
const usT = require('us-atlas/states-10m.json'), wT = require('world-atlas/countries-110m.json');
const r1 = s => s.replace(/(\d+\.\d)\d+/g, '$1');
const US = { w: 960, h: 600 }, WD = { w: 960, h: 470 };
const states = topo.feature(usT, usT.objects.states);
const pU = d3.geoAlbersUsa().fitSize([US.w, US.h], states), gU = d3.geoPath(pU);
const countries = topo.feature(wT, wT.objects.countries);
countries.features = countries.features.filter(f => f.properties.name !== 'Antarctica');
const pW = d3.geoNaturalEarth1().fitSize([WD.w, WD.h], countries), gW = d3.geoPath(pW);
const PTS = {  // [lon, lat]
  'Los Angeles–Long Beach–Anaheim': [-118.24, 34.05], 'Riverside–San Bernardino–Ontario': [-117.38, 33.98], 'Washington–Arlington–Alexandria': [-77.04, 38.90],
  'San Diego–Chula Vista–Carlsbad': [-117.16, 32.72], 'New York–Newark–Jersey City': [-74.01, 40.71], 'Bakersfield–Delano': [-119.02, 35.37],
  'Phoenix–Mesa–Chandler': [-112.07, 33.45], 'Dallas–Fort Worth–Arlington': [-96.80, 32.78], 'Las Vegas–Henderson': [-115.14, 36.17],
  'Las Vegas–Henderson–Paradise': [-115.14, 36.17], 'Chicago–Naperville–Elgin': [-87.63, 41.88], 'Oxnard–Thousand Oaks–Ventura': [-119.18, 34.20],
  'San Francisco–Oakland–Berkeley': [-122.42, 37.77], 'Seattle–Tacoma–Bellevue': [-122.33, 47.61], 'San Jose–Sunnyvale–Santa Clara': [-121.89, 37.34],
  'Sacramento–Roseville–Folsom': [-121.49, 38.58], 'Orlando–Kissimmee–Sanford': [-81.38, 28.54], 'Detroit–Warren–Dearborn': [-83.05, 42.33],
  'Anaheim': [-117.91, 33.84],
  'Mexico': [-102.5, 23.6], 'Canada': [-106.3, 56.1], 'Japan': [138.3, 36.2], 'United Kingdom': [-3.4, 55.4], 'China (mainland)': [104.2, 35.9], 'Australia': [133.8, -25.3]
};
const pts = {};
for (const [k, ll] of Object.entries(PTS)) {
  const u = pU(ll), w = pW(ll);
  pts[k] = { us: u ? u.map(v => +v.toFixed(1)) : null, world: w ? w.map(v => +v.toFixed(1)) : null };
}
const out = {
  us: { w: US.w, h: US.h, states: states.features.map(f => ({ name: f.properties.name, d: r1(gU(f) || '') })).filter(s => s.d) },
  world: { w: WD.w, h: WD.h, countries: countries.features.map(f => ({ name: f.properties.name, d: r1(gW(f) || '') })).filter(s => s.d) },
  pts,
  src: 'U.S. Census Bureau cartographic boundaries (us-atlas 3.0.1); Natural Earth 1:110m (world-atlas 2.0.2)'
};
process.stdout.write(JSON.stringify(out));
