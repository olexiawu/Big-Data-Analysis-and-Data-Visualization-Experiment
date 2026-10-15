
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


# ---------- 画布（831 x 591） ----------
WIDTH, HEIGHT = 831, 591
DPI = 100
BG = '#1A1E43'

fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, WIDTH)
ax.set_ylim(HEIGHT, 0)
ax.set_facecolor(BG)
ax.axis('off')

# ---------- 配色 ----------
C_BAR = '#E74E69'
C_CIRCLE = '#0070C0'
TXT = '#F2F2F2'
NOTE = '#D9D9D9'
AXIS_LINE = '#454866'

ax.add_patch(Rectangle((0, 0), WIDTH, HEIGHT, facecolor=BG, zorder=0))

# ---------- 标题 / 副标题 / 脚注 ----------
ax.text(52, 53, '各区域上半年销量以同比',
        fontproperties=find_chinese_font(bold=True),
        fontsize=23, color='white', va='center', ha='left')
ax.text(52, 102, '东北区域销量持续保持第一，华东和华南同比去年增长最多',
        fontproperties=find_chinese_font(),
        fontsize=14.5, color='white', va='center', ha='left')
ax.text(36, 557, '*注：数据来源于公司销售系统，统计日期截至2022.06,30',
        fontproperties=find_chinese_font(),
        fontsize=11, color=NOTE, va='center', ha='left')

# ---------- 数据 ----------
cats = ['华北', '华南', '东北', '西北', '西南', '华东']
cx = [125, 239, 353, 468, 582, 697]
values = [2354, 1902, 3524, 2698, 2896, 2563]
rates = [12, 25, 16, 21, 18, 25]
diam = [24, 50, 32, 42, 36, 50]
baseline = 499
def yv(v):
    return baseline - 0.07009 * v

# ---------- 粉色柱（宽 36） ----------
bar_w = 36
for x, v in zip(cx, values):
    top = yv(v)
    ax.add_patch(Rectangle((x - bar_w / 2, top), bar_w, baseline - top,
                           facecolor=C_BAR, edgecolor='none', zorder=2))
    ax.text(x, top - 20, str(v), fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='center', zorder=4)

# ---------- 蓝色圆（圆心恒在 y=182） ----------
circle_y = 182
for x, r_label, d in zip(cx, rates, diam):
    r = d / 2.0
    ax.add_patch(Circle((x, circle_y), r, facecolor=C_CIRCLE,
                        edgecolor='none', zorder=3))
    ax.text(x, circle_y + 1, f'{r_label}%',
            fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='center', zorder=4)

# ---------- 横轴 ----------
for x, name in zip(cx, cats):
    ax.text(x, 523, name, fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='center')
ax.add_patch(Rectangle((68, 500), 686, 2, facecolor=AXIS_LINE,
                       edgecolor='none', zorder=1))

# ---------- 保存与显示 ----------
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p26.png')
plt.savefig(save_path, dpi=DPI, facecolor=BG, edgecolor='none', pad_inches=0)
print('图片已生成：')
print(save_path)
plt.show()
