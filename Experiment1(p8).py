import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle
import os, math
plt.rcParams['text.antialiased'] = False

W, H = 867, 613
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)          # y 翻转，左上角为原点
ax.axis('off')

# 背景
ax.add_patch(Rectangle((0, 0), W, H, color='#1A1E43', lw=0, zorder=0))

# ---------------- 字体 ----------------
def pick_font():
    names = ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC',
             'WenQuanYi Zen Hei', 'DejaVu Sans']
    installed = {f.name for f in fm.fontManager.ttflist}
    for n in names:
        if n in installed:
            return n
    return 'DejaVu Sans'
FONT = pick_font()
regions  = ['华东', '西南', '西北', '东北', '华南', '华北']
sales    = [2109, 1369, 1872, 1536, 1946, 4321]
pct      = ['-5.8%', '-17.9%', '-15.9%', '-9.3%', '-20.8%', '-13.6%']
MAX_SALES = 4321
MAX_LEN   = 510        # 条形总长（x 110-619）
BAR_X0    = 110

row_y0    = [180, 242, 304, 366, 428, 490]   # 每行条形顶
BAR_H     = 48          # 条形高（y0 到 y0+47）

DARK  = '#09387E'       # 深蓝 (9,56,126)
LIGHT = '#82ADD7'       # 浅蓝 (130,173,215)
RED   = '#9B3D4F'       # 红色块 (155,61,79)
WHITE = '#FFFFFF'
TEXT  = '#F2F2F2'       # 行内文字（区域名/数值/百分比）主体色 (242,242,242)
GRAY  = '#D9D9D9'       # 注释浅灰 (217,217,217)

import math
for i in range(6):
    y0 = row_y0[i]
    L = math.ceil(sales[i] / MAX_SALES * MAX_LEN)   # 深蓝段长度（向上取整，逐像素匹配）
    # 深蓝段：x 110 到 110+L-1
    ax.add_patch(Rectangle((BAR_X0, y0), L, BAR_H, color=DARK, lw=0, zorder=1))
    # 浅蓝段：x 110+L 到 619
    if 110 + L <= 619:
        ax.add_patch(Rectangle((BAR_X0 + L, y0), 620 - (BAR_X0 + L), BAR_H,
                               color=LIGHT, lw=0, zorder=1))
    # 红色块：x 620-747
    ax.add_patch(Rectangle((620, y0), 128, BAR_H, color=RED, lw=0, zorder=1))
    # 区域名：左对齐 x=56，垂直中心 y0+22
    ax.text(56, y0 + 22, regions[i], fontsize=14, color=TEXT,
            ha='left', va='center', family=FONT, zorder=2)
    # 数值：右对齐，x = 深蓝末端-13，垂直中心 y0+24
    ax.text(110 + L - 13, y0 + 24, str(sales[i]), fontsize=13.5, color=TEXT,
            ha='right', va='center', family=FONT, zorder=2)
    # 百分比：红色块内居中（x 683.5），垂直中心 y0+24
    ax.text(683.5, y0 + 24, pct[i], fontsize=13.5, color=TEXT,
            ha='center', va='center', family=FONT, zorder=2)

if FONT == 'Microsoft YaHei':
    ax.text(59, 55, '2021年各区域销量及同比情况', fontsize=27, color=WHITE,
            ha='left', va='top', family=FONT, fontweight='bold', zorder=2)
else:
    title_offsets = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
                     (1, -1), (2, -1), (3, -1), (4, -1), (0, -1)]
    for dx, dy in title_offsets:
        ax.text(59 + dx, 55 + dy, '2021年各区域销量及同比情况', fontsize=27, color=WHITE,
                ha='left', va='top', family=FONT, zorder=2)
ax.text(54, 113, '各区域商品销量同比去年均有下降，其中华南下降最多，同比下降20.8%',
        fontsize=16.5, color=WHITE, ha='left', va='top', family=FONT, zorder=2)
ax.text(46, 570, '*注: 数据来源于公司销售系统，统计日期截至2022.01.01',
        fontsize=12.5, color=GRAY, ha='left', va='top', family=FONT, zorder=2)

# 输出到脚本所在目录，避免在不同机器上路径不存在
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sales_bar.png')
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=100)
plt.close(fig)
print('saved:', out)
