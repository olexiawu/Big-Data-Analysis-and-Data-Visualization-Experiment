import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
from matplotlib.patches import Rectangle

# ===== 中文字体：Windows 用微软雅黑，其他环境回退 Noto Sans CJK =====
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

# ===== 数据 =====
quarters = ['2021Q1', 'Q2', 'Q3', 'Q4', '2022Q1', 'Q2']
sales    = [3121, 4086, 4321, 4601, 4936, 4231]
profits  = [1020, 1421, 1502, 1623, 1781, 1432]

BLUE  = '#0070C0'
RED   = '#E74E69'
BG    = '#1A1E43'
WHITE = '#FFFFFF'
GRAY  = '#B0B0BC'

# ===== 画布 866x613（与参考图同尺寸）=====
fig, ax = plt.subplots(figsize=(8.66, 6.13), dpi=100)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# ===== 精确设置绘图区：柱底(0值)在517px、6000在157px、组中心在133px、组距117px =====
ax.set_position([0.073, 0.157, 0.837, 0.587])
ax.set_xlim(-0.6, 5.6)
ax.set_ylim(0, 6000)

# ===== 柱子：蓝(销售额)偏左、红(利润)偏右、部分重叠 =====
bar_w  = 0.256
offset = 0.094
n = len(quarters)
ax.bar([i - offset for i in range(n)], sales, width=bar_w,
       color=BLUE, edgecolor='none', zorder=3)
ax.bar([i + offset for i in range(n)], profits, width=bar_w,
       color=RED, edgecolor='none', zorder=3)

# ===== 柱顶数字：白色，中心在柱顶上方约21px(=304数据单位) =====
for i, s, p in zip(range(n), sales, profits):
    ax.text(i - offset, s + 304, str(s), ha='center', va='center',
            color=WHITE, fontsize=12.5, zorder=5)
    ax.text(i + offset, p + 304, str(p), ha='center', va='center',
            color=WHITE, fontsize=12.5, zorder=5)

# ===== x 轴标签：白色，柱底下方26px(=-433数据单位)，中心对齐柱组 =====
for i, q in zip(range(n), quarters):
    ax.text(i, -433, q, ha='center', va='center',
            color=WHITE, fontsize=12, zorder=5)

# ===== 去掉所有轴线和刻度 =====
ax.set_xticks([])
ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_visible(False)

# ===== 图例：两个彩色边框文本框，叠在最后一根柱上方 =====
leg_x0, leg_x1 = 4.86, 5.57
box_h  = 450
gap    = 333
sale_bottom  = 2933
profit_bottom = sale_bottom - box_h - gap

for bottom, ec, label in [(sale_bottom, BLUE, '销售额'),
                          (profit_bottom, RED, '利润额')]:
    ax.add_patch(Rectangle((leg_x0, bottom), leg_x1 - leg_x0, box_h,
                           facecolor=BG, edgecolor=ec, linewidth=1.6, zorder=6))
    ax.text((leg_x0 + leg_x1) / 2, bottom + box_h / 2, label,
            ha='center', va='center', color=WHITE, fontsize=11, zorder=7)

# ===== 标题 / 副标题 =====
fig.text(0.06, 0.912, '2021年至今季度销售额(万)和利润额(万)',
         color=WHITE, fontsize=30, fontweight='bold', va='top')
fig.text(0.06, 0.806, '2022年第二季度销售额首次出现下降，降幅达到15%',
         color=WHITE, fontsize=18, va='top')

# ===== 底部注释 =====
fig.text(0.05, 0.042, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         color=GRAY, fontsize=12)

# ===== 保存：图片生成在脚本所在文件夹，并打印完整路径 =====
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stacked_bar.png')
plt.savefig(out_path, dpi=100, facecolor=BG)
print('图片已保存到:')
print(out_path)
print('done')
