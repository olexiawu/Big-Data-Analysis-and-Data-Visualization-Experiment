
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


def rounded_bar(ax, x0, x1, y, h, color, zorder):
    """绘制两端全圆角的水平条（胶囊形）：条身矩形 + 两端半圆端盖。
    条形总范围为 x0..x1。"""
    r = h / 2.0
    ax.add_patch(Rectangle((x0 + r, y - r), x1 - x0 - 2 * r, h,
                           facecolor=color, edgecolor='none', zorder=zorder))
    ax.add_patch(Circle((x0 + r, y), r, facecolor=color,
                        edgecolor='none', zorder=zorder))
    ax.add_patch(Circle((x1 - r, y), r, facecolor=color,
                        edgecolor='none', zorder=zorder))


# ---------- 画布（831 x 593） ----------
WIDTH, HEIGHT = 831, 593
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
C_GRAY = '#717389'
C_BEAD_GRAY = '#A6A6A6'
RIM = '#F2F2F2'
TXT = '#F2F2F2'
NOTE = '#D9D9D9'

ax.add_patch(Rectangle((0, 0), WIDTH, HEIGHT, facecolor=BG, zorder=0))

# ---------- 标题 / 副标题 / 脚注 ----------
ax.text(60, 59.5, '2022年上半年销量目标达成率同比去年情况',
        fontproperties=find_chinese_font(bold=True),
        fontsize=23, color='white', va='center', ha='left')
ax.text(59, 108, '华南完成率最高达到86%，华东最低35%，其中华南和华东不及2021年',
        fontproperties=find_chinese_font(),
        fontsize=14.5, color='white', va='center', ha='left')
ax.text(69, 560, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
        fontproperties=find_chinese_font(),
        fontsize=11, color=NOTE, va='center', ha='left')

# ---------- 顶部图例 ----------
ax.add_patch(Circle((77, 155), 8.7, facecolor=C_BLUE,
                    edgecolor=RIM, linewidth=1.5, zorder=6))
ax.text(103, 155, '2022完成率', fontproperties=find_chinese_font(),
        fontsize=11.5, color=TXT, va='center', ha='left', zorder=6)
ax.add_patch(Circle((206, 155), 8.7, facecolor=C_BEAD_GRAY,
                    edgecolor=RIM, linewidth=1.5, zorder=6))
ax.text(227, 155, '2021完率', fontproperties=find_chinese_font(),
        fontsize=11.5, color=TXT, va='center', ha='left', zorder=6)

# ---------- 数据 ----------
cats = ['华南', '华北', '东北', '西北', '华东']
row_y = [197, 270, 345, 418, 493]
p2022 = [0.86, 0.74, 0.62, 0.51, 0.35]
p2021 = [0.92, 0.69, 0.53, 0.39, 0.45]
x0 = 124
scale = 536.6
x100 = x0 + scale    # 660.6
bar_h = 13
bead_r = 9

for name, y, a, b in zip(cats, row_y, p2022, p2021):
    xa = x0 + a * scale
    xb = x0 + b * scale
    # 灰色轨道 + 蓝色已完成段
    rounded_bar(ax, x0, x100, y, bar_h, C_GRAY, 2)
    rounded_bar(ax, x0, xa, y, bar_h, C_BLUE, 3)
    # 2021 灰珠（白边）
    ax.add_patch(Circle((xb, y), bead_r, facecolor=C_BEAD_GRAY,
                        edgecolor=RIM, linewidth=2, zorder=5))
    # 2022 蓝珠（白边）
    ax.add_patch(Circle((xa, y), bead_r, facecolor=C_BLUE,
                        edgecolor=RIM, linewidth=2, zorder=6))
    # 蓝珠上方百分比
    ax.text(xa, y - 28.5, f'{int(round(a * 100))}%',
            fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='center', zorder=7)
    # 左侧类目名
    ax.text(105, y, name, fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='right')

# ---------- 保存与显示 ----------
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p30.png')
plt.savefig(save_path, dpi=DPI, facecolor=BG, edgecolor='none', pad_inches=0)
print('图片已生成：')
print(save_path)
plt.show()
