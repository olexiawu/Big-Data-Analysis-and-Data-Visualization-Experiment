import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle, Polygon
import os

# 参考图文字为硬边像素风格（无抗锯齿），关闭文字抗锯齿以获得清晰锐利的笔画
plt.rcParams['text.antialiased'] = False

# ---------------- 画布 ----------------
W, H = 867, 672
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)            # y 翻转：像素坐标直接使用（y 增大向下）
ax.axis('off')
ax.add_patch(Rectangle((0, 0), W, H, color='#1A1E43', lw=0, zorder=0))

# ---------------- 字体（Windows 微软雅黑 / Linux Noto） ----------------
def pick_font():
    names = ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC',
             'WenQuanYi Zen Hei', 'DejaVu Sans']
    installed = {f.name for f in fm.fontManager.ttflist}
    for n in names:
        if n in installed:
            return n
    return 'DejaVu Sans'
FONT = pick_font()

# ---------------- 颜色 ----------------
DARK   = '#0070C0'    # 2021 柱 (0,112,192)
LIGHT  = '#82ADD7'    # 2022 柱 (130,173,215)
EDGE21 = '#61A4D4'    # 2021 柱底高光 (97,164,212)
EDGE22 = '#AFC9E2'    # 2022 柱底高光 (175,201,226)
WHITE  = '#FFFFFF'
TEXT   = '#F2F2F2'    # 数据/图例/标签主体色 (242,242,242)
GRAY   = '#D9D9D9'    # 注释浅灰 (217,217,217)

# ---------------- 数据 ----------------
names   = ['口红', '面膜', '隔离', '防晒', '精华']
sales21 = [3568, 4135, 4436, 4106, 4936]
sales22 = [2569, 3241, 2965, 3209, 3541]
diffs   = [999, 894, 1471, 897, 1395]

# 柱几何（参考图实测）：(21柱左缘, 21柱宽, 22柱左缘, 22柱宽, 21柱高, 22柱高)
bars = [
    (92, 33, 134, 32, 217, 156),
    (240, 33, 282, 33, 251, 197),
    (388, 33, 430, 34, 270, 180),
    (536, 34, 579, 33, 249, 195),
    (685, 33, 727, 33, 300, 215),
]
BOTTOM = 561          # 柱色区底（含 y560 及以下，y561 为高光边线行）

# ---------------- 白色箭头（梯形头 + 竖杆） ----------------
def draw_arrow(cx, t21, t22):
    """cx=22柱中心；箭头尖朝上，头在 21 柱顶+1..+11，杆从 +12 到 22 柱顶-1"""
    y0 = t21 + 1
    pts = [(-1, 0), (1, 0), (1, 1), (2, 2), (2, 3), (3, 4), (3, 5),
           (4, 6), (4, 7), (5, 8), (5, 9), (6, 10),
           (-6, 10), (-5, 9), (-5, 8), (-4, 7), (-4, 6), (-3, 5),
           (-3, 4), (-2, 3), (-2, 2), (-1, 1)]
    ax.add_patch(Polygon([(cx + dx, y0 + dy) for dx, dy in pts], closed=True,
                         facecolor=TEXT, edgecolor='none', zorder=2))
    ax.add_patch(Rectangle((cx - 1, y0 + 11), 2, (t22 - 1) - (y0 + 11) + 1,
                           facecolor=TEXT, edgecolor='none', lw=0, zorder=2))

