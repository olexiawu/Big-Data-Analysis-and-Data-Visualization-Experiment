import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
from matplotlib.colors import LinearSegmentedColormap

# ===== 中文字体设置（直接加载字体文件，避免方框）=====
_font_candidates = [
    r'C:\Windows\Fonts\msyh.ttc',
    r'C:\Windows\Fonts\msyh.ttf',
    r'C:\Windows\Fonts\simhei.ttf',
    r'C:\Windows\Fonts\simsun.ttc',
]
_zh_font = None
for _fp in _font_candidates:
    if os.path.exists(_fp):
        fm.fontManager.addfont(_fp)
        _zh_font = fm.FontProperties(fname=_fp).get_name()
        break
if _zh_font:
    plt.rcParams['font.sans-serif'] = [_zh_font]
else:
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ===== 数据 =====
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales   = [2354, 1902, 3524, 2698, 2896, 2563]
avg     = 2656

# ===== 配色 =====
bg_color      = '#1a1a3e'
bar_top_color = '#0066cc'   # 柱子顶部深蓝
bar_bot_color = '#00c8ff'   # 柱子底部亮青
avg_color     = '#f2c037'   # 平均值线（金黄）

# ===== 画布 =====
fig, ax = plt.subplots(figsize=(8.5, 6), dpi=100)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 渐变：底部亮青 -> 顶部深蓝
cmap = LinearSegmentedColormap.from_list('bar_grad', [bar_bot_color, bar_top_color])

x = np.arange(len(regions))
bar_width = 0.45

# ===== 逐柱绘制渐变 =====
for xi, val in zip(x, sales):
    left, right = xi - bar_width / 2, xi + bar_width / 2
    gradient = np.linspace(0, 1, 256).reshape(-1, 1)
    ax.imshow(gradient, extent=[left, right, 0, val],
              aspect='auto', cmap=cmap, zorder=2, origin='lower')

# ===== 柱顶数值标签 =====
for i, (xi, val) in enumerate(zip(x, sales)):
    if i == len(regions) - 1:
        # 华东柱高接近平均线，数值写在柱内顶部
        ax.text(xi, val - 20, str(val), ha='center', va='top',
                color='white', fontsize=11)
    else:
        ax.text(xi, val + 50, str(val), ha='center', va='bottom',
                color='white', fontsize=11)

# ===== 平均值参考线（起点在华北柱中心，终点在华东柱中心）=====
ax.plot([0, 5], [avg, avg], color=avg_color, linewidth=2, zorder=3)
ax.text(5, avg + 30, f'平均值: {avg}',
        ha='right', va='bottom', color=avg_color, fontsize=11)

# ===== 坐标轴 =====
ax.set_xticks(x)
ax.set_xticklabels(regions, color='white', fontsize=12)
ax.set_ylim(0, 4000)
ax.set_xlim(-0.6, len(regions) - 0.4)
# 不显示 Y 轴刻度
ax.set_yticks([])

# ===== 仅保留底部灰色基线 =====
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#888888')
ax.tick_params(axis='x', length=0)

# ===== 标题 / 副标题 =====
fig.text(0.07, 0.92, '3月各区域销量分布',
         color='white', fontsize=24, fontweight='bold')
fig.text(0.07, 0.86, '东北销量最多占总销量的22%，华南销量最低',
         color='white', fontsize=14)

# ===== 左下角注释 =====
fig.text(0.07, 0.04,
         '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         color='#aaaaaa', fontsize=10)

plt.tight_layout(rect=[0, 0.06, 1, 0.84])
plt.savefig('gradient_bar2.png', dpi=100, facecolor=bg_color, bbox_inches='tight')
plt.show()
print('done')
