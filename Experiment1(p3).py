import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

# ===== 中文字体 =====
_font_candidates = [
    r'C:\Windows\Fonts\msyh.ttc',
    r'C:\Windows\Fonts\msyh.ttf',
    r'C:\Windows\Fonts\simhei.ttf',
]
for _fp in _font_candidates:
    if os.path.exists(_fp):
        fm.fontManager.addfont(_fp)
        plt.rcParams['font.sans-serif'] = [fm.FontProperties(fname=_fp).get_name()]
        break
else:
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ===== 数据 =====
products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
sales    = [653, 523, 648, 856, 714, 785]

# ===== 配色 =====
bg_color   = '#1a1a3e'
bar_top    = '#00f0ff'   # 柱子顶部亮青
bar_bot    = '#002b80'   # 柱子底部深蓝
dot_color  = '#5cb3ff'
label_bg   = '#2d2d5e'
line_color = '#00d0ff'   # 圆点与柱顶之间的连接线颜色

# ===== 画布 =====
fig, ax = plt.subplots(figsize=(9, 6.5), dpi=100)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

cmap = LinearSegmentedColormap.from_list('g', [bar_bot, bar_top])

x = np.arange(len(products))
bar_width = 0.4
r = bar_width / 2  # 半圆半径

# 先画一帧以获取显示比例，用于修正圆角
fig.canvas.draw()
_bbox = ax.get_window_extent()
_x_range = len(products)
_y_range = 1200
_ma = (_bbox.width / _x_range) / (_bbox.height / _y_range)  # mutation_aspect

# ===== 逐柱绘制 =====
for xi, val in zip(x, sales):
    left = xi - bar_width / 2

    # 胶囊形圆角矩形（仅作裁剪路径）
    fancy = FancyBboxPatch((left, 0), bar_width, val,
                           boxstyle="round,pad=0,rounding_size=0.2",
                           linewidth=0)
    fancy.set_mutation_aspect(_ma)  # 关键：修正非等比例坐标下的圆角变形
    ax.add_patch(fancy)
    fancy.set_visible(False)

    # 渐变填充
    grad = np.linspace(0, 1, 256).reshape(-1, 1)
    im = ax.imshow(grad, extent=[left, left + bar_width, 0, val],
                   aspect='auto', cmap=cmap, zorder=2, origin='lower')
    im.set_clip_path(fancy)

    # 柱顶到圆点的连接线（竖线）
    ax.plot([xi, xi], [val, val + 45], color=line_color, linewidth=2, zorder=3)

    # 柱顶圆点
    ax.plot(xi, val + 45, 'o', color=dot_color, markersize=7, zorder=4)

    # 深色圆角标签框 + 数值
    ax.text(xi + 0.18, val + 45, str(val),
            bbox=dict(boxstyle='round,pad=0.35',
                      facecolor=label_bg, edgecolor='none'),
            color='white', fontsize=11, va='center', zorder=5)

# ===== 坐标轴 =====
ax.set_xticks(x)
ax.set_xticklabels(products, color='white', fontsize=12)
ax.set_yticks([0, 200, 400, 600, 800, 1000, 1200])
ax.set_yticklabels(['0', '200', '400', '600', '800', '1000', '1200'],
                   color='white', fontsize=11)
ax.set_ylim(0, 1200)
ax.set_xlim(-0.6, len(products) - 0.4)

# ===== 水平虚线网格 =====
ax.grid(axis='y', color='white', alpha=0.2,
        linestyle='--', linewidth=1, zorder=1)
ax.set_axisbelow(True)

# ===== 边框 =====
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#888888')
ax.tick_params(axis='both', length=0)

# ===== 标题 / 副标题 =====
fig.text(0.06, 0.92, '3月商品销量对比',
         color='white', fontsize=24, fontweight='bold')
fig.text(0.06, 0.86, '防晒销量最多，3月销量856；面膜最少，3月销量523',
         color='white', fontsize=14)

# ===== 注释 =====
fig.text(0.06, 0.04,
         '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         color='#aaaaaa', fontsize=10)

plt.tight_layout(rect=[0, 0.06, 1, 0.84])
plt.savefig('round_bar.png', dpi=100, facecolor=bg_color, bbox_inches='tight')
plt.show()
print('done')
