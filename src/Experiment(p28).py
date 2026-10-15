
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


# ---------- 画布（844 x 603） ----------
WIDTH, HEIGHT = 844, 603
DPI = 100
BG = '#1A1E43'

fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, WIDTH)
ax.set_ylim(HEIGHT, 0)
ax.set_facecolor(BG)
ax.axis('off')

# ---------- 配色 ----------
# 季度大柱：季度色 20% 透明叠在深蓝底上后的实际效果色
C_Q1_BIG = '#242A5F'
C_Q2_BIG = '#472E39'
C_Q3_BIG = '#463938'
C_Q4_BIG = '#35254F'
C_Q1 = '#4A5BD1'
C_Q2 = '#FC6C0F'
C_Q3 = '#F6A50B'
C_Q4 = '#A2417B'
TXT = '#F2F2F2'
NOTE = '#D9D9D9'
AXIS_LINE = '#454866'

ax.add_patch(Rectangle((0, 0), WIDTH, HEIGHT, facecolor=BG, zorder=0))

# ---------- 标题 / 副标题 / 脚注 ----------
ax.text(59, 58.5, '2021年各月化妆品销量走势',
        fontproperties=find_chinese_font(bold=True),
        fontsize=23, color='white', va='center', ha='left')
ax.text(59, 107, '2021年第三季度销量最多9673，9月单月销量最大3621',
        fontproperties=find_chinese_font(),
        fontsize=14.5, color='white', va='center', ha='left')
ax.text(49, 574, '*注：数据来源于公司销售系统，统计日期截至2021.12.31',
        fontproperties=find_chinese_font(),
        fontsize=11, color=NOTE, va='center', ha='left')

# ---------- 数据 ----------
baseline = 500
def yv(v):
    return baseline - 0.03314 * v

# 季度大柱（每季度 3 个相邻槽位，无间隙）
blocks = [
    # x0, x1, 合计, 颜色, 标签中心x, 标签中心y
    (82, 214, 7780, C_Q1_BIG, 148, 225),
    (260, 393, 8157, C_Q2_BIG, 326, 213),
    (438, 571, 9673, C_Q3_BIG, 504, 163),
    (616, 749, 8387, C_Q4_BIG, 682, 205),
]
for x0, x1, v, c, labx, laby in blocks:
    top = yv(v)
    ax.add_patch(Rectangle((x0, top), x1 - x0, baseline - top,
                           facecolor=c, edgecolor='none', zorder=2))
    ax.text(labx, laby, str(v), fontproperties=find_chinese_font(),
            fontsize=10.5, color=TXT, va='center', ha='center', zorder=4)

# 月度小柱
months = [
    ('1月', 103.5, 2354, C_Q1), ('2月', 147.5, 1902, C_Q1), ('3月', 192.5, 3524, C_Q1),
    ('4月', 281.5, 2698, C_Q2), ('5月', 326.5, 2896, C_Q2), ('6月', 370.5, 2563, C_Q2),
    ('7月', 460.5, 3156, C_Q3), ('8月', 504.5, 2896, C_Q3), ('9月', 549.5, 3621, C_Q3),
    ('10月', 638.5, 2635, C_Q4), ('11月', 682.5, 2963, C_Q4), ('12月', 727.5, 2789, C_Q4),
]
bar_w = 18
for name, x, v, c in months:
    top = yv(v)
    ax.add_patch(Rectangle((x - bar_w / 2, top), bar_w, baseline - top,
                           facecolor=c, edgecolor='none', zorder=3))
    ax.text(x, top - 18, str(v), fontproperties=find_chinese_font(),
            fontsize=9.5, color=TXT, va='center', ha='center', zorder=4)

# ---------- 横轴 ----------
for name, x, _, _ in months:
    ax.text(x, 523.5, name, fontproperties=find_chinese_font(),
            fontsize=11.5, color=TXT, va='center', ha='center')
ax.add_patch(Rectangle((82, 500), 668, 2, facecolor=AXIS_LINE,
                       edgecolor='none', zorder=1))

# ---------- 保存与显示 ----------
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p28.png')
plt.savefig(save_path, dpi=DPI, facecolor=BG, edgecolor='none', pad_inches=0)
print('图片已生成：')
print(save_path)
plt.show()
