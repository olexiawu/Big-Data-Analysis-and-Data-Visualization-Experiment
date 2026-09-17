import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

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
products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜', '眼影', '气垫']
sales    = [9221, 5102, 6571, 5760, 6321, 8612, 2645, 5321]
colors   = [
    '#85C1E2',  # 口红 浅蓝
    '#48B8A8',  # 面膜 青绿
    '#E8684A',  # 隔离 橙红
    '#F4C430',  # 防晒 金黄
    '#1E90DD',  # 精华 亮蓝
    '#0066BB',  # 面霜 深蓝
    '#6666DD',  # 眼影 紫蓝
    '#5555BB',  # 气垫 深紫蓝
]

bg_color = '#1a1a3e'

# ===== 画布 =====
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=100)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

x = np.arange(len(products))
bar_width = 0.5

# ===== 绘制柱子 =====
ax.bar(x, sales, width=bar_width, color=colors, zorder=2)

# ===== 柱顶气泡标签框（带小三角指向柱子）=====
for xi, val, c in zip(x, sales, colors):
    ax.annotate(str(val),
                xy=(xi, val),
                xytext=(xi, val + 350),
                ha='center', va='bottom',
                color='white', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.35',
                          facecolor=c, edgecolor='none'),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=2),
                zorder=5)

# ===== 坐标轴 =====
ax.set_xticks(x)
ax.set_xticklabels(products, color='white', fontsize=12)
ax.set_yticks([0, 2000, 4000, 6000, 8000, 10000])
ax.set_yticklabels(['0', '2000', '4000', '6000', '8000', '10000'],
                   color='white', fontsize=11)
ax.set_ylim(0, 10500)
ax.set_xlim(-0.7, len(products) - 0.3)

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
fig.text(0.06, 0.92, '2021年商品销量情况',
         color='white', fontsize=24, fontweight='bold')
fig.text(0.06, 0.86, '口红销量最好达9221，是眼影最低值2645近3.5倍',
         color='white', fontsize=14)

# ===== 注释 =====
fig.text(0.06, 0.04,
         '*注：数据来源于公司销售系统，统计日期截至2022.08.31',
         color='#aaaaaa', fontsize=10)

plt.tight_layout(rect=[0, 0.06, 1, 0.84])
plt.savefig('multi_bar.png', dpi=100, facecolor=bg_color, bbox_inches='tight')
plt.show()
print('done')
