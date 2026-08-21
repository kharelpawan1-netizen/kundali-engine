/**
 * api/static/chart_renderer.js
 * High-precision SVG Chart Renderer for North Indian (Diamond) and South Indian (Square) Vedic Charts.
 */

const ChartRenderer = (function () {
  const PLANET_SHORT_CODES = {
    Sun: "Su",
    Moon: "Mo",
    Mars: "Ma",
    Mercury: "Me",
    Jupiter: "Ju",
    Venus: "Ve",
    Saturn: "Sa",
    Rahu: "Ra",
    Ketu: "Ke",
    Ascendant: "Asc",
  };

  const PLANET_COLORS = {
    Sun: "#f59e0b",
    Moon: "#f1f5f9",
    Mars: "#ef4444",
    Mercury: "#10b981",
    Jupiter: "#fbbf24",
    Venus: "#ec4899",
    Saturn: "#818cf8",
    Rahu: "#c084fc",
    Ketu: "#d8b4fe",
    Ascendant: "#38bdf8",
  };

  // Sign Names array (1 = Aries, ..., 12 = Pisces)
  const SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
  ];

  /**
   * Render North Indian Diamond Chart as SVG string.
   * Coordinate space: 400 x 400.
   */
  function renderNorthIndianSvg(vargaData, planetsMap, options = {}) {
    const W = 400;
    const H = 400;
    const halfW = W / 2;
    const halfH = H / 2;

    const lagnaSign = vargaData.lagna_sign; // 1 to 12
    const housePlacements = vargaData.house_placements || {}; // house 1..12 -> array of planet names

    // 12 House Polygons in North Indian diamond geometry
    // House 1: Top center diamond
    // House 2: Top-left upper triangle
    // House 3: Top-left lower triangle
    // House 4: Left center diamond
    // House 5: Bottom-left upper triangle
    // House 6: Bottom-left lower triangle
    // House 7: Bottom center diamond
    // House 8: Bottom-right lower triangle
    // House 9: Bottom-right upper triangle
    // House 10: Right center diamond
    // House 11: Top-right lower triangle
    // House 12: Top-right upper triangle

    const housePolygons = {
      1: [[halfW, 0], [halfW * 1.5, halfH * 0.5], [halfW, halfH], [halfW * 0.5, halfH * 0.5]],
      2: [[0, 0], [halfW, 0], [halfW * 0.5, halfH * 0.5]],
      3: [[0, 0], [halfW * 0.5, halfH * 0.5], [0, halfH]],
      4: [[0, halfH], [halfW * 0.5, halfH * 0.5], [halfW, halfH], [halfW * 0.5, halfH * 1.5]],
      5: [[0, halfH], [halfW * 0.5, halfH * 1.5], [0, H]],
      6: [[0, H], [halfW * 0.5, halfH * 1.5], [halfW, H]],
      7: [[halfW, halfH], [halfW * 1.5, halfH * 1.5], [halfW, H], [halfW * 0.5, halfH * 1.5]],
      8: [[halfW, H], [halfW * 1.5, halfH * 1.5], [W, H]],
      9: [[W, H], [halfW * 1.5, halfH * 1.5], [W, halfH]],
      10: [[halfW, halfH], [W, halfH], [halfW * 1.5, halfH * 1.5], [halfW * 1.5, halfH * 0.5]],
      11: [[W, halfH], [halfW * 1.5, halfH * 0.5], [W, 0]],
      12: [[halfW, 0], [W, 0], [halfW * 1.5, halfH * 0.5]],
    };

    // Label anchor centers for sign numbers & planets
    const houseCenters = {
      1: { cx: halfW, cy: halfH * 0.48, signPos: { x: halfW, y: 35 } },
      2: { cx: halfW * 0.5, cy: halfH * 0.25, signPos: { x: halfW * 0.5, y: 24 } },
      3: { cx: halfW * 0.22, cy: halfH * 0.48, signPos: { x: 20, y: halfH * 0.45 } },
      4: { cx: halfW * 0.48, cy: halfH, signPos: { x: 35, y: halfH } },
      5: { cx: halfW * 0.22, cy: halfH * 1.52, signPos: { x: 20, y: halfH * 1.55 } },
      6: { cx: halfW * 0.5, cy: halfH * 1.75, signPos: { x: halfW * 0.5, y: H - 15 } },
      7: { cx: halfW, cy: halfH * 1.52, signPos: { x: halfW, y: H - 28 } },
      8: { cx: halfW * 1.5, cy: halfH * 1.75, signPos: { x: halfW * 1.5, y: H - 15 } },
      9: { cx: halfW * 1.78, cy: halfH * 1.52, signPos: { x: W - 20, y: halfH * 1.55 } },
      10: { cx: halfW * 1.52, cy: halfH, signPos: { x: W - 35, y: halfH } },
      11: { cx: halfW * 1.78, cy: halfH * 0.48, signPos: { x: W - 20, y: halfH * 0.45 } },
      12: { cx: halfW * 1.5, cy: halfH * 0.25, signPos: { x: halfW * 1.5, y: 24 } },
    };

    let svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" class="vedic-chart-svg north-chart">`;
    svg += `<defs>
      <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="2" result="blur" />
        <feComposite in="SourceGraphic" in2="blur" operator="over" />
      </filter>
    </defs>`;

    // Background
    svg += `<rect width="${W}" height="${H}" fill="rgba(8, 11, 26, 0.95)" rx="10" />`;

    // Render 12 house interactive polygon areas
    for (let h = 1; h <= 12; h++) {
      const pts = housePolygons[h].map(p => `${p[0]},${p[1]}`).join(" ");
      const signNum = ((lagnaSign + h - 2) % 12) + 1;
      const signName = SIGN_NAMES[signNum - 1];
      const planetsInHouse = housePlacements[h] || [];

      svg += `<polygon points="${pts}" class="chart-house-poly" data-house="${h}" data-sign-num="${signNum}" data-sign-name="${signName}" fill="transparent" stroke="rgba(245, 158, 11, 0.35)" stroke-width="1.2" />`;
    }

    // Outer and diagonal geometric lines for crisp North Indian diamond layout
    svg += `<rect x="0" y="0" width="${W}" height="${H}" fill="none" stroke="#f59e0b" stroke-width="2" rx="4" />`;
    svg += `<line x1="0" y1="0" x2="${W}" y2="${H}" stroke="#f59e0b" stroke-width="1.4" />`;
    svg += `<line x1="${W}" y1="0" x2="0" y2="${H}" stroke="#f59e0b" stroke-width="1.4" />`;
    svg += `<polygon points="${halfW},0 ${W},${halfH} ${halfW},${H} 0,${halfH}" fill="none" stroke="#f59e0b" stroke-width="1.8" />`;

    // Render Sign numbers and Planet tags in each house
    for (let h = 1; h <= 12; h++) {
      const center = houseCenters[h];
      const signNum = ((lagnaSign + h - 2) % 12) + 1;
      const planetsInHouse = housePlacements[h] || [];

      // Sign number in corner/top
      svg += `<text x="${center.signPos.x}" y="${center.signPos.y}" fill="#fbbf24" font-size="11" font-weight="700" font-family="'Plus Jakarta Sans', sans-serif" text-anchor="middle" dominant-baseline="middle" opacity="0.9">${signNum}</text>`;

      // Render Planet tags
      if (planetsInHouse.length > 0) {
        const totalPlanets = planetsInHouse.length;
        const planetSpacing = 16;
        const startY = center.cy - ((totalPlanets - 1) * planetSpacing) / 2;

        planetsInHouse.forEach((pName, idx) => {
          const pCode = PLANET_SHORT_CODES[pName] || pName.substring(0, 2);
          const pColor = PLANET_COLORS[pName] || "#ffffff";
          const pObj = planetsMap ? planetsMap[pName] : null;

          let badge = "";
          if (pObj) {
            if (pObj.retrograde) badge += " <tspan fill='#ef4444' font-size='9'>R</tspan>";
            if (pObj.exalted) badge += " <tspan fill='#34d399' font-size='9'>★</tspan>";
            if (pObj.debilitated) badge += " <tspan fill='#f87171' font-size='9'>▼</tspan>";
          }

          const py = startY + idx * planetSpacing;
          svg += `<text x="${center.cx}" y="${py}" class="chart-planet-label" data-planet="${pName}" data-house="${h}" fill="${pColor}" font-size="12" font-weight="700" font-family="'Outfit', sans-serif" text-anchor="middle" dominant-baseline="middle">${pCode}${badge}</text>`;
        });
      }
    }

    svg += `</svg>`;
    return svg;
  }

  /**
   * Render South Indian Square Chart as SVG string.
   * Coordinate space: 400 x 400.
   */
  function renderSouthIndianSvg(vargaData, planetsMap, options = {}) {
    const W = 400;
    const H = 400;
    const cellW = W / 4;
    const cellH = H / 4;

    const lagnaSign = vargaData.lagna_sign; // 1 to 12
    const planetSigns = vargaData.planet_signs || {}; // Planet name -> sign 1..12

    // Map sign (1..12) to South Indian fixed grid cell coordinates:
    // Row 0: Pisces(12) [col 0], Aries(1) [col 1], Taurus(2) [col 2], Gemini(3) [col 3]
    // Row 1: Aquarius(11) [col 0], Center [cols 1-2], Cancer(4) [col 3]
    // Row 2: Capricorn(10) [col 0], Center [cols 1-2], Leo(5) [col 3]
    // Row 3: Sagittarius(9) [col 0], Scorpio(8) [col 1], Libra(7) [col 2], Virgo(6) [col 3]

    const signGridCells = {
      12: { row: 0, col: 0, name: "Pisces" },
      1: { row: 0, col: 1, name: "Aries" },
      2: { row: 0, col: 2, name: "Taurus" },
      3: { row: 0, col: 3, name: "Gemini" },
      4: { row: 1, col: 3, name: "Cancer" },
      5: { row: 2, col: 3, name: "Leo" },
      6: { row: 3, col: 3, name: "Virgo" },
      7: { row: 3, col: 2, name: "Libra" },
      8: { row: 3, col: 1, name: "Scorpio" },
      9: { row: 3, col: 0, name: "Sagittarius" },
      10: { row: 2, col: 0, name: "Capricorn" },
      11: { row: 1, col: 0, name: "Aquarius" },
    };

    // Group planets by sign
    const signPlanets = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [] };
    for (const [pName, pSign] of Object.entries(planetSigns)) {
      if (signPlanets[pSign]) {
        signPlanets[pSign].push(pName);
      }
    }

    let svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" class="vedic-chart-svg south-chart">`;

    // Background
    svg += `<rect width="${W}" height="${H}" fill="rgba(8, 11, 26, 0.95)" rx="8" />`;

    // Central Box
    svg += `<rect x="${cellW}" y="${cellH}" width="${cellW * 2}" height="${cellH * 2}" fill="rgba(4, 6, 16, 0.95)" stroke="#f59e0b" stroke-width="1.5" />`;
    svg += `<text x="${W / 2}" y="${H / 2 - 8}" fill="#fbbf24" font-family="'Cinzel', serif" font-size="14" font-weight="700" text-anchor="middle" dominant-baseline="middle">${vargaData.code || "D1"} KUNDALI</text>`;
    svg += `<text x="${W / 2}" y="${H / 2 + 14}" fill="#94a3b8" font-family="'Outfit', sans-serif" font-size="11" text-anchor="middle" dominant-baseline="middle">Lagna: ${SIGN_NAMES[lagnaSign - 1]}</text>`;

    // Draw 12 cells
    for (let s = 1; s <= 12; s++) {
      const cell = signGridCells[s];
      const x = cell.col * cellW;
      const y = cell.row * cellH;
      const isLagna = s === lagnaSign;
      const houseNum = ((s - lagnaSign + 12) % 12) + 1;

      svg += `<g class="south-cell-group" data-sign="${s}" data-sign-name="${cell.name}" data-house="${houseNum}">`;
      svg += `<rect x="${x}" y="${y}" width="${cellW}" height="${cellH}" fill="transparent" stroke="rgba(245, 158, 11, 0.4)" stroke-width="1.2" class="chart-house-poly" />`;

      // Sign name in subtle corner
      svg += `<text x="${x + 6}" y="${y + 12}" fill="#64748b" font-size="9" font-weight="600" font-family="'Plus Jakarta Sans', sans-serif">${cell.name.substring(0, 3)} (${s})</text>`;

      // Lagna marker (ASC)
      if (isLagna) {
        svg += `<line x1="${x}" y1="${y}" x2="${x + 24}" y2="${y + 24}" stroke="#38bdf8" stroke-width="2" />`;
        svg += `<text x="${x + cellW - 6}" y="${y + 12}" fill="#38bdf8" font-size="10" font-weight="800" text-anchor="end" font-family="'Outfit', sans-serif">ASC</text>`;
      }

      // House number tag
      svg += `<text x="${x + cellW - 6}" y="${y + cellH - 6}" fill="#fbbf24" font-size="10" font-weight="600" text-anchor="end" font-family="'Plus Jakarta Sans', sans-serif">H${houseNum}</text>`;

      // Planets in this sign
      const planetsInSign = signPlanets[s] || [];
      if (planetsInSign.length > 0) {
        const startY = y + 26;
        const spacing = 15;

        planetsInSign.forEach((pName, idx) => {
          const pCode = PLANET_SHORT_CODES[pName] || pName.substring(0, 2);
          const pColor = PLANET_COLORS[pName] || "#ffffff";
          const pObj = planetsMap ? planetsMap[pName] : null;

          let badge = "";
          if (pObj) {
            if (pObj.retrograde) badge += " <tspan fill='#ef4444' font-size='8'>R</tspan>";
            if (pObj.exalted) badge += " <tspan fill='#34d399' font-size='8'>★</tspan>";
            if (pObj.debilitated) badge += " <tspan fill='#f87171' font-size='8'>▼</tspan>";
          }

          svg += `<text x="${x + cellW / 2}" y="${startY + idx * spacing}" class="chart-planet-label" data-planet="${pName}" data-house="${houseNum}" fill="${pColor}" font-size="11" font-weight="700" font-family="'Outfit', sans-serif" text-anchor="middle" dominant-baseline="middle">${pCode}${badge}</text>`;
        });
      }

      svg += `</g>`;
    }

    // Outer border
    svg += `<rect x="0" y="0" width="${W}" height="${H}" fill="none" stroke="#f59e0b" stroke-width="2" rx="4" />`;

    svg += `</svg>`;
    return svg;
  }

  return {
    renderNorthIndianSvg,
    renderSouthIndianSvg,
  };
})();
