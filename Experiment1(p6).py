import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

_font_candidates = [
    r'C:\Windows\Fonts\msyh.ttc',
    r'C:\Windows\Fonts\msyh.ttf',
    r'C:\Windows\Fonts\simhei.ttf',
    r'C:\Windows\Fonts\simsun.ttc',
]
_font_name = None
for _fp in _font_candidates:
    if os.path.exists(_fp):
        fm.fontManager.addfont(_fp)
        _font_name = fm.FontProperties(fname=_fp).get_name()
        plt.rcParams['font.sans-serif'] = [_font_name]
        break
if _font_name is None:
    _fallbacks = [f.name for f in fm.fontManager.ttflist if 'Noto Sans CJK SC' in f.name]
    if _fallbacks:
        plt.rcParams['font.sans-serif'] = [_fallbacks[0]]
    else:
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False

regions = ['华南', '华北', '东北', '西北', '华东']
sales_2022 = [2238, 1531, 1426, 1321, 1215]
sales_2021 = [2066, 1436, 1531, 1265, 1003]

BLUE  = '#0070C0'
RED   = '#E74E69'
BG    = '#1A1E43'
WHITE = '#FFFFFF'
GRAY  = '#D9D9D9'

fig, ax = plt.subplots(figsize=(8.67, 6.12), dpi=100)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_position([0, 0, 1, 1])
ax.set_xlim(0, 867)
ax.set_ylim(612, 0)
ax.axis('off')

ax.text(58, 46, '2022年上半年各区域对比去年销量',
        fontsize=27, fontweight='bold', color=WHITE, ha='left', va='top')
ax.text(58, 105, '2022年整体销量高于2021年，只有东北区域较2021有所下降',
        fontsize=16.5, color=WHITE, ha='left', va='top')

ax.text(299, 164, '2022', fontsize=13, color=BLUE, ha='left', va='top')
ax.text(516, 164, '2021', fontsize=13, color=RED, ha='left', va='top')

CENTER = 446.0
BLUE_R = 383.0   # 蓝柱右端
RED_L  = 509.0   # 红柱左端
SCALE  = 0.102
BAR_H  = 27

# 每行柱子的 y 中心（从上到下：华南→华东）
y_centers = [209.5, 284.5, 356.5, 431.5, 503.5]

for name, v22, v21, cy in zip(regions, sales_2022, sales_2021, y_centers):
    len22 = v22 * SCALE   # 蓝柱长度
    len21 = v21 * SCALE   # 红柱长度

    # 蓝柱（2022，向左延伸）
    ax.barh(cy, len22, left=BLUE_R - len22, height=BAR_H,
            color=BLUE, edgecolor='none', zorder=3)
    # 红柱（2021，向右延伸）
    ax.barh(cy, len21, left=RED_L, height=BAR_H,
            color=RED, edgecolor='none', zorder=3)

    # 柱内数值：白字，中心距柱外端 30px
    ax.text(BLUE_R - len22 + 30, cy, str(v22),
            fontsize=11.5, color=WHITE, ha='center', va='center', zorder=5)
    ax.text(RED_L + len21 - 30, cy, str(v21),
            fontsize=11.5, color=WHITE, ha='center', va='center', zorder=5)

    # 中间区域标签
    ax.text(CENTER, cy, name, fontsize=12, color=WHITE,
            ha='center', va='center', zorder=5)

# ===== 底部注释 =====
ax.text(54, 586, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
        fontsize=12, color=GRAY, ha='left', va='bottom')

# ===== 保存：图片生成在脚本所在文件夹，并打印完整路径 =====
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'butterfly_bar.png')
plt.savefig(out_path, dpi=100, facecolor=BG)
print('图片已保存到:')
print(out_path)
print('done')
