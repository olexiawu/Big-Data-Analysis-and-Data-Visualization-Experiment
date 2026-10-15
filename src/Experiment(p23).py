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


# ---------- 画布（832 x 594） ----------
WIDTH, HEIGHT = 832, 594
DPI = 100
BG = '#1A1E43'

fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, WIDTH)
ax.set_ylim(HEIGHT, 0)
ax.set_facecolor(BG)
ax.axis('off')

# ---------- 配色 ----------
C_BLUE = '#0070C0'
C_PINK = '#E74E69'
TXT = '#F2F2F2'
NOTE = '#D9D9D9'

ax.add_patch(Rectangle((0, 0), WIDTH, HEIGHT, facecolor=BG, zorder=0))

# ---------- 标题 / 副标题 / 脚注 ----------
ax.text(53, 57, '近六年销售量及增长率',
        fontproperties=find_chinese_font(bold=True),
        fontsize=26, color='white', va='center', ha='left')
ax.text(53, 107, '平台销量近6年持续增长，但近两年增长率有所放缓',
        fontproperties=find_chinese_font(),
        fontsize=15.5, color='white', va='center', ha='left')
ax.text(50, 567, '*注：数据来源于公司销售系统',
        fontproperties=find_chinese_font(),
        fontsize=11.5, color=NOTE, va='center', ha='left')

# ---------- 数据 ----------
cats = ['2017', '2018', '2019', '2020', '2021', '2022']
cx = [121.5, 238.5, 356, 473, 590, 707.5]
bar_left = [103, 221, 338, 455, 572, 690]
bar_w = [37, 36, 37, 37, 37, 36]
sales = [1603, 2106, 2406, 3265, 3721, 3921]
rates = [0.27, 0.31378665003119144, 0.14245014245014254,
         0.35702410640066495, 0.1396630934150076, 0.053748992206396062]
rate_txt = ['27%', '31%', '14%', '36%', '14%', '5%']

# 柱形坐标：基线 498，数值轴最大值 6000，绘图区上沿 148（高 350）
baseline = 498


def yv_bar(v):
    return baseline - v / 6000.0 * 350.0


# 折线坐标：副轴最小值 -1.2、最大值 0.5
plot_top, plot_bottom = 148, 498


def yv_line(v):
    return plot_top + (0.5 - v) / 1.7 * (plot_bottom - plot_top)


# ---------- 销量柱 ----------
for i, v in enumerate(sales):
    top = yv_bar(v)
    ax.add_patch(Rectangle((bar_left[i], top), bar_w[i], baseline - top,
                           facecolor=C_BLUE, edgecolor='none', zorder=2))
# 柱顶数据标签（最后一个标签位置 Excel 手动微调过）
label_y = [387, 358, 340, 290, 263, 260]
for i, v in enumerate(sales):
    ax.text(cx[i], label_y[i], str(v), fontproperties=find_chinese_font(),
            fontsize=10.5, color=TXT, va='center', ha='center', zorder=4)

# ---------- 同比折线 ----------
line_y = [195, 186, 222, 177, 222, 240]
pts = [(cx[i], line_y[i]) for i in range(6)]
ax.plot([p[0] for p in pts], [p[1] for p in pts],
        color=C_PINK, linewidth=2, zorder=3, solid_capstyle='round')
for (x, y), lab in zip(pts, rate_txt):
    ax.add_patch(Circle((x, y), 4.5, facecolor=C_PINK,
                        edgecolor='none', zorder=3))
    ax.text(x, y - 23.5, lab, fontproperties=find_chinese_font(),
            fontsize=10, color=TXT, va='center', ha='center', zorder=4)

# ---------- 横轴类目 ----------
for i, name in enumerate(cats):
    ax.text(cx[i], 523, name, fontproperties=find_chinese_font(),
            fontsize=10.5, color=TXT, va='center', ha='center')

# ---------- 图例（右上角） ----------
# 销售量：蓝色方块 + 文字
ax.add_patch(Rectangle((558, 150), 37, 8, facecolor=C_BLUE,
                       edgecolor='none', zorder=4))
ax.text(601, 153, '销售量', fontproperties=find_chinese_font(),
        fontsize=11, color=TXT, va='center', ha='left', zorder=4)
# 同比：粉色线段 + 圆点 + 文字
ax.plot([665, 706], [153.5, 153.5], color=C_PINK, linewidth=2,
        zorder=4, solid_capstyle='round')
ax.add_patch(Circle((685, 153.5), 5, facecolor=C_PINK,
                    edgecolor='none', zorder=4))
ax.text(711, 153, '同比', fontproperties=find_chinese_font(),
        fontsize=11, color=TXT, va='center', ha='left', zorder=4)

# ---------- 保存与显示 ----------
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p23.png')
plt.savefig(save_path, dpi=DPI, facecolor=BG, edgecolor='none', pad_inches=0)
print('图片已生成：')
print(save_path)
plt.show()
