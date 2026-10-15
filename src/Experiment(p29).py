
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


# ---------- 画布（844 x 593） ----------
WIDTH, HEIGHT = 844, 593
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
RIM = '#F2F2F2'
TXT = '#F2F2F2'
NOTE = '#D9D9D9'

ax.add_patch(Rectangle((0, 0), WIDTH, HEIGHT, facecolor=BG, zorder=0))

# ---------- 标题 / 副标题 / 脚注 ----------
ax.text(65, 53.5, '2022年上半年产品销量目标达成率情况',
        fontproperties=find_chinese_font(bold=True),
        fontsize=23, color='white', va='center', ha='left')
ax.text(64, 102, '华南完成率最高达到86%，华东最低35%',
        fontproperties=find_chinese_font(),
        fontsize=14.5, color='white', va='center', ha='left')
ax.text(65, 558, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
        fontproperties=find_chinese_font(),
        fontsize=11, color=NOTE, va='center', ha='left')

# ---------- 数据 ----------
cats = ['华南', '华北', '东北', '西北', '华东']
row_y = [187, 260, 333, 406, 478]
pct = [0.86, 0.74, 0.62, 0.51, 0.35]
x0 = 136
scale = 475          # 100% 对应 475 像素
x100 = x0 + scale    # 611
bar_h = 29
bead_r = 15

for name, y, p in zip(cats, row_y, pct):
    xe = x0 + p * scale
    # 整条灰色轨道
    rounded_bar(ax, x0, x100, y, bar_h, C_GRAY, 2)
    # 已完成蓝色段
    rounded_bar(ax, x0, xe, y, bar_h, C_BLUE, 3)
    # 白边蓝珠
    ax.add_patch(Circle((xe, y), bead_r, facecolor=C_BLUE,
                        edgecolor=RIM, linewidth=2, zorder=5))
    # 条内百分比（右对齐，位于蓝珠左侧）
    ax.text(xe - 22, y, f'{int(round(p * 100))}%',
            fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='right', zorder=6)
    # 左侧类目名
    ax.text(117, y, name, fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='right')

# ---------- 保存与显示 ----------
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p29.png')
plt.savefig(save_path, dpi=DPI, facecolor=BG, edgecolor='none', pad_inches=0)
print('图片已生成：')
print(save_path)
plt.show()
