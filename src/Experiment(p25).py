import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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


# ---------- 画布（与导出原图同尺寸：842 x 589） ----------
WIDTH, HEIGHT = 842, 589
DPI = 100
BG = '#1A1E43'

fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, WIDTH)
ax.set_ylim(HEIGHT, 0)
ax.set_facecolor(BG)
ax.axis('off')

# ---------- 配色 ----------
C_JIGE = '#82ADD7'     # 及格
C_LIANG = '#0885BC'    # 良好（00B0F0 70% 透明后的效果色）
C_YOUXIU = '#0070C0'   # 优秀
C_ACTUAL = '#0E5DFF'   # 实际
C_TARGET = '#FFC000'   # 目标
TXT = '#F2F2F2'
NOTE = '#D9D9D9'
AXIS_LINE = '#454866'

# 背景
ax.add_patch(Rectangle((0, 0), WIDTH, HEIGHT, facecolor=BG, zorder=0))

# ---------- 标题 / 副标题 / 脚注 ----------
ax.text(54, 53.5, '2022年上半年各商品销量完成情况',
        fontproperties=find_chinese_font(bold=True),
        fontsize=23, color='white', va='center', ha='left')
ax.text(54, 102, '防晒整体销量最好，达到856，面霜远超目标，超额完成30%',
        fontproperties=find_chinese_font(),
        fontsize=14.5, color='white', va='center', ha='left')
ax.text(53, 557, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
        fontproperties=find_chinese_font(),
        fontsize=11, color=NOTE, va='center', ha='left')

# ---------- 图例 ----------
legend_y = 173
legend_items = [
    ('rect', C_JIGE, '及格', 152, 167),
    ('rect', C_LIANG, '良好', 219, 236),
    ('rect', C_YOUXIU, '优秀', 286, 301),
    ('rect', C_ACTUAL, '实际', 352, 369),
    ('dash', C_TARGET, '目标', 419, 437),
]
for kind, color, label, sx, tx in legend_items:
    if kind == 'rect':
        ax.add_patch(Rectangle((sx, legend_y - 4.5), 9, 9,
                               facecolor=color, edgecolor='none', zorder=5))
    else:
        ax.add_patch(Rectangle((sx, legend_y - 1), 9, 2,
                               facecolor=color, edgecolor='none', zorder=5))
    ax.text(tx, legend_y, label, fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='left')

# ---------- 绘图区 ----------
cats = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
cx = [165.5, 280.5, 396.5, 511.5, 627.5, 742.5]
baseline = 489
def yv(v):
    return baseline - 0.264 * v

# 分段背景柱（宽 33）
band_w = 33
y600, y800, y1000 = yv(600), yv(800), yv(1000)
for x in cx:
    # 及格 0-600
    ax.add_patch(Rectangle((x - band_w / 2, y600), band_w, baseline - y600,
                           facecolor=C_JIGE, edgecolor='none', zorder=2))
    # 良好 600-800
    ax.add_patch(Rectangle((x - band_w / 2, y800), band_w, y600 - y800,
                           facecolor=C_LIANG, edgecolor='none', zorder=2))
    # 优秀 800-1000
    ax.add_patch(Rectangle((x - band_w / 2, y1000), band_w, y800 - y1000,
                           facecolor=C_YOUXIU, edgecolor='none', zorder=2))

# 实际销量柱（宽 19）
actual = [653, 523, 648, 856, 714, 785]
act_w = 19
for x, v in zip(cx, actual):
    ax.add_patch(Rectangle((x - act_w / 2, yv(v)), act_w, baseline - yv(v),
                           facecolor=C_ACTUAL, edgecolor='none', zorder=3))

# 目标短杠（宽 20，高 4）
target = [700, 500, 600, 900, 600, 600]
for x, v in zip(cx, target):
    yt = yv(v)
    ax.add_patch(Rectangle((x - 10, yt - 2), 20, 4,
                           facecolor=C_TARGET, edgecolor='none', zorder=4))

# ---------- 坐标轴 ----------
# 纵轴刻度 0、200 … 1200
for v in range(0, 1201, 200):
    ax.text(92, yv(v), str(v), fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='right')
# 横轴类目
for x, name in zip(cx, cats):
    ax.text(x, 513, name, fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='center')
# 底部轴线（白色 20% 透明）
ax.add_patch(Rectangle((107, 490), 693, 2, facecolor=AXIS_LINE,
                       edgecolor='none', zorder=1))

# ---------- 保存与显示 ----------
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p25.png')
plt.savefig(save_path, dpi=DPI, facecolor=BG, edgecolor='none', pad_inches=0)
print('图片已生成：')
print(save_path)
plt.show()
