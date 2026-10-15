
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


# ---------- 画布（844 x 589） ----------
WIDTH, HEIGHT = 844, 589
DPI = 100
BG = '#1A1E43'

fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, WIDTH)
ax.set_ylim(HEIGHT, 0)
ax.set_facecolor(BG)
ax.axis('off')

# ---------- 配色 ----------
C_BLUE = '#0070C0'          # 实际销量柱
C_EDGE = '#86889A'          # 目标柱描边（白色 50% 叠加在深色背景上）
C_AXIS = '#152E5C'          # 淡蓝横轴（#0070C0 20% 叠加）
TXT = '#F2F2F2'
NOTE = '#D9D9D9'

ax.add_patch(Rectangle((0, 0), WIDTH, HEIGHT, facecolor=BG, zorder=0))

# ---------- 标题 / 副标题 / 脚注 ----------
ax.text(62, 57.5, '2022年上半年各商品销量完成情况',
        fontproperties=find_chinese_font(bold=True),
        fontsize=26, color='white', va='center', ha='left')
ax.text(63, 107, '防晒整体销量最好，达到856，面霜远超目标，超额完成30%',
        fontproperties=find_chinese_font(),
        fontsize=15.5, color='white', va='center', ha='left')
ax.text(59, 556, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
        fontproperties=find_chinese_font(),
        fontsize=11.5, color=NOTE, va='center', ha='left')

# ---------- 数据 ----------
cats = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
cx = [122.5, 241.5, 361, 480, 599.5, 718.5]
target = [700, 500, 600, 900, 600, 600]
actual = [653, 523, 648, 856, 714, 785]

# 目标柱：空心描边（x 左沿、宽 31、柱顶 y）
target_left = [107, 226, 345, 465, 584, 703]
target_top = [251, 315, 283, 187, 283, 283]
# 实际柱：蓝色实心（x 左沿、宽、柱顶 y）
actual_left = [112, 231, 351, 470, 589, 708]
actual_w = [22, 22, 21, 21, 22, 22]
actual_top = [267, 308, 268, 202, 247, 224]
bar_bottom = 474

# ---------- 目标销量柱（空心描边，2px 边线） ----------
for i in range(6):
    x0 = target_left[i]
    top = target_top[i]
    ax.add_patch(Rectangle((x0, top), 32, 2, facecolor=C_EDGE,
                           edgecolor='none', zorder=2))              # 上沿
    ax.add_patch(Rectangle((x0, bar_bottom - 1), 32, 2, facecolor=C_EDGE,
                           edgecolor='none', zorder=2))              # 下沿
    ax.add_patch(Rectangle((x0, top), 2, bar_bottom - top + 1,
                           facecolor=C_EDGE, edgecolor='none', zorder=2))   # 左沿
    ax.add_patch(Rectangle((x0 + 30, top), 2, bar_bottom - top + 1,
                           facecolor=C_EDGE, edgecolor='none', zorder=2))   # 右沿

# ---------- 实际销量柱（蓝色实心） ----------
for i in range(6):
    ax.add_patch(Rectangle((actual_left[i], actual_top[i]), actual_w[i],
                           bar_bottom - actual_top[i] + 1,
                           facecolor=C_BLUE, edgecolor='none', zorder=3))

# ---------- 实际值标签（653、856 两个标签在 Excel 中手动上移） ----------
label_y = [237, 290, 250, 174, 229, 207]
for i, v in enumerate(actual):
    ax.text(cx[i], label_y[i], str(v), fontproperties=find_chinese_font(),
            fontsize=10.5, color=TXT, va='center', ha='center', zorder=4)

# ---------- 横轴类目 ----------
for i, name in enumerate(cats):
    ax.text(cx[i], 500, name, fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='center')

# ---------- 横轴（淡蓝，2px） ----------
ax.add_patch(Rectangle((63, 475), 716, 2, facecolor=C_AXIS,
                       edgecolor='none', zorder=1))

# ---------- 图例（左上角） ----------
# 目标销量：空心方块（2px 描边）
hx, hy, hs = 94, 155, 11
ax.add_patch(Rectangle((hx, hy), 10, 2, facecolor=C_EDGE,
                       edgecolor='none', zorder=4))
ax.add_patch(Rectangle((hx, hy + hs - 2), 10, 2, facecolor=C_EDGE,
                       edgecolor='none', zorder=4))
ax.add_patch(Rectangle((hx, hy), 2, hs, facecolor=C_EDGE,
                       edgecolor='none', zorder=4))
ax.add_patch(Rectangle((hx + 8, hy), 2, hs, facecolor=C_EDGE,
                       edgecolor='none', zorder=4))
ax.text(108, 159, '目标销量', fontproperties=find_chinese_font(),
        fontsize=11.5, color=TXT, va='center', ha='left', zorder=4)
# 实际销量：蓝色实心方块
ax.add_patch(Rectangle((188, 156), 9, 9, facecolor=C_BLUE,
                       edgecolor='none', zorder=4))
ax.text(200, 159, '实际销量', fontproperties=find_chinese_font(),
        fontsize=11.5, color=TXT, va='center', ha='left', zorder=4)

# ---------- 保存与显示 ----------
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p24.png')
plt.savefig(save_path, dpi=DPI, facecolor=BG, edgecolor='none', pad_inches=0)
print('图片已生成：')
print(save_path)
plt.show()
