// Initialize heatmap instance for the vowel chart
var heatmapInstance = h337.create({
    container: document.getElementById('vowelQuadrilateral'),
    maxOpacity: 0.6,
    radius: 50,
    blur: 0.75,
});

// Function to draw heatmap zones
function drawHeatmapZones(zoneIntensities, tenseIntensity, laxIntensity) {
    const parentRect = document.getElementById('vowelQuadrilateral').getBoundingClientRect();
    const width = parentRect.width;
    const height = parentRect.height;
    const points = [];

    // Define the quadrilateral zones with vertices relative to the vowel quadrilateral
    const zones = {
        front: [
            { x: width * 0.17, y: height * 0.1 },
            { x: width * 0.5, y: height * 0.1 },
            { x: width * 0.65, y: height * 0.9 },
            { x: width * 0.55, y: height * 0.9 }
        ],
        central: [
            { x: width * 0.4, y: height * 0.1 },
            { x: width * 0.8, y: height * 0.1 },
            { x: width * 0.83, y: height * 0.9 },
            { x: width * 0.65, y: height * 0.9 }
        ],
        back: [
            { x: width * 0.65, y: height * 0.1 },
            { x: width * 0.92, y: height * 0.1 },
            { x: width * 0.92, y: height * 0.9 },
            { x: width * 0.8, y: height * 0.9 }
        ],
        high: [
            { x: width * 0.16, y: height * 0.1 },
            { x: width * 0.92, y: height * 0.1 },
            { x: width * 0.92, y: height * 0.35 },
            { x: width * 0.33, y: height * 0.35 }
        ],
        mid: [
            { x: width * 0.3, y: height * 0.38 },
            { x: width * 0.92, y: height * 0.38 },
            { x: width * 0.92, y: height * 0.7 },
            { x: width * 0.45, y: height * 0.7 }
        ],
        low: [
            { x: width * 0.43, y: height * 0.7 },
            { x: width * 0.55, y: height * 0.9 },
            { x: width * 0.92, y: height * 0.9 },
            { x: width * 0.92, y: height * 0.7 }
        ],
        tenseHigh: [
            { x: width * 0.16, y: height * 0.1 },
            { x: width * 0.92, y: height * 0.1 },
            { x: width * 0.92, y: height * 0.15 },
            { x: width * 0.23, y: height * 0.15 }
        ],
        laxHigh: [
            { x: width * 0.26, y: height * 0.25 },
            { x: width * 0.92, y: height * 0.25 },
            { x: width * 0.92, y: height * 0.35 },
            { x: width * 0.33, y: height * 0.35 }
        ],
        tenseMid: [
            { x: width * 0.33, y: height * 0.4 },
            { x: width * 0.92, y: height * 0.4 },
            { x: width * 0.92, y: height * 0.55 },
                        { x: width * 0.44, y: height * 0.55 }
        ],
        laxMid: [
            { x: width * 0.4, y: height * 0.6 },
            { x: width * 0.92, y: height * 0.6 },
            { x: width * 0.92, y: height * 0.7 },
            { x: width * 0.45, y: height * 0.7 }
        ],
        tenseLow: [
            { x: width * 0.45, y: height * 0.8 },
            { x: width * 0.51, y: height * 0.82 },
            { x: width * 0.92, y: height * 0.82 },
            { x: width * 0.92, y: height * 0.8 }
        ],
        laxLow: [
            { x: width * 0.53, y: height * 0.87 },
            { x: width * 0.55, y: height * 0.95 },
            { x: width * 0.92, y: height * 0.95 },
            { x: width * 0.92, y: height * 0.87 }
        ],
    };

    // Function to generate points within a quadrilateral
    function generatePoints(vertices, intensity, steps = 20) {
        const [v1, v2, v3, v4] = vertices;

        for (let i = 0; i <= steps; i++) {
            const t = i / steps;
            const topX = v1.x + t * (v2.x - v1.x);
            const topY = v1.y + t * (v2.y - v1.y);
            const bottomX = v4.x + t * (v3.x - v4.x);
            const bottomY = v4.y + t * (v3.y - v4.y);

            for (let j = 0; j <= steps; j++) {
                const s = j / steps;
                const x = topX + s * (bottomX - topX);
                const y = topY + s * (bottomY - topY);

                points.push({
                    x: Math.round(x),
                    y: Math.round(y),
                    value: intensity,
                    radius: 20 // Set a smaller radius for point density
                });
            }
        }
    }

    // Generate points for each zone with the corresponding intensity
    Object.keys(zoneIntensities).forEach(zone => {
        if (zones[zone]) {
            generatePoints(zones[zone], zoneIntensities[zone]);
        }
    });

    // Generate points for tense and lax zones with corresponding intensities
    ['tenseHigh', 'tenseMid', 'tenseLow'].forEach(zone => {
        generatePoints(zones[zone], tenseIntensity);
    });

    ['laxHigh', 'laxMid', 'laxLow'].forEach(zone => {
        generatePoints(zones[zone], laxIntensity);
    });

    // Set the heatmap data
    heatmapInstance.setData({
        max: 100,
        data: points
    });
}

// Function to show only the vowels in the provided array
function showVowels(vowelArray) {
    // Hide all vowels
    const allVowels = document.querySelectorAll('.vowel');
    allVowels.forEach(vowel => vowel.style.display = 'none');

    // Show only the vowels in the vowelArray
    vowelArray.forEach(vowel => {
        const vowelElement = document.querySelector(`.vowel.${CSS.escape(vowel)}`);
        if (vowelElement) {
            vowelElement.style.display = 'inline';
        }
    });
}

// Example usage:
const vowelsToShow = [
    'i', 'y', 'ɨ', 'ʉ', 'ɯ', 'u',      // Close vowels
    'ɪ', 'ʏ', 'ʊ',                     // Near-close vowels
    'e', 'ø', 'ɘ', 'ɵ', 'ɤ', 'o',      // Close-mid vowels
    'ə',                               // Mid vowel
    'ɛ', 'œ', 'ɜ', 'ɞ', 'ʌ', 'ɔ',      // Open-mid vowels
    'æ', 'ɐ',                          // Near-open vowels
    'a', 'ɶ', 'ɑ', 'ɒ'                 // Open vowels
];
showVowels(vowelsToShow);

// Set the intensity for each zone
const zoneIntensities = {
    front: 25,   // High intensity for front
    central: 2,  // Medium intensity for central
    back: 0,     // High intensity for back
    high: 20,     // High intensity for high
    mid: 0,      // Medium intensity for mid
    low: 0       // Low intensity for low
};

// Set the intensity for tense and lax zones
const tenseIntensity = 0;  // Intensity for tense zones
const laxIntensity = 5;   // Intensity for lax zones

drawHeatmapZones(zoneIntensities, tenseIntensity, laxIntensity);

