
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib import font_manager


# ---------- 中文字体 ----------
def find_chinese_font(bold=False):
    candidates = [
        r'C:\Windows\Fonts\msyhbd.ttc' if bold else r'C:\Windows\Fonts\msyh.ttc',
        r'C:\Windows\Fonts\msyhbd.ttc',
        r'C:\Windows\Fonts\msyh.ttc',
        r'C:\Windows\Fonts\simhei.ttf',
    ]
    for path in candidates:
        if os.path.exists(path):
            return font_manager.FontProperties(fname=path)
    return font_manager.FontProperties(family='SimHei')


# ---------- 画布（832 x 616） ----------
WIDTH, HEIGHT = 832, 616
DPI = 100
BG = '#1A1E43'

fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, WIDTH)
ax.set_ylim(HEIGHT, 0)
ax.set_facecolor(BG)
ax.axis('off')

# ---------- 配色 ----------
C_2022 = '#0070C0'
C_2021 = '#E74E69'
C_LINE = '#FFC000'
TXT = '#F2F2F2'
NOTE = '#D9D9D9'
AXIS_LINE = '#454866'

ax.add_patch(Rectangle((0, 0), WIDTH, HEIGHT, facecolor=BG, zorder=0))

# ---------- 标题 / 副标题 / 脚注 ----------
ax.text(45, 56.5, '上半年各月商品销量同比去年情况',
        fontproperties=find_chinese_font(bold=True),
        fontsize=23, color='white', va='center', ha='left')
ax.text(46, 107, '2022年相比于2021年销量都有提升，半年整体提升17%',
        fontproperties=find_chinese_font(),
        fontsize=15, color='white', va='center', ha='left')
ax.text(38, 584.5, '*注：数据来源于公司销售系统，统计日期截至2022.06,30',
        fontproperties=find_chinese_font(),
        fontsize=11, color=NOTE, va='center', ha='left')

# ---------- 数据 ----------
cats = ['华北', '华南', '东北', '西北', '西南', '华东']
cluster_x = [125, 242, 359, 476, 593, 710]
blue_x = [108.5, 226, 343, 460, 577.5, 694.5]
pink_x = [142.5, 259.5, 376.5, 493.5, 610.5, 727.5]
blue_v = [2354, 1902, 3524, 2698, 2896, 2563]
pink_v = [2021, 1563, 3213, 2531, 2631, 2361]
baseline = 520
def yv(v):
    return baseline - 0.07123 * v

# ---------- 柱（宽 26） ----------
bar_w = 26
for x, v in zip(blue_x, blue_v):
    top = yv(v)
    ax.add_patch(Rectangle((x - bar_w / 2, top), bar_w, baseline - top,
                           facecolor=C_2022, edgecolor='none', zorder=2))
    ax.text(x, top - 20, str(v), fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='center', zorder=4)
for x, v in zip(pink_x, pink_v):
    top = yv(v)
    ax.add_patch(Rectangle((x - bar_w / 2, top), bar_w, baseline - top,
                           facecolor=C_2021, edgecolor='none', zorder=2))
    ax.text(x, top - 20, str(v), fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='center', zorder=4)

# ---------- 同比折线 ----------
line_pts = [(125, 199), (242, 184), (359, 214), (476, 222), (593, 214), (710, 217)]
rate_labels = ['16%', '22%', '10%', '7%', '10%', '9%']
ax.plot([p[0] for p in line_pts], [p[1] for p in line_pts],
        color=C_LINE, linewidth=2, zorder=3, solid_capstyle='round')
for (x, y), lab in zip(line_pts, rate_labels):
    ax.add_patch(Circle((x, y), 5, facecolor=C_LINE,
                        edgecolor='none', zorder=3))
    ax.text(x, y - 25, lab, fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='center', zorder=4)

# ---------- 横轴 ----------
for x, name in zip(cluster_x, cats):
    ax.text(x, 543, name, fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='center')
ax.add_patch(Rectangle((67, 520), 703, 2, facecolor=AXIS_LINE,
                       edgecolor='none', zorder=1))

# ---------- 右下角图例（两个矩形文本框） ----------
# 2022：深蓝底、蓝色边框
ax.add_patch(Rectangle((685, 405), 73, 34, facecolor=BG,
                       edgecolor=C_2022, linewidth=1.5, zorder=5))
ax.text(722.5, 422, '2022', fontproperties=find_chinese_font(),
        fontsize=11.5, color=TXT, va='center', ha='center', zorder=6)
# 2021：深蓝底、粉色边框
ax.add_patch(Rectangle((687, 448), 74, 34, facecolor=BG,
                       edgecolor=C_2021, linewidth=1.5, zorder=5))
ax.text(725.5, 465, '2021', fontproperties=find_chinese_font(),
        fontsize=11.5, color=TXT, va='center', ha='center', zorder=6)

# ---------- 保存与显示 ----------
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p27.png')
plt.savefig(save_path, dpi=DPI, facecolor=BG, edgecolor='none', pad_inches=0)
print('图片已生成：')
print(save_path)
plt.show()
