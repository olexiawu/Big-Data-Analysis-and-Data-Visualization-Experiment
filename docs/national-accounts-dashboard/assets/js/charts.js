/* ==========================================================================
   驾驶舱图表引擎 —— 零依赖纯 SVG 实现
   所有图表以「容器尺寸」为基准重绘，配合 ResizeObserver 实现响应式。
   ========================================================================== */

(function (global) {
  'use strict';

  const nf1 = new Intl.NumberFormat('zh-CN', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const nf0 = new Intl.NumberFormat('zh-CN', { maximumFractionDigits: 0 });

  const fmt1 = (v) => nf1.format(v);
  const fmt0 = (v) => nf0.format(v);
  const wan1 = (v) => (v / 1e4).toFixed(1);
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const pct = (a, b) => (b ? (a / b - 1) * 100 : 0);
  const signed = (v, d = 1) => (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v).toFixed(d);

  const C = {
    cyan: '#22d3ee',
    cyanSoft: '#67e8f9',
    blue: '#3b82f6',
    violet: '#a78bfa',
    emerald: '#34d399',
    amber: '#fbbf24',
    rose: '#fb7185',
    text: '#e9f2ff',
    text2: '#9fb3cd',
    text3: '#61789a',
    grid: 'rgba(120, 165, 220, 0.13)',
  };

  const esc = (s) =>
    String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /** 静态模式（#static）：用于截图 / 打印，关闭所有入场动效 */
  const noMotion = () => window.__STATIC__ === true;

  /* ------------------------------------------------------------------ */
  /* 基础工具                                                            */
  /* ------------------------------------------------------------------ */

  function size(box) {
    const r = box.getBoundingClientRect();
    return {
      w: Math.max(220, Math.round(r.width)),
      h: Math.max(140, Math.round(r.height)),
    };
  }

  /** 生成「好看」的刻度：返回上界与刻度数组 */
  function niceScale(max, count = 4) {
    if (!isFinite(max) || max <= 0) return { top: 1, ticks: [0, 1] };
    const raw = max / count;
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const norm = raw / mag;
    const step = (norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 2.5 ? 2.5 : norm <= 5 ? 5 : 10) * mag;
    const top = Math.ceil(max / step) * step;
    const ticks = [];
    for (let v = 0; v <= top + step * 0.001; v += step) ticks.push(Number(v.toFixed(6)));
    return { top, ticks };
  }

  const svgOpen = (w, h) =>
    `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">`;

  function hiddenRect(x, y, w, h, ti) {
    return `<rect x="${x}" y="${y}" width="${Math.max(0, w)}" height="${Math.max(0, h)}" fill="transparent" data-ti="${ti}" style="cursor:crosshair"/>`;
  }

  /* ------------------------------------------------------------------ */
  /* Tooltip                                                             */
  /* ------------------------------------------------------------------ */

  let tipEl = null;

  function ensureTip() {
    if (!tipEl) tipEl = document.getElementById('tooltip');
    return tipEl;
  }

  function showTip(html, evt) {
    const t = ensureTip();
    if (!t) return;
    t.innerHTML = html;
    t.classList.add('is-on');
    t.setAttribute('aria-hidden', 'false');
    moveTip(evt);
  }

  function moveTip(evt) {
    const t = ensureTip();
    if (!t || !t.classList.contains('is-on')) return;
    const pad = 14;
    const tw = t.offsetWidth;
    const th = t.offsetHeight;
    let x = evt.clientX + pad;
    let y = evt.clientY + pad;
    if (x + tw > window.innerWidth - 8) x = evt.clientX - tw - pad;
    if (y + th > window.innerHeight - 8) y = evt.clientY - th - pad;
    t.style.transform = `translate3d(${Math.max(8, x)}px, ${Math.max(8, y)}px, 0)`;
  }

  function hideTip() {
    const t = ensureTip();
    if (!t) return;
    t.classList.remove('is-on');
    t.setAttribute('aria-hidden', 'true');
  }

  function bindTips(box, tips) {
    box.querySelectorAll('[data-ti]').forEach((node) => {
      const i = Number(node.getAttribute('data-ti'));
      node.addEventListener('mouseenter', (e) => showTip(tips[i], e));
      node.addEventListener('mousemove', moveTip);
      node.addEventListener('mouseleave', hideTip);
    });
  }

  function tipRow(color, label, value) {
    return `<div class="row"><span>${
      color ? `<i style="background:${color}"></i>` : ''
    }${esc(label)}</span><em>${esc(value)}</em></div>`;
  }

  /* ------------------------------------------------------------------ */
  /* 1. 主图：当季 GDP 三次产业堆叠 + 累计值曲线                          */
  /* ------------------------------------------------------------------ */

  function stacked(box, ctx) {
    const { w, h } = size(box);
    const pad = { t: 30, r: 50, b: 30, l: 46 };
    const pw = w - pad.l - pad.r;
    const ph = h - pad.t - pad.b;
    const n = ctx.quarters.length;
    const step = pw / n;
    const bw = Math.min(44, step * 0.4);
    const baseY = pad.t + ph;

    const maxQ = Math.max(...ctx.gdpQ);
    const qs = niceScale(maxQ, 4);
    const maxC = Math.max(...ctx.gdpCum);
    const cs = niceScale(maxC, 4);

    const y = (v) => pad.t + ph * (1 - v / qs.top);
    const yc = (v) => pad.t + ph * (1 - v / cs.top);

    const tips = [];
    const labels = [];
    const hits = [];
    const points = [];

    ctx.quarters.forEach((q, i) => {
      const cx = pad.l + step * i + step / 2;
      const active = i === ctx.active;

      const totalY = y(ctx.gdpQ[i]);
      labels.push(
        `<text x="${cx}" y="${totalY - 7}" text-anchor="middle" font-size="9.5" fill="${
          active ? '#cfeeff' : '#7e94b3'
        }" letter-spacing="0.3">${fmt0(ctx.gdpQ[i])}</text>`
      );

      const t = [];
      t.push(`<b>${esc(q)}</b>`);
      ctx.sectors.forEach((s) => {
        t.push(tipRow(s.color, s.name, fmt1(s.q[i])));
      });
      t.push('<div class="sep"></div>');
      t.push(tipRow('', 'GDP 当季值', fmt1(ctx.gdpQ[i])));
      t.push(tipRow('', '累计值', fmt1(ctx.gdpCum[i])));
      if (i >= 4) t.push(tipRow('', '同比', signed(pct(ctx.gdpQ[i], ctx.gdpQ[i - 4])) + '%'));
      tips.push(t.join(''));

      hits.push(hiddenRect(pad.l + step * i, pad.t, step, ph, tips.length - 1));

      points.push({ x: cx, y: yc(ctx.gdpCum[i]), v: ctx.gdpCum[i], i });
    });

    const linePath = points.map((p, i) => `${i ? 'L' : 'M'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');

    const grid = qs.ticks
      .map(
        (v) =>
          `<line x1="${pad.l}" y1="${y(v)}" x2="${w - pad.r}" y2="${y(v)}" stroke="${C.grid}" stroke-dasharray="${
            v === 0 ? '0' : '3 5'
          }"/>` +
          `<text x="${pad.l - 8}" y="${y(v) + 3}" text-anchor="end" font-size="9" fill="#5d7492">${wan1(v)}万</text>`
      )
      .join('');

    const rightAxis = cs.ticks
      .filter((v) => v > 0)
      .map(
        (v) =>
          `<text x="${w - pad.r + 8}" y="${yc(v) + 3}" font-size="8.5" fill="rgba(251,191,36,.55)">${wan1(v)}</text>`
      )
      .join('');

    const dots = points
      .map((p) => {
        const active = p.i === ctx.active;
        return (
          `<circle cx="${p.x}" cy="${p.y}" r="${active ? 4.2 : 2.8}" fill="${active ? C.amber : '#0a1420'}" stroke="${
            C.amber
          }" stroke-width="${active ? 2 : 1.4}" />` +
          (active ? `<circle cx="${p.x}" cy="${p.y}" r="9" fill="none" stroke="rgba(251,191,36,.35)" stroke-width="1"/>` : '')
        );
      })
      .join('');

    const xLabels = ctx.quarters
      .map((q, i) => {
        const cx = pad.l + step * i + step / 2;
        const active = i === ctx.active;
        return `<text x="${cx}" y="${baseY + 18}" text-anchor="middle" font-size="9.5" fill="${
          active ? '#d8f4ff' : '#61789a'
        }" letter-spacing="0.5" font-weight="${active ? 600 : 400}">${q}</text>`;
      })
      .join('');

    const svg =
      svgOpen(w, h) +
      `<defs>
        <linearGradient id="grad0" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#4ade9f"/><stop offset="1" stop-color="#0f766e"/>
        </linearGradient>
        <linearGradient id="grad1" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#5ee7ff"/><stop offset="1" stop-color="#1d4ed8"/>
        </linearGradient>
        <linearGradient id="grad2" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#c4b5fd"/><stop offset="1" stop-color="#6d28d9"/>
        </linearGradient>
        <linearGradient id="bandGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="rgba(34,211,238,.14)"/><stop offset="1" stop-color="rgba(34,211,238,0)"/>
        </linearGradient>
        <linearGradient id="cumStroke" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="rgba(251,191,36,.35)"/><stop offset="0.5" stop-color="#fbbf24"/><stop offset="1" stop-color="#fcd34d"/>
        </linearGradient>
        <filter id="lineGlow" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur stdDeviation="3.5" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>` +
      grid +
      rightAxis +
      // 选中季度的背景高亮带
      `<g>${ctx.quarters
        .map((q, i) => {
          if (i !== ctx.active) return '';
          const cx = pad.l + step * i + step / 2;
          return `<rect x="${cx - step / 2 + 3}" y="${pad.t}" width="${step - 6}" height="${ph}" fill="url(#bandGrad)"/>`;
        })
        .join('')}</g>` +
      // 堆叠柱体
      ctx.quarters
        .map((q, i) => {
          const cx = pad.l + step * i + step / 2;
          const x = cx - bw / 2;
          const active = i === ctx.active;
          let acc = 0;
          return ctx.sectors
            .map((s, si) => {
              const v = s.q[i];
              const yTop = y(acc + v);
              const hh = Math.max(0, y(acc) - yTop - 1.4);
              const yy = y(acc) - hh - 0.7;
              acc += v;
              if (hh <= 0.6) return '';
              const isTop = si === ctx.sectors.length - 1;
              return isTop
                ? `<path d="${barPath(x, yy, bw, hh, 2.5)}" fill="url(#grad${si})" opacity="${active ? 1 : 0.86}"/>`
                : `<rect x="${x}" y="${yy}" width="${bw}" height="${hh}" fill="url(#grad${si})" opacity="${active ? 1 : 0.86}"/>`;
            })
            .join('');
        })
        .join('') +
      `<path d="${linePath}" fill="none" stroke="url(#cumStroke)" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round" opacity=".85" pathLength="1" class="draw-line"/>` +
      dots +
      labels.join('') +
      xLabels +
      `<text x="${pad.l - 8}" y="${pad.t - 13}" text-anchor="end" font-size="7.5" fill="#4d6079" letter-spacing="0.12em">当季 · 万</text>` +
      `<text x="${w - pad.r - 2}" y="${pad.t - 13}" text-anchor="end" font-size="7.5" fill="rgba(251,191,36,.55)" letter-spacing="0.12em">累计 · 万</text>` +
      hits.join('') +
      '</svg>';

    box.innerHTML = svg;
    bindTips(box, tips);

    const line = box.querySelector('.draw-line');
    if (!noMotion() && line && line.animate) {
      line.animate([{ strokeDasharray: '1 1', strokeDashoffset: 1 }, { strokeDasharray: '1 1', strokeDashoffset: 0 }], {
        duration: 1100,
        easing: 'cubic-bezier(.35,.9,.3,1)',
        fill: 'backwards',
      });
    }
  }

  function barPath(x, y, w, h, r) {
    r = Math.max(0, Math.min(r, w / 2, h));
    return `M${x},${y + h} L${x},${y + r} Q${x},${y} ${x + r},${y} L${x + w - r},${y} Q${x + w},${y} ${
      x + w
    },${y + r} L${x + w},${y + h} Z`;
  }

  /* ------------------------------------------------------------------ */
  /* 2. 环形图：三次产业结构                                              */
  /* ------------------------------------------------------------------ */

  function donut(box, ctx) {
    const { w, h } = size(box);
    const side = w >= 340; // 图例放在右侧
    const compact = w < 430; // 窄屏图例省略绝对值
    const r = side
      ? clamp(Math.min(h / 2 - 8, (w - (compact ? 150 : 215)) / 2), 56, 108)
      : clamp(Math.min((h - 96) / 2, 70), 42, 70);
    const inner = r * 0.635;
    const cx = side ? r + 18 : w / 2;
    const cy = side ? h / 2 : r + 10;
    const rowH = side ? 27 : 22;
    const rm = (r + inner) / 2;
    const circ = 2 * Math.PI * rm;
    const sw = r - inner;
    const total = ctx.sectors.reduce((s, x) => s + x.q[ctx.active], 0);

    const tips = [];
    let startShare = 0;
    const arcs = ctx.sectors
      .map((s, i) => {
        const v = s.q[ctx.active];
        const share = v / total;
        const gap = share > 0.02 ? 1.6 : 0;
        const len = Math.max(circ * share - gap, 0.8);
        const offset = -circ * startShare;
        startShare += share;

        const t = [`<b>${esc(s.name)}</b>`];
        t.push(tipRow(s.color, '增加值', fmt1(v)));
        t.push(tipRow('', '占 GDP', (share * 100).toFixed(2) + '%'));
        if (ctx.active > 0) t.push(tipRow('', '较上季', signed((share - s.q[ctx.active - 1] / ctx.gdpQ[ctx.active - 1]) * 100, 2) + ' pp'));
        tips.push(t.join(''));

        return (
          `<circle class="seg" data-ti="${tips.length - 1}" cx="${cx}" cy="${cy}" r="${rm}" fill="none" stroke="${
            s.color
          }" stroke-width="${sw}" stroke-dasharray="${len} ${circ}" stroke-dashoffset="${offset}" stroke-linecap="butt" style="cursor:pointer"/>`
        );
      })
      .join('');

    const ticks = Array.from({ length: 60 }, (_, i) => {
      const a = (i / 60) * Math.PI * 2;
      const r1 = r + 5;
      const r2 = r + (i % 5 === 0 ? 11 : 8);
      const o = i % 5 === 0 ? 0.28 : 0.12;
      return `<line x1="${cx + Math.cos(a) * r1}" y1="${cy + Math.sin(a) * r1}" x2="${cx + Math.cos(a) * r2}" y2="${
        cy + Math.sin(a) * r2
      }" stroke="rgba(103,232,249,${o})" stroke-width="1"/>`;
    }).join('');

    const legendRows = ctx.sectors
      .map((s, i) => {
        const v = s.q[ctx.active];
        const share = (v / total) * 100;
        return `<g transform="translate(0,${i * rowH})">
          <rect x="0" y="-5" width="8" height="8" rx="2" fill="${s.color}"/>
          <text x="15" y="0" font-size="9.5" fill="#a8bcd6">${esc(s.name)}</text>
          <text x="74" y="0" font-size="10.5" fill="#e8f7ff" font-weight="600" font-family="Bahnschrift, Segoe UI, sans-serif">${share.toFixed(
            1
          )}%</text>
          ${
            compact
              ? ''
              : `<text x="124" y="0" font-size="8.5" fill="#61789a" font-family="Bahnschrift, Segoe UI, sans-serif">${fmt0(
                  v
                )}</text>`
          }
        </g>`;
      })
      .join('');

    const legendX = side ? cx + r + 26 : Math.max(12, w / 2 - 62);
    const legendY = side ? cy - rowH : cy + r + 28;

    const centerTop = ctx.gdpQ[ctx.active];
    const svg =
      svgOpen(w, h) +
      `<defs>
        <radialGradient id="coreGlow"><stop offset="0" stop-color="rgba(34,211,238,.16)"/><stop offset="1" stop-color="rgba(34,211,238,0)"/></radialGradient>
        <filter id="donutGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>` +
      `<circle cx="${cx}" cy="${cy}" r="${inner * 1.02}" fill="url(#coreGlow)"/>` +
      `<circle cx="${cx}" cy="${cy}" r="${inner - 4}" fill="none" stroke="rgba(34,211,238,.16)" stroke-width="1" stroke-dasharray="2 4"/>` +
      ticks +
      `<g transform="rotate(-90 ${cx} ${cy})">${arcs}</g>` +
      `<text x="${cx}" y="${cy - 2}" text-anchor="middle" font-size="${clamp(r * 0.19, 13, 20)}" font-weight="600" fill="#ffffff" font-family="Bahnschrift, Segoe UI, sans-serif">${wan1(
        centerTop
      )}<tspan font-size="${clamp(r * 0.095, 8, 10)}" fill="#7f95b3"> 万</tspan></text>` +
      `<text x="${cx}" y="${cy + 14}" text-anchor="middle" font-size="${clamp(r * 0.08, 7, 8.5)}" fill="#61789a" letter-spacing="0.16em">当季 GDP · 亿元</text>` +
      `<g transform="translate(${legendX},${legendY})">` +
      legendRows +
      '</g>' +
      '</svg>';

    box.innerHTML = svg;
    bindTips(box, tips);

    box.querySelectorAll('.seg').forEach((seg, i) => {
      if (noMotion() || !seg.animate) return;
      const finalDash = seg.getAttribute('stroke-dasharray');
      const len = parseFloat(finalDash);
      seg.animate([{ strokeDasharray: `0 ${circ}` }, { strokeDasharray: finalDash }], {
        duration: 760,
        delay: i * 130,
        easing: 'cubic-bezier(.25,.85,.3,1)',
        fill: 'backwards',
      });
      seg.addEventListener('mouseenter', () => {
        seg.setAttribute('stroke-width', sw + 5);
        seg.setAttribute('filter', 'url(#donutGlow)');
      });
      seg.addEventListener('mouseleave', () => {
        seg.setAttribute('stroke-width', sw);
        seg.removeAttribute('filter');
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* 3. 行业增加值排行                                                    */
  /* ------------------------------------------------------------------ */

  function rankChart(box, ctx) {
    const { w, h } = size(box);
    const i = ctx.active;
    const list = ctx.industries.slice().sort((a, b) => b.q[i] - a.q[i]);
    const n = list.length;
    const topPad = 4;
    const rowH = (h - topPad - 4) / n;
    const labelW = 58;
    const valW = 64;
    const x0 = labelW + 6;
    const x1 = w - valW;
    const max = Math.max(...list.map((d) => d.q[i]));
    const bh = Math.min(11, rowH * 0.44);
    const tips = [];

    const rows = list
      .map((d, k) => {
        const v = d.q[i];
        const cy = topPad + rowH * k + rowH / 2;
        const bwv = Math.max(2, ((x1 - x0) * v) / max);
        const c = k === 0 ? C.cyan : k === 1 ? '#38bdf8' : k === 2 ? '#60a5fa' : '#3b82f6';
        const share = (v / ctx.gdpQ[i]) * 100;
        const qoq = i > 0 ? pct(v, d.q[i - 1]) : null;
        const yoy = i >= 4 ? pct(v, d.q[i - 4]) : null;

        const t = [`<b>${esc(d.name)}</b>`];
        t.push(tipRow(c, '当季增加值', fmt1(v)));
        t.push(tipRow('', '占 GDP', share.toFixed(2) + '%'));
        if (qoq !== null) t.push(tipRow('', '环比', signed(qoq) + '%'));
        if (yoy !== null) t.push(tipRow('', '同比', signed(yoy) + '%'));
        tips.push(t.join(''));

        return (
          `<g data-ti="${tips.length - 1}" style="cursor:pointer">
            <rect x="0" y="${topPad + rowH * k}" width="${w}" height="${rowH}" fill="transparent"/>
            <text x="0" y="${cy + 3}" font-size="8.5" fill="#4f6a8d" font-family="Bahnschrift, Segoe UI, sans-serif">${String(
              k + 1
            ).padStart(2, '0')}</text>
            <text x="16" y="${cy + 3.4}" font-size="10" fill="${k < 3 ? '#dcefff' : '#a4bad4'}">${esc(d.short)}</text>
            <rect x="${x0}" y="${cy - bh / 2}" width="${x1 - x0}" height="${bh}" rx="${bh / 2}" fill="rgba(120,165,220,.07)"/>
            <rect class="bar-grow" x="${x0}" y="${cy - bh / 2}" width="${bwv}" height="${bh}" rx="${bh / 2}" fill="url(#rk${
              k === 0 ? '0' : '1'
            })" opacity="${k === 0 ? 1 : 0.9}"/>
            <text x="${w - 4}" y="${cy + 3.2}" text-anchor="end" font-size="9.8" fill="${
              k === 0 ? '#e9fbff' : '#9fb3cd'
            }" font-family="Bahnschrift, Segoe UI, sans-serif">${fmt0(v)}</text>
          </g>`
        );
      })
      .join('');

    const svg =
      svgOpen(w, h) +
      `<defs>
        <linearGradient id="rk0" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0e7490"/><stop offset="1" stop-color="#67e8f9"/></linearGradient>
        <linearGradient id="rk1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1e3a8a"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
        <filter id="rkGlow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>` +
      rows +
      '</svg>';

    box.innerHTML = svg;
    bindTips(box, tips);

    box.querySelectorAll('.bar-grow').forEach((r, k) => {
      if (noMotion() || !r.animate) return;
      const width = r.getAttribute('width');
      r.animate([{ width: '0px' }, { width }], {
        duration: 700,
        delay: k * 40,
        easing: 'cubic-bezier(.22,.9,.3,1)',
        fill: 'backwards',
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* 4. 行业增速（同比 / 环比）发散条形                                    */
  /* ------------------------------------------------------------------ */

  function growthChart(box, ctx) {
    const { w, h } = size(box);
    const g = ctx.growth;
    const list = ctx.industries.map((d, i) => ({ d, v: g.values[i] })).sort((a, b) => b.v - a.v);
    const n = list.length;
    const labelW = 58;
    const padR = 34;
    const topPad = 17;
    const rowH = (h - topPad - 4) / n;
    const x0 = labelW + 6;
    const x1 = w - padR;
    const vals = list.map((o) => o.v);
    const hiV = Math.max(0, ...vals);
    const loV = Math.min(0, ...vals);
    const span = Math.max(hiV * 1.18, Math.abs(loV) * 1.35, 6);
    const lo = loV < 0 ? -Math.max(Math.abs(loV) * 1.35, span * 0.18) : 0;
    const hi = loV < 0 ? span + Math.abs(lo) * 0.55 : span;
    const zx = x0 + ((0 - lo) / (hi - lo)) * (x1 - x0);
    const bh = Math.min(10, rowH * 0.42);
    const tips = [];

    // 百分比刻度线，为发散条形提供参照
    const tickStep = hi - lo > 18 ? 5 : 2.5;
    const gridLines = (() => {
      const out = [];
      for (let raw = Math.ceil(lo / tickStep) * tickStep; raw <= hi + 0.001; raw += tickStep) {
        const v = Number(raw.toFixed(2));
        const x = x0 + ((v - lo) / (hi - lo)) * (x1 - x0);
        out.push(
          `<line x1="${x}" y1="${topPad - 5}" x2="${x}" y2="${h}" stroke="rgba(120,165,220,.09)" stroke-dasharray="2 5"/>`
        );
        out.push(
          `<text x="${x}" y="10" text-anchor="middle" font-size="7.5" fill="#4d6079">${
            v === 0 ? '0%' : (v > 0 ? '+' : '') + v + '%'
          }</text>`
        );
      }
      return out.join('');
    })();

    const rows = list
      .map((o, k) => {
        const v = o.v;
        const cy = topPad + rowH * k + rowH / 2;
        const len = Math.abs(v) / (hi - lo) * (x1 - x0);
        const pos = v >= 0;
        const x = pos ? zx : zx - len;
        const c = pos ? 'url(#ggPos)' : 'url(#ggNeg)';

        tips.push(
          [`<b>${esc(o.d.name)}</b>`, tipRow(pos ? C.cyan : C.rose, g.mode === 'yoy' ? '同比增速' : '环比增速', signed(v, 2) + '%'), tipRow('', '当季增加值', fmt1(o.d.q[ctx.active]))].join('')
        );

        return `<g data-ti="${tips.length - 1}" style="cursor:pointer">
          <rect x="0" y="${topPad + rowH * k}" width="${w}" height="${rowH}" fill="transparent"/>
          <text x="0" y="${cy + 3.2}" font-size="9.5" fill="#93a9c4">${esc(o.d.short)}</text>
          <rect class="bar-grow" x="${x}" y="${cy - bh / 2}" width="${Math.max(1.2, len)}" height="${bh}" rx="2" fill="${c}"/>
          <text x="${pos ? x + Math.max(1.2, len) + 5 : x - 5}" y="${cy + 3}" text-anchor="${
          pos ? 'start' : 'end'
        }" font-size="8.5" fill="${pos ? '#67e8f9' : '#fda4af'}" font-family="Bahnschrift, Segoe UI, sans-serif">${signed(
          v,
          1
        )}%</text>
        </g>`;
      })
      .join('');

    const svg =
      svgOpen(w, h) +
      `<defs>
        <linearGradient id="ggPos" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="rgba(34,211,238,.45)"/><stop offset="1" stop-color="#22d3ee"/></linearGradient>
        <linearGradient id="ggNeg" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="rgba(251,113,133,.45)"/><stop offset="1" stop-color="#fb7185"/></linearGradient>
      </defs>` +
      gridLines +
      `<line x1="${zx}" y1="${topPad - 5}" x2="${zx}" y2="${h}" stroke="rgba(160,200,240,.3)" stroke-dasharray="2 4"/>` +
      rows +
      '</svg>';

    box.innerHTML = svg;
    bindTips(box, tips);
    box.querySelectorAll('.bar-grow').forEach((r, k) => {
      if (noMotion() || !r.animate) return;
      const width = r.getAttribute('width');
      r.animate([{ width: '0px', opacity: 0.4 }, { width, opacity: 1 }], {
        duration: 650,
        delay: k * 35,
        easing: 'cubic-bezier(.22,.9,.3,1)',
        fill: 'backwards',
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* 5. 热力图：行业 × 季度 环比增速                                       */
  /* ------------------------------------------------------------------ */

  function heatChart(box, ctx) {
    const { w, h } = size(box);
    const labelW = 58;
    const headH = 16;
    const cols = ctx.quarters.length;
    const rows = ctx.industries.length;
    const cw = (w - labelW) / cols;
    const ch = (h - headH) / rows;
    const gap = 2.5;
    const tips = [];

    const heatColor = (v) => {
      const t = clamp(v / 12, -1, 1);
      return t >= 0
        ? `rgba(34,211,238,${(0.13 + 0.8 * t).toFixed(3)})`
        : `rgba(251,113,133,${(0.13 + 0.8 * -t).toFixed(3)})`;
    };

    const colHead = ctx.quarters
      .map((q, i) => {
        const active = i === ctx.active;
        return `<text x="${labelW + cw * i + cw / 2}" y="${headH - 5}" text-anchor="middle" font-size="8" fill="${
          active ? '#7dd3fc' : '#4d6079'
        }" font-family="Bahnschrift, Segoe UI, sans-serif">${q.slice(2)}</text>`;
      })
      .join('');

    const cells = ctx.industries
      .map((d, r) => {
        const cy = headH + ch * r;
        const label = `<text x="0" y="${cy + ch / 2 + 3}" font-size="8.8" fill="#93a9c4">${esc(d.short)}</text>`;
        const rowCells = ctx.quarters
          .map((q, i) => {
            if (i === 0) {
              return `<rect x="${labelW + cw * i + gap / 2}" y="${cy + gap / 2}" width="${cw - gap}" height="${
                ch - gap
              }" rx="2" fill="rgba(120,165,220,.05)"/>
              <text x="${labelW + cw * i + cw / 2}" y="${cy + ch / 2 + 3}" text-anchor="middle" font-size="7.5" fill="#3f5674">基期</text>`;
            }
            const v = pct(d.q[i], d.q[i - 1]);
            const strong = Math.abs(v) > 6;
            tips.push(
              [`<b>${esc(d.short)} · ${esc(q)}</b>`, tipRow(heatColor(v), '环比增速', signed(v, 2) + '%'), tipRow('', '当季增加值', fmt1(d.q[i]))].join('')
            );
            return `<g data-ti="${tips.length - 1}" style="cursor:pointer">
              <rect x="${labelW + cw * i + gap / 2}" y="${cy + gap / 2}" width="${cw - gap}" height="${
              ch - gap
            }" rx="2" fill="${heatColor(v)}"/>
              <text x="${labelW + cw * i + cw / 2}" y="${cy + ch / 2 + 3}" text-anchor="middle" font-size="8" fill="${
              strong ? '#f2fdff' : 'rgba(214,233,252,.78)'
            }" font-family="Bahnschrift, Segoe UI, sans-serif">${v.toFixed(1)}</text>
            </g>`;
          })
          .join('');
        return label + rowCells;
      })
      .join('');

    const svg = svgOpen(w, h) + colHead + cells + '</svg>';
    box.innerHTML = svg;
    bindTips(box, tips);
  }

  /* ------------------------------------------------------------------ */
  /* 6. 年度累计 GDP 对比                                                 */
  /* ------------------------------------------------------------------ */

  function cumulativeChart(box, ctx) {
    const { w, h } = size(box);
    const pad = { t: 24, r: 62, b: 26, l: 46 };
    const pw = w - pad.l - pad.r;
    const ph = h - pad.t - pad.b;
    const baseY = pad.t + ph;

    // x 轴固定为 Q1..Q4
    const xq = (q) => pad.l + ((q - 1) / 3) * pw;

    const series = [
      { year: '2025', color: '#a78bfa', pts: [] },
      { year: '2026', color: C.cyan, pts: [] },
    ];

    ctx.quarters.forEach((q, i) => {
      const year = q.slice(0, 4);
      const qn = Number(q.slice(5));
      const s = series.find((x) => x.year === year);
      if (s) s.pts.push({ q: qn, v: ctx.gdpCum[i], label: q, i });
    });

    series.forEach((s) => s.pts.sort((a, b) => a.q - b.q));

    const max = Math.max(...series.flatMap((s) => s.pts.map((p) => p.v)));
    const sc = niceScale(max, 4);
    const y = (v) => pad.t + ph * (1 - v / sc.top);

    const ticks = sc.ticks
      .map(
        (v) =>
          `<line x1="${pad.l}" y1="${y(v)}" x2="${w - pad.r}" y2="${y(v)}" stroke="${C.grid}" stroke-dasharray="${
            v === 0 ? 0 : '3 5'
          }"/>` +
          `<text x="${pad.l - 8}" y="${y(v) + 3}" text-anchor="end" font-size="9" fill="#5d7492">${wan1(v)}万</text>`
      )
      .join('');

    const areaPath = (pts) => {
      const top = pts.map((p, i) => `${i ? 'L' : 'M'}${xq(p.q)},${y(p.v)}`).join(' ');
      return `${top} L${xq(pts[pts.length - 1].q)},${baseY} L${xq(pts[0].q)},${baseY} Z`;
    };

    const defs = `<defs>
      <linearGradient id="cumArea26" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(34,211,238,.30)"/><stop offset="1" stop-color="rgba(34,211,238,0)"/></linearGradient>
      <linearGradient id="cumArea25" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(167,139,250,.14)"/><stop offset="1" stop-color="rgba(167,139,250,0)"/></linearGradient>
      <filter id="cumGlow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>`;

    const tips = [];
    const hits = [1, 2, 3, 4].map((q) => {
      const rows = series
        .map((s) => {
          const p = s.pts.find((x) => x.q === q);
          return p ? tipRow(s.color, s.year + ' 年累计', fmt1(p.v)) : '';
        })
        .join('');
      const a = series[0].pts.find((x) => x.q === q);
      const b = series[1].pts.find((x) => x.q === q);
      const gapRow = a && b ? `<div class="sep"></div>${tipRow('', '同比', signed(pct(b.v, a.v)) + '%')}` : '';
      tips.push(`<b>第 ${q} 季度 · 年内累计</b>${rows}${gapRow}`);
      const bandW = pw / 3;
      return hiddenRect(pad.l + (q - 1.4) * bandW, pad.t, bandW, ph, tips.length - 1);
    });

    const paths = series
      .map((s) => {
        const pts = s.pts;
        if (!pts.length) return '';
        const line = pts.map((p, i) => `${i ? 'L' : 'M'}${xq(p.q).toFixed(1)},${y(p.v).toFixed(1)}`).join(' ');
        const areaId = s.year === '2026' ? 'cumArea26' : 'cumArea25';
        const dots = pts
          .map(
            (p) =>
              `<circle cx="${xq(p.q)}" cy="${y(p.v)}" r="3" fill="#08111d" stroke="${s.color}" stroke-width="1.8"/>`
          )
          .join('');
        const last = pts[pts.length - 1];
        const isLatestYear = s.year === '2026';
        return (
          (isLatestYear ? `<path d="${areaPath(pts)}" fill="url(#${areaId})" opacity="0.45"/>` : '') +
          `<path d="${line}" fill="none" stroke="${s.color}" stroke-width="${isLatestYear ? 2.1 : 1.5}" stroke-linejoin="round" stroke-linecap="round" ${
            isLatestYear ? 'filter="url(#cumGlow)" pathLength="1" class="draw-line"' : 'stroke-dasharray="6 5" opacity=".95"'
          }/>` +
          dots +
          `<circle cx="${xq(last.q)}" cy="${y(last.v)}" r="7" fill="none" stroke="${s.color}" stroke-width="1" opacity="0.45"/>` +
          `<text x="${xq(last.q) + 10}" y="${y(last.v) + (isLatestYear ? -8 : 3)}" font-size="9.5" fill="${s.color}" font-family="Bahnschrift, Segoe UI, sans-serif">${wan1(
            last.v
          )}万</text>`
        );
      })
      .join('');

    const xLabels = [1, 2, 3, 4]
      .map(
        (q) =>
          `<text x="${xq(q)}" y="${baseY + 17}" text-anchor="middle" font-size="9" fill="#61789a">Q${q}</text>`
      )
      .join('');

    const svg =
      svgOpen(w, h) + defs +
      // 尚未公布的季度区域
      `<rect x="${xq(3)}" y="${pad.t}" width="${xq(4) - xq(3)}" height="${ph}" fill="rgba(120,165,220,.035)"/>` +
      `<line x1="${xq(3)}" y1="${pad.t}" x2="${xq(3)}" y2="${baseY}" stroke="rgba(34,211,238,.32)" stroke-dasharray="3 4"/>` +
      ticks + paths + xLabels + hits.join('') +
      `<text x="${xq(3) + 7}" y="${pad.t + 10}" font-size="8" fill="#4d6079" letter-spacing="0.06em">2026Q4 待公布</text>` +
      `<text x="${pad.l - 8}" y="${pad.t - 10}" text-anchor="end" font-size="7.5" fill="#4d6079" letter-spacing="0.08em">累计 · 万</text>` +
      '</svg>';

    box.innerHTML = svg;
    bindTips(box, tips);
    box.querySelectorAll('.draw-line').forEach((p, i) => {
      if (noMotion() || !p.animate) return;
      p.animate([{ strokeDasharray: '1 1', strokeDashoffset: 1 }, { strokeDasharray: '1 1', strokeDashoffset: 0 }], {
        duration: 900,
        delay: i * 160,
        easing: 'cubic-bezier(.35,.9,.3,1)',
        fill: 'backwards',
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* 7. 迷你趋势线（KPI 卡片）                                            */
  /* ------------------------------------------------------------------ */

  function sparkline(values, color) {
    const w = 74;
    const h = 26;
    const min = Math.min(...values);
    const max = Math.max(...values);
    const span = max - min || 1;
    const pts = values.map((v, i) => {
      const x = 2 + (i / (values.length - 1)) * (w - 4);
      const y = h - 3 - ((v - min) / span) * (h - 7);
      return [x, y];
    });
    const line = pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');
    const last = pts[pts.length - 1];
    return `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" class="spark" aria-hidden="true">
      <defs><linearGradient id="sp-${color.replace('#', '')}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="${color}" stop-opacity=".35"/><stop offset="1" stop-color="${color}" stop-opacity="0"/>
      </linearGradient></defs>
      <path d="${line} L${last[0]},${h} L2,${h} Z" fill="url(#sp-${color.replace('#', '')})"/>
      <path d="${line}" fill="none" stroke="${color}" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/>
      <circle cx="${last[0]}" cy="${last[1]}" r="2" fill="${color}"/>
    </svg>`;
  }

  global.Charts = {
    stacked,
    donut,
    rankChart,
    growthChart,
    heatChart,
    cumulativeChart,
    sparkline,
    fmt1,
    fmt0,
    wan1,
    signed,
    pct,
  };
})(window);