# ---------------- 柱形 + 数据文字 ----------------
for i in range(5):
    x21, w21, x22, w22, h21, h22 = bars[i]
    t21 = BOTTOM - h21          # 21 柱顶
    t22 = BOTTOM - h22          # 22 柱顶
    c21 = x21 + w21 / 2         # 21 柱中心
    c22 = x22 + w22 / 2         # 22 柱中心

    # 2021 柱（深蓝）+ 柱底高光
    ax.add_patch(Rectangle((x21, t21), w21, h21, color=DARK, lw=0, zorder=1))
    ax.add_patch(Rectangle((x21, BOTTOM), w21, 1, color=EDGE21, lw=0, zorder=1))
    # 2022 柱（浅蓝）+ 柱底高光
    ax.add_patch(Rectangle((x22, t22), w22, h22, color=LIGHT, lw=0, zorder=1))
    ax.add_patch(Rectangle((x22, BOTTOM), w22, 1, color=EDGE22, lw=0, zorder=1))
    # 白色箭头
    draw_arrow(c22, t21, t22)
    # 2021 值：水平居中 21 柱，中心在柱顶上方约 20px（参考图实测）
    y21_center = [324, 289, 271, 291, 241]
    ax.text(c21, y21_center[i], str(sales21[i]), fontsize=11.5, color=TEXT,
            ha='center', va='center', family=FONT, zorder=3)
    # 2022 值：写 22 柱面内，柱顶下方约 20.5px（参考图实测）
    y22_center = [426, 385.5, 401.5, 387.5, 366.5]
    ax.text(c22, y22_center[i], str(sales22[i]), fontsize=11.5, color=TEXT,
            ha='center', va='center', family=FONT, zorder=3)

# 差值文字（箭头右侧空隙，参考图实测位置）
diff_x = [171, 318.5, 470, 615.5, 775.5]
diff_y = [386, 342, 349, 346, 312]
for i in range(5):
    ax.text(diff_x[i], diff_y[i], str(diffs[i]), fontsize=11.5, color=TEXT,
            ha='center', va='center', family=FONT, zorder=3)

# ---------------- 标题 / 副标题 ----------------
# 参考标题为粗体（字形 558x40、笔画粗）。Windows 微软雅黑有 Bold 变体 → 单次 bold；
# 本机（Noto Sans CJK SC）无粗体变体 → 多重偏移模拟加粗（与 sales_bar 同法）
if FONT == 'Microsoft YaHei':
    ax.text(331.5, 73.5, '2022年商品对比去年销售情况', fontsize=30.5, color=WHITE,
            ha='center', va='center', family=FONT, fontweight='bold', zorder=2)
else:
    title_offsets = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (2, 1)]  # 5次水平+1次中心下移，实测最优
    for dx, dy in title_offsets:
        ax.text(331.5 + dx, 73.5 + dy, '2022年商品对比去年销售情况', fontsize=30.5,
                color=WHITE, ha='center', va='center', family=FONT, zorder=2)
ax.text(388.25, 131.25, '商品整体比去年销量有所下降，其中隔离下降最多，下降33%',
        fontsize=18, color=WHITE, ha='center', va='center', family=FONT, zorder=2)

# ---------------- 图例 ----------------
ax.add_patch(Rectangle((66, 192), 11, 10, color=DARK, lw=0, zorder=2))
ax.text(80, 196.5, '2021销量', fontsize=13, color=TEXT,
        ha='left', va='center', family=FONT, zorder=3)
ax.add_patch(Rectangle((177, 192), 10, 10, color=LIGHT, lw=0, zorder=2))
ax.text(190, 196.5, '2022销量', fontsize=13, color=TEXT,
        ha='left', va='center', family=FONT, zorder=3)

# ---------------- 柱下商品名 ----------------
label_x = [129.5, 280, 427, 575, 723.5]  # 参考字形中心 +1.5（Noto 渲染偏移，实测最优）
for i in range(5):
    ax.text(label_x[i], 586.5, names[i], fontsize=12.8, color=TEXT,
            ha='center', va='center', family=FONT, zorder=3)

# ---------------- 底部注释 ----------------
ax.text(37.5, 636, '*注：数据来源于公司销售系统，统计日期截至2022.01.01',
        fontsize=11.9, color=GRAY, ha='left', va='center', family=FONT, zorder=2)

# ---------------- 保存 ----------------
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p9.png')
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=100)
plt.close(fig)
print('saved:', out)
