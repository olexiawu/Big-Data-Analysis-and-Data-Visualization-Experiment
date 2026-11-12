/* ==========================================================================
   驾驶舱应用层：数据派生、KPI、季切换、明细表、响应式重绘
   ========================================================================== */

(function () {
  'use strict';

  const D = window.GDP_DATA;
  const C = window.Charts;

  /** 静态模式：地址带 #static 时关闭全部入场动效，便于截图与打印 */
  const STATIC = /(?:^|[?#&])static\b/i.test(location.hash + location.search);
  if (STATIC) {
    window.__STATIC__ = true;
    document.documentElement.classList.add('is-static');
  }

  if (!D) {
    console.error('未找到 window.GDP_DATA，请确认 assets/js/data.js 已加载');
    return;
  }

  const fmt1 = C.fmt1;
  const fmt0 = C.fmt0;
  const signed = C.signed;
  const pct = C.pct;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  const SECTOR_COLORS = { primary: '#34d399', secondary: '#38bdf8', tertiary: '#a78bfa' };

  const state = { active: D.quarters.length - 1 };

  /* ---------- 视图模型 ---------- */

  const byKey = {};
  D.indicators.forEach((d) => {
    byKey[d.key] = d;
  });

  const quarters = D.quarters;
  const gdpQ = byKey.gdp.q;
  const gdpCum = byKey.gdp.cum;
  const sectors = D.indicators
    .filter((d) => d.level === 'sector')
    .map((d) => ({ ...d, color: SECTOR_COLORS[d.key] }));
  const industries = D.indicators
    .filter((d) => d.level === 'industry')
    .map((d) => ({ ...d, color: '#38bdf8' }));

  /** 增速口径：优先同比（有上年同季数据时），否则环比 */
  function growthFor(i) {
    if (i >= 4) {
      return {
        mode: 'yoy',
        values: industries.map((d) => pct(d.q[i], d.q[i - 4])),
        label: '同比',
        note: `${quarters[i]} vs ${quarters[i - 4]}`,
      };
    }
    if (i >= 1) {
      return {
        mode: 'qoq',
        values: industries.map((d) => pct(d.q[i], d.q[i - 1])),
        label: '环比',
        note: `${quarters[i]} vs ${quarters[i - 1]}`,
      };
    }
    return { mode: 'none', values: industries.map(() => 0), label: '—', note: '缺少基期' };
  }

  function buildCtx() {
    return {
      quarters,
      gdpQ,
      gdpCum,
      sectors,
      industries,
      active: state.active,
      growth: growthFor(state.active),
    };
  }

  /* ---------- 数字滚动 ---------- */

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function tween(el, to, decimals, duration) {
    const dur = duration || 720;
    if (reduceMotion || STATIC) {
      el.textContent = decimals ? fmt1(to) : fmt0(to);
      return;
    }
    const t0 = performance.now();
    const step = (now) => {
      const p = Math.min(1, (now - t0) / dur);
      const v = to * (1 - Math.pow(1 - p, 3));
      el.textContent = decimals ? fmt1(v) : fmt0(v);
      if (p < 1) el._raf = requestAnimationFrame(step);
    };
    cancelAnimationFrame(el._raf);
    el._raf = requestAnimationFrame(step);
  }

  /* ---------- KPI ---------- */

  function chipHTML(v, suffix, note) {
    if (v === undefined) {
      return `<span class="kpi__note">${note}</span>`;
    }
    if (v === null || !isFinite(v)) {
      return `<span class="chip chip--flat">—</span><span class="kpi__note">${note}</span>`;
    }
    const cls = v > 0.0001 ? 'chip--up' : v < -0.0001 ? 'chip--down' : 'chip--flat';
    const arrow = v > 0.0001 ? '▲' : v < -0.0001 ? '▼' : '·';
    return `<span class="chip ${cls}">${arrow} ${Math.abs(v).toFixed(1)}${suffix || '%'}</span><span class="kpi__note">${note}</span>`;
  }

  function kpiHTML(card) {
    return `<article class="kpi" style="--accent:${card.accent}">
      <div class="kpi__top">
        <span class="kpi__label">${card.label}</span>
        <span class="kpi__en">${card.en}</span>
      </div>
      <div class="kpi__value">
        <span class="kpi__num" data-to="${card.value}" data-dec="${card.decimals}">${card.decimals ? fmt1(card.value) : fmt0(card.value)}</span>
        <span class="kpi__unit">${card.unit}</span>
      </div>
      <div class="kpi__foot">
        <div class="kpi__meta">${chipHTML(card.delta, card.deltaSuffix, card.note)}</div>
        ${card.spark ? C.sparkline(card.spark.values, card.spark.color) : ''}
      </div>
    </article>`;
  }

  function renderKpis() {
    const i = state.active;
    const q = gdpQ[i];
    const prev = i > 0 ? gdpQ[i - 1] : null;

    const shareOf = (key, idx) => (byKey[key].q[idx] / gdpQ[idx]) * 100;
    const sharesT = quarters.map((_, k) => shareOf('tertiary', k));
    const sharesM = quarters.map((_, k) => shareOf('manufacturing', k));

    const growth = growthFor(i);
    let topIdx = 0;
    growth.values.forEach((v, k) => {
      if (v > growth.values[topIdx]) topIdx = k;
    });
    const top = industries[topIdx];

    const expanding = growth.values.filter((v) => v > 0).length;
    const prevGrowth = i >= 1 ? growthFor(i - 1).values.filter((v) => v > 0).length : null;

    const cards = [
      {
        label: '当季 GDP',
        en: 'GDP · QUARTER',
        value: q,
        decimals: true,
        unit: '亿元',
        accent: '#22d3ee',
        delta: prev ? pct(q, prev) : null,
        note: '环比',
        spark: { values: gdpQ, color: '#22d3ee' },
      },
      {
        label: '年度累计 GDP',
        en: 'GDP · YTD',
        value: gdpCum[i],
        decimals: true,
        unit: '亿元',
        accent: '#38bdf8',
        delta: i >= 4 ? pct(gdpCum[i], gdpCum[i - 4]) : null,
        note: '累计同比',
        spark: { values: gdpCum, color: '#38bdf8' },
      },
      {
        label: '第三产业占比',
        en: 'SERVICE SHARE',
        value: sharesT[i],
        decimals: true,
        unit: '%',
        accent: '#a78bfa',
        delta: i > 0 ? sharesT[i] - sharesT[i - 1] : null,
        deltaSuffix: 'pp',
        note: '较上季',
        spark: { values: sharesT, color: '#a78bfa' },
      },
      {
        label: '制造业占比',
        en: 'MANUFACTURING',
        value: sharesM[i],
        decimals: true,
        unit: '%',
        accent: '#34d399',
        delta: i > 0 ? sharesM[i] - sharesM[i - 1] : null,
        deltaSuffix: 'pp',
        note: '较上季',
        spark: { values: sharesM, color: '#34d399' },
      },
      {
        label: '领先行业增速',
        en: 'TOP MOMENTUM',
        value: growth.values[topIdx],
        decimals: true,
        unit: '%',
        accent: '#fbbf24',
        delta: undefined,
        note: top ? `${top.short} · ${growth.label}` : growth.label,
        spark: top ? { values: top.q, color: '#fbbf24' } : null,
      },
      {
        label: '扩张行业数',
        en: 'EXPANDING',
        value: expanding,
        decimals: false,
        unit: `/ ${industries.length} 行业`,
        accent: '#fb7185',
        delta: prevGrowth === null ? null : expanding - prevGrowth,
        deltaSuffix: ' 个',
        note: `${growth.label}为正`,
      },
    ];

    const box = document.getElementById('kpis');
    box.innerHTML = cards.map(kpiHTML).join('');
    box.querySelectorAll('.kpi__num').forEach((el) => {
      const to = Number(el.getAttribute('data-to'));
      const dec = el.getAttribute('data-dec') === 'true';
      el.textContent = dec ? fmt1(0) : fmt0(0);
      tween(el, to, dec, 900);
    });
  }

  /* ---------- 图例 / 标签 ---------- */

  function renderChrome() {
    const i = state.active;
    const q = quarters[i];

    document.getElementById('legend-main').innerHTML =
      sectors
        .map(
          (s) =>
            `<span class="legend__item"><i class="legend__swatch" style="--sw:${s.color};background:${s.color}"></i>${s.name}</span>`
        )
        .join('') +
      `<span class="legend__item"><i class="legend__swatch--line" style="--sw:#fbbf24;background:#fbbf24"></i>累计值</span>`;

    document.getElementById('legend-cum').innerHTML = [
      ['#8b5cf6', '2025 年累计'],
      ['#22d3ee', '2026 年累计'],
    ]
      .map(
        ([c, t]) =>
          `<span class="legend__item"><i class="legend__swatch--line" style="--sw:${c};background:${c}"></i>${t}</span>`
      )
      .join('');

    document.getElementById('tag-donut').textContent = q;
    document.getElementById('tag-rank').textContent = q + ' · 当季';
    document.getElementById('tag-table').textContent = q;

    const g = growthFor(i);
    const tagGrowth = document.getElementById('tag-growth');
    tagGrowth.textContent = g.mode === 'none' ? '缺少基期' : `${g.label} · ${g.note}`;
    tagGrowth.title = g.mode === 'yoy' ? '与上年同季对比' : '与上一季度对比';

    document.getElementById('foot-updated').textContent = D.meta.updated;
  }

  /* ---------- 明细表 ---------- */

  function renderTable() {
    const i = state.active;
    const rows = [byKey.gdp, ...sectors, ...industries];

    const body = rows
      .map((d) => {
        const v = d.q[i];
        const share = (v / gdpQ[i]) * 100;
        const qoq = i > 0 ? pct(v, d.q[i - 1]) : null;
        const yoy = i >= 4 ? pct(v, d.q[i - 4]) : null;
        const cls = (x) => (x === null ? 'mute' : x > 0.05 ? 'pos' : x < -0.05 ? 'neg' : 'mute');
        const cell = (x) => (x === null ? '—' : signed(x) + '%');
        return `<tr class="${d.key === 'gdp' ? 'is-total' : ''}">
          <td>${d.name}</td>
          <td>${fmt1(v)}</td>
          <td>${share.toFixed(1)}%</td>
          <td class="${cls(qoq)}">${cell(qoq)}</td>
          <td class="${cls(yoy)}">${cell(yoy)}</td>
        </tr>`;
      })
      .join('');

    document.getElementById('table-wrap').innerHTML = `<table class="ledger">
      <thead><tr><th>指标</th><th>当季值</th><th>占比</th><th>环比</th><th>同比</th></tr></thead>
      <tbody>${body}</tbody>
    </table>`;
  }

  /* ---------- 季度切换 ---------- */

  function renderChips() {
    const box = document.getElementById('quarters');
    box.innerHTML = quarters
      .map(
        (q, i) =>
          `<button type="button" class="q-chip${i === state.active ? ' is-active' : ''}" data-i="${i}" aria-pressed="${
            i === state.active
          }" title="${q} 数据">${q.slice(2)}</button>`
      )
      .join('');
  }

  /* ---------- 图表渲染调度 ---------- */

  const VIEWS = {
    'chart-main': 'stacked',
    'chart-donut': 'donut',
    'chart-rank': 'rankChart',
    'chart-growth': 'growthChart',
    'chart-heat': 'heatChart',
    'chart-cum': 'cumulativeChart',
  };

  const lastSize = {};

  function renderChart(id) {
    const box = document.getElementById(id);
    if (!box) return;
    const rect = box.getBoundingClientRect();
    if (rect.width < 10 || rect.height < 10) return;
    C[VIEWS[id]](box, buildCtx());
  }

  function renderAll() {
    Object.keys(VIEWS).forEach(renderChart);
  }

  /* ---------- 统一刷新 ---------- */

  function refresh() {
    renderChips();
    renderKpis();
    renderChrome();
    renderTable();
    renderAll();
  }

  function setActive(i) {
    const next = clamp(i, 0, quarters.length - 1);
    if (next === state.active) return;
    state.active = next;
    refresh();
  }

  /* ---------- 初始化 ---------- */

  function init() {
    renderChips();
    renderKpis();
    renderChrome();
    renderTable();
    // 等待布局稳定后再绘制；静态模式直接同步绘制，便于截图 / 打印
    if (STATIC) {
      renderAll();
    } else {
      requestAnimationFrame(renderAll);
    }

    document.getElementById('quarters').addEventListener('click', (e) => {
      const btn = e.target.closest('.q-chip');
      if (!btn) return;
      setActive(Number(btn.getAttribute('data-i')));
    });

    document.addEventListener('keydown', (e) => {
      if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
      if (e.key === 'ArrowRight') setActive(state.active + 1);
      if (e.key === 'ArrowLeft') setActive(state.active - 1);
    });

    // 时钟
    const clock = document.getElementById('clock');
    const tick = () => {
      const d = new Date();
      const z = (n) => String(n).padStart(2, '0');
      clock.textContent = `${z(d.getHours())}:${z(d.getMinutes())}:${z(d.getSeconds())}`;
    };
    tick();
    setInterval(tick, 1000);

    // 响应式重绘
    if ('ResizeObserver' in window) {
      const ro = new ResizeObserver((entries) => {
        let dirty = false;
        entries.forEach((entry) => {
          const id = entry.target.id;
          const r = entry.contentRect;
          const prev = lastSize[id];
          if (!prev || Math.abs(prev.w - r.width) > 2 || Math.abs(prev.h - r.height) > 2) {
            lastSize[id] = { w: r.width, h: r.height };
            dirty = true;
          }
        });
        if (dirty) {
          cancelAnimationFrame(init._raf);
          init._raf = requestAnimationFrame(renderAll);
        }
      });
      Object.keys(VIEWS).forEach((id) => {
        const box = document.getElementById(id);
        if (!box) return;
        const r = box.getBoundingClientRect();
        lastSize[id] = { w: r.width, h: r.height };
        ro.observe(box);
      });
    } else {
      window.addEventListener('resize', () => renderAll());
    }

    window.addEventListener('resize', () => {
      cancelAnimationFrame(init._raf2);
      init._raf2 = requestAnimationFrame(renderTable);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
