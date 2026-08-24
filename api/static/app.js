/**
 * api/static/app.js
 * Master Client Controller for Vedic Kundali Analytics Platform.
 */

(function () {
  "use strict";

  // State
  let currentChartData = null;
  let currentChartStyle = "north"; // 'north' | 'south'
  let currentVarga = "D1";
  let sampleProfiles = [];
  let nepalDistrictsData = null;
  let lastGeocodedPlace = "Kathmandu, Nepal";

  // DOM Elements
  const chartForm = document.getElementById("chartForm");
  const loadingPanel = document.getElementById("loadingPanel");
  const resultsContainer = document.getElementById("resultsContainer");
  const chartSvgWrapper = document.getElementById("chartSvgWrapper");
  const currentChartTitle = document.getElementById("currentChartTitle");
  const vargaSelect = document.getElementById("vargaSelect");
  const birthPlaceInput = document.getElementById("birthPlace");
  const cityDropdown = document.getElementById("cityDropdown");
  const btnClearCity = document.getElementById("btnClearCity");
  const btnToggleManualCoords = document.getElementById("btnToggleManualCoords");
  const manualCoordsDrawer = document.getElementById("manualCoordsDrawer");
  const astralTooltip = document.getElementById("astralTooltip");
  const toastContainer = document.getElementById("toastContainer");
  const btnThemeToggle = document.getElementById("btnThemeToggle");
  const themeIcon = document.getElementById("themeIcon");

  // ============================================================
  // THEME CONTROLLER (DARK / LIGHT)
  // ============================================================

  function initTheme() {
    const savedTheme = localStorage.getItem("kundali_theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);
    updateThemeIcon(savedTheme);

    if (btnThemeToggle) {
      btnThemeToggle.addEventListener("click", () => {
        const current = document.documentElement.getAttribute("data-theme") || "dark";
        const next = current === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        localStorage.setItem("kundali_theme", next);
        updateThemeIcon(next);
        if (currentChartData) {
          renderCurrentChart();
          renderVargasGrid(currentChartData.vargas, currentChartData.planets_map);
        }
      });
    }
  }

  function updateThemeIcon(theme) {
    if (themeIcon) {
      themeIcon.textContent = theme === "dark" ? "🌙" : "☀️";
    }
  }

  // ============================================================
  // TOAST NOTIFICATIONS
  // ============================================================

  function showToast(message, type = "info") {
    if (!toastContainer) return;
    const toast = document.createElement("div");
    toast.className = `toast-message toast-${type}`;
    const icon = type === "success" ? "✓" : (type === "error" ? "⚠️" : "ℹ️");
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(100%)";
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  // ============================================================
  // COSMIC STARS CANVAS ANIMATION
  // ============================================================

  function initCosmicStars() {
    const canvas = document.getElementById("starsCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener("resize", () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    const starCount = 80;
    const stars = [];
    for (let i = 0; i < starCount; i++) {
      stars.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 1.5 + 0.5,
        alpha: Math.random() * 0.7 + 0.2,
        speed: Math.random() * 0.2 + 0.05,
      });
    }

    function animate() {
      ctx.clearRect(0, 0, width, height);
      const isDark = document.documentElement.getAttribute("data-theme") !== "light";
      const starColor = isDark ? "245, 158, 11" : "217, 119, 6";

      stars.forEach((s) => {
        s.y -= s.speed;
        if (s.y < 0) s.y = height;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${starColor}, ${s.alpha})`;
        ctx.fill();
      });
      requestAnimationFrame(animate);
    }
    animate();
  }

  // ============================================================
  // FORM & CALCULATION CONTROLLER
  // ============================================================

  async function handleChartCalculation(e) {
    if (e) e.preventDefault();

    const name = document.getElementById("nativeName").value.trim() || "Native";
    const gender = document.getElementById("nativeGender").value;
    const birthDate = document.getElementById("birthDate").value;
    const birthTime = document.getElementById("birthTime").value;
    const place = birthPlaceInput.value.trim() || "Kathmandu, Nepal";
    let lat = parseFloat(document.getElementById("inputLat").value) || 27.7172;
    let lng = parseFloat(document.getElementById("inputLng").value) || 85.3240;
    let tz = document.getElementById("inputTz").value.trim() || "Asia/Kathmandu";
    const ayanamsha = document.getElementById("ayanamshaSelect").value || "LAHIRI";

    if (loadingPanel) loadingPanel.style.display = "block";
    if (resultsContainer) resultsContainer.style.opacity = "0.4";

    try {
      // Dynamic on-the-fly geocoding when custom place query is typed instead of clicked
      if (place.toLowerCase() !== lastGeocodedPlace.toLowerCase()) {
        const geoRes = await fetch("/api/geocode", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: place }),
        });
        if (geoRes.ok) {
          const geoData = await geoRes.json();
          if (geoData && geoData.match) {
            const match = geoData.match;
            lat = match.latitude;
            lng = match.longitude;
            tz = match.timezone;
            document.getElementById("inputLat").value = lat;
            document.getElementById("inputLng").value = lng;
            document.getElementById("inputTz").value = tz;
            lastGeocodedPlace = place;
            showToast(`Location resolved: ${match.name} (${lat}°, ${lng}°)`, "success");
          }
        }
      }

      const payload = {
        name,
        gender,
        birth_date: birthDate,
        birth_time: birthTime,
        place,
        latitude: lat,
        longitude: lng,
        timezone: tz,
        ayanamsha,
      };

      const res = await fetch("/api/chart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errJson = await res.json();
        throw new Error(errJson.message || errJson.detail || "Calculation failed");
      }

      currentChartData = await res.json();
      renderCompleteDashboard(currentChartData);
      showToast(`Kundali calculated successfully for ${name}!`, "success");
    } catch (err) {
      console.error("Calculation Error:", err);
      showToast(err.message || "Failed to calculate horoscope", "error");
    } finally {
      if (loadingPanel) loadingPanel.style.display = "none";
      if (resultsContainer) {
        resultsContainer.style.opacity = "1";
        resultsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }
  }

  // ============================================================
  // DASHBOARD MASTER RENDERER
  // ============================================================

  function renderCompleteDashboard(data) {
    if (!data) return;

    // 1. Hero Overview
    renderHeroOverview(data);

    // 2. Main Chart SVG
    renderCurrentChart();

    // 3. Side Key Insights
    renderSideInsights(data);

    // 4. Tab 1: Grahas & Balas Strengths
    renderPlanetsTable(data.planets);
    renderBalasSection(data.balas);

    // 5. Tab 2: 12 Bhavas
    renderHousesGrid(data.houses);

    // 6. Tab 3: Vimshottari Dasha
    renderDashaExplorer(data.dashas);

    // 7. Tab 4: Vedic Yogas
    renderYogasTab(data.yogas);

    // 8. Tab 5: Shani Sade Sati
    renderSadeSatiTab(data.sade_sati);

    // 9. Tab 6: Panchadha Maitri Matrix
    renderPanchadhaMatrix(data.panchadha);

    // 10. Tab 7: Live Transits (Gochara)
    renderTransitsTab(data.transits);

    // 11. Tab 8: Life Synthesis
    renderSynthesisTab(data.synthesis);

    // 12. Tab 9: Shodashavarga (All 16 Vargas)
    renderVargasGrid(data.vargas, data.planets_map);
  }

  // ============================================================
  // 1. HERO OVERVIEW
  // ============================================================

  function renderHeroOverview(data) {
    const native = data.native;
    const asc = data.ascendant;
    const moon = data.planets_map["Moon"] || {};
    const sun = data.planets_map["Sun"] || {};
    const dasha = data.dashas.active_chain || {};
    const sadeSati = data.sade_sati || {};

    const elName = document.getElementById("heroNativeName");
    const elMeta = document.getElementById("heroNativeMeta");
    const elAyan = document.getElementById("heroAyanamsha");
    const elLagna = document.getElementById("heroLagna");
    const elLagnaDeg = document.getElementById("heroLagnaDegree");
    const elRasi = document.getElementById("heroRasi");
    const elNak = document.getElementById("heroNakshatra");
    const elSun = document.getElementById("heroSunSign");
    const elSunDig = document.getElementById("heroSunDignity");
    const elDasha = document.getElementById("heroActiveDasha");
    const elPratyantar = document.getElementById("heroActivePratyantar");
    const elSadeSatiStatus = document.getElementById("heroSadeSatiStatus");
    const elSadeSatiPhase = document.getElementById("heroSadeSatiPhase");

    if (elName) elName.textContent = native.name;
    if (elMeta) elMeta.textContent = `Born: ${native.birth_date_display} at ${native.birth_time_display} • ${native.place} (${native.timezone})`;
    if (elAyan) elAyan.textContent = `${native.ayanamsa_name}: ${native.ayanamsa_dms}`;
    if (elLagna) elLagna.textContent = asc.sign_sanskrit;
    if (elLagnaDeg) elLagnaDeg.textContent = `${asc.sign_degree_dms} • Lord: ${asc.sign_lord}`;
    if (elRasi) elRasi.textContent = moon.sign_sanskrit || native.janma_rasi;
    if (elNak) elNak.textContent = `${moon.nakshatra} Pada ${moon.pada} • Lord: ${moon.nakshatra_lord}`;
    if (elSun) elSun.textContent = sun.sign_sanskrit || native.sun_sign;
    if (elSunDig) elSunDig.textContent = `${sun.dignity} • ${sun.sign_degree_dms}`;

    const mdLord = dasha.mahadasha ? dasha.mahadasha.lord : "N/A";
    const adLord = dasha.antardasha ? dasha.antardasha.lord : "N/A";
    const pdLord = dasha.pratyantardasha ? dasha.pratyantardasha.lord : "N/A";
    const sdLord = dasha.sookshma ? dasha.sookshma.lord : "N/A";

    if (elDasha) elDasha.textContent = `${mdLord} MD / ${adLord} AD`;
    if (elPratyantar) elPratyantar.textContent = `${pdLord} PD • ${sdLord} SD`;

    if (elSadeSatiStatus) {
      elSadeSatiStatus.textContent = sadeSati.is_active ? `Active (${sadeSati.current_phase})` : "Inactive";
      elSadeSatiStatus.style.color = sadeSati.is_active ? "var(--accent-red)" : "var(--accent-green)";
    }
    if (elSadeSatiPhase) {
      elSadeSatiPhase.textContent = `Saturn in ${sadeSati.transiting_saturn_sign || 'Pisces'}`;
    }
  }

  // ============================================================
  // 2. CHART SVG RENDERER
  // ============================================================

  function renderCurrentChart() {
    if (!currentChartData || !chartSvgWrapper) return;

    const vargas = currentChartData.vargas;
    const vargaData = vargas[currentVarga] || vargas["D1"];
    const planetsMap = currentChartData.planets_map;

    const adaptedVarga = {
      code: vargaData.code,
      title: vargaData.title,
      lagna_sign: vargaData.lagna_sign_number,
      house_placements: {},
      planet_signs: {},
    };

    for (let h = 1; h <= 12; h++) {
      adaptedVarga.house_placements[h] = (vargaData.houses[h] && vargaData.houses[h].planets) || [];
    }

    for (const [pName, pObj] of Object.entries(vargaData.planets)) {
      adaptedVarga.planet_signs[pName] = pObj.sign_number;
    }

    let svgHtml = "";
    if (currentChartStyle === "south") {
      svgHtml = ChartRenderer.renderSouthIndianSvg(adaptedVarga, planetsMap);
    } else {
      svgHtml = ChartRenderer.renderNorthIndianSvg(adaptedVarga, planetsMap);
    }

    chartSvgWrapper.innerHTML = svgHtml;
    if (currentChartTitle) {
      currentChartTitle.textContent = `${vargaData.code} • ${vargaData.title.toUpperCase()}`;
    }

    attachChartInteractions();
  }

  function attachChartInteractions() {
    const polys = chartSvgWrapper.querySelectorAll(".chart-house-poly, .south-cell-group");
    polys.forEach((p) => {
      p.addEventListener("mouseenter", (e) => {
        const house = p.getAttribute("data-house") || p.dataset.house;
        const sign = p.getAttribute("data-sign-name") || p.dataset.signName;
        if (!house || !currentChartData) return;

        const hData = currentChartData.houses[parseInt(house) - 1];
        if (!hData) return;

        const occupantsStr = hData.occupants.length ? hData.occupants.join(", ") : "None";
        const aspectsStr = hData.aspecting_planets.length ? hData.aspecting_planets.join(", ") : "None";

        astralTooltip.innerHTML = `
          <strong>House ${house} (${sign})</strong><br>
          <span style="color:var(--gold-primary)">Lord: ${hData.sign_lord}</span><br>
          Occupants: ${occupantsStr}<br>
          Drishti (Aspects): ${aspectsStr}<br>
          <small style="color:var(--text-secondary)">${hData.significance_title}</small>
        `;
        astralTooltip.style.display = "block";
      });

      p.addEventListener("mousemove", (e) => {
        astralTooltip.style.left = e.pageX + 14 + "px";
        astralTooltip.style.top = e.pageY + 14 + "px";
      });

      p.addEventListener("mouseleave", () => {
        astralTooltip.style.display = "none";
      });
    });
  }

  // ============================================================
  // 3. SIDE INSIGHTS
  // ============================================================

  function renderSideInsights(data) {
    const asc = data.ascendant;
    const moon = data.planets_map["Moon"] || {};

    const elDeg = document.getElementById("metricLagnaDeg");
    const elNak = document.getElementById("metricLagnaNak");
    const elLord = document.getElementById("metricLagnaLord");
    const elMoonDeg = document.getElementById("metricMoonDeg");

    if (elDeg) elDeg.textContent = asc.sign_degree_dms;
    if (elNak) elNak.textContent = `${asc.nakshatra} (${asc.pada})`;
    if (elLord) elLord.textContent = `${asc.sign_lord}`;
    if (elMoonDeg) elMoonDeg.textContent = `${moon.sign_degree_dms || 'N/A'}`;

    // Dignity highlights cloud
    const dignityCloud = document.getElementById("dignityTagsCloud");
    if (dignityCloud) {
      dignityCloud.innerHTML = "";
      data.planets.forEach((p) => {
        if (p.exalted) {
          dignityCloud.innerHTML += `<span class="dignity-tag dignity-exalted">★ ${p.name} Exalted (${p.sign})</span>`;
        } else if (p.own_sign || p.moolatrikona) {
          dignityCloud.innerHTML += `<span class="dignity-tag dignity-own">✦ ${p.name} Own Sign</span>`;
        } else if (p.debilitated) {
          dignityCloud.innerHTML += `<span class="dignity-tag dignity-debilitated">▼ ${p.name} Debilitated</span>`;
        }
        if (p.is_combust) {
          dignityCloud.innerHTML += `<span class="dignity-tag dignity-combust">🔥 ${p.name} Combust</span>`;
        }
      });
      if (!dignityCloud.innerHTML) {
        dignityCloud.innerHTML = `<span style="font-size:12px;color:var(--text-muted)">Balanced planetary dignities.</span>`;
      }
    }

    // Quick Yogas list
    const quickList = document.getElementById("quickYogaList");
    const quickCount = document.getElementById("quickYogaCount");
    const tabCount = document.getElementById("tabYogaCount");

    const detectedYogas = data.yogas.detected || [];
    if (quickCount) quickCount.textContent = detectedYogas.length;
    if (tabCount) tabCount.textContent = detectedYogas.length;

    if (quickList) {
      quickList.innerHTML = "";
      if (detectedYogas.length === 0) {
        quickList.innerHTML = `<li style="font-size:12px;color:var(--text-muted)">No major structural yogas detected.</li>`;
      } else {
        detectedYogas.slice(0, 4).forEach((y) => {
          quickList.innerHTML += `
            <li class="quick-yoga-item">
              <span><strong>${y.name}</strong></span>
              <span style="color:var(--gold-primary);font-size:10.5px">${y.nature || 'Auspicious'}</span>
            </li>
          `;
        });
      }
    }
  }

  // ============================================================
  // 4. TAB 1: GRAHAS & BALAS STRENGTHS
  // ============================================================

  function renderPlanetsTable(planets) {
    const tbody = document.getElementById("planetsTableBody");
    if (!tbody || !planets) return;

    tbody.innerHTML = "";
    planets.forEach((p) => {
      let stateBadges = [];
      if (p.retrograde) stateBadges.push(`<span style="color:var(--gold-primary);font-weight:700">[R] Retro</span>`);
      if (p.speed < 0) stateBadges.push(`<small>Speed: ${p.speed}°/d</small>`);

      let combustBadge = p.is_combust
        ? `<span class="dignity-tag dignity-combust">🔥 Combust (${p.combust_separation}°)</span>`
        : `<span style="color:var(--text-muted)">Clear</span>`;

      tbody.innerHTML += `
        <tr>
          <td>
            <strong style="color:${p.color}">${p.symbol} ${p.name}</strong><br>
            <small style="color:var(--text-muted)">${p.sanskrit_name}</small>
          </td>
          <td>
            <strong>${p.sign}</strong> (${p.sign_number})<br>
            <small style="color:var(--text-secondary)">${p.sign_sanskrit.split("-")[0]}</small>
          </td>
          <td>${p.sign_lord}</td>
          <td><strong>${p.sign_degree_dms}</strong></td>
          <td><strong>House ${p.house}</strong></td>
          <td>${p.nakshatra} (Pada ${p.pada})</td>
          <td>${p.nakshatra_lord}</td>
          <td>
            <span class="dignity-tag ${p.exalted ? 'dignity-exalted' : (p.debilitated ? 'dignity-debilitated' : (p.own_sign ? 'dignity-own' : ''))}">
              ${p.dignity}
            </span>
          </td>
          <td>${combustBadge}</td>
          <td>${stateBadges.join(" ") || "Direct"}</td>
        </tr>
      `;
    });
  }

  function renderBalasSection(balas) {
    const container = document.getElementById("balasCardsGrid");
    if (!container || !balas || !balas.planets) return;

    container.innerHTML = "";
    balas.planets.forEach((bp) => {
      const statusColor = bp.status === "Strong" ? "var(--accent-green)" : (bp.status === "Moderate" ? "var(--gold-primary)" : "var(--accent-red)");

      container.innerHTML += `
        <div class="bala-card">
          <div class="bala-card-header">
            <span class="bala-planet-name">${bp.planet}</span>
            <span style="color:${statusColor};font-size:12px;font-weight:700">${bp.status} (${bp.relative_percentage}%)</span>
          </div>
          <div class="bala-bar-wrap">
            <div class="bala-bar-fill" style="width:${bp.relative_percentage}%"></div>
          </div>
          <div class="bala-breakdown-row">
            <span>Cheshta: ${bp.cheshta_bala}</span>
            <span>Dig: ${bp.dig_bala}</span>
            <span>Uccha: ${bp.uccha_bala}</span>
          </div>
          <div class="bala-breakdown-row">
            <span>Naisargika: ${bp.naisargika_bala}</span>
            <span>Paksha: ${bp.paksha_bala}</span>
            <span>Total: <strong>${bp.total_virupas} Virupas</strong></span>
          </div>
        </div>
      `;
    });
  }

  // ============================================================
  // 5. TAB 2: 12 HOUSES (BHAVAS)
  // ============================================================

  function renderHousesGrid(houses) {
    const grid = document.getElementById("housesGrid");
    if (!grid || !houses) return;

    grid.innerHTML = "";
    houses.forEach((h) => {
      const occupantsChips = h.occupants.map(p => `<span class="planet-chip">${p}</span>`).join(" ") || `<span style="font-size:11px;color:var(--text-muted)">Empty</span>`;
      const aspectsStr = h.aspecting_planets.length ? h.aspecting_planets.join(", ") : "None";

      grid.innerHTML += `
        <div class="house-card">
          <div class="house-header">
            <span class="house-number-badge">Bhava ${h.house}</span>
            <span class="house-sign-tag">${h.sign_sanskrit} (${h.element})</span>
          </div>
          <div style="font-size:12px">
            <strong>Lord:</strong> ${h.sign_lord} &nbsp;|&nbsp; <strong>Aspects:</strong> ${aspectsStr}
          </div>
          <div class="house-occupants-list">
            <strong>Planets:</strong> ${occupantsChips}
          </div>
          <p class="house-domains">${h.significance_domains}</p>
        </div>
      `;
    });
  }

  // ============================================================
  // 6. TAB 3: VIMSHOTTARI DASHA EXPLORER
  // ============================================================

  function renderDashaExplorer(dashas) {
    const levelsRow = document.getElementById("dashaLevelsRow");
    const accordionList = document.getElementById("dashaAccordionList");
    if (!dashas) return;

    // Active Chain
    if (levelsRow && dashas.active_chain) {
      const chain = dashas.active_chain;
      levelsRow.innerHTML = `
        <div class="dasha-level-pill">
          <span class="dasha-level-title">Mahadasha (MD)</span>
          <span class="dasha-level-lord">${chain.mahadasha ? chain.mahadasha.lord : 'N/A'}</span>
          <span class="dasha-level-dates">${chain.mahadasha ? `${chain.mahadasha.start} to ${chain.mahadasha.end}` : ''}</span>
        </div>
        <div class="dasha-level-pill">
          <span class="dasha-level-title">Antardasha (AD)</span>
          <span class="dasha-level-lord">${chain.antardasha ? chain.antardasha.lord : 'N/A'}</span>
          <span class="dasha-level-dates">${chain.antardasha ? `${chain.antardasha.start} to ${chain.antardasha.end}` : ''}</span>
        </div>
        <div class="dasha-level-pill">
          <span class="dasha-level-title">Pratyantardasha (PD)</span>
          <span class="dasha-level-lord">${chain.pratyantardasha ? chain.pratyantardasha.lord : 'N/A'}</span>
          <span class="dasha-level-dates">${chain.pratyantardasha ? `${chain.pratyantardasha.start} to ${chain.pratyantardasha.end}` : ''}</span>
        </div>
        <div class="dasha-level-pill">
          <span class="dasha-level-title">Sookshma Dasha (SD)</span>
          <span class="dasha-level-lord">${chain.sookshma ? chain.sookshma.lord : 'N/A'}</span>
          <span class="dasha-level-dates">${chain.sookshma ? `${chain.sookshma.start} to ${chain.sookshma.end}` : ''}</span>
        </div>
        <div class="dasha-level-pill">
          <span class="dasha-level-title">Prana Dasha</span>
          <span class="dasha-level-lord">${chain.prana ? chain.prana.lord : 'N/A'}</span>
          <span class="dasha-level-dates">${chain.prana ? `${chain.prana.start} to ${chain.prana.end}` : ''}</span>
        </div>
      `;
    }

    // 120-Year Accordion
    if (accordionList && dashas.mahadashas) {
      accordionList.innerHTML = "";
      dashas.mahadashas.forEach((md, idx) => {
        const isAct = md.is_active;
        const antardashasHtml = (md.antardashas || []).map((ad) => `
          <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px dashed var(--border-subtle);font-size:12px">
            <span style="${ad.is_active ? 'color:var(--gold-primary);font-weight:700' : ''}">▸ ${ad.lord} AD</span>
            <span style="color:var(--text-secondary)">${ad.start} → ${ad.end}</span>
          </div>
        `).join("");

        accordionList.innerHTML += `
          <div class="accordion-item">
            <div class="accordion-header ${isAct ? 'active' : ''}" onclick="this.nextElementSibling.classList.toggle('show')">
              <span><strong>${md.lord} Mahadasha</strong> (${md.duration_years} Years) ${isAct ? '<span class="badge badge-gold">Active Now</span>' : ''}</span>
              <span style="font-size:12px;color:var(--text-secondary)">${md.start} to ${md.end} ▾</span>
            </div>
            <div class="accordion-body ${isAct ? 'show' : ''}">
              <div style="display:flex;flex-direction:column;gap:4px">
                ${antardashasHtml}
              </div>
            </div>
          </div>
        `;
      });
    }
  }

  // ============================================================
  // 7. TAB 4: VEDIC YOGAS
  // ============================================================

  function renderYogasTab(yogasData) {
    const grid = document.getElementById("yogasGrid");
    if (!grid || !yogasData) return;

    grid.innerHTML = "";
    const yogas = yogasData.all || [];

    yogas.forEach((y) => {
      const isDetected = y.detected;
      const isChallenging = y.nature && y.nature.toLowerCase().includes("challenging");
      const cardClass = isChallenging ? "challenging" : "auspicious";

      grid.innerHTML += `
        <div class="yoga-card ${cardClass}" style="${!isDetected ? 'opacity:0.4' : ''}">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span class="yoga-title">${y.name}</span>
            <span class="badge ${isDetected ? 'badge-gold' : ''}">${isDetected ? 'DETECTED' : 'Not Formed'}</span>
          </div>
          <span class="yoga-category">${y.category || 'General Yoga'} • ${y.nature || 'Auspicious'}</span>
          <p class="yoga-desc">${y.description || 'Classical Parashari Yoga combination.'}</p>
          ${y.evidence && y.evidence.length ? `<div class="yoga-evidence"><strong>Evidence:</strong> ${y.evidence.join(" | ")}</div>` : ''}
        </div>
      `;
    });
  }

  // ============================================================
  // 8. TAB 5: SHANI SADE SATI
  // ============================================================

  function renderSadeSatiTab(sadeSati) {
    const container = document.getElementById("sadeSatiContainer");
    if (!container || !sadeSati) return;

    const isActive = sadeSati.is_active;
    const currentPhase = sadeSati.current_phase || "Inactive";

    const periodsRows = (sadeSati.estimated_periods || []).map(p => `
      <tr>
        <td><strong>${p.phase}</strong></td>
        <td>${p.saturn_sign}</td>
        <td>House ${p.house_from_moon} from Moon</td>
        <td>${p.start}</td>
        <td>${p.end}</td>
        <td>${p.duration_years} yrs</td>
      </tr>
    `).join("");

    container.innerHTML = `
      <div class="sade-sati-hero-banner">
        <div class="sade-sati-status-group">
          <span style="font-size:36px">🪐</span>
          <div>
            <h3 style="font-size:20px;color:var(--text-primary)">
              Sade Sati Status: <span style="color:${isActive ? 'var(--accent-red)' : 'var(--accent-green)'}">${isActive ? 'ACTIVE' : 'INACTIVE'}</span>
            </h3>
            <p style="font-size:13px;color:var(--text-secondary)">
              Natal Moon: <strong>${sadeSati.natal_moon_sign}</strong> | Transiting Saturn: <strong>${sadeSati.transiting_saturn_sign}</strong>
            </p>
          </div>
        </div>
        <span class="sade-sati-phase-badge ${isActive ? 'active' : 'inactive'}">
          ${currentPhase}
        </span>
      </div>

      <div class="side-card">
        <h4 class="side-card-title">✦ Phase Guidance</h4>
        <p style="font-size:13px;color:var(--text-primary);line-height:1.5">${sadeSati.phase_description}</p>
      </div>

      <div class="sade-sati-phases-roadmap">
        <div class="phase-step-card ${currentPhase.includes('Rising') ? 'current-phase' : ''}">
          <h4 style="font-size:13px;color:var(--gold-primary)">1. Rising Phase (1st Dhaiya)</h4>
          <p style="font-size:12px;color:var(--text-secondary)">Saturn enters 12th from Moon. Focus on expenditure, foreign affairs, sleep, and emotional peace.</p>
        </div>
        <div class="phase-step-card ${currentPhase.includes('Peak') ? 'current-phase' : ''}">
          <h4 style="font-size:13px;color:var(--gold-primary)">2. Peak Phase (Janma Shani)</h4>
          <p style="font-size:12px;color:var(--text-secondary)">Saturn transits natal Moon. Major personal transformations, mental discipline, and resilience.</p>
        </div>
        <div class="phase-step-card ${currentPhase.includes('Setting') ? 'current-phase' : ''}">
          <h4 style="font-size:13px;color:var(--gold-primary)">3. Setting Phase (3rd Dhaiya)</h4>
          <p style="font-size:12px;color:var(--text-secondary)">Saturn transits 2nd from Moon. Family matters, financial restructuring, and stabilizing rewards.</p>
        </div>
      </div>

      <div class="table-responsive" style="margin-top:10px">
        <table class="data-table">
          <thead>
            <tr>
              <th>Phase</th>
              <th>Saturn Sign</th>
              <th>Relative Placement</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Duration</th>
            </tr>
          </thead>
          <tbody>
            ${periodsRows}
          </tbody>
        </table>
      </div>
    `;
  }

  // ============================================================
  // 9. TAB 6: PANCHADHA MAITRI MATRIX
  // ============================================================

  function renderPanchadhaMatrix(panchadha) {
    const tbody = document.getElementById("panchadhaTableBody");
    if (!tbody || !panchadha || !panchadha.matrix) return;

    tbody.innerHTML = "";
    const planets = panchadha.planets || ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];

    planets.forEach((src) => {
      const row = panchadha.matrix[src] || {};
      let cellsHtml = `<td><strong>${src}</strong></td>`;

      planets.forEach((tgt) => {
        const item = row[tgt] || { relationship: "Neutral", badge_class: "rel-neutral" };
        cellsHtml += `<td><span class="rel-badge ${item.badge_class}">${item.relationship}</span></td>`;
      });

      tbody.innerHTML += `<tr>${cellsHtml}</tr>`;
    });
  }

  // ============================================================
  // 10. TAB 7: LIVE TRANSITS (GOCHARA)
  // ============================================================

  function renderTransitsTab(transitsData) {
    const grid = document.getElementById("transitsGrid");
    if (!grid || !transitsData || !transitsData.transits) return;

    grid.innerHTML = "";
    transitsData.transits.forEach((tr) => {
      grid.innerHTML += `
        <div class="transit-card">
          <div class="transit-card-header">
            <span style="font-weight:700;color:${tr.color}">${tr.symbol} ${tr.planet}</span>
            <span style="font-size:12px;color:var(--text-secondary)">${tr.current_sign} (${tr.current_longitude_dms})</span>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:12px;margin:4px 0">
            <span>From Moon: <strong>House ${tr.house_from_moon}</strong></span>
            <span>From Lagna: <strong>House ${tr.house_from_ascendant}</strong></span>
          </div>
          <div class="transit-influence-tag">
            ✦ ${tr.gochara_influence}
          </div>
        </div>
      `;
    });
  }

  // ============================================================
  // 11. TAB 8: LIFE SYNTHESIS
  // ============================================================

  function renderSynthesisTab(synthesis) {
    const synthP = document.getElementById("synthPersonality");
    const synthC = document.getElementById("synthCareer");
    const synthW = document.getElementById("synthWealth");
    const synthH = document.getElementById("synthHealth");
    const synthT = document.getElementById("synthThemes");

    if (!synthesis) return;

    const themes = synthesis.themes || [];
    const cautions = synthesis.cautions || [];
    const evidence = synthesis.evidence || [];

    if (synthP) synthP.innerHTML = `<p>${themes[0] || 'Strong character orientation based on Ascendant and Moon.'}</p>`;
    if (synthC) synthC.innerHTML = `<p>${themes[1] || 'Professional growth supported through 10th house karmic placements.'}</p>`;
    if (synthW) synthW.innerHTML = `<p>${themes[2] || 'Wealth accumulation facilitated by 2nd and 11th lord alignments.'}</p>`;
    if (synthH) synthH.innerHTML = `<p>${cautions[0] || 'Maintain balanced routines during sensitive transits and sub-dashas.'}</p>`;

    if (synthT) {
      const themesList = themes.map(t => `<li>${t}</li>`).join("");
      const cautionsList = cautions.map(c => `<li style="color:var(--accent-red)">⚠️ ${c}</li>`).join("");
      synthT.innerHTML = `<ul class="synth-list">${themesList}${cautionsList}</ul>`;
    }
  }

  // ============================================================
  // 12. TAB 9: SHODASHAVARGA (ALL 16 VARGAS)
  // ============================================================

  function renderVargasGrid(vargas, planetsMap) {
    const grid = document.getElementById("vargasMiniGrid");
    if (!grid || !vargas) return;

    grid.innerHTML = "";
    Object.values(vargas).forEach((v) => {
      const adapted = {
        code: v.code,
        title: v.title,
        lagna_sign: v.lagna_sign_number,
        house_placements: {},
        planet_signs: {},
      };
      for (let h = 1; h <= 12; h++) {
        adapted.house_placements[h] = (v.houses[h] && v.houses[h].planets) || [];
      }
      for (const [pName, pObj] of Object.entries(v.planets || {})) {
        adapted.planet_signs[pName] = pObj.sign_number;
      }

      let miniSvg = "";
      if (currentChartStyle === "south") {
        miniSvg = ChartRenderer.renderSouthIndianSvg(adapted, planetsMap);
      } else {
        miniSvg = ChartRenderer.renderNorthIndianSvg(adapted, planetsMap);
      }

      grid.innerHTML += `
        <div class="varga-mini-card" data-varga-code="${v.code}">
          <span class="varga-mini-title">${v.code} • ${v.title}</span>
          <div class="varga-mini-svg">${miniSvg}</div>
        </div>
      `;
    });

    // Click mini chart to load in main viewer
    grid.querySelectorAll(".varga-mini-card").forEach((card) => {
      card.addEventListener("click", () => {
        const code = card.getAttribute("data-varga-code");
        if (vargaSelect) vargaSelect.value = code;
        currentVarga = code;
        renderCurrentChart();
        window.scrollTo({ top: 300, behavior: "smooth" });
      });
    });
  }

  // ============================================================
  // NEPAL 77 DISTRICTS MODAL
  // ============================================================

  async function loadNepalDistricts() {
    if (nepalDistrictsData) return;
    try {
      const res = await fetch("/api/nepal-districts");
      nepalDistrictsData = await res.json();
      buildNepalDistrictsModal(nepalDistrictsData);
    } catch (err) {
      console.error("Failed to load Nepal districts:", err);
    }
  }

  function buildNepalDistrictsModal(data) {
    const container = document.getElementById("nepalProvincesContainer");
    if (!container || !data || !data.provinces) return;

    container.innerHTML = "";
    for (const [provName, dList] of Object.entries(data.provinces)) {
      const chipsHtml = dList.map(d => `
        <button type="button" class="district-chip" data-name="${d.name}" data-lat="${d.latitude}" data-lng="${d.longitude}" data-tz="${d.timezone}">
          ${d.name} (${d.headquarters})
        </button>
      `).join("");

      container.innerHTML += `
        <div class="province-group" data-province="${provName.toLowerCase()}">
          <h4 class="province-title">🚩 Province: ${provName} (${dList.length} Districts)</h4>
          <div class="districts-chips-wrap">
            ${chipsHtml}
          </div>
        </div>
      `;
    }

    // Attach click to chips
    container.querySelectorAll(".district-chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        birthPlaceInput.value = chip.dataset.name + ", Nepal";
        document.getElementById("inputLat").value = chip.dataset.lat;
        document.getElementById("inputLng").value = chip.dataset.lng;
        document.getElementById("inputTz").value = chip.dataset.tz;
        lastGeocodedPlace = chip.dataset.name + ", Nepal";
        closeModal("modalNepalDistricts");
        showToast(`Selected Nepal District: ${chip.dataset.name}`, "info");
      });
    });
  }

  function filterNepalDistricts(query) {
    const q = query.toLowerCase().trim();
    const groups = document.querySelectorAll(".province-group");
    groups.forEach((grp) => {
      const chips = grp.querySelectorAll(".district-chip");
      let hasMatch = false;
      chips.forEach((c) => {
        const text = c.textContent.toLowerCase();
        if (text.includes(q)) {
          c.style.display = "inline-flex";
          hasMatch = true;
        } else {
          c.style.display = "none";
        }
      });
      grp.style.display = hasMatch ? "block" : "none";
    });
  }

  // ============================================================
  // CITY AUTOCOMPLETE SEARCH
  // ============================================================

  let debounceTimer = null;
  function handleCitySearch(query) {
    clearTimeout(debounceTimer);
    if (!query || query.length < 2) {
      if (cityDropdown) cityDropdown.style.display = "none";
      return;
    }

    debounceTimer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/cities?q=${encodeURIComponent(query)}&limit=8`);
        const data = await res.json();
        renderCityDropdown(data.results || []);
      } catch (err) {
        console.error("City search error:", err);
      }
    }, 200);
  }

  function renderCityDropdown(results) {
    if (!cityDropdown) return;
    if (!results.length) {
      cityDropdown.innerHTML = `<div class="city-item" style="color:var(--text-muted)">No matching locations found.</div>`;
      cityDropdown.style.display = "block";
      return;
    }

    cityDropdown.innerHTML = "";
    results.forEach((c) => {
      const div = document.createElement("div");
      div.className = "city-item";
      div.innerHTML = `
        <span class="city-item-name">${c.name}</span>
        <span class="city-item-badge">${c.timezone}</span>
      `;
      div.addEventListener("click", () => {
        birthPlaceInput.value = c.name;
        document.getElementById("inputLat").value = c.latitude;
        document.getElementById("inputLng").value = c.longitude;
        document.getElementById("inputTz").value = c.timezone;
        lastGeocodedPlace = c.name;
        cityDropdown.style.display = "none";
      });
      cityDropdown.appendChild(div);
    });
    cityDropdown.style.display = "block";
  }

  // ============================================================
  // MODALS CONTROLLER
  // ============================================================

  function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.style.display = "flex";
  }

  function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.style.display = "none";
  }

  // ============================================================
  // INITIALIZATION & EVENT LISTENERS
  // ============================================================

  function initApp() {
    initTheme();
    initCosmicStars();

    // Chart Form
    if (chartForm) {
      chartForm.addEventListener("submit", handleChartCalculation);
    }

    // Chart Style Toggles
    document.querySelectorAll(".btn-toggle-tab").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".btn-toggle-tab").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentChartStyle = btn.dataset.chartStyle;
        renderCurrentChart();
      });
    });

    // Varga Selector
    if (vargaSelect) {
      vargaSelect.addEventListener("change", (e) => {
        currentVarga = e.target.value;
        renderCurrentChart();
      });
    }

    // Workspace Tabs
    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
        btn.classList.add("active");
        const target = document.getElementById(btn.dataset.tab);
        if (target) target.classList.add("active");
      });
    });

    // City Autocomplete
    if (birthPlaceInput) {
      birthPlaceInput.addEventListener("input", (e) => handleCitySearch(e.target.value));
      document.addEventListener("click", (e) => {
        if (!e.target.closest(".city-search-container") && cityDropdown) {
          cityDropdown.style.display = "none";
        }
      });
    }

    if (btnClearCity) {
      btnClearCity.addEventListener("click", () => {
        birthPlaceInput.value = "";
        if (cityDropdown) cityDropdown.style.display = "none";
        birthPlaceInput.focus();
      });
    }

    // Manual Coordinates Toggle
    if (btnToggleManualCoords && manualCoordsDrawer) {
      btnToggleManualCoords.addEventListener("click", () => {
        const isHidden = manualCoordsDrawer.style.display === "none";
        manualCoordsDrawer.style.display = isHidden ? "block" : "none";
        btnToggleManualCoords.textContent = isHidden ? "Manual Coordinates ▴" : "Manual Coordinates ▾";
      });
    }

    // Nepal Districts Modal
    const btnOpenDistricts = document.getElementById("btnOpenDistrictsModal");
    const btnCloseDistricts = document.getElementById("btnCloseDistrictsModal");
    const districtFilter = document.getElementById("districtFilterInput");

    if (btnOpenDistricts) {
      btnOpenDistricts.addEventListener("click", () => {
        loadNepalDistricts();
        openModal("modalNepalDistricts");
      });
    }
    if (btnCloseDistricts) {
      btnCloseDistricts.addEventListener("click", () => closeModal("modalNepalDistricts"));
    }
    if (districtFilter) {
      districtFilter.addEventListener("input", (e) => filterNepalDistricts(e.target.value));
    }

    // Sample Profiles Modal
    const btnSampleProfiles = document.getElementById("btnSampleProfiles");
    const btnCloseSampleModal = document.getElementById("btnCloseSampleModal");
    const sampleList = document.getElementById("sampleProfilesList");

    if (btnSampleProfiles) {
      btnSampleProfiles.addEventListener("click", async () => {
        if (!sampleProfiles.length) {
          try {
            const res = await fetch("/api/sample-profiles");
            sampleProfiles = await res.json();
          } catch (e) {
            console.error(e);
          }
        }
        if (sampleList) {
          sampleList.innerHTML = sampleProfiles.map(p => `
            <div class="profile-card" data-id="${p.id}">
              <div>
                <span class="profile-title">${p.name}</span> (${p.gender})<br>
                <span class="profile-desc">${p.description}</span><br>
                <small style="color:var(--text-muted)">${p.birth_date} ${p.birth_time} • ${p.place}</small>
              </div>
              <button type="button" class="btn btn-sm btn-gold">Load</button>
            </div>
          `).join("");

          sampleList.querySelectorAll(".profile-card").forEach((card, idx) => {
            card.addEventListener("click", () => {
              const sp = sampleProfiles[idx];
              document.getElementById("nativeName").value = sp.name;
              document.getElementById("nativeGender").value = sp.gender;
              document.getElementById("birthDate").value = sp.birth_date;
              document.getElementById("birthTime").value = sp.birth_time;
              birthPlaceInput.value = sp.place;
              document.getElementById("inputLat").value = sp.latitude;
              document.getElementById("inputLng").value = sp.longitude;
              document.getElementById("inputTz").value = sp.timezone;
              lastGeocodedPlace = sp.place;
              closeModal("modalSampleProfiles");
              handleChartCalculation();
            });
          });
        }
        openModal("modalSampleProfiles");
      });
    }
    if (btnCloseSampleModal) {
      btnCloseSampleModal.addEventListener("click", () => closeModal("modalSampleProfiles"));
    }

    // Quick Chips
    document.querySelectorAll(".chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        birthPlaceInput.value = chip.dataset.city;
        document.getElementById("inputLat").value = chip.dataset.lat;
        document.getElementById("inputLng").value = chip.dataset.lng;
        document.getElementById("inputTz").value = chip.dataset.tz;
        lastGeocodedPlace = chip.dataset.city;
      });
    });

    // Profile Storage Manager
    function getSavedProfiles() {
      try {
        return JSON.parse(localStorage.getItem("kundali_saved_profiles") || "[]");
      } catch (e) {
        return [];
      }
    }

    function saveProfilesToStorage(list) {
      localStorage.setItem("kundali_saved_profiles", JSON.stringify(list));
      updateSavedCount();
    }

    function updateSavedCount() {
      const el = document.getElementById("savedCount");
      if (el) el.textContent = getSavedProfiles().length;
    }

    // Save Current Profile Button
    const btnSaveCurrent = document.getElementById("btnSaveCurrent");
    if (btnSaveCurrent) {
      btnSaveCurrent.addEventListener("click", () => {
        const name = document.getElementById("nativeName").value.trim() || "Native";
        const gender = document.getElementById("nativeGender").value;
        const birthDate = document.getElementById("birthDate").value;
        const birthTime = document.getElementById("birthTime").value;
        const place = birthPlaceInput.value.trim() || "Kathmandu, Nepal";
        const lat = parseFloat(document.getElementById("inputLat").value) || 27.7172;
        const lng = parseFloat(document.getElementById("inputLng").value) || 85.3240;
        const tz = document.getElementById("inputTz").value.trim() || "Asia/Kathmandu";
        const ayanamsha = document.getElementById("ayanamshaSelect").value || "LAHIRI";

        const profile = {
          id: "prof_" + Date.now(),
          name,
          gender,
          birth_date: birthDate,
          birth_time: birthTime,
          place,
          latitude: lat,
          longitude: lng,
          timezone: tz,
          ayanamsha,
          saved_at: new Date().toISOString(),
        };

        const list = getSavedProfiles();
        list.unshift(profile);
        saveProfilesToStorage(list);
        showToast(`Profile "${name}" saved locally!`, "success");
      });
    }

    // Saved Profiles Modal
    const btnSavedProfiles = document.getElementById("btnSavedProfiles");
    const btnCloseSavedModal = document.getElementById("btnCloseSavedModal");
    const savedListEl = document.getElementById("savedProfilesList");
    const btnExportJson = document.getElementById("btnExportJson");
    const importJsonInput = document.getElementById("importJsonInput");

    function renderSavedProfilesModal() {
      const list = getSavedProfiles();
      if (!savedListEl) return;
      if (!list.length) {
        savedListEl.innerHTML = `<div style="text-align:center;padding:30px;color:var(--text-muted)">No saved profiles yet. Click "Save Profile" to store horoscopes.</div>`;
        return;
      }

      savedListEl.innerHTML = list.map((p, idx) => `
        <div class="profile-card" data-idx="${idx}">
          <div>
            <span class="profile-title">${p.name}</span> (${p.gender || 'Native'})<br>
            <small style="color:var(--text-secondary)">Born: ${p.birth_date} ${p.birth_time} • ${p.place}</small>
          </div>
          <div style="display:flex;gap:6px">
            <button type="button" class="btn btn-sm btn-gold btn-load-saved" data-idx="${idx}">Load</button>
            <button type="button" class="btn btn-sm btn-outline btn-delete-saved" data-idx="${idx}" style="color:var(--accent-red)">✕</button>
          </div>
        </div>
      `).join("");

      savedListEl.querySelectorAll(".btn-load-saved").forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const idx = parseInt(btn.dataset.idx);
          const p = list[idx];
          if (!p) return;
          document.getElementById("nativeName").value = p.name;
          document.getElementById("nativeGender").value = p.gender || "Male";
          document.getElementById("birthDate").value = p.birth_date;
          document.getElementById("birthTime").value = p.birth_time;
          birthPlaceInput.value = p.place;
          document.getElementById("inputLat").value = p.latitude;
          document.getElementById("inputLng").value = p.longitude;
          document.getElementById("inputTz").value = p.timezone;
          lastGeocodedPlace = p.place;
          if (document.getElementById("ayanamshaSelect")) {
            document.getElementById("ayanamshaSelect").value = p.ayanamsha || "LAHIRI";
          }
          closeModal("modalSavedProfiles");
          handleChartCalculation();
        });
      });

      savedListEl.querySelectorAll(".btn-delete-saved").forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const idx = parseInt(btn.dataset.idx);
          list.splice(idx, 1);
          saveProfilesToStorage(list);
          renderSavedProfilesModal();
          showToast("Profile deleted.", "info");
        });
      });
    }

    if (btnSavedProfiles) {
      btnSavedProfiles.addEventListener("click", () => {
        renderSavedProfilesModal();
        openModal("modalSavedProfiles");
      });
    }
    if (btnCloseSavedModal) {
      btnCloseSavedModal.addEventListener("click", () => closeModal("modalSavedProfiles"));
    }

    // Export Profiles to JSON
    if (btnExportJson) {
      btnExportJson.addEventListener("click", () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(getSavedProfiles(), null, 2));
        const a = document.createElement("a");
        a.href = dataStr;
        a.download = "kundali_profiles.json";
        a.click();
        showToast("Exported profiles as JSON!", "success");
      });
    }

    // Import Profiles from JSON
    if (importJsonInput) {
      importJsonInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (evt) => {
          try {
            const imported = JSON.parse(evt.target.result);
            if (Array.isArray(imported)) {
              const merged = [...imported, ...getSavedProfiles()];
              saveProfilesToStorage(merged);
              renderSavedProfilesModal();
              showToast(`Imported ${imported.length} profiles!`, "success");
            }
          } catch (err) {
            showToast("Failed to parse JSON file.", "error");
          }
        };
        reader.readAsText(file);
      });
    }

    // Download SVG
    function triggerDownloadSvg() {
      const svgEl = chartSvgWrapper ? chartSvgWrapper.querySelector("svg") : null;
      if (!svgEl) {
        showToast("No active chart SVG found to download.", "error");
        return;
      }
      const svgData = new XMLSerializer().serializeToString(svgEl);
      const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      const name = (document.getElementById("nativeName").value || "Kundali").replace(/\s+/g, "_");
      link.href = url;
      link.download = `${name}_${currentVarga}_Chart.svg`;
      link.click();
      URL.revokeObjectURL(url);
      showToast(`Downloaded ${currentVarga} Chart as SVG!`, "success");
    }

    const btnDownloadSvg = document.getElementById("btnDownloadSvg");
    if (btnDownloadSvg) {
      btnDownloadSvg.addEventListener("click", triggerDownloadSvg);
    }

    // Export & Print Modal Controller
    const btnPrintReport = document.getElementById("btnPrintReport");
    const btnCloseExportModal = document.getElementById("btnCloseExportModal");
    const btnTriggerPrint = document.getElementById("btnTriggerPrint");
    const btnExportSvgModal = document.getElementById("btnExportSvgModal");
    const btnExportChartJson = document.getElementById("btnExportChartJson");

    if (btnPrintReport) {
      btnPrintReport.addEventListener("click", () => {
        openModal("modalExportReport");
      });
    }

    if (btnCloseExportModal) {
      btnCloseExportModal.addEventListener("click", () => {
        closeModal("modalExportReport");
      });
    }

    if (btnTriggerPrint) {
      btnTriggerPrint.addEventListener("click", () => {
        closeModal("modalExportReport");
        setTimeout(() => {
          window.print();
        }, 200);
      });
    }

    if (btnExportSvgModal) {
      btnExportSvgModal.addEventListener("click", () => {
        closeModal("modalExportReport");
        triggerDownloadSvg();
      });
    }

    if (btnExportChartJson) {
      btnExportChartJson.addEventListener("click", () => {
        closeModal("modalExportReport");
        if (!currentChartData) {
          showToast("Please calculate a chart first before exporting data.", "error");
          return;
        }
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(currentChartData, null, 2));
        const a = document.createElement("a");
        const name = (document.getElementById("nativeName").value || "Kundali").replace(/\s+/g, "_");
        a.href = dataStr;
        a.download = `${name}_Complete_Kundali_Data.json`;
        a.click();
        showToast("Horoscope JSON dataset exported successfully!", "success");
      });
    }

    // Update Saved Count on Startup
    updateSavedCount();

    // Auto-calculate initial chart
    handleChartCalculation();
  }

  // Run on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initApp);
  } else {
    initApp();
  }
})();
