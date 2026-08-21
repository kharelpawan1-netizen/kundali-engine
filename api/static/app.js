/**
 * api/static/app.js
 * Master Application Controller for Vedic Kundali Dashboard.
 */

(function () {
  // Global State
  const state = {
    chartData: null,
    chartStyle: "north", // "north" | "south"
    currentVarga: "D1",
    savedProfiles: [],
    sampleProfiles: [],
    citySearchTimer: null,
  };

  // DOM Elements
  const elements = {
    chartForm: document.getElementById("chartForm"),
    nativeName: document.getElementById("nativeName"),
    nativeGender: document.getElementById("nativeGender"),
    birthDate: document.getElementById("birthDate"),
    birthTime: document.getElementById("birthTime"),
    birthPlace: document.getElementById("birthPlace"),
    btnClearCity: document.getElementById("btnClearCity"),
    cityDropdown: document.getElementById("cityDropdown"),
    inputLat: document.getElementById("inputLat"),
    inputLng: document.getElementById("inputLng"),
    inputTz: document.getElementById("inputTz"),
    btnToggleManualCoords: document.getElementById("btnToggleManualCoords"),
    manualCoordsDrawer: document.getElementById("manualCoordsDrawer"),
    ayanamshaSelect: document.getElementById("ayanamshaSelect"),
    btnCalculate: document.getElementById("btnCalculate"),
    btnSaveCurrent: document.getElementById("btnSaveCurrent"),
    loadingPanel: document.getElementById("loadingPanel"),
    resultsContainer: document.getElementById("resultsContainer"),

    // Hero Overview
    heroNativeName: document.getElementById("heroNativeName"),
    heroNativeMeta: document.getElementById("heroNativeMeta"),
    heroAyanamsha: document.getElementById("heroAyanamsha"),
    heroLagna: document.getElementById("heroLagna"),
    heroLagnaDegree: document.getElementById("heroLagnaDegree"),
    heroRasi: document.getElementById("heroRasi"),
    heroNakshatra: document.getElementById("heroNakshatra"),
    heroSunSign: document.getElementById("heroSunSign"),
    heroSunDignity: document.getElementById("heroSunDignity"),
    heroActiveDasha: document.getElementById("heroActiveDasha"),
    heroActivePratyantar: document.getElementById("heroActivePratyantar"),

    // Chart Canvas & Toolbar
    chartStyleButtons: document.querySelectorAll("[data-chart-style]"),
    vargaSelect: document.getElementById("vargaSelect"),
    currentChartTitle: document.getElementById("currentChartTitle"),
    chartSvgWrapper: document.getElementById("chartSvgWrapper"),
    metricLagnaDeg: document.getElementById("metricLagnaDeg"),
    metricLagnaNak: document.getElementById("metricLagnaNak"),
    metricLagnaLord: document.getElementById("metricLagnaLord"),
    metricMoonDeg: document.getElementById("metricMoonDeg"),
    metricTithi: document.getElementById("metricTithi"),
    dignityTagsCloud: document.getElementById("dignityTagsCloud"),
    quickYogaCount: document.getElementById("quickYogaCount"),
    quickYogaList: document.getElementById("quickYogaList"),

    // Workspace Tabs
    workspaceTabButtons: document.querySelectorAll(".tab-btn"),
    tabPanes: document.querySelectorAll(".tab-pane"),
    tabYogaCount: document.getElementById("tabYogaCount"),

    // Tab Contents
    planetsTableBody: document.getElementById("planetsTableBody"),
    housesGrid: document.getElementById("housesGrid"),
    dashaCalcTimestamp: document.getElementById("dashaCalcTimestamp"),
    dashaLevelsRow: document.getElementById("dashaLevelsRow"),
    dashaAccordionList: document.getElementById("dashaAccordionList"),
    yogasGrid: document.getElementById("yogasGrid"),
    synthPersonality: document.getElementById("synthPersonality"),
    synthCareer: document.getElementById("synthCareer"),
    synthWealth: document.getElementById("synthWealth"),
    synthHealth: document.getElementById("synthHealth"),
    synthThemes: document.getElementById("synthThemes"),
    vargasMiniGrid: document.getElementById("vargasMiniGrid"),

    // Modals
    btnSampleProfiles: document.getElementById("btnSampleProfiles"),
    btnSavedProfiles: document.getElementById("btnSavedProfiles"),
    savedCount: document.getElementById("savedCount"),
    btnPrintReport: document.getElementById("btnPrintReport"),
    modalSampleProfiles: document.getElementById("modalSampleProfiles"),
    btnCloseSampleModal: document.getElementById("btnCloseSampleModal"),
    sampleProfilesList: document.getElementById("sampleProfilesList"),
    modalSavedProfiles: document.getElementById("modalSavedProfiles"),
    btnCloseSavedModal: document.getElementById("btnCloseSavedModal"),
    savedProfilesList: document.getElementById("savedProfilesList"),
    btnExportJson: document.getElementById("btnExportJson"),
    importJsonInput: document.getElementById("importJsonInput"),

    // Tooltip & Canvas
    astralTooltip: document.getElementById("astralTooltip"),
    starsCanvas: document.getElementById("starsCanvas"),
  };

  // ============================================================
  // Initialize Application
  // ============================================================
  function init() {
    initStarsCanvas();
    loadSavedProfilesFromStorage();
    fetchSampleProfiles();
    setupEventListeners();

    // Trigger initial calculation with default form values
    submitChartCalculation();
  }

  // ============================================================
  // Background Cosmic Stars Canvas
  // ============================================================
  function initStarsCanvas() {
    const canvas = elements.starsCanvas;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener("resize", () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    const stars = Array.from({ length: 90 }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 1.5 + 0.3,
      alpha: Math.random() * 0.8 + 0.2,
      speed: Math.random() * 0.015 + 0.005,
    }));

    function animateStars() {
      ctx.clearRect(0, 0, width, height);
      stars.forEach((star) => {
        star.alpha += star.speed;
        if (star.alpha > 1 || star.alpha < 0.2) star.speed = -star.speed;
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(251, 191, 36, ${Math.abs(star.alpha)})`;
        ctx.fill();
      });
      requestAnimationFrame(animateStars);
    }
    animateStars();
  }

  // ============================================================
  // Event Listeners Setup
  // ============================================================
  function setupEventListeners() {
    // Form Submit
    elements.chartForm.addEventListener("submit", (e) => {
      e.preventDefault();
      submitChartCalculation();
    });

    // Preset Chips
    document.querySelectorAll(".chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        elements.birthPlace.value = chip.dataset.city;
        elements.inputLat.value = chip.dataset.lat;
        elements.inputLng.value = chip.dataset.lng;
        elements.inputTz.value = chip.dataset.tz;
      });
    });

    // Toggle Manual Coordinates Drawer
    elements.btnToggleManualCoords.addEventListener("click", () => {
      const drawer = elements.manualCoordsDrawer;
      const isHidden = drawer.style.display === "none";
      drawer.style.display = isHidden ? "block" : "none";
      elements.btnToggleManualCoords.textContent = isHidden
        ? "Manual Coordinates ▴"
        : "Manual Coordinates ▾";
    });

    // City Autocomplete Search
    elements.birthPlace.addEventListener("input", (e) => {
      clearTimeout(state.citySearchTimer);
      const val = e.target.value.trim();
      if (val.length < 2) {
        elements.cityDropdown.style.display = "none";
        return;
      }
      state.citySearchTimer = setTimeout(() => {
        fetchCitySuggestions(val);
      }, 250);
    });

    elements.btnClearCity.addEventListener("click", () => {
      elements.birthPlace.value = "";
      elements.cityDropdown.style.display = "none";
      elements.birthPlace.focus();
    });

    document.addEventListener("click", (e) => {
      if (!elements.birthPlace.contains(e.target) && !elements.cityDropdown.contains(e.target)) {
        elements.cityDropdown.style.display = "none";
      }
    });

    // Chart Style Toggle (North / South)
    elements.chartStyleButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        elements.chartStyleButtons.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        state.chartStyle = btn.dataset.chartStyle;
        renderActiveChart();
      });
    });

    // Varga Divisional Chart Select
    elements.vargaSelect.addEventListener("change", (e) => {
      state.currentVarga = e.target.value;
      renderActiveChart();
    });

    // Workspace Tabs
    elements.workspaceTabButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        elements.workspaceTabButtons.forEach((b) => b.classList.remove("active"));
        elements.tabPanes.forEach((p) => p.classList.remove("active"));
        btn.classList.add("active");
        const targetPane = document.getElementById(btn.dataset.tab);
        if (targetPane) targetPane.classList.add("active");
      });
    });

    // Modals
    elements.btnSampleProfiles.addEventListener("click", () => {
      elements.modalSampleProfiles.style.display = "flex";
    });
    elements.btnCloseSampleModal.addEventListener("click", () => {
      elements.modalSampleProfiles.style.display = "none";
    });

    elements.btnSavedProfiles.addEventListener("click", () => {
      renderSavedProfilesList();
      elements.modalSavedProfiles.style.display = "flex";
    });
    elements.btnCloseSavedModal.addEventListener("click", () => {
      elements.modalSavedProfiles.style.display = "none";
    });

    elements.btnSaveCurrent.addEventListener("click", saveCurrentProfile);
    elements.btnPrintReport.addEventListener("click", () => window.print());

    elements.btnExportJson.addEventListener("click", exportProfilesToJson);
    elements.importJsonInput.addEventListener("change", importProfilesFromJson);

    // Global Tooltip Hover Setup for SVG Charts
    setupTooltipInteractions();
  }

  // ============================================================
  // City Search & Geocoding
  // ============================================================
  async function fetchCitySuggestions(query) {
    try {
      const res = await fetch(`/api/cities?q=${encodeURIComponent(query)}&limit=10`);
      const data = await res.json();
      if (data.results && data.results.length > 0) {
        elements.cityDropdown.innerHTML = data.results
          .map(
            (c) => `
          <div class="city-item" data-name="${c.name}" data-lat="${c.latitude}" data-lng="${c.longitude}" data-tz="${c.timezone}">
            <span class="city-item-name">📍 ${c.name}</span>
            <span class="city-item-tz">${c.timezone}</span>
          </div>
        `
          )
          .join("");
        elements.cityDropdown.style.display = "block";

        elements.cityDropdown.querySelectorAll(".city-item").forEach((item) => {
          item.addEventListener("click", () => {
            elements.birthPlace.value = item.dataset.name;
            elements.inputLat.value = item.dataset.lat;
            elements.inputLng.value = item.dataset.lng;
            elements.inputTz.value = item.dataset.tz;
            elements.cityDropdown.style.display = "none";
          });
        });
      } else {
        elements.cityDropdown.style.display = "none";
      }
    } catch (err) {
      console.warn("City autocomplete error:", err);
    }
  }

  // ============================================================
  // Chart Calculation Request
  // ============================================================
  async function submitChartCalculation() {
    const payload = {
      name: elements.nativeName.value.trim() || "Native",
      gender: elements.nativeGender.value,
      birth_date: elements.birthDate.value,
      birth_time: elements.birthTime.value,
      place: elements.birthPlace.value.trim() || "Kathmandu, Nepal",
      latitude: parseFloat(elements.inputLat.value) || 27.7172,
      longitude: parseFloat(elements.inputLng.value) || 85.324,
      timezone: elements.inputTz.value.trim() || "Asia/Kathmandu",
      elevation: 0.0,
      ayanamsha: elements.ayanamshaSelect.value || "LAHIRI",
    };

    // UI Loading State
    elements.loadingPanel.style.display = "block";
    elements.resultsContainer.style.opacity = "0.4";
    elements.btnCalculate.disabled = true;

    try {
      const response = await fetch("/api/chart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Chart calculation failed.");
      }

      const chartData = await response.json();
      state.chartData = chartData;

      // Populate all Dashboard components
      renderCompleteDashboard(chartData);
    } catch (err) {
      alert(`⚠️ Error: ${err.message}`);
      console.error(err);
    } finally {
      elements.loadingPanel.style.display = "none";
      elements.resultsContainer.style.opacity = "1";
      elements.btnCalculate.disabled = false;
    }
  }

  // ============================================================
  // Main Dashboard Rendering
  // ============================================================
  function renderCompleteDashboard(data) {
    const { native, ascendant, planets, planets_map, houses, vargas, dashas, yogas, synthesis } = data;

    // 1. Hero Overview Banner
    elements.heroNativeName.textContent = native.name;
    elements.heroNativeMeta.textContent = `Born: ${native.birth_date_display} at ${native.birth_time_display} • ${native.place} (${native.timezone})`;
    elements.heroAyanamsha.textContent = `${native.ayanamsa_name}: ${native.ayanamsa_dms}`;

    elements.heroLagna.textContent = `${ascendant.sign} (${ascendant.sign_sanskrit.split(" ")[0]})`;
    elements.heroLagnaDegree.textContent = `${ascendant.sign_degree_dms} • Lord: ${ascendant.sign_lord}`;

    elements.heroRasi.textContent = `${native.janma_rasi || "—"}`;
    elements.heroNakshatra.textContent = `${native.janma_nakshatra} (Pada ${native.janma_pada}) • Lord: ${ascendant.nakshatra_lord || "—"}`;

    elements.heroSunSign.textContent = `${native.sun_sign || "—"}`;
    const sunObj = planets_map["Sun"];
    elements.heroSunDignity.textContent = sunObj ? `${sunObj.dignity} in House ${sunObj.house}` : "—";

    const activeChain = dashas.active_chain;
    if (activeChain && activeChain.mahadasha) {
      elements.heroActiveDasha.textContent = `${activeChain.mahadasha.lord} MD / ${activeChain.antardasha ? activeChain.antardasha.lord : ""} AD`;
      elements.heroActivePratyantar.textContent = `${activeChain.pratyantardasha ? activeChain.pratyantardasha.lord + " PD" : ""} • ${activeChain.sookshma ? activeChain.sookshma.lord + " SD" : ""}`;
    }

    // 2. Key Metrics in Side Panel
    elements.metricLagnaDeg.textContent = ascendant.sign_degree_dms;
    elements.metricLagnaNak.textContent = `${ascendant.nakshatra} (${ascendant.pada})`;
    elements.metricLagnaLord.textContent = `${ascendant.sign_lord}`;
    const moonObj = planets_map["Moon"];
    elements.metricMoonDeg.textContent = moonObj ? moonObj.sign_degree_dms : "—";
    elements.metricTithi.textContent = `${moonObj ? moonObj.nakshatra : "Sidereal Lunar"}`;

    // Dignity Cloud
    renderDignityTagsCloud(planets);

    // Detected Yogas Quick Summary
    const detectedYogas = yogas.detected || [];
    elements.quickYogaCount.textContent = detectedYogas.length;
    elements.tabYogaCount.textContent = detectedYogas.length;
    elements.quickYogaList.innerHTML = detectedYogas.length
      ? detectedYogas
          .slice(0, 5)
          .map(
            (y) => `
        <li class="quick-yoga-item">
          <span>${y.name}</span>
          <span class="badge badge-gold">${y.nature}</span>
        </li>
      `
          )
          .join("")
      : `<li class="quick-yoga-item"><span>Standard Parashari Placements</span></li>`;

    // 3. Render Active Chart (North/South Indian SVG)
    renderActiveChart();

    // 4. Tab 1: Planets Table
    renderPlanetsTable(planets);

    // 5. Tab 2: Houses Grid
    renderHousesGrid(houses, planets_map);

    // 6. Tab 3: Vimshottari Dasha Hierarchy & Timeline
    renderDashaSection(dashas);

    // 7. Tab 4: Vedic Yogas Cards
    renderYogasGrid(yogas.all || []);

    // 8. Tab 5: Life Synthesis
    renderSynthesis(synthesis, data);

    // 9. Tab 6: Shodashavarga Grid
    renderVargasGrid(vargas, planets_map);
  }

  // ============================================================
  // Chart Rendering Handler
  // ============================================================
  function renderActiveChart() {
    if (!state.chartData) return;
    const vargas = state.chartData.vargas;
    const vargaKey = state.currentVarga || "D1";
    const vargaData = vargas[vargaKey] || vargas["D1"];
    const planetsMap = state.chartData.planets_map;

    elements.currentChartTitle.textContent = `${vargaData.code} • ${vargaData.title.toUpperCase()}`;

    let svgMarkup = "";
    if (state.chartStyle === "south") {
      svgMarkup = ChartRenderer.renderSouthIndianSvg(vargaData, planetsMap);
    } else {
      svgMarkup = ChartRenderer.renderNorthIndianSvg(vargaData, planetsMap);
    }

    elements.chartSvgWrapper.innerHTML = svgMarkup;
  }

  // ============================================================
  // Dignity Highlights Cloud
  // ============================================================
  function renderDignityTagsCloud(planets) {
    let pills = "";
    planets.forEach((p) => {
      if (p.exalted) {
        pills += `<span class="dignity-pill dignity-exalted">★ ${p.name} Exalted (${p.sign})</span>`;
      } else if (p.moolatrikona) {
        pills += `<span class="dignity-pill dignity-moolatrikona">✦ ${p.name} Moolatrikona</span>`;
      } else if (p.own_sign) {
        pills += `<span class="dignity-pill dignity-own">🛡️ ${p.name} Own Sign (${p.sign})</span>`;
      } else if (p.debilitated) {
        pills += `<span class="dignity-pill dignity-debilitated">▼ ${p.name} Debilitated (${p.sign})</span>`;
      }
    });

    if (!pills) {
      pills = `<span class="dignity-pill" style="background:rgba(255,255,255,0.05);color:var(--text-muted)">Balanced Planetary Placements</span>`;
    }
    elements.dignityTagsCloud.innerHTML = pills;
  }

  // ============================================================
  // Tab 1: Planets Table
  // ============================================================
  function renderPlanetsTable(planets) {
    elements.planetsTableBody.innerHTML = planets
      .map((p) => {
        let dignityClass = "";
        if (p.exalted) dignityClass = "dignity-exalted";
        else if (p.moolatrikona) dignityClass = "dignity-moolatrikona";
        else if (p.own_sign) dignityClass = "dignity-own";
        else if (p.debilitated) dignityClass = "dignity-debilitated";

        const motionBadge = p.retrograde
          ? `<span class="motion-badge motion-retro">Retro (R)</span>`
          : `<span class="motion-badge motion-direct">Direct</span>`;

        return `
        <tr>
          <td>
            <div class="planet-name-cell">
              <span class="planet-icon-dot" style="background: ${p.color}"></span>
              <strong>${p.name}</strong> <span style="font-size:11px;color:var(--text-dim)">(${p.sanskrit_name.split(" ")[0]})</span>
            </div>
          </td>
          <td>${p.sign}</td>
          <td>${p.sign_lord}</td>
          <td><strong>${p.sign_degree_dms}</strong></td>
          <td><span class="badge badge-gold">House ${p.house}</span></td>
          <td>${p.nakshatra} (${p.pada})</td>
          <td>${p.nakshatra_lord}</td>
          <td><span class="dignity-pill ${dignityClass}">${p.dignity}</span></td>
          <td>${motionBadge} <span style="font-size:11px;color:var(--text-dim)">(${p.speed > 0 ? "+" : ""}${p.speed.toFixed(3)}°/d)</span></td>
        </tr>
      `;
      })
      .join("");
  }

  // ============================================================
  // Tab 2: Houses Grid
  // ============================================================
  function renderHousesGrid(houses, planetsMap) {
    elements.housesGrid.innerHTML = houses
      .map((h) => {
        const occupantPills = h.occupants.length
          ? h.occupants
              .map((pName) => {
                const pColor = (planetsMap[pName] && planetsMap[pName].color) || "#fff";
                return `<span class="occupant-pill" style="border-color:${pColor}; color:${pColor}">● ${pName}</span>`;
              })
              .join(" ")
          : `<span style="color:var(--text-dim);font-size:11px;">Empty</span>`;

        const aspectsText = h.aspecting_planets.length
          ? `Aspects: ${h.aspecting_planets.join(", ")}`
          : `No direct drishti`;

        return `
        <div class="house-card">
          <div class="house-card-header">
            <span class="house-num-badge">BHAVA ${h.house}</span>
            <span class="house-sign-tag">${h.sign} (Lord: ${h.sign_lord})</span>
          </div>
          <div class="house-occupants-list">
            <span class="occupants-label">Occupants:</span>
            <div class="occupants-badges">${occupantPills}</div>
          </div>
          <div class="house-aspects-text">${aspectsText}</div>
          <div class="house-domains-desc">${h.significance_domains}</div>
        </div>
      `;
      })
      .join("");
  }

  // ============================================================
  // Tab 3: Vimshottari Dasha Explorer
  // ============================================================
  function renderDashaSection(dashas) {
    const chain = dashas.active_chain;
    elements.dashaCalcTimestamp.textContent = `As of ${new Date().toLocaleDateString()}`;

    // Active Chain Cards
    const levels = [
      { key: "mahadasha", label: "Mahadasha (MD)" },
      { key: "antardasha", label: "Antardasha (AD)" },
      { key: "pratyantardasha", label: "Pratyantardasha (PD)" },
      { key: "sookshma", label: "Sookshma (SD)" },
      { key: "prana", label: "Prana Dasha" },
      { key: "deha", label: "Deha Dasha" },
    ];

    elements.dashaLevelsRow.innerHTML = levels
      .map((lvl) => {
        const item = chain ? chain[lvl.key] : null;
        if (!item) return "";
        return `
        <div class="dasha-node active-node">
          <div class="node-level">${lvl.label}</div>
          <div class="node-lord">${item.lord}</div>
          <div class="node-dates">${item.duration ? `(${item.duration})` : ""}</div>
        </div>
      `;
      })
      .join("");

    // Accordion Timeline
    elements.dashaAccordionList.innerHTML = dashas.mahadashas
      .map((md, idx) => {
        const isRunning = md.is_active;
        const runningTag = isRunning ? `<span class="md-running-tag">CURRENT</span>` : "";

        const adRows = md.antardashas
          .map((ad) => {
            const adActiveStyle = ad.is_active ? 'style="font-weight:700; color:var(--gold-light)"' : "";
            const adMarker = ad.is_active ? " ◀ Active" : "";
            return `
            <tr ${adActiveStyle}>
              <td><strong>${ad.lord}</strong>${adMarker}</td>
              <td>${ad.start_display}</td>
              <td>${ad.end_display}</td>
              <td>${ad.duration}</td>
            </tr>
          `;
          })
          .join("");

        return `
        <div class="mahadasha-item ${isRunning ? "is-running expanded" : ""}" data-md-index="${idx}">
          <div class="mahadasha-header">
            <div class="md-lord-title">
              <span>● ${md.lord} Mahadasha</span>
              ${runningTag}
            </div>
            <div class="md-dates-info">
              <span>${md.start_display} → ${md.end_display} (${md.years} yrs)</span>
              <span class="accordion-icon">▾</span>
            </div>
          </div>
          <div class="antardasha-container">
            <table class="antardasha-table">
              <thead>
                <tr>
                  <th>Antardasha Lord</th>
                  <th>Start Date</th>
                  <th>End Date</th>
                  <th>Duration</th>
                </tr>
              </thead>
              <tbody>
                ${adRows}
              </tbody>
            </table>
          </div>
        </div>
      `;
      })
      .join("");

    // Accordion click interactions
    elements.dashaAccordionList.querySelectorAll(".mahadasha-header").forEach((header) => {
      header.addEventListener("click", () => {
        const item = header.closest(".mahadasha-item");
        item.classList.toggle("expanded");
      });
    });
  }

  // ============================================================
  // Tab 4: Vedic Yogas
  // ============================================================
  function renderYogasGrid(yogas) {
    elements.yogasGrid.innerHTML = yogas
      .map((y) => {
        const isDetected = y.detected;
        const natureBadge = isDetected
          ? `<span class="badge badge-gold">${y.nature}</span>`
          : `<span class="badge" style="background:rgba(255,255,255,0.05); color:var(--text-dim)">Not Formed</span>`;

        const evidenceHtml =
          isDetected && y.evidence && y.evidence.length
            ? `<div class="yoga-evidence-box"><strong>Forming Combination:</strong> ${y.evidence.join(" • ")}</div>`
            : "";

        return `
        <div class="yoga-card ${isDetected ? "detected-card" : ""}">
          <div class="yoga-card-header">
            <div>
              <h4 class="yoga-name">${y.name}</h4>
              <span class="yoga-category">${y.category}</span>
            </div>
            ${natureBadge}
          </div>
          <p class="yoga-desc">${y.description || "Classical Parashari auspicious combination conferring status, prosperity, and intellect."}</p>
          ${evidenceHtml}
        </div>
      `;
      })
      .join("");
  }

  // ============================================================
  // Tab 5: Life Synthesis
  // ============================================================
  function renderSynthesis(synth, fullData) {
    const { native, ascendant, planets_map } = fullData;

    elements.synthPersonality.innerHTML = `
      <p>Native possesses a <strong>${ascendant.sign}</strong> Ascendant (Lagna) governed by <strong>${ascendant.sign_lord}</strong>, bestowing inherent leadership, willpower, and individuality.</p>
      <p>The Janma Rasi is situated in <strong>${native.janma_rasi}</strong> under the governance of <strong>${native.janma_nakshatra}</strong>, providing strong emotional stability and mental focus.</p>
    `;

    const tenthHouse = fullData.houses.find((h) => h.house === 10);
    const sunPlanet = planets_map["Sun"];
    elements.synthCareer.innerHTML = `
      <p>The 10th House of Karma and Profession resides in <strong>${tenthHouse ? tenthHouse.sign : "Aries"}</strong> (Lord: ${tenthHouse ? tenthHouse.sign_lord : "Mars"}).</p>
      <p>Sun is placed in <strong>${sunPlanet ? sunPlanet.sign : "Leo"}</strong> (${sunPlanet ? sunPlanet.dignity : "Strong"}), suggesting professional inclinations toward administration, entrepreneurship, and authoritative responsibilities.</p>
    `;

    const secondHouse = fullData.houses.find((h) => h.house === 2);
    const eleventhHouse = fullData.houses.find((h) => h.house === 11);
    elements.synthWealth.innerHTML = `
      <p>Wealth accumulative potential (2nd Bhava in ${secondHouse ? secondHouse.sign : ""}) and revenue generation (11th Bhava in ${eleventhHouse ? eleventhHouse.sign : ""}) indicate positive financial flow through purposeful endeavors.</p>
      <p>Jupiter's placement and auspicious Dhana Yogas enhance long-term prosperity and material stability.</p>
    `;

    elements.synthHealth.innerHTML = `
      <p>Vitality and bodily constitution (Tanu Bhava) are reinforced by the Lagna Lord's dignity. Maintaining balanced daily regimens and mind-body harmony will preserve radiant wellness.</p>
    `;

    const themesList = synth && synth.themes && synth.themes.length
      ? synth.themes.map((t) => `<li>✨ ${t}</li>`).join("")
      : `<li>✨ Harmonious planetary strengths support righteous endeavors and steady personal growth.</li><li>✨ Favorable Dasha timing enables strategic life decisions.</li>`;

    elements.synthThemes.innerHTML = `<ul>${themesList}</ul>`;
  }

  // ============================================================
  // Tab 6: Shodashavarga Grid
  // ============================================================
  function renderVargasGrid(vargas, planetsMap) {
    const vargaKeys = Object.keys(vargas);
    elements.vargasMiniGrid.innerHTML = vargaKeys
      .map((code) => {
        const v = vargas[code];
        const svgStr = ChartRenderer.renderNorthIndianSvg(v, planetsMap);
        return `
        <div class="varga-mini-card">
          <div class="varga-mini-header">
            <span class="varga-mini-title">${v.code} - ${v.title.split("(")[0]}</span>
            <span class="badge badge-gold" style="font-size:9px">Lagna: ${v.lagna_sign_name}</span>
          </div>
          <div class="varga-mini-svg-box">
            ${svgStr}
          </div>
        </div>
      `;
      })
      .join("");
  }

  // ============================================================
  // Tooltip Interaction Setup
  // ============================================================
  function setupTooltipInteractions() {
    const tooltip = elements.astralTooltip;

    document.addEventListener("mouseover", (e) => {
      const planetTarget = e.target.closest(".chart-planet-label");
      const houseTarget = e.target.closest(".chart-house-poly, .south-cell-group");

      if (planetTarget && state.chartData) {
        const pName = planetTarget.dataset.planet;
        const pObj = state.chartData.planets_map[pName];
        if (pObj) {
          tooltip.innerHTML = `
            <div style="font-weight:700; color:${pObj.color}; margin-bottom:2px">● ${pObj.name} (${pObj.sanskrit_name})</div>
            <div>Sign: <strong>${pObj.sign}</strong> (${pObj.sign_degree_dms})</div>
            <div>House: <strong>${pObj.house}</strong> • Dignity: <strong>${pObj.dignity}</strong></div>
            <div>Nakshatra: <strong>${pObj.nakshatra} (${pObj.pada})</strong></div>
          `;
          tooltip.classList.add("visible");
        }
      } else if (houseTarget && state.chartData) {
        const houseNum = houseTarget.dataset.house;
        const houseObj = state.chartData.houses.find((h) => h.house == houseNum);
        if (houseObj) {
          tooltip.innerHTML = `
            <div style="font-weight:700; color:var(--gold-light)">🏛️ House ${houseObj.house} (${houseObj.sign})</div>
            <div>Lord: <strong>${houseObj.sign_lord}</strong></div>
            <div>Significance: <strong>${houseObj.significance_title}</strong></div>
            <div>Occupants: <strong>${houseObj.occupants.join(", ") || "None"}</strong></div>
          `;
          tooltip.classList.add("visible");
        }
      }
    });

    document.addEventListener("mousemove", (e) => {
      if (tooltip.classList.contains("visible")) {
        tooltip.style.left = `${e.clientX + 14}px`;
        tooltip.style.top = `${e.clientY + 14}px`;
      }
    });

    document.addEventListener("mouseout", (e) => {
      if (e.target.closest(".chart-planet-label, .chart-house-poly, .south-cell-group")) {
        tooltip.classList.remove("visible");
      }
    });
  }

  // ============================================================
  // Sample & Saved Profiles Handling
  // ============================================================
  async function fetchSampleProfiles() {
    try {
      const res = await fetch("/api/sample-profiles");
      const profiles = await res.json();
      state.sampleProfiles = profiles;
      renderSampleProfilesList(profiles);
    } catch (err) {
      console.warn("Error loading sample profiles:", err);
    }
  }

  function renderSampleProfilesList(profiles) {
    elements.sampleProfilesList.innerHTML = profiles
      .map(
        (p) => `
      <div class="sample-profile-item" data-id="${p.id}">
        <div class="profile-info">
          <h4>${p.name}</h4>
          <p>${p.birth_date} ${p.birth_time} • ${p.place}</p>
          <span style="font-size:11px; color:var(--gold-light)">${p.description}</span>
        </div>
        <button type="button" class="btn btn-sm btn-gold">Load Chart</button>
      </div>
    `
      )
      .join("");

    elements.sampleProfilesList.querySelectorAll(".sample-profile-item").forEach((item) => {
      item.addEventListener("click", () => {
        const prof = state.sampleProfiles.find((p) => p.id === item.dataset.id);
        if (prof) {
          elements.nativeName.value = prof.name;
          elements.nativeGender.value = prof.gender || "Male";
          elements.birthDate.value = prof.birth_date;
          elements.birthTime.value = prof.birth_time;
          elements.birthPlace.value = prof.place;
          elements.inputLat.value = prof.latitude;
          elements.inputLng.value = prof.longitude;
          elements.inputTz.value = prof.timezone;
          elements.modalSampleProfiles.style.display = "none";
          submitChartCalculation();
        }
      });
    });
  }

  function loadSavedProfilesFromStorage() {
    try {
      const raw = localStorage.getItem("kundali_saved_profiles");
      state.savedProfiles = raw ? JSON.parse(raw) : [];
      elements.savedCount.textContent = state.savedProfiles.length;
    } catch (e) {
      state.savedProfiles = [];
    }
  }

  function saveCurrentProfile() {
    const profile = {
      id: "profile_" + Date.now(),
      name: elements.nativeName.value.trim() || "Native",
      gender: elements.nativeGender.value,
      birth_date: elements.birthDate.value,
      birth_time: elements.birthTime.value,
      place: elements.birthPlace.value.trim(),
      latitude: elements.inputLat.value,
      longitude: elements.inputLng.value,
      timezone: elements.inputTz.value,
      savedAt: new Date().toISOString(),
    };

    state.savedProfiles.unshift(profile);
    localStorage.setItem("kundali_saved_profiles", JSON.stringify(state.savedProfiles));
    elements.savedCount.textContent = state.savedProfiles.length;
    alert(`✅ Kundali profile for "${profile.name}" saved to browser memory!`);
  }

  function renderSavedProfilesList() {
    if (!state.savedProfiles.length) {
      elements.savedProfilesList.innerHTML = `<p style="color:var(--text-muted);font-size:13px;text-align:center;padding:20px 0;">No saved profiles yet. Click "Save Profile" to store your charts.</p>`;
      return;
    }

    elements.savedProfilesList.innerHTML = state.savedProfiles
      .map(
        (p, idx) => `
      <div class="saved-profile-item" data-index="${idx}">
        <div class="profile-info">
          <h4>${p.name}</h4>
          <p>${p.birth_date} ${p.birth_time} • ${p.place}</p>
        </div>
        <div style="display:flex; gap:8px">
          <button type="button" class="btn btn-sm btn-gold btn-load-saved">Load</button>
          <button type="button" class="btn btn-sm btn-outline btn-delete-saved" style="color:#ef4444">✕</button>
        </div>
      </div>
    `
      )
      .join("");

    elements.savedProfilesList.querySelectorAll(".saved-profile-item").forEach((item) => {
      const idx = parseInt(item.dataset.index, 10);
      const prof = state.savedProfiles[idx];

      item.querySelector(".btn-load-saved").addEventListener("click", () => {
        elements.nativeName.value = prof.name;
        elements.nativeGender.value = prof.gender || "Male";
        elements.birthDate.value = prof.birth_date;
        elements.birthTime.value = prof.birth_time;
        elements.birthPlace.value = prof.place;
        elements.inputLat.value = prof.latitude;
        elements.inputLng.value = prof.longitude;
        elements.inputTz.value = prof.timezone;
        elements.modalSavedProfiles.style.display = "none";
        submitChartCalculation();
      });

      item.querySelector(".btn-delete-saved").addEventListener("click", (e) => {
        e.stopPropagation();
        if (confirm(`Delete saved profile "${prof.name}"?`)) {
          state.savedProfiles.splice(idx, 1);
          localStorage.setItem("kundali_saved_profiles", JSON.stringify(state.savedProfiles));
          elements.savedCount.textContent = state.savedProfiles.length;
          renderSavedProfilesList();
        }
      });
    });
  }

  function exportProfilesToJson() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(state.savedProfiles, null, 2));
    const dlAnchor = document.createElement("a");
    dlAnchor.setAttribute("href", dataStr);
    dlAnchor.setAttribute("download", `kundali_saved_profiles_${Date.now()}.json`);
    dlAnchor.click();
  }

  function importProfilesFromJson(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const imported = JSON.parse(event.target.result);
        if (Array.isArray(imported)) {
          state.savedProfiles = [...imported, ...state.savedProfiles];
          localStorage.setItem("kundali_saved_profiles", JSON.stringify(state.savedProfiles));
          elements.savedCount.textContent = state.savedProfiles.length;
          renderSavedProfilesList();
          alert(`✅ Successfully imported ${imported.length} profiles!`);
        }
      } catch (err) {
        alert("Invalid JSON file format.");
      }
    };
    reader.readAsText(file);
  }

  // Run initial boot
  document.addEventListener("DOMContentLoaded", init);
})();
