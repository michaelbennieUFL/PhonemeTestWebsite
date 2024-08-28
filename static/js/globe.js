// Assuming highlightLanguages is injected from the Flask template
fetch('../static/geodata/Languages_with_List_of_Countries.json')
  .then(response => response.json())
  .then(languageCountryMapping => {
    processMap(languageCountryMapping);
  });

function processMap(languageCountryMapping) {
  const highlightCountries = {};
  highlightLanguages.forEach(([languageCode, languageName, transparency]) => {
    const countries = languageCountryMapping[languageCode] || [];
    countries.forEach(countryCode => {
      if (!highlightCountries[countryCode]) {
        highlightCountries[countryCode] = { transparency: 0, languages: [] };
      }
      highlightCountries[countryCode].transparency += transparency;
      highlightCountries[countryCode].languages.push(languageName);
    });
  });

  const world = Globe()
    (document.getElementById('globeViz'))
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
    .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
    .width(document.getElementById('globeViz').clientWidth)
    .height(document.getElementById('globeViz').clientHeight)
    .backgroundColor('rgba(0,0,0,0)')
    .showGlobe(true)
    .showAtmosphere(false);

  window.addEventListener('resize', () => {
    const globeViz = document.getElementById('globeViz');
    world.width(globeViz.clientWidth);
    world.height(globeViz.clientHeight);
  });

  fetch('//unpkg.com/world-atlas/land-110m.json').then(res => res.json())
    .then(landTopo => {
      world
        .polygonsData(topojson.feature(landTopo, landTopo.objects.land).features)
        .polygonCapMaterial(new THREE.MeshLambertMaterial({
          color: 'rgba(37, 255, 20, 0.1)',
          side: THREE.DoubleSide
        }))
        .polygonSideColor(() => 'rgba(0,0,0,0)')
        .polygonAltitude(({ properties: d }) => {
          return highlightCountries[d.ISO_A2] ? 0.06 : 0;
        });
    });

  fetch('../static/geodata/ne_110m_admin_0_countries.geojson')
    .then(res => res.json())
    .then(countries => {
      const filteredCountries = {
        ...countries,
        features: countries.features.filter(f => Object.keys(highlightCountries).includes(f.properties.ISO_A2))
      };

      world
        .hexPolygonsData(filteredCountries.features)
        .hexPolygonResolution(4)
        .hexPolygonMargin(0.2)
        .hexPolygonUseDots(false)
          .hexPolygonColor(({ properties: d }) => {
          const { transparency } = highlightCountries[d.ISO_A2];
          const finalTransparency = Math.min(transparency, 1); // 限制透明度最大值為1
          return `rgba(57, 255, 20, ${finalTransparency})`;  // 霓虹綠色並應用透明度
        })
        .hexPolygonLabel(({ properties: d }) => {
          const { languages } = highlightCountries[d.ISO_A2];
          return `
            <b>${d.ADMIN} (${d.ISO_A2})</b> <br />
            Languages: <i>${languages.join(', ')}</i>
          `;
        });
    });
}

